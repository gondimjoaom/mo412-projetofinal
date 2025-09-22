import pandas as pd
import openpyxl
from collections import defaultdict
import json
# from node import Node
excel_file_path = "Histórico de Defesas de Mestrado e Doutorado.xlsx"
workbook = openpyxl.load_workbook(excel_file_path)


for ano in range(2006, 2025):
    ano = str(ano)
    sheet = workbook[ano]# Or specify a sheet name: workbook['Sheet1']
    hyperlinks_data = {"tipo": [], "url": []}


    tipo = None
    for row_index, row in enumerate(sheet.iter_rows(), start=1):
        for col_index, cell in enumerate(row, start=1):
            if cell.value is not None and cell.value in ["DOUTORADO", "MESTRADO", "MESTRADO PROFISSIONAL"]:
                tipo = cell.value
            # if cell.hyperlink and cell.hyperlink.target.startswith("https://repositorio"):
            if cell.hyperlink and "repositorio" in cell.hyperlink.target:
                # Store the hyperlink target along with its cell reference
                cell_reference = cell.coordinate
                hyperlinks_data["url"].append(cell.hyperlink.target)
                hyperlinks_data["tipo"].append(tipo)
    
    # with open("links" + ano + ".json", "w") as jsonFile:
    #     json.dump(hyperlinks_data, jsonFile, indent=4)
    hyperlinks_data = pd.DataFrame(hyperlinks_data)
    hyperlinks_data.to_csv("links" + ano + ".csv", index=False)