from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
import time

from selenium.webdriver.support.wait import WebDriverWait

from pages.addcart_page import Cart

class EditCart(Cart):
    increase_btn = (By.CSS_SELECTOR, ".qty-plus.items-count.p-0.border-left")
    decrease_btn = (By.CSS_SELECTOR, ".qty-minus.items-count.p-0.border-right")

    def click_visible_button(self, locator, action_name):
        try:
            elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(locator)
            )
        except TimeoutException:
            raise Exception(f"Không tìm thấy bất kỳ nút {action_name} nào trên trang!")

        # Lọc các phần tử hiển thị (tránh click vào phần tử ẩn)
        visible_buttons = [el for el in elements if el.is_displayed()]

        if not visible_buttons:
            raise Exception(f"Không có nút {action_name} nào hiển thị trên trang!")

        # Lấy nút đầu tiên hiển thị (trong giỏ hàng)
        btn = visible_buttons[0]

        # Click bằng JavaScript để tránh lỗi “element not clickable”
        self.driver.execute_script("arguments[0].click();", btn)
        time.sleep(1)

    def increase_quantity(self, times=1):
        for _ in range(times):
            self.click_visible_button(self.increase_btn, "tăng")

    def decrease_quantity(self, times=1):
        for _ in range(times):
            self.click_visible_button(self.decrease_btn, "giảm")

    def input_quantity(self, qty):
        try:
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.cart_quantity))

            # Dùng JS để gán giá trị và kích hoạt sự kiện "change" cho trang cập nhật
            self.driver.execute_script("""
                arguments[0].value = arguments[1];
                arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            """, element, str(qty))
            time.sleep(1)

        except TimeoutException:
            raise Exception("Không thể nhập vào ô số lượng!")

    def get_quantity(self):
        quantity_element = self.driver.find_element(*self.cart_quantity)
        return int(quantity_element.get_attribute("value"))

    def verify_total_amount(self):
        actual_total = self.get_total_amount()
        expected_total = self.calculate_total_amount()
        assert actual_total == expected_total, \
            f"Tổng tiền sai! Mong đợi: {expected_total}, Thực tế: {actual_total}"
        return actual_total, expected_total
