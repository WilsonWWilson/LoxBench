from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from cryptography.hazmat.primitives import serialization, hashes, hmac
from cryptography.hazmat.primitives.ciphers import algorithms, Cipher, modes
import base64
import asyncio
import requests
from requests.structures import CaseInsensitiveDict
import re
import os
import json
import binascii
from communication.loxsocket import LoxSocket
from http_status_codes import HttpStatusCode
# from api import SESSION_COMMANDS as CMD


TOKEN_CFG_VERSION = "8.4.5.10"
ENCRYPTION_CFG_VERSION = "8.1.10.14"
HDR_FORMAT = "BBBBI"


class CMD:
    GET_API = "jdev/cfg/api"
    GET_PUBLIC_KEY = "jdev/sys/getPublicKey"
    GET_TOKEN = "jdev/sys/gettoken/{hash}/{user}/{permission}/{uuid}/{info}"
    FENC = "jdev/sys/fenc/{}?sk={}"
    GET_SALT_AND_KEY = "jdev/sys/getkey2/{}"
    EXCHANGE_KEY = "jdev/sys/keyexchange/{}"
    AUTH_WITH_TOKEN = "authwithoken/{}/{}"


class Permission:
    Undefined = 0               # only for logging purposes
    ADMIN = 1                   # User is in "Administrator" group (no token, just a permissive info)
    WEB = 2                     # short-lived token, used for the WI
    APP = 4                     # long lived token, used for the app (> 4 weeks)
    CONFIG = 8                  # Login with Loxone Config
    FTP = 16                    # Login with FTP(only an access right, no token login for FTP)
    USER_EDIT = 32  	        # edit user details(password change, very short lived - if an admin has this token, he may also edit other users credentials)
    EXPERT_MODE = 64 	        # use expert mode.
    OP_MODES = 128 	            # Edit operating modes
    SYS_WS = 256 	            # Call System Webservices(e.g.reboot)
    AUTOPILOT = 512 	        # Edit / create autopilots
    EXPERT_MODE_LIGHT = 1024 	# expert mode light(nice and clear UI, only UI relevant settings, no configuration possible)


