# import openpyxl
#
# def read(file_path, sheet_name):
#     workbook = openpyxl.load_workbook(file_path)
#     sheet = workbook[sheet_name]
#
#     data = []
#     for i in range(2, sheet.max_row + 1):  # bắt đầu từ dòng 2
#         row_data = []
#         for j in range(1, sheet.max_column + 1):
#             cell = sheet.cell(row=i, column=j).value
#             row_data.append(cell if cell is not None else "")
#         data.append(tuple(row_data))
#     return data

import pandas as pd

def read(file_path, sheet_name):
    # Đọc file Excel, không coi dòng nào là header
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=None, dtype=str)

    # Thay None thành chuỗi rỗng
    df = df.fillna("")

    # Bỏ dòng đầu tiên nếu nó là header "Email, Password, Expected"
    data = df.values.tolist()[1:]

    return [tuple(row) for row in data]
