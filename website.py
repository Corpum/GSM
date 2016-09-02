import os
from flask import Flask, request, redirect, url_for, send_from_directory, render_template, send_file
from werkzeug import secure_filename
import src
from time import sleep

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['xlsx'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Goodwill Schedule Manager</h1>
    <h2>Upload File</h2>
    <form action="" method=post enctype=multipart/form-data>
        <p><input type=file name=file>
            <input type=submit value=Upload>
    </form>
    '''


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    src.create_schedule()
    return send_file('/home/kyle/Dropbox/GSM/updated_sched3.xlsx', as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
