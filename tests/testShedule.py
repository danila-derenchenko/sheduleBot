from ..main import find_schedule


def test_good_data():
    schedule = find_schedule("пятница чётный")
    assert schedule ==  "12345"
