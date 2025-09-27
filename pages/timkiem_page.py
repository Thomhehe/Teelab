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

    def lay_ketqua(self):
        return self.get_text(self.ketqua).strip()

    def lay_slthucte(self):
        wait = WebDriverWait(self.driver, 10)
        ds_sanpham = set()

        while True:
            # Lấy danh sách sản phẩm hiện tại
            sanphams = self.driver.find_elements(*self.sanpham)

            # Duyệt qua từng sản phẩm trong trang
            for sp in sanphams:
                try:
                    # Lấy ra khóa duy nhất cho sản phẩm
                    tukhoa = sp.get_attribute("href") or sp.text
                    if tukhoa:
                        # Thêm vào danh sách sản phẩm - bỏ sản phẩm trùng lặp
                        ds_sanpham.add(tukhoa.strip())
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

        return len(ds_sanpham) if ds_sanpham else 0

    def lay_slmongdoi(self):
        result = self.lay_ketqua()
        # Duyệt từng ký tự, chỉ giữ lại ký tự là số
        digits = "".join(filter(str.isdigit, result))
        return int(digits) if digits else 0
