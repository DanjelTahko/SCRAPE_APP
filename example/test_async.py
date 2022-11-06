import asyncio 

async def main():
    print('tim')
    await foo('text')

async def foo(text):
    print(text)
    await asyncio.sleep(1)

async def counter():
    new_i = 30
    while (new_i > 0):
        print(new_i)
        new_i -= 1
        await asyncio.sleep(1)


index = 0
while (index<30):
    if (index == 0):
        asyncio.run(counter())

    if (index == 20):
        asyncio.run(main())
    print(index)
    index += 1