class LoxComm:
    def __init__(self, host, user, pwd, socket=None):
        self._host = host
        self._token = None
        self._user = user
        self._pwd = pwd
        self._pubkey = None
        self._request_queue = asyncio.Queue()
        self._ws = socket if socket else LoxSocket(host, user, pwd)

    @staticmethod
    def lox_get(host, cmd, credentials=None, full_response=False):
        r = requests.get('http://{}/{}'.format(host, cmd), auth=credentials)
        code, content, res_cmd = None, None, cmd

        if r.status_code == HttpStatusCode.OK:
            # res = CaseInsensitiveDict(r.json()['LL'])
            content_type = r.headers['Content-Type']
            if 'json' in content_type:
                try:
                    res = r.json()['LL']
                    if full_response:
                        code = int(res.get('Code', res.get('code', 1337)))
                        content, cmd = res['value'] = res['value'], res['control']        # can't unify it with parsing of socket response, because there the 'code' is lowercase
                    else:
                        content = res['value']
                except json.decoder.JSONDecodeError as exc:
                    print("Couldn't decode response to '{}': {}".format(cmd, exc))
                    code, content = r.status_code, r.content
                except KeyError as exc:     # response was not a regular api command
                    code, content = r.status_code, r.content
            # elif content_type.endswith('xml'):
            #     code, content = r.status_code, r.content
                # TODO extract data from response,if it's a command response
            else:
                code, content = r.status_code, r.content
        elif full_response:
            code = r.status_code

        if full_response:
            return HttpStatusCode(code), content, res_cmd
        else:
            return content

    @staticmethod
    def fix_public_key(pub_key_pem):
        # format return by the Miniserver is not a valid PEM format:
        pub_key_pem = re.sub(r'^(-+BEGIN.*?-+)(\w)', r'\1\n\2', pub_key_pem)        # BEGIN and END must be on separate lines
        pub_key_pem = re.sub(r'(\w)(-+END.*?-+)', r'\1\n\2', pub_key_pem)
        pub_key_pem = pub_key_pem.replace("CERTIFICATE", "PUBLIC KEY")              # it's not a certificate but a public key
        return pub_key_pem.encode('utf-8')

    async def _get_public_key(self):
        if self._pubkey:
            return self._pubkey
        pub_key_pem = self.lox_get(self._host, CMD.GET_PUBLIC_KEY)
        pub_key = serialization.load_pem_public_key(
            self.fix_public_key(pub_key_pem),
            backend=default_backend())
        self._pubkey = pub_key
        return pub_key

    def get_public_key(self):
        if self._pubkey:
            return self._pubkey
        pub_key_pem = self.lox_get(self._host, CMD.GET_PUBLIC_KEY)
        pub_key = serialization.load_pem_public_key(
            self.fix_public_key(pub_key_pem),
            backend=default_backend())
        self._pubkey = pub_key
        return pub_key

    @staticmethod
    def generate_session_key(pub_key, aes_key, aes_iv=None):
        if type(aes_iv) == str:
            aes_iv = aes_iv.encode('utf-8')
        elif aes_iv is None:
            aes_iv = os.urandom(16)
        # aes_iv = binascii.unhexlify(aes_iv) if aes_iv else os.urandom(16)
        # aes_key = binascii.unhexlify(aes_key)

        if type(aes_iv) == str:
            aes_key = aes_iv.encode('utf-8')
        elif aes_key is None:
            aes_key = os.urandom(32)

        ct = pub_key.encrypt(
            aes_key + b':' + aes_iv,
            padding=PKCS1v15()
        )
        return base64.b64encode(ct).decode('utf-8')

    # async def _get_ws_response(self, ws, full_response=False):
    #     res = await ws.recv()
    #     _, msg_type, info, rsvd, msg_len = struct.unpack_from(HDR_FORMAT, res, 0)
    #     is_estimated = info & 0x80
    #
    #     if msg_type == 0:
    #         msg = await ws.recv()
    #         res = json.loads(msg)['LL']
    #         if full_response:
    #             code = res['code'] if 'code' in res else res['Code']    # response is not consistent/ difference between HTTP-Request and socket
    #             return int(code), res['value'], res['control']
    #         else:
    #             return res['value']

    async def _acquire_token(self, credentials, ws=None):
        user, pwd = credentials
        if ws:
            await ws.send(CMD.GET_SALT_AND_KEY.format(user))
            res = await self.send(ws)
        else:
            res = self.lox_get(self._host, CMD.GET_SALT_AND_KEY.format(user))

        digest = hashes.Hash(hashes.SHA1(), backend=default_backend())
        salt = res["salt"]
        digest.update("{}:{}".format(pwd, salt).encode('utf-8'))
        pwd_hash = binascii.hexlify(digest.finalize()).upper().decode('utf-8')

        key = binascii.unhexlify(res['key'])
        h = hmac.HMAC(key, hashes.SHA1(), backend=default_backend())
        h.update("{}:{}".format(user, pwd_hash).encode('utf-8'))
        cred_hash = binascii.hexlify(h.finalize()).decode('utf-8')

        # TODO test what happens if info is not URLencoded
        # TODO play around with UUID
        cmd = CMD.GET_TOKEN.format(hash=cred_hash, user=user, permission=Permission.WEB, uuid="0a8c7351-00ac-1e18-ffff112233445566", info="LoxBench")
        enc_cmd = await self.encrypt_command(cmd)
        if ws:
            await ws.send(enc_cmd)
            code, token, _ = await self._get_ws_response(ws, True)
        else:
            code, res, _ = self.lox_get(self._host, enc_cmd, full_response=True)
        if code == 200:
            self._token = token
            return token
        else:
            a = 5
            return None

    async def authenticate_with_token(self, ws):
        # TODO hash = hmac(user:token)
        # TODO CMD.AUTH_WITH_TOKEN/hash/user
        # TODO {authCmd}
        pass

    def connect(self, credentials=None):
        if credentials is None:
            credentials = (self._user, self._pwd)
        asyncio.get_event_loop().run_until_complete(self.lox_comm(credentials))

    async def lox_comm(self, credentials):
        # pub_key = await self._get_public_key()
        # sk = self.generate_session_key(pub_key, "ThisIsASecretPasswordWith32Bytes")
        if not self._token:
            token = await self._acquire_token(credentials)
            if token:
                await self._ws.connect(token)

        # async with websockets.connect('ws://{}/ws/rfc6455'.format(self._host), subprotocols=['remotecontrol']) as ws:
        #     await ws.send(CMD.EXCHANGE_KEY.format(session_key))
        #     res = await self._get_ws_response(ws)       # TODO what to do with the session key?
        #     if self._token:
        #         await self.authenticate_with_token(ws)
        #     else:
        #         await self._acquire_token(credentials)
        #
        #     listener_task = asyncio.ensure_future(self._response_handler(ws))
        #     sender_task = asyncio.ensure_future(self._request_handler(ws))
        #     done, pending = await asyncio.wait(
        #         [listener_task, sender_task],
        #         return_when=asyncio.FIRST_COMPLETED
        #     )
        #     for task in pending:
        #         task.cancel()

    # async def _response_handler(self, ws):
    #     while True:
    #         msg = await ws.recv()
    #
    # async def _request_handler(self, ws):
    #     while True:
    #         msg = await self._request_queue.get()
    #         await ws.send(msg)

    async def send(self, ws, msg):
        pass

    def get_credentials(self):
        return self._user, self._pwd

    def get_host(self):
        return self._host

    def request(self, cmd, full_response=False):
        return self.lox_get(self._host, cmd, (self._user, self._pwd), full_response)

    async def encrypt_command(self, command, session_key=None, pub_key=None):
        if pub_key is None:
            pub_key = await self._get_public_key()
        # aes_iv = os.urandom(16)
        if session_key:
            s_iv = session_key[0]
            aes_iv = binascii.unhexlify(s_iv)
            s_key = session_key[1]
        else:
            aes_iv = os.urandom(16)
            s_key = 'adc6546388faf24d1b7771ed3123c1d84603b3defb220a10e0be50f8c8fe4937'
        aes_key = binascii.unhexlify(s_key)

        salt = '5cf8'

        algo = algorithms.AES(aes_key)
        cipher = Cipher(algo, mode=modes.CBC(aes_iv), backend=default_backend())
        aes = cipher.encryptor()
        pt = "salt/{}/{}".format(salt, command)
        aes_ct = aes.update(pt.encode('utf-8'))
        aes_ct = binascii.hexlify(aes_ct)
        aes_ct = base64.b64encode(aes_ct).decode('utf-8')

        rsa_session_key = self.generate_session_key(pub_key, aes_key, aes_iv)
        # rsa_ct = pub_key.encrypt(
        #     session_key + ':' + session_iv,
        #     padding=PKCS1v15()
        # )
        # rsa_session_key = base64.b64encode(rsa_ct).decode('utf-8')

        enc_cmd = CMD.FENC.format(aes_ct, rsa_session_key)

        return enc_cmd

    @staticmethod
    def decrypt_ciphertext(ct, session_key):
        pass

    def http_connect(self, credentials):
        # api/getKey
        key = "32413742453530363146394434344644333146423234393631324533344543323738423841453231"
        pub_key = self.get_public_key()
        user, pwd = credentials
        res = self.lox_get(self._host, CMD.GET_SALT_AND_KEY.format(user))

        # hash the credentials
        digest = hashes.Hash(hashes.SHA1(), backend=default_backend())
        res = {
            'salt': '44394433344636373039364239394342393932464233393633383442373733313146343941354237',
            'key': '31303761303130362D303235342D323564352D66666666623634626663346332383562'
        }
        salt = res["salt"]
        digest.update("{}:{}".format(pwd, salt).encode('utf-8'))
        pwd_hash = binascii.hexlify(digest.finalize()).upper().decode('utf-8')

        key = binascii.unhexlify(res['key'])
        h = hmac.HMAC(key, hashes.SHA1(), backend=default_backend())
        h.update("{}:{}".format(user, pwd_hash).encode('utf-8'))
        cred_hash = binascii.hexlify(h.finalize()).decode('utf-8')

        # get token
        cmd = CMD.GET_TOKEN.format(hash=cred_hash, user=user, permission=Permission.WEB, uuid="ddd5fc8c-e0d4-4798-a037-65e9f14e688e", info="Application")
        cmd_ref = 'jdev/sys/gettoken/7226a3e16580c5bfc1074587be5e0fa0d043c2dc/web/2/Webinterface / Linux x86_64  Mozilla/5.0 (X11; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0/ddd5fc8c-e0d4-4798-a037-65e9f14e688e'
        enc_cmd = self.encrypt_command(cmd, pub_key)

        token = self.lox_get(self._host, enc_cmd)
        token2 = self.lox_get(self._host, cmd_ref)


class DummyComm():
    def request(self, cmd, full_request=False):
        # print("Request: '{:<30}\r".format(cmd), end='')
        print("Request: '{:<30}".format(cmd))
        return HttpStatusCode.NOT_FOUND, '-'


