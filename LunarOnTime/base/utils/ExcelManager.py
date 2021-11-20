import pandas as pd


def readFileExcel(pathFile, sheetName):
    # Cach truy cap vao cac truong
    # https://pythoninoffice.com/get-values-rows-and-columns-in-pandas-dataframe/
    # listContent = ExcelManager.readFileExcel(r'C:\Users\84167\Downloads\Remitano_Metaminer (1).xlsx', 'Ref List')
    # listSTT = listContent.columns
    # print(listSTT[0])
    # print(listSTT)
    # print(listContent['Ref Link/ID'])
    df = pd.read_excel(pathFile, sheet_name=sheetName)
    return df
