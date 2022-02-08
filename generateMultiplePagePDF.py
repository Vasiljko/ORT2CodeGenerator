import PyPDF2
pdfFileObj = open('FormularSimulator.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
pdfWriter = PyPDF2.PdfFileWriter()

for pageNum in range(20):
    pageObj = pdfReader.getPage(0)
    pdfWriter.addPage(pageObj)

pdfOutput = open('proba.pdf', 'wb')
pdfWriter.write(pdfOutput)
pdfOutput.close()