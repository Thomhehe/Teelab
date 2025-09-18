from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_icon():
    driver = webdriver.Chrome()
    driver.set_window_size(1024, 768)
    driver.get("https://teelab.vn/")

    wait = WebDriverWait(driver, 10)
    icon = wait.until(EC.presence_of_element_located((By.XPATH, "//a[@title='Tìm kiếm']")))
    driver.execute_script("arguments[0].click();", icon)  # Click bằng JS

    icon.click()

    # Check search box xuất hiện
    search_box = wait.until(EC.presence_of_element_located((By.NAME, "query")))
    assert search_box.is_displayed()

    driver.quit()
