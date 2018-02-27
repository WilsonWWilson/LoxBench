from unpacker import unpack
from comm import LoxComm
from secrets.credentials import user, password
import asyncio


async def echo(websocket, path):
    async for message in websocket:
        await websocket.send(message)


def main():
    comm = LoxComm("192.168.1.111", "80")
    comm.connect((user, password))

# TODO check certificates
# TODO analyze UPD format


if __name__ == "__main__":
    main()
