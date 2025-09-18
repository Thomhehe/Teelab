import datetime
import os

import pytest
from openpyxl import Workbook, load_workbook
from selenium import webdriver
from pages.timkiem_page import Timkiem
from utils.excel import read

test_data = read("Teelab.xlsx")
report_file = "Teelab_Result.xlsx"

# Hàm ghi dữ liệu vào Excel
def report(filename, row_data):
    if not os.path.exists(filename):
        # Tạo file Excel mới + header nếu chưa có
        wb = Workbook()
        ws = wb.active
        ws.append([
            "Thời gian Test",
            "Từ khóa",
            "Expected",
            "Actual",
            "Đếm Sản phẩm",
            "Số lượng sản phẩm muốn",
            "Status"
        ])
        wb.save(filename)

    # Mở file và ghi thêm kết quả
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
    print(f"Từ khóa: {tukhoa} | Kết quả thực tế: {result} | Mong đợi: {expected}")
    # assert expected in result

    so_sanpham = timkiem_page.get_sanpham_count()
    print(f"Số sản phẩm thực tế: {so_sanpham}")

    so_text = int("".join(filter(str.isdigit, result)))
    print(f"Số sản phẩm trong text: {so_text}")
    status = "PASS"
    try:
        assert expected in result
        assert so_sanpham == so_text
    except AssertionError:
        status = "FAIL"

    test_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report("Teelab_Result.xlsx", [test_time, tukhoa, expected, result, so_sanpham, so_text, status])

    driver.quit()
