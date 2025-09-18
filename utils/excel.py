import openpyxl

def read(file_path, sheet_name="Timkiem"):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook[sheet_name]

    data = []
    for row in sheet.iter_rows(min_row=2, values_only=True):  # bỏ dòng tiêu đề
        tukhoa, expected = row
        data.append((tukhoa, expected))
    return data

