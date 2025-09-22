import openpyxl

def read(file_path, sheet_name):
    sheet = openpyxl.load_workbook(file_path, data_only=True)[sheet_name]
    data = [
        tuple(cell or "" for cell in row)
        for row in sheet.iter_rows(min_row=2, values_only=True)
        if any(cell not in (None, "") for cell in row)
    ]
    return data