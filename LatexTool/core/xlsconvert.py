import win32com.client
import os

def xls2pdf(name,pdfname):
    name = os.path.abspath(name)
    pdfname = os.path.abspath(pdfname)

    o = win32com.client.Dispatch("Excel.Application")
    # o = xls.Documents.Open(name, ReadOnly = 1)
    o.Visible = False
    wb = o.Workbooks.Open(name)
    # o.Run("tc")
    wb.ActiveSheet.ExportAsFixedFormat(0, pdfname)
    wb.Close(SaveChanges=0)
    # o.SaveAs(pdfname, FileFormat = 17)
    # o.Close()


if __name__ == "__main__":
    xls2pdf("temp.xlsx","tes.pdf")