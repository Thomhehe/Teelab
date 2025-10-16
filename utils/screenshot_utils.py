import os
from datetime import datetime

def take_screenshot(driver, name_prefix="error"):

    folder_path = os.path.join(os.getcwd(), "screenshots")
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{name_prefix}_{timestamp}.png"
    file_path = os.path.join(folder_path, file_name)

    try:
        driver.save_screenshot(file_path)
        print(f"[SCREENSHOT] Đã lưu ảnh lỗi: {file_path}")
    except Exception as e:
        print(f"[ERROR] Không thể chụp ảnh màn hình: {e}")

    return file_path
