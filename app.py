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

        # Return a URL to the uploaded image
        return jsonify({'url': f"http://diorscooked.lol/i/{random_string}"}), 200

    return jsonify({'error': 'Invalid file type. Only PNGs are allowed.'}), 400

@app.route('/i/<random_string>')
def serve_image(random_string):
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{random_string}.png")
    if os.path.exists(image_path):
        # Serve the image
        return render_template('image.html', image_url=f"http://diorscooked.lol/u/{random_string}.png")
    else:
        return jsonify({'error': 'Image not found.'}), 404

# Start the Flask app (you can also use Gunicorn to serve it in production)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)  # Listen on port 80
