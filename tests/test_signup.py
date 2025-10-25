from datetime import datetime

import pytest
from selenium import webdriver

from pages.login_page import Login
from pages.signup_page import Signup
from utils.data_utils import load_excel_data
from utils.report_utils import write_report
from utils.screenshot_utils import take_screenshot

test_data = load_excel_data("Teelab.xlsx", sheetname="Signup")

ids = [f"{i+1}. ({row[5]})" for i, row in enumerate(test_data)]

@pytest.mark.parametrize("lastname, name, email, phone, password, expected", test_data, ids=ids)
def test_signup(lastname, name, email, phone, password, expected):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://teelab.vn/")
    login_page = Login(driver)
    signup_page = Signup(driver)

    login_page.account()
    signup_page.signup_select()
    signup_page.lastname_enter(lastname)
    signup_page.name_enter(name)
    signup_page.email_enter(email)
    signup_page.phone_enter(phone)
    signup_page.password_enter(password)
    signup_page.signup_enter()

    actual = signup_page.get_result()

    print(f"\nExpected: {expected}")
    print(f"Actual: {actual}")

    test_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename_report = r"D:\PyCharm\Teelab\reports\Signup_Report.xlsx"
    screenshot_path = ""

    try:
        assert actual.strip() == expected.strip(), f"Expected: {expected}, Actual: {actual}"
        status = "PASS"
    except AssertionError:
        status = "FAIL"
        screenshot_path = take_screenshot(driver, f"signupfail_{email}")
        raise

    finally:
        write_report(filename_report, {
            "Time": test_time,
            "LastName": lastname,
            "Name": name,
            "Email": email,
            "Phone": phone,
            "Password": password,
            "Expected": expected,
            "Actual": actual,
            "Status": status,
            "Screenshot": screenshot_path
        })
        driver.quit()