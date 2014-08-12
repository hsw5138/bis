import xlrd

def get_row_values(inputfile):
	rows = []
	workbook = xlrd.open_workbook(file_contents=inputfile.read())
	sheet = workbook.sheet_by_index(0)
	for rownum in range(sheet.nrows):
		rows.append(sheet.row_values(rownum))
	return rows