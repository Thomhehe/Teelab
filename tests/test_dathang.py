import os
from datetime import datetime

import pytest
from openpyxl import Workbook, load_workbook
from selenium import webdriver

from pages.dathang_page import Dathang
from utils.data_utils import load_excel_data
from utils.report_utils import write_report
from utils.screenshot_utils import take_screenshot

test_data = load_excel_data("Teelab.xlsx", sheetname="Dathang")

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
    filename_report = r"D:\PyCharm\Teelab\reports\Dathang_Report.xlsx"
    screenshot_path = ""

    try:
        assert expected.strip() == actual.strip(), f"Thông báo mong đợi {expected}, thực tế {actual}"
        status = "PASS"
    except AssertionError:
        status = "FAIL"
        screenshot_path = take_screenshot(driver, f"dathangfail_{hoten}")
        raise
    finally:
        write_report(filename_report, {
            "Thời gian": test_time,
            "Họ tên": hoten,
            "Số điện thoại": sdt,
            "Địa chỉ": diachi,
            "Tình thành": tinhthanh,
            "Quận huyện": quanhuyen,
            "Phường xã": phuongxa,
            "Kết quả mong đợi": expected,
            "Kết quả thực tế": actual,
            "Trạng thái": status,
            "Screenshot": screenshot_path})
        driver.quit()