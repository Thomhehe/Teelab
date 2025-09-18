from datetime import datetime
import os

import pytest
from openpyxl import Workbook, load_workbook
from selenium import webdriver
from pages.timkiem_page import Timkiem
from utils.read import read

test_data = read("Teelab.xlsx")
report_created = False

def report(filename, row_data):
    global report_created
    if not report_created:

        wb = Workbook()
        ws = wb.active
        ws.append([
            "Time",
            "Keyword",
            "Expected",
            "Actual",
            "Actual quantity",
            "Expected quantity",
            "Status"
        ])
        wb.save(filename)
        report_created = True

    wb = load_workbook(filename)
    ws = wb.active
    ws.append(row_data)
    wb.save(filename)

@pytest.mark.parametrize("tukhoa, expected", test_data)
def test_timkiem(tukhoa, expected):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://teelab.vn/")
    timkiem_page = Timkiem(driver)

    timkiem_page.tim(tukhoa)
    result = timkiem_page.get_ketqua()
    so_mongdoi = timkiem_page.get_soluongsp()
    so_thucte = timkiem_page.get_sanpham()

    print(f"Từ khóa: {tukhoa}")
    print(f"Kết quả mong đợi: {expected}")
    print(f"Kết quả thực tế: {result}")
    print(f"Số sản phẩm mong đợi: {so_mongdoi}")
    print(f"Số sản phẩm thực tế: {so_thucte}")

    test_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    assert expected.strip() in result.strip(), "Text kết quả không khớp"
    assert so_thucte == so_mongdoi, f"Số lượng sai: mong đợi {so_mongdoi}, thực tế {so_thucte}"

    status = "PASS"
    report(os.path.join("tests", "report", "Teelab_Result.xlsx"),
           [test_time, tukhoa, expected, result, so_mongdoi, so_thucte, status])
    driver.quit()