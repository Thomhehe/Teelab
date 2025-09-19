from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://teelab.vn/account/login")

email = driver.find_element(By.ID, "customer_email")
submit = driver.find_element(By.CSS_SELECTOR, ".btn.btn-style.btn_50")

submit.click()  # click nút login
msg = driver.execute_script("arguments[0].reportValidity(); return arguments[0].validationMessage;", email)
print("Validation message:", msg)
driver.quit()
