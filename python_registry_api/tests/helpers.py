import random
import string


def create_test_company(reg_code="1111112", name="Test Company", reg_date="2022-01-01"):
    company = {"reg_code": reg_code, "name": name, "reg_date": reg_date}
    return company


def add_shareholder(company, **kwargs):
    shareholder = {
        "name": "Test Company",
        "reg_code": "1234567",
        "share_amount": 2500,
        "founder": True,
        "physical_person": False,
    }
    if kwargs:
        for key in kwargs.keys():
            if kwargs[key] == None:
                shareholder.pop(key)
            else:
                shareholder[key] = kwargs[key]
    try:
        company["shareholders"].append(shareholder)
    except:
        shareholder = {"shareholders": [shareholder]}
        company.update(shareholder)

    return company


def generate_name(length):
    letters = string.ascii_lowercase
    result_str = "".join(random.choice(letters) for i in range(length))
    return result_str


def generate_reg_code(length):
    letters = string.digits
    result_str = "".join(random.choice(letters) for i in range(length))
    return result_str
