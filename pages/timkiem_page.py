import time

from selenium.common import ElementClickInterceptedException, NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from pages.base import Base

class Timkiem(Base):

    icon_timkiem = (By.CSS_SELECTOR, "a[title='Tìm kiếm']")
    nhap_tukhoa = (By.NAME, "query")
    ketqua = (By.CSS_SELECTOR, ".title-head.title_search")
    sanpham = (By.CSS_SELECTOR, "div.col-6.col-md-4.col-lg-3")
    chuyentrang_icon = (By.CSS_SELECTOR, "li.page-item.hidden-xs > a.page-link.rounded > svg.fa-angle-right")

    def tim(self, tukhoa):
        icon = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.icon_timkiem)
        )
        self.driver.execute_script("arguments[0].classList.remove('d-none')", icon)
        self.driver.execute_script("arguments[0].click();", icon)
        time.sleep(1)

        self.type_text(self.nhap_tukhoa, tukhoa)
        self.driver.find_element(*self.nhap_tukhoa).send_keys(Keys.RETURN)

    def get_ketqua(self):
        try:
            return self.get_text(self.ketqua).strip()
        except:
            return ""

    def get_slthucte(self):
        wait = WebDriverWait(self.driver, 10)
        all_products = set()

        while True:
            # Lấy danh sách sản phẩm hiện tại
            sanphams = self.driver.find_elements(*self.sanpham)

            for sp in sanphams:
                try:
                    product_key = sp.get_attribute("href") or sp.text
                    if product_key:
                        all_products.add(product_key.strip())
                except Exception:
                    continue

            try:
                # Tìm nút chuyển trang (icon SVG) → lấy thẻ <a> cha để click
                chuyentrang_btn_icon = self.driver.find_element(*self.chuyentrang_icon)
                chuyentrang_btn = chuyentrang_btn_icon.find_element(By.XPATH, "./..")
            except NoSuchElementException:
                break  # Hết trang

            try:
                chuyentrang_btn.click()
            except ElementClickInterceptedException:
                self.driver.execute_script("arguments[0].click();", chuyentrang_btn)

            wait.until(EC.presence_of_all_elements_located(self.sanpham))

        return len(all_products) if all_products else 0

    def get_slmongdoi(self):

        result = self.get_ketqua()
        digits = "".join(filter(str.isdigit, result))
        return int(digits) if digits else 0
