from selenium.webdriver.common.by import By

from pages.addcart_page import Cart

class DeleteCart(Cart):

    delete_btn = (By.CSS_SELECTOR, "button.btn.btn-outline-danger.remove-item-cart")
    msg = (By.CSS_SELECTOR, "div[class='CartPageContainer'] p")

    def delete(self):
        self.click(self.delete_btn)

    def get_message(self):
        return self.get_text(self.msg)