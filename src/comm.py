from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from cryptography.hazmat.primitives import serialization, hashes, hmac
import base64
import asyncio
import websockets
import requests
import re
import os
import struct
import json
import binascii


TOKEN_CFG_VERSION = "8.4.5.10"
ENCRYPTION_CFG_VERSION = "8.1.10.14"
HDR_FORMAT = "BBBBI"


class CMD:
    GET_API = "jdev/cfg/api"
    GET_PUBLIC_KEY = "jdev/sys/getPublicKey"
    GET_TOKEN = "jdev/sys/gettoken/{hash}/{user}/{permission}/{uuid}/{info}"
    FENC = "jdev/sys/fenc/"     # ???
    GET_SALT_AND_KEY = "jdev/sys/getkey2/{}"
    EXCHANGE_KEY = "jdev/sys/keyexchange/{}"
    AUTH_WITH_TOKEN = "authwithoken/{}/{}"


class Permission:
    WEB = 2     # short lifespan
    APP = 4     # last > 4 weeks


class LoxComm:
    def __init__(self, ip, port):
        self._ip = ip
        self._port = port
        self._token = None
        self._request_queue = asyncio.Queue()

    @staticmethod
    def lox_get(ip, cmd, full_response=False):
        r = requests.get('http://{}/{}'.format(ip, cmd))
        res = r.json()['LL']
        if full_response:
            return res['Code'], res['value'], res['control']        # can't unify it with parsing of socket response, because there the 'code' is lowercase
        else:
            return res['value']

    async def _get_public_key(self):
        pub_key_pem = self.lox_get(self._ip, CMD.GET_PUBLIC_KEY)
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
        cmd = CMD.GET_TOKEN.format(hash=cred_hash, user=user, permission=Permission.WEB, uuid="0a8c7351-00ac-1e18-ffff112233445566", info="Hugin")
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
        # authenticate("192.168.1.111", )
        async with websockets.connect('ws://{}:{}/ws/rfc6455'.format(self._ip, self._port)) as ws:
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

    def connect(self, credentials):
        asyncio.get_event_loop().run_until_complete(self.lox_comm(credentials))
