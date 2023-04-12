import time

from helpers import generate_name, generate_reg_code
import pytest
from playwright.sync_api import Page


@pytest.fixture()
def navigate(page: Page):
    page.goto("http://testfrontend/")


@pytest.fixture()
def starting_company(page: Page, navigate):
    page.locator("#create").click()
    page.locator("#companyName").fill(generate_name(10))
    page.locator("#regCode").fill(generate_reg_code(7))
    page.locator("#showFormButton").click()
    page.locator("#idCode").fill(generate_reg_code(11))
    page.locator("#firstName").fill(generate_name(5))
    page.locator("#lastName").fill(generate_name(5))
    page.locator("#addButton").click()
    page.locator("#closeButton").click()
    page.locator("#capital").fill("2500")
    page.locator("#createButton").click()

    page.wait_for_selector("#companyHeader", timeout=5000)

@pytest.mark.web
def test_open_home_page_should_succeed(page: Page,navigate) -> None:
    page.wait_for_selector("#create")

@pytest.mark.web
@pytest.mark.xfail
def test_create_new_company_should_succeed(page: Page, starting_company) -> None:
    page.wait_for_selector("#companyHeader")


@pytest.mark.web
def test_add_shareholder_to_existing_company_should_succeed(
    page: Page, starting_company
) -> None:
    page.locator("#editButton").click()
    page.locator("#showFormButton").click()
    page.locator("#idCode").fill(generate_reg_code(11))
    page.locator("#firstName").fill(generate_name(5))
    page.locator("#lastName").fill(generate_name(5))
    page.locator("#addButton").click()
    page.locator("#closeButton").click()
    page.locator("#capital").all().pop().fill("1")

    time.sleep(0.5)
    page.locator("#updateButton").click()
    page.wait_for_selector("#successMessage")


@pytest.mark.web
@pytest.mark.parametrize(
    "company_name, company_reg_code, expected_error",
    [
        (
            generate_name(10),
            generate_reg_code(6),
            "Registration code must be 7 digits long and contain only numbers",
        ),
        (
            generate_name(10),
            generate_reg_code(8),
            "Registration code must be 7 digits long and contain only numbers",
        ),
        (
            generate_name(2),
            generate_reg_code(7),
            "Name must be between 3 and 100 characters long.",
        ),
        (
            generate_name(101),
            generate_reg_code(7),
            "Name must be between 3 and 100 characters long.",
        ),
        ("AS TEST123", generate_reg_code(7), "Company name can include only letters"),
        (
            "<script>alert('test')</script>",
            generate_reg_code(7),
            "Company name can include only letters",
        ),
        (
            "(generate_name(10)",
            "1234ABC",
            "Registration code must be 7 digits long and contain only numbers",
        ),
        (
            "(generate_name(10)",
            "<script>alert('test')</script>",
            "Registration code must be 7 digits long and contain only numbers",
        ),
    ],
)
def test_create_company_faulty_parameters_should_fail(
    page: Page, navigate, company_name, company_reg_code, expected_error
) -> None:
    page.locator("#create").click()
    page.locator("#companyName").fill(company_name)
    entered_name = page.locator("#companyName").input_value()

    if entered_name != company_name and len(entered_name) != len(company_name):
        return

    page.locator("#regCode").fill(company_reg_code)
    entered_reg_code = page.locator("#regCode").input_value()

    if entered_reg_code != company_reg_code and len(entered_reg_code) != len(
        company_reg_code
    ):
        return

    page.locator("#showFormButton").click()
    page.locator("#idCode").fill(generate_reg_code(11))
    page.locator("#firstName").fill(generate_name(5))
    page.locator("#lastName").fill(generate_name(5))
    page.locator("#addButton").click()
    page.locator("#closeButton").click()
    page.locator("#capital").fill("2500")
    page.locator("#createButton").click()

    assert page.locator("#errorMessage").inner_html() == expected_error


