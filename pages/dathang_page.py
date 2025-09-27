import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from pages.base import Base

class Dathang(Base):

    chon_sanpham = (By.CSS_SELECTOR, ".line_1")
    muahang_btn = (By.CSS_SELECTOR, ".btn.btn-buy-now.rounded-0.w-100.px-4.px-md-3.px-lg-5")
    thanhtoan_btn = (By.CSS_SELECTOR, ".btn.checkout.p-0.text-white.text-center.border-0.rounded")
    nhap_hoten = (By.ID, "billingName")
    nhap_sdt = (By.ID, "billingPhone")
    nhap_diachi = (By.ID, "billingAddress")
    chon_tinhthanh = (By.ID, "billingProvince")
    chon_quanhuyen = (By.ID, "billingDistrict")
    chon_phuongxa = (By.ID, "billingWard")
    chon_pttt = (By.CSS_SELECTOR, ".radio__input")

    dathang_btn = (By.CSS_SELECTOR, ".btn.btn-checkout.spinner")

    tb_loi = (By.CSS_SELECTOR, ".field__message.field__message--error")
    dat_thanhcong = (By.CSS_SELECTOR, ".section__title")

    def dathang (self, hoten, sdt, diachi, tinhthanh, quanhuyen, phuongxa):

        self.click(self.muahang_btn)
        self.click(self.thanhtoan_btn)

        self.type_text(self.nhap_hoten, hoten if hoten else "")
        self.type_text(self.nhap_sdt, sdt if sdt else "")
        self.type_text(self.nhap_diachi, diachi if diachi else "")

        if tinhthanh:
            tinh_select = Select(self.driver.find_element(*self.chon_tinhthanh))
            tinh_select.select_by_visible_text(tinhthanh)

        if quanhuyen:
            quan_select = Select(self.driver.find_element(*self.chon_quanhuyen))
            quan_select.select_by_visible_text(quanhuyen)

        if phuongxa:
            xa_select = Select(self.driver.find_element(*self.chon_phuongxa))
            xa_select.select_by_visible_text(phuongxa)

        self.click(self.chon_pttt)
        time.sleep(1)

        element = self.driver.find_element(*self.dathang_btn)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        try:
            element.click()
        except:
            self.driver.execute_script("arguments[0].click();", element)

        time.sleep(2)

    def lay_thongbao (self):
        try:
            try:
                loi = self.driver.find_element(*self.tb_loi)
                if loi.is_displayed():
                    return loi.text.strip()
            except:
                pass

            try:
                thanhcong = self.driver.find_element(*self.dat_thanhcong)
                if thanhcong.is_displayed():
                    return thanhcong.text.strip()
            except:
                pass

            return None
        except:
            return None