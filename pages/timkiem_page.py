import time

from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from pages.base import Base

class Timkiem(Base):

    icon_timkiem = (By.CSS_SELECTOR, "a[title='Tìm kiếm']")
    timkiem = (By.NAME, "query")
    ketqua = (By.CSS_SELECTOR, ".title-head.title_search")
    sanpham = (By.CSS_SELECTOR, ".item_product_main")

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
        return self.get_text(self.ketqua)


    def get_sanpham(self):
        products = self.get_elements(self.sanpham)
        return len(products)