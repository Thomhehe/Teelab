from selenium.webdriver.common.by import By

from pages.base import Base

class Login(Base):

    icon_account = (By.CSS_SELECTOR, ".user-header.btn-head.d-inline-block.ml-xl-1")
    email_input = (By.ID, "customer_email")
    password_input = (By.ID, "customer_password")
    login_btn = (By.CSS_SELECTOR, ".btn.btn-style.btn_50")

    error = (By.CSS_SELECTOR, ".form-signup")
    success = (By.CSS_SELECTOR, "p:has(span[style*='color:#ef4339'])")

    def account(self):
        self.click(self.icon_account)

    def email_enter(self, email):
        self.type_text(self.email_input, email or "")

    def password_enter(self, password):
        self.type_text(self.password_input, password or "")

    def login(self):
        self.click(self.login_btn)

    def get_result(self):
        try:
            try:
                success_login = self.get_text(self.success)
                if success_login:
                    return success_login.strip()
            except:
                pass

            try:
                error_login = self.get_text(self.error)
                if error_login:
                    return error_login.strip()
            except:
                pass

            try:
                Email = self.driver.find_element(*self.email_input)
                Password = self.driver.find_element(*self.password_input)

                email_msg = self.driver.execute_script("return arguments[0].validationMessage;", Email)
                if email_msg and email_msg.strip():
                    return email_msg.strip()

                pw_msg = self.driver.execute_script("return arguments[0].validationMessage;", Password)
                if pw_msg and pw_msg.strip():
                    return pw_msg.strip()
            except Exception as e:
                print("Không lấy được validationMessage:", e)

            return ""
        except:
            return ""
