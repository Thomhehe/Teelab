import time
from selenium import webdriver

from pages.editcart_page import EditCart
from utils.data_utils import load_excel_data
import pytest

from utils.report_utils import write_report
from utils.screenshot_utils import take_screenshot

test_data = load_excel_data(sheetname="EditQuantity")

formatted_data = []
ids = []
for i, row in enumerate(test_data):
    try:
        action_ = str(row[0]).strip().lower()
        value_ = int(row[1])
        formatted_data.append((action_, value_))
        ids.append(f"{i+1}. ({action_} {value_})")
    except Exception as e:
        print(f"Bỏ qua dòng dữ liệu lỗi: {row} ({e})")

@pytest.mark.parametrize("action, value", formatted_data, ids=ids)
def test_editcart(action, value):
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://teelab.vn/")

    editcart_page = EditCart(driver)
    editcart_page.select_product_buy()
    details = editcart_page.get_information_details()
    editcart_page.add_product_cart()
    cart = editcart_page.get_information_cart()

    details_color_size = f"{details['color']} / {details['size']}"
    expected = f"{details['name']} | {details['price']} | {details_color_size}".strip()
    actual = f"{cart['name']} | {cart['price']} | {cart['color_size']}".strip()
    assert expected == actual, f"Sản phẩm trong giỏ không trùng khớp thông tin chi tiết!"
    print(f"\nExpected: {expected}")
    print(f"Actual: {actual}")

    time.sleep(2)

    old_qty = editcart_page.get_quantity()

    if action == "decrease" and old_qty <= value:
        print("Số lượng quá thấp, tự động tăng trước để tránh xóa sản phẩm.")
        editcart_page.increase_quantity(times=value + 1)
        time.sleep(1)
        old_qty = editcart_page.get_quantity()

    if action == "increase":
        editcart_page.increase_quantity(times=value)
        expected_qty = old_qty + value
    elif action == "decrease":
        editcart_page.decrease_quantity(times=value)
        expected_qty = max(1, old_qty - value)
    elif action == "input_quantity":
        editcart_page.input_quantity(qty=value)
        expected_qty = value
    else:
        pytest.skip(f"Hành động không hợp lệ: {action}")
    time.sleep(2)

    new_qty = editcart_page.get_quantity()
    actual_total, expected_total = editcart_page.get_actual_and_expected_total()
    screenshot_path = ""

    if new_qty == expected_qty and actual_total == expected_total:
        status = "PASS"
    else:
        status = "FAIL"
        screenshot_path = take_screenshot(driver, name_prefix=f"editcart_{action}")

    print(f"[{action}] Expected quantity={expected_qty}, Actual quantity={new_qty}")
    print(f"[{action}] Expected total={expected_total}, Actual total={actual_total}")

    filename_report = r"D:\PyCharm\Teelab\reports\EditCart_Report.xlsx"

    write_report(filename_report, {
        "Action": action,
        "Value": value,
        "Expected_Qty": expected_qty,
        "Actual_Qty": new_qty,
        "Expected_Total": expected_total,
        "Actual_Total": actual_total,
        "Status": status,
        "Screenshot": screenshot_path
    })

    driver.quit()
