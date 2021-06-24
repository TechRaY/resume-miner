import os

#https://stackoverflow.com/questions/55499989/correctly-parse-pdf-paragraphs-with-python
#https://stackoverflow.com/questions/58606054/how-to-split-pdf-into-paragraphs-using-tika
def create_paragraphs(file_data_content):
    lines = file_data_content.splitlines(True)
    paragraph = []
    for line in lines:
        if line.isspace():
            if paragraph:
                yield ''.join(paragraph)
                paragraph = []
        else:
            paragraph.append(line)
    if paragraph:
        yield ''.join(paragraph)

    return paragraph

def createFileAndWriteParagraphData(paragraphs, fileName):
    output_file_path = os.path.join("training_data/", str(fileName) + '.txt')
    if os.path.exists(output_file_path):
        return
    with open(output_file_path, 'wt', encoding='utf8') as f:
        for paragraph in paragraphs:
            f.write(paragraph)
            f.write('\n')