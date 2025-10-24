import os
from datetime import datetime

from selenium import webdriver

from pages.addcart_page import Cart
from utils.report_utils import write_report
from utils.screenshot_utils import take_screenshot

def test_addcart():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://teelab.vn/")

    addcart_page = Cart(driver)

    addcart_page.select_product_buy()
    details = addcart_page.get_information_details()
    details_color_size = f"{details['color']} / {details['size']}"
    addcart_page.add_product_cart()
    cart = addcart_page.get_information_cart()

    expected = f"{details['name']} | {details['price']} | {details_color_size}".strip()
    actual = f"{cart['name']} | {cart['price']} | {cart['color_size']}".strip()

    print(f"\nExpected: {expected}")
    print(f"Actual: {actual}")

    # --- Tính tổng tiền mong đợi & lấy tổng tiền thực tế ---
    total_expected = addcart_page.calculate_total_amount()
    total_actual = addcart_page.get_total_amount()

    print(f"Total_expected: {total_expected}")
    print(f"Total_actual: {total_actual}")

    test_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename_report = r"D:\PyCharm\Teelab\reports\AddCart_Report.xlsx"
    screenshot_path = ""

    try:
        assert expected == actual, f"Expected{expected}, actual {actual}"
        assert total_expected == total_actual, f"Expected{total_expected}, actual {total_actual}"
        status = "PASS"
    except AssertionError as e:
        status = "FAIL"
        screenshot_path = take_screenshot(driver, f"addcartfail_{details['name']}")
        raise e
    finally:
        write_report(filename_report, {
            "Time": test_time,
            "Product_Name_Expected": details["name"],
            "Product_Name_Actual": cart["name"],
            "Price_Expected": details["price"],
            "Price_Actual": cart["price"],
            "Color/Size_Expected": details_color_size,
            "Color/Size_Actual": cart["color_size"],
            "Total_Expected": total_expected,
            "Total_Actual": total_actual,
            "Status": status,
            "Screenshot": screenshot_path})
        driver.quit()