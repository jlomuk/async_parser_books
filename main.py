import asyncio
import sys
import aiohttp
import parsing_fields

from data_store import store_datadict_to_json
from bs4 import BeautifulSoup as bs4
from time import sleep

HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
}
ITEMS = []


def get_books(html_text: str) -> None:
    bs = bs4(html_text, 'lxml')
    list_books = bs.find_all('div', {'data-item-type': 'book'})
    for item in list_books:
        data = {
            'name': parsing_fields.get_name(item),
            'author': parsing_fields.get_author(item),
            'price': parsing_fields.get_price(item),
            'href': parsing_fields.get_href(item)
        }
        ITEMS.append(data)


async def get_page(queue: asyncio.Queue, session: aiohttp.ClientSession) -> None:
    while True:
        url = await queue.get()
        try:
            response = await session.get(url)
            print(f'Status {response.status} - {response.url}')
            get_books(await response.text())
        except Exception as e:
            print('ERROR, reload request', url, e)
            sleep(.5)
            await queue.put(url)
        queue.task_done()


async def producer_queue(queue: asyncio.Queue) -> None:
    pattern = "https://www.bookvoed.ru/books?genre=27&offset={}"
    n = 0
    while n < 1000:
        url = pattern.format(n)
        await queue.put(url)
        n += 60


async def main(workers: int):
    url_queue = asyncio.Queue(maxsize=workers * 2)
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        producer = asyncio.create_task(producer_queue(url_queue))
        tasks = [asyncio.create_task(get_page(url_queue, session)) for _ in range(workers)]
        await asyncio.gather(producer, url_queue.join())
        for task in tasks:
            task.cancel()


if __name__ == '__main__':
    if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    workers = int(input('Введите кол-во асинхронных воркеров: ').strip())
    asyncio.run(main(workers))
    store_datadict_to_json(ITEMS)
    print('Успешно')
