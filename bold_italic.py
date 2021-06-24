import os
from docx import *

path_input = 'pdf/'
path_output = 'doc/'

## To extract bold and italic texts from docx
file_bold_italic = {}
for file in os.listdir(path_output):
    print(file)
    document = Document(path_output+file)
    bolds=[]
    italics=[]
    boltalic={}
    fonts = {}
    for para in document.paragraphs:
        #print(para)
        for run in para.runs:
            if run.font.size != None :
                fonts[run.text] = run.font.size.pt
            if run.font.italic :
                italics.append(run.text)
            if run.font.bold :
                bolds.append(run.text)

    boltalic={'bold':bolds,
              'italic':italics, 'fonts' : fonts}
    file_bold_italic[file] = boltalic

print(file_bold_italic)