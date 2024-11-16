# Face Recognition System
[![Created by DineshSuthar.com](https://img.shields.io/badge/Created%20by-DineshSuthar.com-blue)](https://dineshsuthar.com)

A robust Face Recognition System built with Flask and Python that enables real-time face detection, recognition, and user management. The system provides a web interface for uploading images, recognizing faces, and managing user data through a SQLite database.
## Screenshots

Here are some screenshots of the project:

![Screenshot of the app](./screenshots/FaceRecognitionSystem.png)



## Table of Contents
- [Features](#features)
- [System Architecture](#system-architecture)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Database Schema](#database-schema)
- [Project Structure](#project-structure)
- [Future Enhancements](#future-enhancements)
- [License](#license)

## Features
- 🎯 Face Detection & Recognition in uploaded images
- 👤 User Registration with name and face data
- 🔄 Dynamic name updates for existing users
- 💾 Efficient file management system for images and embeddings
- 🗄️ SQLite database integration for data persistence
- 🔍 Advanced face embedding comparison using cosine distance
- 🖼️ Support for various image formats
- 🚀 Fast and accurate face recognition using state-of-the-art libraries

## System Architecture
### Frontend
- HTML/CSS/JS interface for image upload and feedback
- Responsive design for multiple devices
- Real-time status updates

### Backend
- Flask REST API
- Face Recognition & Processing engine
- File system management
- Database operations

### Storage
- SQLite database for user data
- File system for images and embeddings

## Technologies Used
- **Flask**: Web framework for API development
- **OpenCV**: Image processing and manipulation
- **dlib**: Face detection and landmark recognition
- **face_recognition**: Face embedding extraction and comparison
- **NumPy**: Numerical computations and array operations
- **SQLite**: Database management
- **SciPy**: Scientific computing and distance calculations
- **Flask-CORS**: Cross-Origin Resource Sharing support

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/face-recognition-system.git
cd face-recognition-system
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python init_db.py
```

5. Start the application:
```bash
python app.py
```

## Usage
1. Access the web interface at `http://localhost:5000`
2. Upload an image containing a face
3. The system will either:
   - Recognize the face and display the name
   - Prompt for a name if the face is unknown
4. For new faces, enter a name to register them
5. For existing faces, you can update their name if needed

## API Endpoints

### POST /recognize
Recognizes faces in uploaded images.

**Parameters:**
- `image`: Image file (required)
- `name`: User name (optional)

**Example Request:**
```bash
curl -X POST -F "image=@photo.jpg" -F "name=John Doe" http://localhost:5000/recognize
```

**Example Response:**
```json
{
    "name": "John Doe",
    "confidence": 0.92
}
```

## Database Schema

### Faces Table
| Column    | Type | Description           |
|-----------|------|-----------------------|
| name      | TEXT | User's name          |
| embedding | BLOB | Face embedding data   |

## Project Structure
```
face-recognition-system/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── static/               # Static files (CSS, JS)
├── templates/            # HTML templates
├── embeddings/           # User embeddings (.npy files)
├── uploads/              # Uploaded images
├── database/             # SQLite database
└── models/               # Face recognition models
```

## Future Enhancements
- Real-time webcam recognition
- Multiple face detection support
- Advanced database management
- User authentication system
- Face recognition accuracy improvements
- Mobile application support
- Batch processing capabilities

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
Created with ❤️ by [DineshSuthar.com](https://dineshsuthar.com)

© 2024 DineshSuthar.com. All Rights Reserved.