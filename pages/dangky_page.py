import time

from selenium.webdriver.common.by import By

from pages.base import Base

class Dangky(Base):

    icon_taikhoan = (By.CSS_SELECTOR, ".user-header.btn-head.d-inline-block.ml-xl-1")
    chon_dangky = (By.CSS_SELECTOR, ".btn-link-style.btn-register")
    nhap_ho = (By.ID, "lastName")
    nhap_ten = (By.ID, "firstName")
    nhap_email = (By.ID, "email")
    nhap_sdt = (By.NAME, "Phone")
    nhap_matkhau = (By.ID, "password")
    dangky_btn = (By.CSS_SELECTOR, ".btn.btn-style.btn_50")

    tb_loi = (By.CSS_SELECTOR, ".errors")

    def dangky(self, ho, ten, email, sdt, matkhau):

        self.click(self.icon_taikhoan)
        self.click(self.chon_dangky)

        self.type_text(self.nhap_ho, ho or "")
        self.type_text(self.nhap_ten, ten or "")
        self.type_text(self.nhap_email, email or "")
        self.type_text(self.nhap_sdt, sdt or "")
        self.type_text(self.nhap_matkhau, matkhau or "")

        self.click(self.dangky_btn)

    def lay_thongbao(self):
        try:
            try:
                current_url = self.driver.current_url
                if "teelab.vn" in current_url and "account" not in current_url:
                    return ""
            except:
                pass

            try:
                return self.get_text(self.tb_loi).strip()
            except:
                pass

            try:
                Email = self.driver.find_element(*self.nhap_email)
                Sdt = self.driver.find_element(*self.nhap_sdt)

                email_ = self.driver.execute_script("return arguments[0].validationMessage;", Email)
                sdt_ = self.driver.execute_script("return arguments[0].validationMessage;", Sdt)

                if email_:
                    return email_.strip()
                elif sdt_:
                    return sdt_.strip()
            except:
                pass

            return None
        except:
            return None