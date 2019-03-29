#smtp tarpit
#https://nullprogram.com/blog/2019/03/22/
#implement an SMTP tarpit using asyncio. Bonus points for using TLS connections and testing it against real spammers.

import asyncio
import random

async def handler(_reader, writer):
    writer.write(b'220 \r\n') #smtp greeting https://tools.ietf.org/html/rfc5321#section-4.2
    try:
        while True:
            await asyncio.sleep(5)
            header = random.randint(0, 2**32)
            value = random.randint(0, 2**32)
            writer.write(b'X-%x: %x\r\n' % (header, value))
            await writer.drain()
        except ConnectionResetError:
            pass

async def main():
        server = await asyncio.start_server(handler, '0.0.0.0', 25)
        async with server:
            await server.serve_forever()

asyncio.run(main())
