import time

from selenium.common import ElementClickInterceptedException, NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from pages.base import Base

class Search(Base):

    icon_search = (By.CSS_SELECTOR, "a[title='Tìm kiếm']")
    keyword_input = (By.NAME, "query")
    result = (By.CSS_SELECTOR, ".title-head.title_search")
    product = (By.CSS_SELECTOR, "div.col-6.col-md-4.col-lg-3")
    next_icon = (By.CSS_SELECTOR, "li.page-item.hidden-xs > a.page-link.rounded > svg.fa-angle-right")

    def search(self, keyword):
        icon = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.icon_search)
        )
        self.driver.execute_script("arguments[0].classList.remove('d-none')", icon)
        self.driver.execute_script("arguments[0].click();", icon)
        time.sleep(1)

        self.type_text(self.keyword_input, keyword)
        self.driver.find_element(*self.keyword_input).send_keys(Keys.RETURN)

    def get_result(self):
        return self.get_text(self.result).strip()

    def get_quantity(self):
        wait = WebDriverWait(self.driver, 10)
        product_list = set()

        while True:
            # Lấy danh sách sản phẩm hiện tại
            products = self.driver.find_elements(*self.product)

            # Duyệt qua từng sản phẩm trong trang
            for prd in products:
                try:
                    # Lấy ra khóa duy nhất cho sản phẩm
                    keyword = prd.get_attribute("href") or prd.text
                    if keyword:
                        # Thêm vào danh sách sản phẩm - bỏ sản phẩm trùng lặp
                        product_list.add(keyword.strip())
                except Exception:
                    continue

            try:
                # Tìm nút chuyển trang (icon SVG) → lấy thẻ <a> cha để click
                next_btn_icon = self.driver.find_element(*self.next_icon)
                next_btn = next_btn_icon.find_element(By.XPATH, "./..")
            except NoSuchElementException:
                break  # Hết trang

            try:
                next_btn.click()
            except ElementClickInterceptedException:
                self.driver.execute_script("arguments[0].click();", next_btn)

            wait.until(EC.presence_of_all_elements_located(self.product))

        return len(product_list) if product_list else 0

    def get_quantity_expected(self):
        result = self.get_result()
        # Duyệt từng ký tự, chỉ giữ lại ký tự là số
        digits = "".join(filter(str.isdigit, result))
        return int(digits) if digits else 0
