from openpyxl import load_workbook
from openpyxl import Workbook
import numpy as np

wb = load_workbook('output.xlsx')
print(wb.sheetnames)
ws = wb.get_sheet_by_name('Sheet1')
A = np.array([[i.value for i in j] for j in ws['C1':'I1']]).ravel()
B = np.array([[i.value for i in j] for j in ws['C2':'I2']]).ravel()
d = list(B)
c = list(A)
print(c)
print(d)

print(np.random.choice(c, 100, p=d))
