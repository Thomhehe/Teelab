import os
from datetime import datetime

import pytest
from openpyxl import Workbook, load_workbook
from selenium import webdriver

from pages.dathang_page import Dathang
from utils.data_utils import load_excel_data
from utils.screenshot_utils import take_screenshot

test_data = load_excel_data("Teelab.xlsx", sheetname="Dathang")

filename_report = r"D:\PyCharm\Teelab\reports\Dathang_Report.xlsx"
if os.path.exists(filename_report):
    os.remove(filename_report)

def report(filename, row_data):
    if not os.path.exists(filename):
        wb = Workbook()
        ws = wb.active
        ws.append([
            "Thời gian",
            "Họ tên",
            "Số điện thoại",
            "Địa chỉ",
            "Tình thành",
            "Quận huyện",
            "Phường xã",
            "Kết quả mong đợi",
            "Kết quả thực tế",
            "Trạng thái",
            "Screenshot"
        ])
    else:
        wb = load_workbook(filename)
        ws = wb.active

    ws.append(row_data)
    wb.save(filename)

@pytest.mark.parametrize("hoten, sdt, diachi, tinhthanh, quanhuyen, phuongxa, expected", test_data)
def test_dathang(hoten, sdt, diachi, tinhthanh, quanhuyen, phuongxa, expected):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://teelab.vn/")

    dathang_page = Dathang(driver)
    dathang_page.dathang(hoten, sdt, diachi, tinhthanh, quanhuyen, phuongxa)

    actual = dathang_page.lay_thongbao()

    print(f"Kết quả mong đợi: {expected}")
    print(f"Kết quả thực tế: {actual}")

    test_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    screenshot_path = ""

    try:
        assert expected.strip() == actual.strip(), f"Thông báo mong đợi {expected}, thực tế {actual}"
        status = "PASS"
    except AssertionError:
        status = "FAIL"
        screenshot_path = take_screenshot(driver, f"dathangfail_{hoten}")
        raise
    finally:
        report(filename_report, [test_time, hoten, sdt, diachi, tinhthanh, quanhuyen, phuongxa, expected, actual, status, screenshot_path])
        driver.quit()