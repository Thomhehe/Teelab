from datetime import datetime

import pytest
from selenium import webdriver

from pages.login_page import Login
from utils.data_utils import load_excel_data
from utils.report_utils import write_report
from utils.screenshot_utils import take_screenshot

test_data = load_excel_data("Teelab.xlsx", sheetname="Login")
ids = [f"{i+1}. ({row[2]})" for i, row in enumerate(test_data)]

@pytest.mark.parametrize("email, password, expected", test_data, ids=ids)
def test_login(email, password, expected):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://teelab.vn/")
    login_page = Login(driver)

    login_page.account()
    login_page.email_enter(email)
    login_page.password_enter(password)
    login_page.login()

    actual = login_page.get_result()

    print(f"\nExpected: {expected}")
    print(f"Actual: {actual}")

    filename_report = r"D:\PyCharm\Teelab\reports\Login_Report.xlsx"
    screenshot_path = ""

    try:
        assert actual.strip() == expected.strip(), f"Expected: {expected}, Actual: {actual}"
        status = "PASS"
    except AssertionError:
        status = "FAIL"
        screenshot_path = take_screenshot(driver, f"loginfail_{email}")
        raise

    finally:
        write_report(filename_report, {
            "Email": email,
            "Password": password,
            "Expected": expected,
            "Actual": actual,
            "Status": status,
            "Screenshot": screenshot_path
        })
        driver.quit()