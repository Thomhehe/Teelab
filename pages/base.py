from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

class Base:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 5)

    #đợi đến khi element click được
    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    #đợi đến khi element tồn tại trong DOM để nhập
    def type_text(self, locator, text):
        element = self.wait.until(EC.presence_of_element_located(locator))
        element.clear()
        element.send_keys(text)

    #trả về danh sách elements(list)
    def get_elements(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def get_text(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator)).text