import json
import os
from pathlib import Path

def load_operations():
    """Загружает список операций из файла"""
    operations = Path(__file__).parent.joinpath('../data/operations.json')
    with open(os.path.join(operations), "r", encoding='utf-8') as operations_list:
        return json.load(operations_list)


def sorted_operations(operations):
    """Сортирует список выполненных операций по дате"""
    operations = sorted(operations, key=lambda operation: operation.get("date", ""), reverse=True)
    return operations


def filter_operations(operations):
    """Фильтрация операций по статусу транзакций"""
    executed_operations = []
    for i in operations:
        if i == {}:
            continue
        elif i["state"] == "EXECUTED":
            executed_operations.append(i)
    return executed_operations[:5]


def is_card(number):
    """Возвращает длину номера карты, необходима для проверки"""
    return len(number.split()[-1]) == 16


def is_account(number):
    """Возвращает длину номера счета пользователя, необходима для проверки"""
    return len(number.split()[-1]) == 20


def operations_from_(from_):
    """Проверяет откуда совершена тарнзакция"""
    if from_:
        if is_card(from_):
            operation["from"] = mask_number_card(from_)
        elif is_account(from_):
            operation["from"] = mask_account_number(from_)


def operations_to(to):
    """Проверяет куда совершена транзакция"""
    if to:
        if is_card(to):
            operation["to"] = mask_number_card(to)
        elif is_account(to):
            operation["to"] = mask_account_number(to)


def mask_operation(operation):
    """Получает доступ к данным  словарей по ключам"""
    from_ = operation.get("from")
    operations_from_(from_)

    to = operation.get("to")
    operations_to(to)



def mask_number_card(card_number):
    """Зашифровывает часть данных карты пользователя"""
    card_parts = card_number.split()
    card_number = card_parts[-1]
    card_name = " ".join(card_parts[:-1])
    masked_number_card = f"{card_name} {card_number[:4]} {card_number[4:6]}** **** {card_number[12:]}"
    return masked_number_card


def mask_account_number(account_number):
    """Зашифровывает лицевой счет пользователя"""
    account_parts = account_number.split()
    account_number = account_parts[-1]
    masked_account_number = f"Счет **{account_number[-4:]}"
    return masked_account_number


def formatter_date(operation):
    """Изменяет формат даты"""
    date = operation.get("date")
    get_date = date[:10]
    return f"{get_date[8:10]}.{get_date[5:7]}.{get_date[0:4]}"


def operation_amount(operation):
    amount_operation = operation.get("operationAmount")
    amount = amount_operation.get("amount")
    return amount.strip('')


def operation_currency(operation):
    amount_operation = operation.get("operationAmount")
    currency = amount_operation.get("currency").get("name")
    return currency.strip('')

if __name__ == '__main__':
    operations = load_operations()
    operations = sorted_operations(operations)
    operations = filter_operations(operations)
    for operation in operations:
        mask_operation(operation)
        print(formatter_date(operation), operation["description"])
        print(f"{operation.get("from", "Источник не известен")} -> {operation["to"]}")
        print(f"{operation_amount(operation)} {operation_currency(operation)} \n")