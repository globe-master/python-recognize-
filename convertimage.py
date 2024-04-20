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

def extract_characters(image, color_image, width, height):
    # Load the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply thresholding
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize an empty list to store tuples of characters and their x positions
    characters_with_positions = []

    # Extract and save each character region
    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)

        x = x - 10
        if x < 0 :
            x = 0

        w = w + 20
        if x + w > width:
            w = width - x

        y = y - 10
        if y < 0:
            y = 0

        h = h + 20
        if y + h > height:
            h = height - y

        char_image = image[y:y+h, x:x+w]
        #cv2.imwrite(f'character_{i}.png', char_image)
        #char_image = cv2.imread(f'character_{i}.png')
        character = recognize_letters(char_image)

        # Append a tuple of character and its x position to the list
        characters_with_positions.append((character, x))

    # Sort the characters based on their x positions
    sorted_characters = sorted(characters_with_positions, key=lambda item: item[1])

    # Extract characters from the sorted list
    sorted_characters_only = [char for char, _ in sorted_characters]

    # Merge the characters into a single string
    merged_string = ''.join(sorted_characters_only)

    # Print or use the merged string as needed
    # print(merged_string)
    return merged_string

# Multi images import
def import_multi_images(folder_path):
    image_files = os.listdir(folder_path)
    count = 0
    for filename in image_files:
        if filename.endswith((".jpg", ".jpeg", ".png", ".bmp")):
            # Construct the full path to the image file
            image_path = os.path.join(folder_path, filename)
            image = cv2.imread(image_path)

            # Get image width and height
            height, width, _ = image.shape
            
            # Fill non-white areas with black
            gray_image = fill_non_white_with_black(image)
            
            extracted_text = extract_characters(gray_image, image, width, height)
            if filename[:4] != extracted_text.upper():
                count += 1
                print(filename[:4] + ":" + extracted_text)
    print("count:" + count)

def import_single_image(file_path):
    image = cv2.imread(file_path)

    # Get image width and height
    height, width, _ = image.shape
    
    # Fill non-white areas with black
    gray_image = fill_non_white_with_black(image)
    
    extracted_text = extract_characters(gray_image, image, width, height)
    print(extracted_text)

folder_path = "./imagies"
file_path = "./imagies/CBYH.png"
# import_multi_images(folder_path)
import_single_image(file_path)