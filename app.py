from flask import Flask, request, jsonify
import numpy as np
import cv2
from scipy.spatial.distance import cosine
import os
import sqlite3
from face_recognition import get_face_embeddings, save_embeddings
from flask_cors import CORS
from flask import Flask, render_template

# Initialize Flask app
app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Set up a directory to store uploaded files temporarily
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load known face embeddings (from the 'embeddings' directory)
known_face_encodings = {}
known_face_names = []

# Ensure the embeddings directory exists
if not os.path.exists('embeddings'):
    os.makedirs('embeddings')

# SQLite setup
DATABASE = 'faces.db'

# Create a database table if it doesn't exist
def create_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS faces
                 (name TEXT, embedding BLOB)''')
    conn.commit()
    conn.close()

create_db()

# Load saved embeddings from the 'embeddings' folder
for file in os.listdir('embeddings'):
    if file.endswith('.npy'):  # Ensure we're only loading .npy files
        name = file.split('.')[0]
        embedding = np.load(f'embeddings/{file}')
        known_face_encodings[name] = embedding
        known_face_names.append(name)

# Compare face embedding with known ones
def match_face(embedding, threshold=0.6):
    min_dist = float('inf')
    name = "Unknown"
    
    # Compare with each known face
    for known_name, known_embedding in known_face_encodings.items():
        dist = cosine(embedding, known_embedding)
        
        if dist < min_dist:
            min_dist = dist
            name = known_name
            
    # Return name if distance is below threshold, otherwise "Unknown"
    return name if min_dist < threshold else "Unknown"

# Route for face recognition and saving embeddings
# Route for face recognition and saving embeddings
@app.route('/recognize', methods=['POST'])
def recognize():
    try:
        # Check if the request contains the 'image' field
        if 'image' not in request.files:
            return jsonify({"error": "No image file part"}), 400

        # Get the uploaded image file
        file = request.files['image']

        # Check if the filename is empty
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        
        # Get the name of the user from the form data
        name = request.form.get('name', None)

        # Save the file to a temporary location
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Check if the file was saved correctly
        if not os.path.exists(file_path):
            return jsonify({"error": "Failed to save the file"}), 500

        # Ensure the file is a valid image
        if not file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')): 
            return jsonify({"error": "Invalid image file format"}), 400
        
        # Read and process the image
        img = cv2.imread(file_path)

        if img is None:
            return jsonify({"error": "Failed to read the image file"}), 500

        # Get face embeddings from the image
        embeddings = get_face_embeddings(file_path)

        # If embeddings are found, match the face with known faces
        if len(embeddings) > 0:
            name_found = match_face(embeddings[0])  # Assuming only one face is present

            # If face is recognized and the user has provided a new name
            if name_found != "Unknown" and name:
                # If a new name is provided by the user, we update the name everywhere
                if name_found != name:
                    # Delete the old embedding from the database and embeddings
                    conn = sqlite3.connect(DATABASE)
                    c = conn.cursor()
                    c.execute("DELETE FROM faces WHERE name = ?", (name_found,))
                    conn.commit()
                    conn.close()
                    
                    # Remove the old name from known embeddings
                    del known_face_encodings[name_found]
                    known_face_names.remove(name_found)
                    
                    # Rename the old embedding file
                    old_file_path = os.path.join('embeddings', f'{name_found}.npy')
                    if os.path.exists(old_file_path):
                        new_file_path = os.path.join('embeddings', f'{name}.npy')
                        os.rename(old_file_path, new_file_path)
                    
                    # Save the new embedding with the new name
                    save_embeddings(embeddings[0], name)  # Save the embedding with the new name
                    known_face_encodings[name] = embeddings[0]
                    known_face_names.append(name)

                    # Save the new name and embedding to SQLite database
                    conn = sqlite3.connect(DATABASE)
                    c = conn.cursor()
                    c.execute("INSERT INTO faces (name, embedding) VALUES (?, ?)",
                              (name, embeddings[0].tobytes()))
                    conn.commit()
                    conn.close()
                    
                    return jsonify({'name': name})

            # If no new name is provided, return the recognized name
            return jsonify({'name': name_found})

        # If no faces are detected in the image
        else:
            return jsonify({'error': 'No face detected'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Route for home (index)
@app.route('/')
def home():
    return render_template('index.html')

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
