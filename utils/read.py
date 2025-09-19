import openpyxl

def read(file_path, sheet_name):
    workbook = openpyxl.load_workbook(file_path, data_only=True)
    sheet = workbook[sheet_name]

    data = []
    for i in range(2, sheet.max_row + 1):  # bắt đầu từ dòng 2
        row_data = []
        for j in range(1, sheet.max_column + 1):
            cell = sheet.cell(row=i, column=j).value
            row_data.append(cell if cell is not None else "")
        data.append(tuple(row_data))
    workbook.close()
    return data