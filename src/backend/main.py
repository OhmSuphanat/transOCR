from config import app,db,ALLOWED_EXTENSIONS
from flask import request, jsonify, render_template
from model import User
from werkzeug.utils import secure_filename
import os

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

@app.route("/")
def homepage():
    return render_template("hompage.html")

@app.route('/upload_image/<int:user_id>', methods=['POST'])
def upload_image(user_id):
    user = User.query.get(user_id)
    if user is None:
        return 'User not found', 404

    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        user.image = filename
        db.session.commit()
        return 'File successfully uploaded', 200

    return 'File type not allowed', 400
