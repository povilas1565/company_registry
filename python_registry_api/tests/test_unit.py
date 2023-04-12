import pytest
from configmodule import TestingConfig
from app import create_app
from database import db
from helpers import (
    create_test_company,
    add_shareholder,
    generate_name,
    generate_reg_code,
)
import time


@pytest.fixture(scope="function")
def app():
    app = create_app(TestingConfig)
    with app.app_context():
        db.create_all()
    yield app


@pytest.fixture(scope="function")
def client(app):
    return app.test_client()


@pytest.mark.api
def test_create_single_company_should_succeed(client) -> None:
    company = create_test_company()
    company = add_shareholder(company)
    res = client.post("/company/", json=company)
    assert res.status_code == 201
    assert res.json["name"] == company["name"]
    assert res.json["reg_code"] == company["reg_code"]
    assert res.json["shareholders"] == company["shareholders"]


@pytest.mark.api
def test_get_company_should_succeed(client) -> None:
    company = create_test_company()
    company = add_shareholder(company)
    res_post = client.post("/company/", json=company)
    res_get = client.get(f"/company/{company['reg_code']}")
    assert res_get.status_code == 200
    assert res_get.json["name"] == company["name"]
    assert res_get.json["reg_code"] == company["reg_code"]
    assert res_get.json["shareholders"] == company["shareholders"]


@pytest.mark.api
@pytest.mark.parametrize(
    "company, shareholder_variables, expected_error",
    [
        (
            create_test_company(reg_code=generate_reg_code(8), name=generate_name(4)),
            {},
            "Registration code must be 7 digits long and contain only numbers",
        ),
        (
            create_test_company(reg_code=generate_reg_code(6), name=generate_name(4)),
            {},
            "Registration code must be 7 digits long and contain only numbers",
        ),
        (
            create_test_company(reg_code="AAAAAAA", name=generate_name(4)),
            {},
            "Registration code must be 7 digits long and contain only numbers",
        ),
        (
            create_test_company(reg_code="123!<>@", name=generate_name(4)),
            {},
            "Registration code must be 7 digits long and contain only numbers",
        ),
        (
            create_test_company(reg_code=generate_reg_code(7), name=generate_name(2)),
            {},
            "Name must be between 3 and 100 characters long.",
        ),
        (
            create_test_company(reg_code=generate_reg_code(7), name=generate_name(101)),
            {},
            "Name must be between 3 and 100 characters long.",
        ),
        (
            create_test_company(reg_code=None, name=generate_name(4)),
            {},
            "Required info is missing",
        ),
        (
            create_test_company(reg_code=generate_reg_code(7), name=None),
            {},
            "Required info is missing",
        ),
        (
            create_test_company(reg_code=generate_reg_code(7), name="123ABC"),
            {},
            "Company name can include only letters",
        ),
        (
            create_test_company(reg_code=generate_reg_code(7), name="ABC!<>@"),
            {},
            "Company name can include only letters",
        ),
        (
            create_test_company(reg_code=generate_reg_code(7), name=generate_name(4)),
            {"name": "123ABC"},
            "Shareholder name can include only letters",
        ),
        (
            create_test_company(reg_code=generate_reg_code(7), name=generate_name(4)),
            {"name": None},
            "Required info is missing",
        ),
        (
            create_test_company(reg_code=generate_reg_code(7), name=generate_name(4)),
            {"reg_code": None},
            "Required info is missing",
        ),
        (
            create_test_company(reg_code=generate_reg_code(7), name=generate_name(4)),
            {"share_amount": None},
            "Required info is missing",
        ),
        (
            create_test_company(reg_code=generate_reg_code(7), name=generate_name(4)),
            {"share_amount": 2499},
            "Total share amount must be at least 2500",
        ),
        (
            create_test_company(
                reg_code=generate_reg_code(7),
                name=generate_name(4),
                reg_date="2100-01-01",
            ),
            {},
            "Registration date cannot be in the future",
        ),
    ],
)
@pytest.mark.api
def test_create_new_company_out_of_bounds_parameters_should_fail(
    client, company, shareholder_variables, expected_error
) -> None:
    company = company
    company = add_shareholder(company, **shareholder_variables)
    res = client.post("/company/", json=company)
    assert res.status_code == 400
    assert res.json["Error"] == expected_error


@pytest.mark.api
def test_company_name_or_reg_code_already_exists_should_fail(client) -> None:
    company = create_test_company()
    company = add_shareholder(company)
    res_post1 = client.post("/company/", json=company)
    res_post2 = client.post("/company/", json=company)
    assert res_post2.status_code == 400
    assert (
        res_post2.json["Error"] == "Company with this name or reg_code already exists"
    )


