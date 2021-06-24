import os
from docx import *

path_input = 'Resumes/pdf/'
path_output = 'Resumes/doc/'

## To extract bold and italic texts from docx
file_bold_italic = {}

def getBoldItalic():
    for file in os.listdir(path_output):
        print(file)
        document = Document(path_output+file)
        bolds=[]
        italics=[]
        boltalic={}
        for para in document.paragraphs:
            print(para.text)
            for run in para.runs:
                if run.italic :
                    italics.append(run.text)
                if run.bold :
                    bolds.append(run.text)

        boltalic={'bold':bolds,
                  'italic':italics}
        file_bold_italic[file] = boltalic

    print(file_bold_italic)


if __name__ == "__main__":
    getBoldItalic()