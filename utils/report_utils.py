import os
from datetime import datetime
from openpyxl import Workbook, load_workbook

_report_initialized = set()

def write_report(filename, data_dict):

    os.makedirs(os.path.dirname(filename), exist_ok=True)

    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_dict = {"Time": time_now, **data_dict}

    # Tạo mới nếu file chưa khởi tạo
    if filename not in _report_initialized or not os.path.exists(filename):
        wb = Workbook()
        ws = wb.active
        ws.title = "Report"
        ws.append(list(data_dict.keys()))
        _report_initialized.add(filename)
    else:
        wb = load_workbook(filename)
        ws = wb.active

    ws.append(list(data_dict.values()))
    wb.save(filename)
    wb.close()
