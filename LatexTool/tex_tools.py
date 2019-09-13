from LatexTool.ast import tabel

if __name__ == '__main__':
    # tab = tabel.Tabel("../test.xlsx",center=False,fill=False)
    tab = tabel.Tabel("../test.xlsx")
    print(tab.to_tex())

