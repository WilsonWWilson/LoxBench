from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from cryptography.hazmat.primitives import serialization, hashes, hmac
from cryptography.hazmat.primitives.ciphers import algorithms, Cipher, modes
import base64
import asyncio
import websockets
import requests
from requests.structures import CaseInsensitiveDict
import re
import os
import struct
import json
import binascii
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
    def __init__(self, host, user, pwd):
        self._host = host
        self._token = None
        self._user = user
        self._pwd = pwd
        self._request_queue = asyncio.Queue()

    @staticmethod
    def lox_get(host, cmd, credentials=None, full_response=False):
        r = requests.get('http://{}/{}'.format(host, cmd), auth=credentials)

        if r.status_code == HttpStatusCode.OK:
            # res = CaseInsensitiveDict(r.json()['LL'])
            content_type = r.headers['Content-Type']
            if 'json' in content_type:
                res = r.json()['LL']
                if full_response:
                    code = res.get('Code', res.get('code', "-can't retrieve code-"))
                    return code, res['value'], res['control']        # can't unify it with parsing of socket response, because there the 'code' is lowercase
                else:
                    return res['value']
            # elif content_type.endswith('xml'):
            #     pass
            else:
                if full_response:
                    return HttpStatusCode(r.status_code), r.content, cmd
                else:
                    return r.content
        else:
            return HttpStatusCode(r.status_code)

    async def _get_public_key(self):
        pub_key_pem = self.lox_get(self._host, CMD.GET_PUBLIC_KEY)
        # format return by the Miniserver is not a valid PEM format:
        pub_key_pem = re.sub(r'^(-+BEGIN.*?-+)(\w)', r'\1\n\2', pub_key_pem)        # BEGIN and END must be on separate lines
        pub_key_pem = re.sub(r'(\w)(-+END.*?-+)', r'\1\n\2', pub_key_pem)
        pub_key_pem = pub_key_pem.replace("CERTIFICATE", "PUBLIC KEY")              # it's not a certificate but a public key
        pub_key = serialization.load_pem_public_key(
            pub_key_pem.encode('utf-8'),
            backend=default_backend())
        return pub_key

    @staticmethod
    def _generate_session_key(pub_key, aes_key):
        aes_iv = os.urandom(16)
        ct = pub_key.encrypt(
            aes_key + b':' + aes_iv,
            padding=PKCS1v15()
        )
        return base64.b64encode(ct).decode('utf-8')

    async def _authenticate(self):
        pub_key = await self._get_public_key()
        aes_key = "ThisIsASecretPasswordWith32Bytes".encode('utf-8')
        return self._generate_session_key(pub_key, aes_key)

    async def _get_ws_response(self, ws, full_response=False):
        res = await ws.recv()
        _, msg_type, info, rsvd, msg_len = struct.unpack_from(HDR_FORMAT, res, 0)
        is_estimated = info & 0x80

        if msg_type == 0:
            msg = await ws.recv()
            res = json.loads(msg)['LL']
            if full_response:
                code = res['code'] if 'code' in res else res['Code']    # response is not consistent/ difference between HTTP-Request and socket
                return int(code), res['value'], res['control']
            else:
                return res['value']

    async def _acquire_token(self, ws, credentials):
        user, pwd = credentials
        await ws.send(CMD.GET_SALT_AND_KEY.format(user))
        res = await self._get_ws_response(ws)

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
        await ws.send(cmd)
        code, token, _ = await self._get_ws_response(ws, True)
        if code == 200:
            self._token = token
        a = 5

    async def authenticate_with_token(self, ws):
        # TODO hash = hmac(user:token)
        # TODO CMD.AUTH_WITH_TOKEN/hash/user
        # TODO {authCmd}
        pass

    async def lox_comm(self, credentials):
        session_key = await self._authenticate()
        async with websockets.connect('ws://{}/ws/rfc6455'.format(self._host)) as ws:
            await ws.send(CMD.EXCHANGE_KEY.format(session_key))
            res = await self._get_ws_response(ws)       # TODO what to do with the session key?
            if self._token:
                await self.authenticate_with_token(ws)
            else:
                await self._acquire_token(ws, credentials)

            listener_task = asyncio.ensure_future(self._response_handler(ws))
            sender_task = asyncio.ensure_future(self._request_handler(ws))
            done, pending = await asyncio.wait(
                [listener_task, sender_task],
                return_when=asyncio.FIRST_COMPLETED
            )
            for task in pending:
                task.cancel()

    async def _response_handler(self, ws):
        while True:
            msg = await ws.recv()

    async def _request_handler(self, ws):
        while True:
            msg = await self._request_queue.get()
            await ws.send(msg)

    async def send(self, ws, msg):
        pass

    def connect(self, credentials=None):
        if credentials is None:
            credentials = (self._user, self._pwd)
        asyncio.get_event_loop().run_until_complete(self.lox_comm(credentials))

    def get_credentials(self):
        return self._user, self._pwd

    def get_host(self):
        return self._host

    def request(self, cmd, full_response=False):
        return self.lox_get(self._host, cmd, (self._user, self._pwd), full_response)

    def get_public_key(self):
        pub_key_pem = self.lox_get(self._host, CMD.GET_PUBLIC_KEY)
        # format return by the Miniserver is not a valid PEM format:
        pub_key_pem = re.sub(r'^(-+BEGIN.*?-+)(\w)', r'\1\n\2', pub_key_pem)        # BEGIN and END must be on separate lines
        pub_key_pem = re.sub(r'(\w)(-+END.*?-+)', r'\1\n\2', pub_key_pem)
        pub_key_pem = pub_key_pem.replace("CERTIFICATE", "PUBLIC KEY")              # it's not a certificate but a public key
        pub_key = serialization.load_pem_public_key(
            pub_key_pem.encode('utf-8'),
            backend=default_backend())
        return pub_key

    def encrypt_command(self, command, pub_key):
        aes_iv = os.urandom(16)
        aes_iv = '3790b3fb3c0403c3bd33ca0dd4ed57fa'
        aes_key = '20892f4919759aef35537fa94b7330401f441ffbe901f80154a0047095288142'

        # salt = '5cf8'
        # aes_cipher = 'pGOly+8m8Gcj2EveGP1HK74SYCYrJIXJh53zcetn+Rk='
        # rsa_cipher = 'lz8YMHFNSx6yQztu9wXCYG5DTBvFp7/n9zmZRB2oqgaRegq7muUcWWu5ZIAnZRiNBUb9J7iVNp7C1ue0usdTuI5yU+aEwq87+T+NnQHWEfOi3xnCwSAeVyZ0XhL4VPID05+hLf7pKDSVO5vPXPlnkSr1eXpT1EwllqPX81E2NSw='
        # enc_cmd = 'jdev/sys/fenc/pGOly+8m8Gcj2EveGP1HK74SYCYrJIXJh53zcetn+Rk=?sk=lz8YMHFNSx6yQztu9wXCYG5DTBvFp7/n9zmZRB2oqgaRegq7muUcWWu5ZIAnZRiNBUb9J7iVNp7C1ue0usdTuI5yU+aEwq87+T+NnQHWEfOi3xnCwSAeVyZ0XhL4VPID05+hLf7pKDSVO5vPXPlnkSr1eXpT1EwllqPX81E2NSw='

        # ------   get_token
        aesIV = "c958711cc7031decd02245d294603b83"
        aesKey = "9651d392c6bbf62e5fc73825cb2bc075e4603aac8c3794f2231535b483077071"
        encCmd = "jdev/sys/fenc/F1N/Pz3jTq49W8B3ShcrWZZpueyg9ERkyg2oEIKRS7iWSR+H6G34oAMuFlVBY4Hrz5GljE9Y5GTZPL7WhyitGoxO4YgpU2aZwl/QhIZ/8CIWpyH7dnPdSVR3mL0+ilpZvPpThWGo2Vv7JMIpICP2KOQZeXyv9/QUw/stOH4ulXNET9jSSrV6c9oY+czxEnOW8vmsWx5pYjqwbqY+DlyqEj5kN4IpIEO2cLv0tXRuTfn1GkdNfg65mhEyy7fZAHP9/RDNE6Ox4B04+S6VWir0yX0TMrpWmaETBcliV7t3w/8=?sk=rDD0yyGR5XmwBkCRVo/WTR2wHI3dF0Fxn16JlMCmBKwNQ5haJHL9+nEVEylQfOSwn1igSfW7++6xfkm3ssFcgU2mA1098Qq8KAja5w6lz9fSaJqgB0NYgWyRD/Ri9J+GbxHij+5WtqvnmteS/3mF+B9uS0UH5CkHr6Wr4iJMqro="
        salt = "ca2c"
        # 'rsa_token = 'rDD0yyGR5XmwBkCRVo/WTR2wHI3dF0Fxn16JlMCmBKwNQ5haJHL9+nEVEylQfOSwn1igSfW7++6xfkm3ssFcgU2mA1098Qq8KAja5w6lz9fSaJqgB0NYgWyRD/Ri9J+GbxHij+5WtqvnmteS/3mF+B9uS0UH5CkHr6Wr4iJMqro='

        aes_iv = binascii.unhexlify(aesIV)
        aes_key = binascii.unhexlify(aesKey)

        algo = algorithms.AES(aes_key)
        cipher = Cipher(algo, mode=modes.CBC(aes_iv), backend=default_backend())
        aes = cipher.encryptor()
        aes_ct = aes.update(command.encode('utf-8'))
        aes_ct = binascii.hexlify(aes_ct)
        aes_ct = base64.b64encode(aes_ct).decode('utf-8')

        ref_aes_ct = 'F1N/Pz3jTq49W8B3ShcrWZZpueyg9ERkyg2oEIKRS7iWSR+H6G34oAMuFlVBY4Hrz5GljE9Y5GTZPL7WhyitGoxO4YgpU2aZwl/QhIZ/8CIWpyH7dnPdSVR3mL0+ilpZvPpThWGo2Vv7JMIpICP2KOQZeXyv9/QUw/stOH4ulXNET9jSSrV6c9oY+czxEnOW8vmsWx5pYjqwbqY+DlyqEj5kN4IpIEO2cLv0tXRuTfn1GkdNfg65mhEyy7fZAHP9/RDNE6Ox4B04+S6VWir0yX0TMrpWmaETBcliV7t3w/8='

        rsa_ct = pub_key.encrypt(
            aesKey + ':' + aesIV,
            padding=PKCS1v15()
        )
        rsa_session_key = base64.b64encode(rsa_ct).decode('utf-8')

        enc_cmd = CMD.FENC.format(aes_ct, rsa_session_key)

        return enc_cmd

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