@pytest.mark.web
@pytest.mark.parametrize(
    "code, first_name, last_name,is_physical_shareholder, expected_error",
    [
        (
            generate_reg_code(10),
            generate_name(5),
            generate_name(5),
            True,
            "ID code must be exactly 11 digits long",
        ),
        (
            generate_reg_code(12),
            generate_name(5),
            generate_name(5),
            True,
            "ID code must be exactly 11 digits long",
        ),
        ("12345678ABC", generate_name(5), generate_name(5), True, ""),
        (
            "<script>alert('test')</script>",
            generate_name(5),
            generate_name(5),
            True,
            "",
        ),
        (generate_reg_code(11), "123ABCD", generate_name(5), True, ""),
        (
            generate_reg_code(11),
            "<script>alert('test')</script>",
            generate_name(5),
            True,
            "",
        ),
        (generate_reg_code(11), generate_name(5), "123ABCD", True, ""),
        (
            generate_reg_code(11),
            generate_name(5),
            "<script>alert('test')</script>",
            True,
            "",
        ),
        (
            generate_reg_code(11),
            "",
            generate_name(5),
            True,
            "All fields must be filled",
        ),
        (
            generate_reg_code(11),
            generate_name(5),
            "",
            True,
            "All fields must be filled",
        ),
        ("", generate_name(5), generate_name(5), True, "ID code must be exactly 11 digits long"),
        (
            generate_reg_code(6),
            generate_name(5),
            "",
            False,
            "Registration code must be exactly 7 digits long",
        ),
        (
            generate_reg_code(8),
            generate_name(5),
            "",
            False,
            "Registration code must be exactly 7 digits long",
        ),
        (
            "1234ABC",
            generate_name(5),
            "",
            False,
            "Registration code must be exactly 7 digits long",
        ),
        (
            "<script>alert('test')</script>",
            generate_name(5),
            "",
            False,
            "Registration code must be exactly 7 digits long",
        ),
        (generate_reg_code(7), "", "", False, "All fields must be filled"),
        (generate_reg_code(7), "1234ABC", "", False, ""),
        (generate_reg_code(7), "<script>alert('test')</script>", "", False, ""),
    ],
)
def test_shareholder_form_errors_should_fail(
    page: Page, navigate, code, first_name, last_name, is_physical_shareholder, expected_error
) -> None:
    page.locator("#create").click()
    page.locator("#showFormButton").click()
    if is_physical_shareholder:
        page.locator("#idCode").fill(code)
        entered_code = page.locator("#idCode").input_value()
        if entered_code != code:
            return
        page.locator("#firstName").fill(first_name)
        filled_first_name = page.locator("#firstName").input_value()
        if filled_first_name != first_name:
            return
        page.locator("#lastName").fill(last_name)
        filled_last_name = page.locator("#lastName").input_value()
        if filled_last_name != last_name:
            return
    else:
        page.locator("#showJuridicalShareholderForm").click()
        page.locator("#shareholderRegCode").fill(code)
        entered_code = page.locator("#shareholderRegCode").input_value()
        if entered_code != code:
            return
        page.locator("#shareholderName").fill(first_name)
        entered_name = page.locator("#shareholderName").input_value()
        if entered_name != first_name:
            return

    page.locator("#addButton").click()
    try:
        error_msg = page.locator("#lengthError").inner_html(timeout=1000)
    except:
        error_msg = page.locator("#validationError").inner_html()

    assert error_msg == expected_error


@pytest.mark.web

def test_insufficient_share_capital_should_fail(page: Page, navigate) -> None:
    page.locator("#create").click()
    page.locator("#companyName").fill(generate_name(10))
    page.locator("#regCode").fill(generate_reg_code(7))
    page.locator("#showFormButton").click()
    page.locator("#idCode").fill(generate_reg_code(11))
    page.locator("#firstName").fill(generate_name(5))
    page.locator("#lastName").fill(generate_name(5))
    page.locator("#addButton").click()
    page.locator("#closeButton").click()
    page.locator("#capital").fill("2499")
    page.locator("#createButton").click()
    assert page.locator("#errorMessage").inner_html() == "Total share capital must be at least 2500EUR."



@pytest.mark.web
def test_duplicate_shareholders_should_fail(page: Page, navigate) -> None:
    page.locator("#create").click()
    page.locator("#companyName").fill(generate_name(10))
    page.locator("#regCode").fill(generate_reg_code(7))
    page.locator("#showFormButton").click()
    page.locator("#idCode").fill("12345678901")
    page.locator("#firstName").fill("First")
    page.locator("#lastName").fill("Last")
    page.locator("#addButton").click()
    page.locator("#idCode").fill("12345678901")
    page.locator("#firstName").fill("First")
    page.locator("#lastName").fill("Last")
    page.locator("#addButton").click()
    page.locator("#closeButton").click()
    locators = page.locator("#capital").all()
    for locator in locators:
        locator.fill("1250")
    page.locator("#createButton").click()
    assert (
        page.locator("#errorMessage").inner_html()
        == "Each shareholder must have unique code"
    )


