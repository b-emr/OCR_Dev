import csv
import sys
from io import BytesIO
from PIL import Image
import pytesseract
import requests
import re

class CsvImages:

    def __init__(self, id, imageUrl, examCategoryId=0):
        self.id = id
        self.imageUrl = imageUrl
        self.examCategoryId = examCategoryId

    def setId(self, id):
        self.id = id

    def getId(self):
        return self.id

    def setImageUrl(self, imageUrl):
        self.imageUrl = imageUrl

    def getImageUrl(self):
        return self.imageUrl

    def setExamCategoryId(self, examCategoryId):
        self.examCategoryId = examCategoryId

    def getExamCategoryId(self):
        return self.examCategoryId

class WordsCoordinates:
    def __init__(self, word, first_x, first_y, second_x, second_y, width, height):
        self.word = word
        self.first_x = first_x
        self.first_y = first_y
        self.second_x = second_x
        self.second_y = second_y
        self.width = width
        self.height = height

class CoordinatedImage:
    def __init__(self, id, imageUrl, ax1, ax2, ay1, ay2, bx1, bx2, by1, by2, cx1, cx2, cy1, cy2, dx1, dx2, dy1, dy2, ex1, ex2, ey1, ey2):
        self.id = id
        self.imageUrl = imageUrl
        self.ax1 = ax1
        self.ax2 = ax2
        self.ay1 = ay1
        self.ay2 = ay2
        self.bx1 = bx1
        self.bx2 = bx2
        self.by1 = by1
        self.by2 = by2
        self.cx1 = cx1
        self.cx2 = cx2
        self.cy1 = cy1
        self.cy2 = cy2
        self.dx1 = dx1
        self.dx2 = dx2
        self.dy1 = dy1
        self.dy2 = dy2
        self.ex1 = ex1
        self.ex2 = ex2
        self.ey1 = ey1
        self.ey2 = ey2

