import re
from datetime import datetime
import os

import pytest
from openpyxl import Workbook, load_workbook
from selenium import webdriver
from pages.search_page import Search
from utils.data_utils import load_excel_data
from utils.screenshot_utils import take_screenshot

test_data = load_excel_data("Teelab.xlsx", sheetname="Search")
ids = [f"{i+1}. ({row[0]})" for i, row in enumerate(test_data)]

filename_report = r"D:\PyCharm\Teelab\reports\Search_Report.xlsx"
if os.path.exists(filename_report):
    os.remove(filename_report)

def report(filename, row_data):
    if not os.path.exists(filename):
        wb = Workbook()
        ws = wb.active
        ws.append([
            "Time",
            "Keyword",
            "Expected",
            "Actual",
            "Expected Quantity",
            "Actual Quantity",
            "Status",
            "Screenshot"
        ])
    else:
        wb = load_workbook(filename)
        ws = wb.active

    ws.append(row_data)
    wb.save(filename)

@pytest.mark.parametrize("keyword, expected", test_data, ids=ids)
def test_search(keyword, expected):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://teelab.vn/")
    search_page = Search(driver)

    search_page.search(keyword)
    actual = search_page.get_result()
    quantity_expected = int(re.search(r"\d+", expected).group()) if re.search(r"\d+", expected) else 0
    quantity_actual = search_page.get_quantity()

    print(f"\nKeyword: {keyword}")
    print(f"Expected: {expected}")
    print(f"Actual: {actual}")
    print(f"Quantity expected: {quantity_expected}")
    print(f"Quantity actual: {quantity_actual}")

    test_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    screenshot_path = ""

    try:
        assert expected.strip() == actual.strip(), f"Expected {expected}, Actual {actual}"
        assert quantity_actual == quantity_expected, f"Quantity expected {quantity_expected}, actual {quantity_actual}"
        status = "PASS"
    except AssertionError:
        status = "FAIL"
        screenshot_path = take_screenshot(driver, name_prefix=f"search_{keyword}")
        raise
    finally:
        report(filename_report, [test_time, keyword, expected, actual, quantity_expected, quantity_actual, status, screenshot_path])
        driver.quit()