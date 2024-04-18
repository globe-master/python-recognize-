import cv2
import pytesseract
import os

def fill_non_white_with_black(image):
    # Convert image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Threshold the grayscale image to get a binary image where non-white pixels are white
    _, thresholded = cv2.threshold(gray_image, 240, 255, cv2.THRESH_BINARY_INV)

    # Invert the binary image so non-white pixels become black
    inverted_thresholded = cv2.bitwise_not(thresholded)
    
    # Use the inverted binary image as a mask to fill non-white areas with black
    result = cv2.bitwise_and(image, image, mask=inverted_thresholded)

    #cv2.imwrite('gray_image.jpg', result)

    return result

# Function to extract 4 letters from a PNG image
def recognize_letters(image):
    
    # Use pytesseract to extract text
    extracted_text = pytesseract.image_to_string(image, lang='eng', config='-l eng --oem 3 --psm 10')
    #print(f'Extracted letters: {extracted_text[:1]}')

    # Process extracted text to get 4 letters
    extracted_letters = extracted_text[:1]

    return extracted_letters
