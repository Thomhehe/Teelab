import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from pages.base import Base

class Dangnhap(Base):

    icon_taikhoan = (By.CSS_SELECTOR, ".user-header.btn-head.d-inline-block.ml-xl-1")
    nhap_email = (By.ID, "customer_email")
    nhap_matkhau = (By.ID, "customer_password")
    dangnhap_btn = (By.CSS_SELECTOR, ".btn.btn-style.btn_50")

    tb_loi = (By.CSS_SELECTOR, "span.form-signup")
    thanhcong = (By.CSS_SELECTOR, "p:has(span[style*='color:#ef4339'])")

    def dangnhap(self, email, matkhau):

        Email = self.driver.find_element(*self.nhap_email)
        Email.clear()
        Email.send_keys(email if email else "")

        Matkhau = self.driver.find_element(*self.nhap_matkhau)
        Matkhau.clear()
        Matkhau.send_keys(matkhau if matkhau else "")

        self.driver.find_element(*self.dangnhap_btn).click()
        time.sleep(1)

    def get_thongbao(self):

        Email = self.driver.find_element(*self.nhap_email)
        Matkhau = self.driver.find_element(*self.nhap_matkhau)

        if Email.get_attribute("validationMessage"):
            return Email.get_attribute("validationMessage")
        if Matkhau.get_attribute("validationMessage"):
            return Matkhau.get_attribute("validationMessage")

        try:
            loi = self.driver.find_element(*self.tb_loi)
            if loi.is_displayed():
                return loi.text.strip()
        except NoSuchElementException:
            pass

        try:
            success = self.driver.find_element(*self.thanhcong)
            if success.is_displayed():
                return success.text.strip()
        except NoSuchElementException:
            pass

        return ""