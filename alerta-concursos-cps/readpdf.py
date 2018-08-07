import textract
file = 'concursos/edital.pdf'
text = textract.process(file, method='pdfminer')

print(text)