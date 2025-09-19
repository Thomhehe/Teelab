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

        self.driver.find_element(*self.icon_taikhoan).click()
        self.driver.find_element(*self.chon_dangky).click()

        Ho = self.driver.find_element(*self.nhap_ho)
        Ho.clear()
        Ho.send_keys(ho if ho else "")

        Ten = self.driver.find_element(*self.nhap_ten)
        Ten.clear()
        Ten.send_keys(ten if ten else "")

        Email = self.driver.find_element(*self.nhap_email)
        Email.clear()
        Email.send_keys(email if email else "")

        Sdt = self.driver.find_element(*self.nhap_sdt)
        Sdt.clear()
        Sdt.send_keys(sdt if sdt else "")

        Matkhau = self.driver.find_element(*self.nhap_matkhau)
        Matkhau.clear()
        Matkhau.send_keys(matkhau if matkhau else "")

        self.driver.find_element(*self.dangky_btn).click()
        time.sleep(1)

    def get_thongbao(self):
        try:
            try:
                current_url = self.driver.current_url
                if "teelab.vn" in current_url and "account" not in current_url:
                    return ""
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