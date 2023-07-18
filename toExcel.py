import pandas as pd
import xlsxwriter
import json
from model.agModel import Desktop

"""with open("desktop.json", encoding='utf-8') as meu_json:
    dados = json.load(meu_json)
print(dados)
"""

a = pd.read_sql_table("desktop.db")
print(a)

'''df = pd.DataFrame(data)

writer = pd.ExcelWriter("output.xlsx", engine="xlsxwriter")
df.to_excel(writer, sheet_name="Sheet1")

workbook = writer.book
worksheet = writer.sheets["Sheet1"]

chart = workbook.add_chart({"type": "line"})
chart.add_series({"values": "=Sheet1!$C$2:$C$4"})
worksheet.insert_chart("E2", chart)

writer.close()'''