import time

from selenium.common import ElementClickInterceptedException, NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from pages.base import Base

class Timkiem(Base):

    icon_timkiem = (By.CSS_SELECTOR, "a[title='Tìm kiếm']")
    timkiem = (By.NAME, "query")
    ketqua = (By.CSS_SELECTOR, ".title-head.title_search")
    sanpham = (By.CSS_SELECTOR, "div.col-6.col-md-4.col-lg-3")
    chuyentrang = (By.XPATH, "//a[.//svg[contains(@class,'fa-angle-right')]]")

    def tim(self, tukhoa):
        icon = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.icon_timkiem)
        )
        self.driver.execute_script("arguments[0].classList.remove('d-none')", icon)
        self.driver.execute_script("arguments[0].click();", icon)
        time.sleep(1)

        self.type_text(self.timkiem, tukhoa)
        self.driver.find_element(*self.timkiem).send_keys(Keys.RETURN)

    def get_ketqua(self):
        try:
            return self.get_text(self.ketqua).strip()
        except:
            return ""

    def get_sanpham(self):
        total = 0
        wait = WebDriverWait(self.driver, 10)

        while True:
            sanphams = self.driver.find_elements(*self.sanpham)
            total += len(sanphams)

            try:
                next_btn = self.driver.find_element(*self.chuyentrang)
                if "disabled" in next_btn.get_attribute("class") or not next_btn.get_attribute("href"):
                    break
                try:
                    next_btn.click()
                except ElementClickInterceptedException:
                    self.driver.execute_script("arguments[0].click();", next_btn)

                try:
                    wait.until(lambda d: len(d.find_elements(*self.sanpham)) > total)
                except TimeoutException:
                    break

            except NoSuchElementException:
                break

        return total

    def get_soluongsp(self):

        result = self.get_ketqua()
        digits = "".join(filter(str.isdigit, result))
        return int(digits) if digits else 0
