import asyncio
import json
import logging
import numexpr as ne
from datetime import datetime

logging.basicConfig(filename='server.log', level=logging.INFO)

async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    logging.info(f"Accepted connection from {addr} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    data = await reader.read(1024)
    request = json.loads(data.decode())
    logging.info(f"Received request: {request} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        result = ne.evaluate(request['expression'])
        response = {'result': result.tolist()}
    except Exception as e:
        logging.error(str(e),datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        response = {'error': str(e)}

    writer.write(json.dumps(response).encode())
    logging.info(f"Sending response: {response} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    writer.close()
    await writer.wait_closed()
    logging.info(f"Client {addr} disconnected at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
async def start_server():
    server = await asyncio.start_server(handle_client, 'localhost', 8888)
    addr = server.sockets[0].getsockname()
    logging.info(f"Serving on {addr} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(start_server())