@pytest.mark.api
@pytest.mark.xfail
def test_delete_company_should_succeed(client) -> None:
    company = create_test_company(reg_code=generate_reg_code(7), name=generate_name(5))
    company = add_shareholder(company)
    res_post = client.post("/company/", json=company)
    time.sleep(0.5)
    res_del = client.delete(f"/company/{company['reg_code']}")
    assert res_del.status_code == 200
    assert res_del.json["Success"] == f"Company {company['reg_code']} was deleted"


@pytest.mark.api

def test_delete_not_existing_company_should_fail(client) -> None:
    res_del = client.delete(f"/company/999999")
    assert res_del.status_code == 404
    assert res_del.json["Error"] == "Company not found"


@pytest.mark.api
def test_add_shareholder_twice_should_fail(client) -> None:
    company = create_test_company(reg_code=generate_reg_code(7), name=generate_name(5))
    shareholder_variable = {"reg_code": "1234567"}
    company = add_shareholder(company, **shareholder_variable)
    company = add_shareholder(company, **shareholder_variable)
    res = client.post("/company/", json=company)
    assert res.status_code == 400
    assert res.json["Error"] == "Each shareholder must be unique"


@pytest.mark.api
def test_create_delete_create_same_company_should_succeed(client) -> None:
    company = create_test_company(reg_code=generate_reg_code(7), name=generate_name(6))
    company = add_shareholder(company)
    res_post = client.post("/company/", json=company)
    assert res_post.status_code == 201
    time.sleep(0.5)
    res_del = client.delete(f"/company/{company['reg_code']}")
    assert res_del.status_code == 200
    time.sleep(0.5)
    res_post2 = client.post("/company/", json=company)
    assert res_post2.status_code == 201
    assert res_post2.json["name"] == company["name"]
    assert res_post2.json["reg_code"] == company["reg_code"]
    assert res_post2.json["shareholders"] == company["shareholders"]


@pytest.mark.api
@pytest.mark.xfail
def test_update_company_shareholders_should_succeed(client) -> None:
    company = create_test_company(reg_code=generate_reg_code(7), name=generate_name(6))
    company = add_shareholder(company)
    res = client.post("/company/", json=company)
    shareholder_variables = {"reg_code": generate_reg_code(7), "name": generate_name(6)}
    company = add_shareholder(company, **shareholder_variables)
    res = client.put(f"/company/{company['reg_code']}", json=company)
    assert res.status_code == 201
    assert res.json["name"] == company["name"]
    assert res.json["reg_code"] == company["reg_code"]
    assert res.json["shareholders"] == company["shareholders"]


@pytest.mark.api
@pytest.mark.parametrize(
    "company, new_shareholder_variables, expected_error",
    [
        (
            create_test_company(),
            {"share_amount": 2499},
            "Total share amount must be at least 2500",
        ),
        (
            create_test_company(),
            {"reg_code": "123456"},
            "Shareholder reg code must be 11 or 7 digits long and contain only numbers",
        ),
        (
            create_test_company(),
            {"reg_code": "1234567890"},
            "Shareholder reg code must be 11 or 7 digits long and contain only numbers",
        ),
        (
            create_test_company(),
            {"reg_code": "1234ABC"},
            "Shareholder reg code must be 11 or 7 digits long and contain only numbers",
        ),
        (
            create_test_company(),
            {"reg_code": "ABC!<>@"},
            "Shareholder reg code must be 11 or 7 digits long and contain only numbers",
        ),
        (
            create_test_company(),
            {"name": "ABC!<>@"},
            "Shareholder name can include only letters",
        ),
        (
            create_test_company(),
            {"reg_code": "ABC!<>@"},
            "Shareholder reg code must be 11 or 7 digits long and contain only numbers",
        ),
    ],
)
@pytest.mark.api
def test_update_company_shareholders_faulty_parameters_should_fail(
    client, company, new_shareholder_variables, expected_error
) -> None:
    company = add_shareholder(company)
    res = client.post("/company/", json=company)
    company.pop("shareholders")
    time.sleep(0.5)
    company = add_shareholder(company, **new_shareholder_variables)
    res = client.put(f"/company/{company['reg_code']}", json=company)
    assert res.status_code == 400
    assert res.json["Error"] == expected_error


@pytest.mark.api
def test_create_company_with_10_shareholders_should_succeed(client) -> None:
    company = create_test_company(reg_code=generate_reg_code(7), name=generate_name(6))
    for i in range(10):
        shareholder_variables = {
            "reg_code": generate_reg_code(7),
            "name": generate_name(6),
        }
        company = add_shareholder(company, **shareholder_variables)
    print(company)
    res = client.post("/company/", json=company)
    assert res.status_code == 201
    assert res.json["name"] == company["name"]
    assert res.json["reg_code"] == company["reg_code"]
    assert res.json["shareholders"] == company["shareholders"]


