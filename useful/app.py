# import os
# from flask import Flask, render_template, request
# from werkzeug.utils import secure_filename

# app = Flask(__name__)

# @app.route('/upload', methods=['GET', 'POST'])
# def upload():
#     if request.method == 'POST':
#         file = request.files['file']
#         if file:
#             filename = secure_filename(file.filename)
#             # Create the 'uploads' directory if it doesn't exist
#             if not os.path.exists('uploads'):
#                 os.makedirs('uploads')
#             file.save(os.path.join('uploads', filename))
#             return 'File uploaded successfully'
#     return render_template('base/upload.html')

# if __name__ == '__main__':
#     app.run(debug=True)

# def process_file(filename):
#     # Open the workbook
#     workbook = openpyxl.load_workbook(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
#     # Assuming the data is in the first sheet, get the active sheet
#     sheet = workbook.active
    
#     # Extract the data from the sheet
#     data = []
#     for row in sheet.iter_rows(values_only=True):
#         data.append(row)
    
#     # Pass the data to the frontend or perform any further processing
#     # ...

# if __name__ == '__main__':
#     app.config['UPLOAD_FOLDER'] = 'uploads'  # Set the upload folder path
#     app.run(debug=True)  # Run the application in debug mode


