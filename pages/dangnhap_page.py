from selenium.webdriver.common.by import By

from pages.base import Base

class Dangnhap(Base):

    icon_timkiem = (By.CSS_SELECTOR, "a[title='Tìm kiếm']")
    timkiem = (By.NAME, "query")
    ketqua = (By.CSS_SELECTOR, ".title-head.title_search")
    sanpham = (By.CSS_SELECTOR, "div.col-6.col-md-4.col-lg-3")
    chuyentrang = (By.CSS_SELECTOR, ".page-link.rounded")

    def get_ketqua(self):
        return self.get_text(self.ketqua)
