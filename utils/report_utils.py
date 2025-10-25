import os
from datetime import datetime
from openpyxl import Workbook, load_workbook

def write_report(filename, data_dict):
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    if "Time" not in data_dict:
        data_dict["Time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ordered_data = {"Time": data_dict.pop("Time")}
    ordered_data.update(data_dict)

    if not os.path.exists(filename):
        wb = Workbook()
        ws = wb.active
        ws.title = "Report"
        ws.append(list(ordered_data.keys()))
        ws.append(list(ordered_data.values()))
        wb.save(filename)
        wb.close()
        return

    wb = load_workbook(filename)
    ws = wb.active

    ws.delete_rows(1, ws.max_row)

    ws.append(list(ordered_data.keys()))
    ws.append(list(ordered_data.values()))

    wb.save(filename)
    wb.close()
