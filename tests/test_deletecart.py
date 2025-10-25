import time
from datetime import datetime

from selenium import webdriver
from pages.deletecart_page import DeleteCart
from utils.report_utils import write_report
from utils.screenshot_utils import take_screenshot

test_data = [("Không có sản phẩm nào trong giỏ hàng của bạn",)]

def test_deletecart():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://teelab.vn/")
    deletecart_page = DeleteCart(driver)

    deletecart_page.select_product_buy()
    details = deletecart_page.get_information_details()
    deletecart_page.add_product_cart()
    cart = deletecart_page.get_information_cart()

    details_color_size = f"{details['color']} / {details['size']}"
    expected_product = f"{details['name']} | {details['price']} | {details_color_size}".strip()
    actual_product = f"{cart['name']} | {cart['price']} | {cart['color_size']}".strip()
    assert expected_product == actual_product, f"Sản phẩm trong giỏ không trùng khớp thông tin chi tiết!"
    print(f"\nExpected: {expected_product}")
    print(f"Actual: {actual_product}")

    deletecart_page.delete()
    time.sleep(1)

    expected_msg = test_data[0][0]
    actual_msg = deletecart_page.get_message()

    print(f"\nExpected message: {expected_msg}")
    print(f"Actual message: {actual_msg}")

    test_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename_report = r"D:\PyCharm\Teelab\reports\DeleteCart_Report.xlsx"
    screenshot_path = ""

    try:
        assert actual_msg.strip() == expected_msg.strip(), f"Expected message: {expected_msg}, Actual message: {actual_msg}"
        status = "PASS"
    except AssertionError:
        status = "FAIL"
        screenshot_path = take_screenshot(driver, f"deletefail_{expected_msg}")
        raise

    finally:
        write_report(filename_report, {
            "Time": test_time,
            "Expected": expected_msg,
            "Actual": actual_msg,
            "Status": status,
            "Screenshot": screenshot_path
        })
        driver.quit()