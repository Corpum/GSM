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
    <head>
    <style>
    body {
        text-align:center;
        margin-top 50em;
        font-family: "Helvetica", "Arial", sans-serif;
        line-height: 1.5;
        padding: 4em 1em;
    }
    </style>
    </head>
    <body>
    <title>Upload new File</title>
    <h1> Goodwill Schedule Manager</h1>
    <form action="" method=post enctype=multipart/form-data>
        <p><input type=file id=files class=hidden name=file></p>
        <p><input type=submit value=Make a Schedule></p>
    </form>
    </body>
    '''


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    src.create_schedule()
    os.remove('/home/kyle/Dropbox/GSM/stafflist.db')
    return send_file('/home/kyle/Dropbox/GSM/updated_sched3.xlsx', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
