import time

from selenium.webdriver.common.by import By

from pages.base import Base

class Dangnhap(Base):

    icon_taikhoan = (By.CSS_SELECTOR, ".user-header.btn-head.d-inline-block.ml-xl-1")
    nhap_email = (By.ID, "customer_email")
    nhap_matkhau = (By.ID, "customer_password")
    dangnhap_btn = (By.CSS_SELECTOR, ".btn.btn-style.btn_50")

    tb_loi = (By.CSS_SELECTOR, ".form-signup")
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
        try:
            # 1. Ưu tiên thông báo thành công
            try:
                success = self.driver.find_element(*self.thanhcong)
                if success.is_displayed():
                    return success.text.strip()
            except:
                pass

            # 2. Nếu không thành công thì check lỗi server hiển thị
            try:
                loi = self.driver.find_element(*self.tb_loi)
                if loi.is_displayed():
                    return loi.text.strip()
            except:
                pass

            # 3. Nếu không có 2 cái trên thì check lỗi HTML5
            try:
                Email = self.driver.find_element(*self.nhap_email)
                Matkhau = self.driver.find_element(*self.nhap_matkhau)

                email_msg = self.driver.execute_script("return arguments[0].validationMessage;", Email)
                pass_msg = self.driver.execute_script("return arguments[0].validationMessage;", Matkhau)

                if email_msg:
                    return email_msg.strip()
                elif pass_msg:
                    return pass_msg.strip()
            except:
                pass

            return None
        except:
            return None