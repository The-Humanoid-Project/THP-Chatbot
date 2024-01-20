import easyocr
import re

class OCR():

    def __init__(self) -> None:
        self.reader = easyocr.Reader(['en'])
        self.r = re.compile("^[0-9]{5,6}$")

    def getAccessionNo(self, path):  
        text = self.reader.readtext(path)
        text = [x[-2] for x in text]
        accession_no = list(filter(self.r.match, text))
        return (len(accession_no) > 0, accession_no)
    
if __name__ == "__main__":
    ocr = OCR()
    print(ocr.getAccessionNo('crops/Label/1.jpg'))