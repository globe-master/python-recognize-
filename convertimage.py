import cv2
import pytesseract
import os

def recognize_letters(image):
    
    # Use pytesseract to extract text
    extracted_text = pytesseract.image_to_string(image, lang='eng', config='-l eng --oem 3 --psm 10')
    #print(f'Extracted letters: {extracted_text[:1]}')

    # Process extracted text to get 4 letters
    extracted_letters = extracted_text[:1]

    return extracted_letters
