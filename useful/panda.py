# import pandas as pd
# import requests

# # Read the data from the Excel file
# data = pd.read_excel('uploads\cate.xlsx')  # Replace 'path/to/your/file.xlsx' with the actual path to your Excel file

# # Access the 'category_name' and 'category_image' columns
# category_names = data['category_name']
# category_images = data['category_image']

# # Iterate over the category data and save the images locally
# for name, image_url in zip(category_names, category_images):
#     print(f"Category: {name}")
#     print(f"Image URL: {image_url}")
    
#     # Extract the image filename from the URL
#     filename = image_url.split('/')[-1]
    
#     try:
#         # Send a GET request to retrieve the image data
#         response = requests.get(image_url)
        
#         # Save the image locally
#         with open(f"images/{filename}", 'wb') as file:
#             file.write(response.content)
        
#         print("Image saved successfully.")
#     except Exception as e:
#         print(f"Error saving image: {str(e)}")
    
#     print()  # Add an empty line for better readability
