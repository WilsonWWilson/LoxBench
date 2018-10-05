import asyncio
import websockets
import struct
import json


HDR_FORMAT = "BBBBI"


class LoxSocket:
    def __init__(self, host, user, pwd):
        self._request_queue = asyncio.Queue()
        self._host = host
        self._creds = (user, pwd)
        self._ws = None

    async def connect(self, token, credentials=None):
        async with websockets.connect('ws://{}/ws/rfc6455'.format(self._host), subprotocols=['remotecontrol']) as ws:
            self._ws = ws
            # await ws.send(CMD.EXCHANGE_KEY.format(session_key))
            # res = await self._get_ws_response(ws)       # TODO what to do with the session key?
            # if self._token:
            #     await self.authenticate_with_token(ws)
            # else:
            #     await self._acquire_token(credentials)

            listener_task = asyncio.ensure_future(self._response_handler(ws))
            sender_task = asyncio.ensure_future(self._request_handler(ws))
            done, pending = await asyncio.wait(
                [listener_task, sender_task],
                return_when=asyncio.FIRST_COMPLETED
            )
            for task in pending:
                task.cancel()
            self._ws = None

    async def send(self, cmd, full_response=False):
        await self._ws.send(cmd)
        res = await self._get_ws_response(full_response)
        return res

    async def _response_handler(self, ws):
        while True:
            msg = await ws.recv()

    async def _request_handler(self, ws):
        while True:
            msg = await self._request_queue.get()
            await ws.send(msg)

    async def _get_ws_response(self, full_response=False):
        res = await self._ws.recv()
        _, msg_type, info, rsvd, msg_len = struct.unpack_from(HDR_FORMAT, res, 0)
        is_estimated = info & 0x80

        if msg_type == 0:
            msg = await self._ws.recv()
            res = json.loads(msg)['LL']
            if full_response:
                code = res['code'] if 'code' in res else res['Code']    # response is not consistent/ difference between HTTP-Request and socket
                return int(code), res['value'], res['control']
            else:
                return res['value']
