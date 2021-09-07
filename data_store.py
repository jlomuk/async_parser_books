import json


def store_datadict_to_json(datadict: list[dict]) -> None:
    """Сохраняет данные в json в папке из переменной DIRECTORY_FOR_DATA"""
    with open(f'data.json', 'w', encoding='utf8') as file:
        json.dump(datadict, file, indent=4, ensure_ascii=False)
