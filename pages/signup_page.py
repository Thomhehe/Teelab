from selenium.webdriver.common.by import By

from pages.base import Base

class Signup(Base):

    signup_btn = (By.CSS_SELECTOR, ".btn-link-style.btn-register")
    lastname_input= (By.ID, "lastName")
    name_input = (By.ID, "firstName")
    email_input = (By.ID, "email")
    phone_input = (By.NAME, "Phone")
    password_input = (By.ID, "password")
    signup = (By.CSS_SELECTOR, ".btn.btn-style.btn_50")

    error = (By.CSS_SELECTOR, ".errors")

    def signup_select(self):
        self.click(self.signup_btn)

    def lastname_enter(self, lastname):
        self.type_text(self.lastname_input, lastname or "")

    def name_enter(self, name):
        self.type_text(self.name_input, name or "")

    def email_enter(self, email):
        self.type_text(self.email_input, email or "")

    def phone_enter(self, phone):
        self.type_text(self.phone_input, phone or "")

    def password_enter(self, password):
        self.type_text(self.password_input, password or "")

    def signup_enter (self):
        self.click(self.signup)

    def get_result(self):
        try:
            try:
                current_url = self.driver.current_url
                if "teelab.vn" in current_url and "account" not in current_url:
                    return ""
            except:
                pass

            try:
                return self.get_text(self.error).strip()
            except:
                pass

            try:
                Email = self.driver.find_element(*self.email_input)
                Phone = self.driver.find_element(*self.phone_input)

                email_msg = self.driver.execute_script("return arguments[0].validationMessage;", Email)
                phone_msg = self.driver.execute_script("return arguments[0].validationMessage;", Phone)

                if email_msg:
                    return email_msg.strip()
                elif phone_msg:
                    return phone_msg.strip()
            except:
                pass

            return None
        except:
            return None