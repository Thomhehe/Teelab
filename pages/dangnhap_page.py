import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from pages.base import Base

class Dangnhap(Base):

    icon_taikhoan = (By.CSS_SELECTOR, ".user-header.btn-head.d-inline-block.ml-xl-1")
    nhap_email = (By.ID, "customer_email")
    nhap_matkhau = (By.ID, "customer_password")
    dangnhap_btn = (By.CSS_SELECTOR, ".btn.btn-style.btn_50")

    tb_loi = (By.CSS_SELECTOR, ".form-signup")
    thanhcong = (By.CSS_SELECTOR, "p:has(span[style*='color:#ef4339'])")

    def dangnhap(self, email, matkhau):

        self.driver.find_element(*self.icon_taikhoan).click()

        Email = self.driver.find_element(*self.nhap_email)
        Email.clear()
        Email.send_keys(email if email else "")

        Matkhau = self.driver.find_element(*self.nhap_matkhau)
        Matkhau.clear()
        Matkhau.send_keys(matkhau if matkhau else "")

        self.driver.find_element(*self.dangnhap_btn).click()
        time.sleep(1)

    def get_thongbao(self):
        try:
            try:
                dn_thanhcong = self.driver.find_element(*self.thanhcong)
                if dn_thanhcong.is_displayed() and dn_thanhcong.text.strip():
                    return dn_thanhcong.text.strip()
            except:
                pass

            try:
                loi = self.driver.find_element(*self.tb_loi)
                if loi.is_displayed() and loi.text.strip():
                    return loi.text.strip()
            except:
                pass

            try:
                Email = self.driver.find_element(*self.nhap_email)
                Matkhau = self.driver.find_element(*self.nhap_matkhau)

                email_msg = self.driver.execute_script("return arguments[0].validationMessage;", Email)
                if email_msg and email_msg.strip():
                    return email_msg.strip()

                mk_msg = self.driver.execute_script("return arguments[0].validationMessage;", Matkhau)
                if mk_msg and mk_msg.strip():
                    return mk_msg.strip()
            except Exception as e:
                print("Không lấy được validationMessage:", e)

            return ""
        except:
            return ""