@pytest.mark.web
def test_2_shareholders_1_no_capital_should_fail(page: Page, navigate) -> None:
    page.locator("#create").click()
    page.locator("#companyName").fill(generate_name(10))
    page.locator("#regCode").fill(generate_reg_code(7))
    page.locator("#showFormButton").click()
    page.locator("#idCode").fill(generate_reg_code(11))
    page.locator("#firstName").fill(generate_name(10))
    page.locator("#lastName").fill(generate_name(10))
    page.locator("#addButton").click()
    page.locator("#idCode").fill(generate_reg_code(11))
    page.locator("#firstName").fill(generate_name(10))
    page.locator("#lastName").fill(generate_name(10))
    page.locator("#addButton").click()
    page.locator("#closeButton").click()
    locators = page.locator("#capital").all()
    locators[0].fill("2500")
    page.locator("#createButton").click()
    assert page.locator("#errorMessage").inner_html() == "All shareholders must have share capital"

@pytest.mark.web
@pytest.mark.xfail
def test_update_add_already_existing_shareholder_should_fail(
    page: Page, starting_company
) -> None:
    page.locator("#editButton").click()
    page.locator("#showFormButton").click()
    page.locator("#idCode").fill(generate_reg_code(11))
    page.locator("#firstName").fill(generate_name(5))
    page.locator("#lastName").fill(generate_name(5))
    page.locator("#addButton").click()
    page.locator("#closeButton").click()
    page.locator("#capital").all().pop().fill("1")

    time.sleep(0.5)
    page.locator("#updateButton").click()
    page.wait_for_selector("#successMessage")
    assert page.locator("#founder").all().pop().input_value() == "false"

@pytest.mark.web
@pytest.mark.xfail
def test_update_add_shareholder_empty_capital_should_fail(
    page: Page, starting_company
) -> None:
    page.locator("#editButton").click()
    page.locator("#showFormButton").click()
    page.locator("#idCode").fill(generate_reg_code(11))
    page.locator("#firstName").fill(generate_name(5))
    page.locator("#lastName").fill(generate_name(5))
    page.locator("#addButton").click()
    page.locator("#closeButton").click()
    page.locator("#updateButton").click()
    assert page.locator("#errorMessage").inner_html() == "All shareholders must have share capital"

@pytest.mark.web
def test_update_insufficient_capital_should_fail(
    page: Page, starting_company
) -> None:
    page.locator("#editButton").click()
    page.locator("#showFormButton").click()
    page.locator("#idCode").fill(generate_reg_code(11))
    page.locator("#firstName").fill(generate_name(5))
    page.locator("#lastName").fill(generate_name(5))
    page.locator("#addButton").click()
    page.locator("#closeButton").click()
    locators = page.locator("#capital").all()
    for locator in locators:
        locator.fill("1249")

    page.locator("#updateButton").click()
    assert page.locator("#errorMessage").inner_html() == "Total share capital must be at least 2500EUR."
@pytest.mark.web
@pytest.mark.xfail
def test_added_shareholder_should_not_be_founder_should_succeed(
    page: Page, starting_company
) -> None:
    page.locator("#editButton").click()
    page.locator("#showFormButton").click()
    page.locator("#idCode").fill(generate_reg_code(11))
    page.locator("#firstName").fill(generate_name(5))
    page.locator("#lastName").fill(generate_name(5))
    page.locator("#addButton").click()
    page.locator("#closeButton").click()
    page.locator("#capital").all().pop().fill("1")

    time.sleep(0.5)
    page.locator("#updateButton").click()
    page.wait_for_selector("#successMessage")
    assert page.locator("#founder").all().pop().input_value() == "false"


@pytest.mark.web
@pytest.mark.xfail
def test_create_company_physical_and_juridical_shareholder_should_succeed(
    page: Page, navigate
) -> None:
    page.locator("#create").click()
    page.locator("#companyName").fill(generate_name(10))
    page.locator("#regCode").fill(generate_reg_code(7))
    page.locator("#showFormButton").click()
    page.locator("#idCode").fill(generate_reg_code(11))
    page.locator("#firstName").fill(generate_name(5))
    page.locator("#lastName").fill(generate_name(5))
    page.locator("#addButton").click()
    page.locator("#showJuridicalShareholderForm").click()
    page.locator("#shareholderRegCode").fill(generate_reg_code(7))
    page.locator("#shareholderName").fill(generate_name(5))
    page.locator("#addButton").click()
    page.locator("#closeButton").click()
    locators = page.locator("#capital").all()

    for locator in locators:
        locator.fill("1250")

    page.locator("#createButton").click()
    page.wait_for_selector("#companyHeader")


