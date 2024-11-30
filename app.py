from flask import Flask, request, jsonify, render_template
import os
import random
import string
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Set the folder for uploaded images and allowed file extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Function to check if a file is a valid PNG
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Generate a random string for the URL
def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_uppercase, k=length))

@app.route('/')
def index():
    return 'Upload your PNG image by using /upload endpoint.'

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        random_string = generate_random_string()
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{random_string}.png")
        file.save(filepath)

        # Return the URL of the uploaded image as a JSON response
        image_url = f'http://{request.host}/u/{random_string}.png'

        return jsonify({'image_url': image_url}), 200

    return jsonify({'error': 'Invalid file type. Only PNGs are allowed.'}), 400


@app.route('/i/<random_string>')
def serve_image(random_string):
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{random_string}.png")
    if os.path.exists(image_path):
        # Serve the uploaded image in the HTML format
        uploaded_image_name = f"{random_string}.png"
        uploader_name = "dior"  # You can modify this based on your user data
        return render_template('image.html', 
                               image_name=uploaded_image_name, 
                               uploader=uploader_name,
                               random_string=random_string), 200
    else:
        return jsonify({'error': 'Image not found.'}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
