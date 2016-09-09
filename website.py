import os
from flask import Flask, request, redirect, url_for, send_file
from werkzeug import secure_filename
import src

UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = set(['xlsx'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def date_form():
    return ''''
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
        <h1>Goodwill Schedule Manager</h1>
        <form action ="" method=POST>
            <p><input type=text name=date></p>
            <p><input type=submit name=dateform value=Send></p>
        </form>
    </body>
    </html>
    '''


@app.route('/', methods=['POST'])
def date_form_post():
    text = request.form['date']
    return redirect(url_for('upload_file', date=text))


@app.route('/uploads/<date>', methods=['GET', 'POST'])
def upload_file(date):
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename, date=date))
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


@app.route('/uploads/<date>/<filename>')
def uploaded_file(filename, date):
    date = date.replace('-', '/')
    src.create_schedule(date)
    os.remove(src.folder + '/stafflist.db')
    return send_file(src.folder + '/updated_sched3.xlsx', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