@pytest.mark.web
@pytest.mark.xfail
def test_create_company_with_10_shareholders_should_succeed(page: Page, navigate):
    page.locator("#create").click()
    page.locator("#companyName").fill(generate_name(10))
    page.locator("#regCode").fill(generate_reg_code(7))
    page.locator("#showFormButton").click()
    for i in range(10):
        if i % 2:
            page.locator("#showPhysicalShareholderForm").click()
            page.locator("#idCode").fill(generate_reg_code(11))
            page.locator("#firstName").fill(generate_name(5))
            page.locator("#lastName").fill(generate_name(5))
        else:
            page.locator("#showJuridicalShareholderForm").click()
            page.locator("#shareholderRegCode").fill(generate_reg_code(7))
            page.locator("#shareholderName").fill(generate_name(5))
        page.locator("#addButton").click()

    page.locator("#closeButton").click()
    locators = page.locator("#capital").all()

    for locator in locators:
        locator.fill("250")
    page.locator("#createButton").click()
    page.wait_for_selector("#companyHeader")

@pytest.mark.web
def test_search_company_physical_shareholder_should_succeed(page: Page, navigate):
        company_reg_code = generate_reg_code(7)
        company_name = generate_name(12)
        first_name = generate_name(12)
        last_name = generate_name(12)
        id_code = generate_reg_code(11)
        page.locator("#create").click()
        page.locator("#companyName").fill(company_name)
        page.locator("#regCode").fill(company_reg_code)
        page.locator("#showFormButton").click()
        page.locator("#idCode").fill(id_code)
        page.locator("#firstName").fill(first_name)
        page.locator("#lastName").fill(last_name)
        page.locator("#addButton").click()
        page.locator("#closeButton").click()
        page.locator("#capital").fill("2500")
        page.locator("#createButton").click()
        time.sleep(0.5)

        page.wait_for_selector("#companyHeader", timeout=2000)
        page.goto("http://testfrontend/")

        page.locator("#search").fill(company_reg_code)
        result = page.get_by_text(f"{company_reg_code} -- {company_name}")
        assert result
        page.locator("#search").clear()

        page.locator("#search").fill(id_code)
        result = page.get_by_text(f"{company_reg_code} -- {company_name}")
        assert result
        page.locator("#search").clear()

        for i in range(0,12,3):
            page.locator("#search").fill(company_name[i:i + 3])
            result = page.get_by_text(f"{company_reg_code} -- {company_name}")
            assert result
            page.locator("#search").clear()
            page.locator("#search").fill(first_name[i:i + 3])
            result = page.get_by_text(f"{company_reg_code} -- {company_name}")
            assert result
            page.locator("#search").clear()
            page.locator("#search").fill(last_name[i:i + 3])
            result = page.get_by_text(f"{company_reg_code} -- {company_name}")
            assert result
            page.locator("#search").clear()


@pytest.mark.web
def test_search_company_juridical_shareholder_should_succeed(page: Page, navigate):
    company_reg_code = generate_reg_code(7)
    company_name = generate_name(12)
    reg_code = generate_reg_code(7)
    name = generate_name(12)

    page.locator("#create").click()
    page.locator("#companyName").fill(company_name)
    page.locator("#regCode").fill(company_reg_code)
    page.locator("#showFormButton").click()
    page.locator("#showJuridicalShareholderForm").click()
    page.locator("#shareholderRegCode").fill(reg_code)
    page.locator("#shareholderName").fill(name)
    page.locator("#addButton").click()
    page.locator("#closeButton").click()
    page.locator("#capital").fill("2500")
    page.locator("#createButton").click()
    time.sleep(0.5)

    page.wait_for_selector("#companyHeader", timeout=2000)
    page.goto("http://testfrontend/")

    page.locator("#search").fill(company_reg_code)
    result = page.get_by_text(f"{company_reg_code} -- {company_name}")
    assert result
    page.locator("#search").clear()

    page.locator("#search").fill(reg_code)
    result = page.get_by_text(f"{company_reg_code} -- {company_name}")
    assert result
    page.locator("#search").clear()

    for i in range(0, 12, 3):
        page.locator("#search").fill(company_name[i:i + 3])
        result = page.get_by_text(f"{company_reg_code} -- {company_name}")
        assert result
        page.locator("#search").clear()
        page.locator("#search").fill(name[i:i + 3])
        result = page.get_by_text(f"{company_reg_code} -- {company_name}")
        assert result
        page.locator("#search").clear()

def test_all_info_is_present_on_company_page():
    pass