def readCsv(filepath):
    allImages = []
    with open(filepath, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            allImages.append(CsvImages(row["Id"], row["ImageUrl"]))
    return allImages

def getCoordinates(allImages):
    count = 0
    coordinatedImages = []
    errorList = []
    for image in allImages:
        try:
            response = requests.get(image.imageUrl)
            img = Image.open(BytesIO(response.content))
            if img is not None:
                ocr_data = pytesseract.image_to_data(img, lang="tur", config="--psm 6", output_type=pytesseract.Output.DICT)

                aWords = []
                bWords = []
                cWords = []
                dWords = []
                eWords = []
                lastWord = ""
                for i in range(len(ocr_data['text'])):
                    if ocr_data['text'][i].strip() == "A)":
                        lastWord = "A)"
                    elif ocr_data['text'][i].strip() == "B)":
                        lastWord = "B)"
                    elif ocr_data['text'][i].strip() == "C)":
                        lastWord = "C)"
                    elif ocr_data['text'][i].strip() == "D)":
                        lastWord = "D)"
                    elif ocr_data['text'][i].strip() == "E)":
                        lastWord = "E)"

                    if lastWord == "A)" and ocr_data['text'][i].strip():
                        word = WordsCoordinates(
                            word=ocr_data['text'][i],
                            first_x=ocr_data['left'][i],
                            first_y=ocr_data['top'][i],
                            second_x=ocr_data['left'][i] + ocr_data['width'][i],
                            second_y=ocr_data['top'][i] + ocr_data['height'][i],
                            width=ocr_data['width'][i],
                            height=ocr_data['height'][i]
                        )
                        aWords.append(word)
                    elif lastWord == "B)" and ocr_data['text'][i].strip():
                        word = WordsCoordinates(
                            word=ocr_data['text'][i],
                            first_x=ocr_data['left'][i],
                            first_y=ocr_data['top'][i],
                            second_x=ocr_data['left'][i] + ocr_data['width'][i],
                            second_y=ocr_data['top'][i] + ocr_data['height'][i],
                            width=ocr_data['width'][i],
                            height=ocr_data['height'][i]
                        )
                        bWords.append(word)

                    elif lastWord == "C)" and ocr_data['text'][i].strip():
                        word = WordsCoordinates(
                            word=ocr_data['text'][i],
                            first_x=ocr_data['left'][i],
                            first_y=ocr_data['top'][i],
                            second_x=ocr_data['left'][i] + ocr_data['width'][i],
                            second_y=ocr_data['top'][i] + ocr_data['height'][i],
                            width=ocr_data['width'][i],
                            height=ocr_data['height'][i]
                        )
                        cWords.append(word)
                    elif lastWord == "D)" and ocr_data['text'][i].strip():
                        word = WordsCoordinates(
                            word=ocr_data['text'][i],
                            first_x=ocr_data['left'][i],
                            first_y=ocr_data['top'][i],
                            second_x=ocr_data['left'][i] + ocr_data['width'][i],
                            second_y=ocr_data['top'][i] + ocr_data['height'][i],
                            width=ocr_data['width'][i],
                            height=ocr_data['height'][i]
                        )
                        dWords.append(word)
                    elif lastWord == "E)" and ocr_data['text'][i].strip():
                        word = WordsCoordinates(
                            word=ocr_data['text'][i],
                            first_x=ocr_data['left'][i],
                            first_y=ocr_data['top'][i],
                            second_x=ocr_data['left'][i] + ocr_data['width'][i],
                            second_y=ocr_data['top'][i] + ocr_data['height'][i],
                            width=ocr_data['width'][i],
                            height=ocr_data['height'][i]
                        )
                        eWords.append(word)

                #writeInfo(aWords,bWords,cWords,dWords,eWords)

                aminX = sys.maxsize
                amaxX = -sys.maxsize - 1
                aminY = sys.maxsize
                amaxY = -sys.maxsize - 1
                bminX = sys.maxsize
                bmaxX = -sys.maxsize - 1
                bminY = sys.maxsize
                bmaxY = -sys.maxsize - 1
                cminX = sys.maxsize
                cmaxX = -sys.maxsize - 1
                cminY = sys.maxsize
                cmaxY = -sys.maxsize - 1
                dminX = sys.maxsize
                dmaxX = -sys.maxsize - 1
                dminY = sys.maxsize
                dmaxY = -sys.maxsize - 1
                eminX = sys.maxsize
                emaxX = -sys.maxsize - 1
                eminY = sys.maxsize
                emaxY = -sys.maxsize - 1

                for word in aWords:
                    if word.first_x < aminX:
                        aminX = word.first_x
                    if word.second_x < aminX:
                        aminX = word.second_x
                    if word.first_x > amaxX:
                        amaxX = word.first_x
                    if word.second_x > amaxX:
                        amaxX = word.second_x
                    if word.first_y < aminY:
                        aminY = word.first_y
                    if word.second_y < aminY:
                        aminY = word.second_y
                    if word.first_y > amaxY:
                        amaxY = word.first_y
                    if word.second_y > amaxY:
                        amaxY = word.second_y

                for word in bWords:
                    if word.first_x < bminX:
                        bminX = word.first_x
                    if word.second_x < bminX:
                        bminX = word.second_x
                    if word.first_x > bmaxX:
                        bmaxX = word.first_x
                    if word.second_x > bmaxX:
                        bmaxX = word.second_x
                    if word.first_y < bminY:
                        bminY = word.first_y
                    if word.second_y < bminY:
                        bminY = word.second_y
                    if word.first_y > bmaxY:
                        bmaxY = word.first_y
                    if word.second_y > bmaxY:
                        bmaxY = word.second_y

                for word in cWords:
                    if word.first_x < cminX:
                        cminX = word.first_x
                    if word.second_x < cminX:
                        cminX = word.second_x
                    if word.first_x > cmaxX:
                        cmaxX = word.first_x
                    if word.second_x > cmaxX:
                        cmaxX = word.second_x
                    if word.first_y < cminY:
                        cminY = word.first_y
                    if word.second_y < cminY:
                        cminY = word.second_y
                    if word.first_y > cmaxY:
                        cmaxY = word.first_y
                    if word.second_y > cmaxY:
                        cmaxY = word.second_y

                for word in dWords:
                    if word.first_x < dminX:
                        dminX = word.first_x
                    if word.second_x < dminX:
                        dminX = word.second_x
                    if word.first_x > dmaxX:
                        dmaxX = word.first_x
                    if word.second_x > dmaxX:
                        dmaxX = word.second_x
                    if word.first_y < dminY:
                        dminY = word.first_y
                    if word.second_y < dminY:
                        dminY = word.second_y
                    if word.first_y > dmaxY:
                        dmaxY = word.first_y
                    if word.second_y > dmaxY:
                        dmaxY = word.second_y

                for word in eWords:
                    if word.first_x < eminX:
                        eminX = word.first_x
                    if word.second_x < eminX:
                        eminX = word.second_x
                    if word.first_x > emaxX:
                        emaxX = word.first_x
                    if word.second_x > emaxX:
                        emaxX = word.second_x
                    if word.first_y < eminY:
                        eminY = word.first_y
                    if word.second_y < eminY:
                        eminY = word.second_y
                    if word.first_y > emaxY:
                        emaxY = word.first_y
                    if word.second_y > emaxY:
                        emaxY = word.second_y

                if eminX == sys.maxsize:
                    eminX = -1
                if emaxX == -sys.maxsize - 1:
                    emaxX = -1
                if eminY == sys.maxsize:
                    eminY = -1
                if emaxY == -sys.maxsize - 1:
                    emaxY = -1

                newImage = CoordinatedImage(image.id, image.imageUrl, aminX, amaxX, aminY, amaxY, bminX, bmaxX, bminY, bmaxY, cminX, cmaxX, cminY, cmaxY, dminX, dmaxX, dminY, dmaxY, eminX, emaxX, eminY, emaxY)
                coordinatedImages.append(newImage)

        except Exception as e:
            print("Error: ", e, "Error in ID: ", image.id)
            errorList.append(image)

    return coordinatedImages, errorList

def writeCoordinates(allImages):
    for image in allImages:
        print(f"ID: {image.id}, A: ({image.ax1}, {image.ax2}, {image.ay1}, {image.ay2}), B: ({image.bx1}, {image.bx2}, {image.by1}, {image.by2}), C: ({image.cx1}, {image.cx2}, {image.cy1}, {image.cy2}), D: ({image.dx1}, {image.dx2}, {image.dy1}, {image.dy2}), E: ({image.ex1}, {image.ex2}, {image.ey1}, {image.ey2}),")

def writeCsv(allImages):
    datas = []
    for image in allImages:
        datas.append({"Id": image.id, "ImageUrl": image.imageUrl, "A_X1_Coordinate": image.ax1, "A_X2_Coordinate": image.ax2, "A_Y1_Coordinate": image.ay1, "A_Y2_Coordinate": image.ay2, "B_X1_Coordinate": image.bx1, "B_X2_Coordinate": image.bx2, "B_Y1_Coordinate": image.by1, "B_Y2_Coordinate": image.by2, "C_X1_Coordinate": image.cx1, "C_X2_Coordinate": image.cx2, "C_Y1_Coordinate": image.cy1, "C_Y2_Coordinate": image.cy2, "D_X1_Coordinate": image.dx1, "D_X2_Coordinate": image.dx2, "D_Y1_Coordinate": image.dy1, "D_Y2_Coordinate": image.dy2, "E_X1_Coordinate": image.ex1, "E_X2_Coordinate": image.ex2, "E_Y1_Coordinate": image.ey1, "E_Y2_Coordinate": image.ey2})
    with open("created_with_python.csv", mode="a", newline='') as file:
        fieldnames = ['Id', 'ImageUrl', 'A_X1_Coordinate', 'A_X2_Coordinate', 'A_Y1_Coordinate', 'A_Y2_Coordinate', 'B_X1_Coordinate', 'B_X2_Coordinate', 'B_Y1_Coordinate', 'B_Y2_Coordinate', 'C_X1_Coordinate', 'C_X2_Coordinate', 'C_Y1_Coordinate', 'C_Y2_Coordinate', 'D_X1_Coordinate', 'D_X2_Coordinate', 'D_Y1_Coordinate', 'D_Y2_Coordinate', 'E_X1_Coordinate', 'E_X2_Coordinate', 'E_Y1_Coordinate', 'E_Y2_Coordinate']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(datas)

def writeErrors(errorList):
    datas = []
    for image in errorList:
        datas.append({"Id": image.id, "ImageUrl": image.imageUrl})
    with open("created_with_python_errors.csv", mode="a", newline='') as file:
        fieldnames = ['Id', 'ImageUrl']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(datas)

def func_1(images):
    for image in images:
        response = requests.get(image.imageUrl)
        img = Image.open(BytesIO(response.content))
        img = img.convert("L")
        ocr_data = pytesseract.image_to_data(img, lang="tur", config="--psm 6 --oem 3", output_type=pytesseract.Output.DICT)

        aWords = []
        bWords = []
        cWords = []
        dWords = []
        eWords = []
        lastWord = ""
        for i in range(len(ocr_data['text'])):
            if ocr_data['text'][i].strip() == "A)":
                lastWord = "A)"
            elif ocr_data['text'][i].strip() == "B)":
                lastWord = "B)"
            elif ocr_data['text'][i].strip() == "C)":
                lastWord = "C)"
            elif ocr_data['text'][i].strip() == "D)":
                lastWord = "D)"
            elif ocr_data['text'][i].strip() == "E)":
                lastWord = "E)"

            if lastWord == "A)" and ocr_data['text'][i].strip():
                word = WordsCoordinates(
                    word=ocr_data['text'][i],
                    first_x=ocr_data['left'][i],
                    first_y=ocr_data['top'][i],
                    second_x=ocr_data['left'][i] + ocr_data['width'][i],
                    second_y=ocr_data['top'][i] + ocr_data['height'][i],
                    width=ocr_data['width'][i],
                    height=ocr_data['height'][i]
                )
                aWords.append(word)
            elif lastWord == "B)" and ocr_data['text'][i].strip():
                word = WordsCoordinates(
                    word=ocr_data['text'][i],
                    first_x=ocr_data['left'][i],
                    first_y=ocr_data['top'][i],
                    second_x=ocr_data['left'][i] + ocr_data['width'][i],
                    second_y=ocr_data['top'][i] + ocr_data['height'][i],
                    width=ocr_data['width'][i],
                    height=ocr_data['height'][i]
                )
                bWords.append(word)

            elif lastWord == "C)" and ocr_data['text'][i].strip():
                word = WordsCoordinates(
                    word=ocr_data['text'][i],
                    first_x=ocr_data['left'][i],
                    first_y=ocr_data['top'][i],
                    second_x=ocr_data['left'][i] + ocr_data['width'][i],
                    second_y=ocr_data['top'][i] + ocr_data['height'][i],
                    width=ocr_data['width'][i],
                    height=ocr_data['height'][i]
                )
                cWords.append(word)
            elif lastWord == "D)" and ocr_data['text'][i].strip():
                word = WordsCoordinates(
                    word=ocr_data['text'][i],
                    first_x=ocr_data['left'][i],
                    first_y=ocr_data['top'][i],
                    second_x=ocr_data['left'][i] + ocr_data['width'][i],
                    second_y=ocr_data['top'][i] + ocr_data['height'][i],
                    width=ocr_data['width'][i],
                    height=ocr_data['height'][i]
                )
                dWords.append(word)
            elif lastWord == "E)" and ocr_data['text'][i].strip():
                word = WordsCoordinates(
                    word=ocr_data['text'][i],
                    first_x=ocr_data['left'][i],
                    first_y=ocr_data['top'][i],
                    second_x=ocr_data['left'][i] + ocr_data['width'][i],
                    second_y=ocr_data['top'][i] + ocr_data['height'][i],
                    width=ocr_data['width'][i],
                    height=ocr_data['height'][i]
                )
                eWords.append(word)

        print(image.imageUrl)
        print("A Words:")
        for item in aWords:
            print(item.word," ",end="")
        print()
        print("B Words:")
        for item in bWords:
            print(item.word, " ", end="")
        print()
        print("C Words:")
        for item in cWords:
            print(item.word, " ", end="")
        print()
        print("D Words:")
        for item in dWords:
            print(item.word, " ", end="")
        print()
        print("E Words:")
        for item in eWords:
            print(item.word, " ", end="")
        print()




if __name__ == "__main__":
    allImages = readCsv("datas/bscCoordinates.csv")
    func_1(allImages)
    #newImages, errorList = getCoordinates(allImages)
    #writeCoordinates(newImages)
    #writeCsv(newImages)
    #writeErrors(errorList)
