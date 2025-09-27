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

        self.click(self.icon_taikhoan)

        self.type_text(self.nhap_email, email or "")
        self.type_text(self.nhap_matkhau, matkhau or "")

        self.click(self.dangnhap_btn)

    def lay_thongbao(self):
        try:
            try:
                dn_thanhcong = self.get_text(self.thanhcong)
                if dn_thanhcong:
                    return dn_thanhcong.strip()
            except:
                pass

            try:
                loi = self.get_text(self.tb_loi)
                if loi:
                    return loi.strip()
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
