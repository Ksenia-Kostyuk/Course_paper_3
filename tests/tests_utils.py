from main.utils import filter_operations, sorted_operations, is_card, is_account, mask_number_card, mask_account_number


def test_filter_operations():
    assert filter_operations([{"1": '11', "state": "EXECUTED"}, {}, {"2": "12", "state": "CANCELED"}]) == [{"1": '11', "state": "EXECUTED"}]


def test_sorted_operations():
    assert sorted_operations([{"date": "2023-06-11"}, {"date": "2023-05-12"}, {"date": "2024-06-11"}]) == [{"date": "2024-06-11"}, {"date": "2023-06-11"}, {"date": "2023-05-12"}]


def test_is_card():
    assert is_card("1246377376343588") == True
    assert is_card("14211924144426031657") == False


def test_is_account():
    assert is_account("14211924144426031657") == True
    assert is_account("1246377376343588") == False


def test_mask_number_card():
    assert mask_number_card("Visa Platinum 1246377376343588") == "Visa Platinum 1246 37** **** 3588"

def test_mask_account_number():
    assert mask_account_number("Счет 14211924144426031657") == "Счет **1657"





