from selenium.webdriver.common.by import By

from pages.base import Base

class Dangnhap(Base):

    icon_taikhoan = (By.CSS_SELECTOR, ".user-header.btn-head.d-inline-block.ml-xl-1")
    dangky = (By.CSS_SELECTOR, ".btn-link-style.btn-register")
    nhap_ho = (By.ID, "lastName")
    sanpham = (By.CSS_SELECTOR, "div.col-6.col-md-4.col-lg-3")
    chuyentrang = (By.CSS_SELECTOR, ".page-link.rounded")

    def get_ketqua(self):
        return self.get_text(self.ketqua)