@pytest.mark.api
def test_create_company_without_shareholders_should_fail(client) -> None:
    company = create_test_company(reg_code="6666666", name="AS TEST")
    res = client.post("/company/", json=company)
    assert res.status_code == 400
    assert res.json["Error"] == "Unable to create a company without shareholders"

@pytest.mark.xfail
@pytest.mark.api
def test_update_with_existing_shareholder_should_fail(client) -> None:
    company = create_test_company(reg_code=generate_reg_code(7), name=generate_name(6))
    shareholder_variables = {"reg_code": generate_reg_code(7), "name": generate_name(6)}
    company = add_shareholder(company, **shareholder_variables)
    res = client.post("/company/", json=company)
    assert res.status_code == 201
    time.sleep(0.5)
    company = add_shareholder(company, **shareholder_variables)
    res = client.put(f"/company/{company['reg_code']}", json=company)
    assert res.status_code == 400
    assert res.json["Error"] == "Each shareholder must be unique"


@pytest.mark.api
def test_create_company_w_2_shareholders_w_1250_share_capital_should_succeed(
    client,
) -> None:
    company = create_test_company()
    shareholder_variables = {
        "reg_code": generate_reg_code(7),
        "name": generate_name(6),
        "share_amount": 1250,
    }
    shareholder_variables2 = {
        "reg_code": generate_reg_code(7),
        "name": generate_name(6),
        "share_amount": 1250,
    }
    company = add_shareholder(company, **shareholder_variables)
    company = add_shareholder(company, **shareholder_variables2)
    res = client.post("/company/", json=company)
    assert res.status_code == 201
    assert res.json["name"] == company["name"]
    assert res.json["reg_code"] == company["reg_code"]
    assert res.json["shareholders"] == company["shareholders"]


@pytest.mark.api
def test_update_create_company_w_2_shareholders_w_1250_share_capital_should_succeed(
    client,
) -> None:
    company = create_test_company()
    company = add_shareholder(company)
    shareholder_variables = {
        "reg_code": generate_reg_code(7),
        "name": generate_name(6),
        "share_amount": 1250,
    }
    shareholder_variables2 = {
        "reg_code": generate_reg_code(7),
        "name": generate_name(6),
        "share_amount": 1250,
    }
    res = client.post("/company/", json=company)
    assert res.status_code == 201
    time.sleep(0.5)
    company.pop("shareholders")
    company = add_shareholder(company, **shareholder_variables)
    company = add_shareholder(company, **shareholder_variables2)
    res = client.put(f"/company/{company['reg_code']}", json=company)
    assert res.status_code == 201
    assert res.json["name"] == company["name"]
    assert res.json["reg_code"] == company["reg_code"]
    assert res.json["shareholders"] == company["shareholders"]


@pytest.mark.api
def test_get_all_companies(client) -> None:
    for i in range(10):
        company = create_test_company(
            reg_code=generate_reg_code(7), name=generate_name(6)
        )
        shareholder_variables = {
            "reg_code": generate_reg_code(7),
            "name": generate_name(6),
        }
        company = add_shareholder(company, **shareholder_variables)
        res = client.post("/company/", json=company)
        assert res.status_code == 201

    res = client.get("/company/")
    assert res.status_code == 200
    assert len(res.json["result"]) == 10


@pytest.mark.api
def test_create_company_with_combinations_of_physical_and_founders_should_succeed(
    client,
) -> None:
    company = create_test_company()

    for i in range(10):
        if i % 2:
            shareholder_variables = {
                "reg_code": generate_reg_code(11),
                "name": f"{generate_name(6)} {generate_name(6)}",
                "physical_person": True,
            }
            company = add_shareholder(company, **shareholder_variables)
        else:
            shareholder_variables = {
                "reg_code": generate_reg_code(7),
                "name": generate_name(6),
                "physical_person": False,

            }
            company = add_shareholder(company, **shareholder_variables)


    res = client.post("/company/", json=company)
    assert res.status_code == 201
    assert res.json["name"] == company["name"]
    assert res.json["reg_code"] == company["reg_code"]
    assert res.json["shareholders"] == company["shareholders"]


@pytest.mark.api
def test_query_physical_person_should_succeed(client) -> None:
    company = create_test_company(reg_code=generate_reg_code(7), name=generate_name(6))
    shareholder_variables = {
        "name": "Ants Mats",
        "reg_code": "11234567890",
        "physical_person": True,
    }
    company = add_shareholder(company, **shareholder_variables)
    res_post = client.post("/company/", json=company)
    print(res_post.json)
    assert res_post.status_code == 201
    res_get = client.get("/person/?q=11234567890")
    assert res_get.status_code == 200
    assert res_get.json == {
        "result": [{"reg_code": "11234567890", "firstName": "Ants", "lastName": "Mats"}]
    }
