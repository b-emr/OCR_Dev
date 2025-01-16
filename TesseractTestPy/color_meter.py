import csv
from PIL import Image
import requests
from io import BytesIO
import numpy as np
import time

class CsvImages:

    def __init__(self, id, imageUrl):
        self.id = id
        self.imageUrl = imageUrl

    def setId(self, id):
        self.id = id

    def getId(self):
        return self.id

    def setImageUrl(self, imageUrl):
        self.imageUrl = imageUrl

    def getImageUrl(self):
        return self.imageUrl

def readCsvForColors(filepath):
    allImages = []
    start_time = time.time()
    with open(filepath, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            image = download_image(row["ImageUrl"])
            allImages.append({'Id':row["Id"], 'HundredTimeResized':calculate_distinct_avg(scale_image_by_factor(image,0.1))})
    total_time = time.time() - start_time
    print(f"Total Time readCsvForColors: {total_time:.2f} seconds")
    return allImages

def scale_image_by_factor(img, scale_factor):
    start_time = time.time()
    original_width, original_height = img.size

    new_width = int(original_width * scale_factor)
    new_height = int(original_height * scale_factor)
    total_time = time.time() - start_time
    print(f"Total Time scale Image: {total_time:.2f} seconds")
    return img.resize((new_width, new_height))

def scale_image(img):
    """
    Scales an image to a width of 100 pixels while maintaining the aspect ratio.

    Args:
        image_path (str): Path to the input image.
        output_path (str): Path to save the scaled image.
    """
    try:

            # Calculate new dimensions
        original_width, original_height = img.size
        new_width = 100
        scale_factor = new_width / original_width
        new_height = int(original_height * scale_factor)
        print("Scale factor:",(1/scale_factor))

            # Resize the image
        scaled_img = img.resize((new_width, new_height))
        return scaled_img
            # Save the scaled image


    except Exception as e:
        print(f"An error occurred: {e}")

def writeCsvForColors(allItems, filename):
    with open(filename, mode="a", newline='') as file:
        fieldnames = ['Id', 'HundredTimeResized']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(allItems)

def download_image(url):
    """Download an image from a URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise exception for HTTP errors
        return Image.open(BytesIO(response.content)).convert('RGB')
    except Exception as e:
        print(f"Failed to download image from {url}: {e}")
        return None

def calculate_distinct_avg(image):
    """Calculate the distinctAvg for an image."""
    start_time = time.time()
    width, height = image.size
    total_pixels = width * height
    image = image.convert("RGB")

    # Convert the image data to a NumPy array
    pixels = np.array(image)

    # Reshape the 3D array to a 2D array where each row is a color
    pixels = pixels.reshape(-1, 3)

    # Find distinct colors
    unique_colors = np.unique(pixels, axis=0)

    print(f"Number of distinct colors: {len(unique_colors)}")


    distinctAvg = round(len(unique_colors) / total_pixels * 100, 2)
    print("Calculated: ", distinctAvg)

    total_time = time.time() - start_time
    print(f"Total Time calculate_Distinct_Average: {total_time:.5f} seconds")
    return distinctAvg

def add_old_value(allImages,filepath):
    start_time = time.time()
    with open(filepath, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            for element in allImages:
                if element["Id"] == row["BookSectionCropId"]:
                    element["OldValue"] = row["AVGDistinct"]
    total_time = time.time() - start_time
    print(f"Total Time add_old_value: {total_time:.2f} seconds")
    return allImages

def analyze(filepath):
    allItemList = []
    maxItem = {}
    minItem = {}
    max = -1
    min = 10000
    sum = 0
    with open(filepath, mode="r") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            result = ((float(row["HundredTimeResized"]) / 100.0) / (float(row["OldValue"]) + 1.0)) * 100.0
            if(result > max):
                max = result
                maxItem = row
            if(result < min):
                min = result
                minItem = row
            sum += result
            allItemList.append({"Id":row["Id"], "OldValue": row["OldValue"], "HundredTimeResized": row["HundredTimeResized"], "ErrorPercantage": result})

    with open("analyzed_data.csv", mode="a", newline='') as file:
        fieldnames = ['Id', 'OldValue', 'HundredTimeResized', 'ErrorPercantage']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(allItemList)

    print(maxItem)
    print(minItem)
    print("Average: ", sum/100.0)


if __name__ == "__main__":
    allItems = readCsvForColors("datas/bscCoordinates.csv")
    writeCsvForColors(allItems, "test_colormeter.csv")