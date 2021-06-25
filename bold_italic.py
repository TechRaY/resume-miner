import os
from docx import *

path_input = 'Sample/PDF/'
path_output = 'Sample/Doc/'

## To extract bold and italic texts from all docx files

def getFontInfoForFiles():
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
                'italic':italics, 'fonts' : fonts,'font_info':{}}
        file_bold_italic[file] = boltalic

    print(file_bold_italic)
    info = dict()
    for file_name, info in file_bold_italic.items():
        for key, value in info["fonts"].items():
            if value not in info["font_info"].keys():
                info["font_info"][value] = [key]
            else:
                info["font_info"].get(value).append(key)
    print(info)

if __name__ == "__main__":
    getFontInfoForFiles()