from bs4 import BeautifulSoup


def no_value_wrapper(func):
    """Обертка в случаи отсутствия значения в описании товара"""

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            return "НЕТ ЗНАЧЕНИЯ"

    return inner


@no_value_wrapper
def get_name(item: BeautifulSoup) -> str:
    return item.select('.Lr.Mr a')[0].text.strip()


@no_value_wrapper
def get_price(item: BeautifulSoup) -> str:
    return item.select('.wg')[0].text.split()[0]


@no_value_wrapper
def get_author(item: BeautifulSoup) -> str:
    return item.select('.Pr')[0].text.strip()


@no_value_wrapper
def get_href(item: BeautifulSoup) -> str:
    return item.select('.Lr.Mr a')[0].get('href')
