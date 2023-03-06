import argparse
import asyncio
import json
import logging
import time
from datetime import datetime
logging.basicConfig(filename='client.log', level=logging.INFO)

async def send_request(expression):
    try:
        reader, writer = await asyncio.open_connection('localhost', 8888)
        logging.info(f"Connected to server {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        request = {'expression': expression}
        logging.info(f"Sending request: {request} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        writer.write(json.dumps(request).encode())

        data = await reader.read(1024)
        response = json.loads(data.decode())
        logging.info(f"Received response: {response} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        writer.close()
        await writer.wait_closed()

        if 'result' in response:
            result = response['result']
            print(f'Result: {result}')
        elif 'error' in response:
            error = response['error']
            print(f'Error: {error}')
            logging.error(f"Error in expression '{error}'")
    except:
        logging.error(f"Error: server not found")
async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('expression', nargs='?')
    parser.add_argument('--file')

    args = parser.parse_args()

    if args.expression:
        expression = args.expression
    elif args.file:
        with open(args.txt, 'r') as f:
            expression = f.read()
    else:
        print('Error: no expression or file specified')
        logging.error(f"'Error: no expression or file not found'")
        return

    start_time = time.time()
    await send_request(expression)
    time_work = time.time() - start_time
    logging.info(f'Work time: {time_work} seconds')

if __name__ == '__main__':
    asyncio.run(main())