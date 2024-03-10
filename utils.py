import os
from werkzeug.utils import secure_filename

def save_image(file, directory='static/uploads'):
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = secure_filename(file.filename)
    filepath = os.path.join(directory, filename)
    file.save(filepath)
    return filename
