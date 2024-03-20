from flask import Flask, redirect, request, render_template
from contact import Contact


app = Flask(__name__)


@app.route('/')
def index():
    return redirect('/contacts')


@app.route('/contacts')
def contacts():
    search = request.args.get('q')
    if search:
        contacts_set = Contact.search(search)
    else:
        contacts_set = Contact.all()
    return render_template('index.html', contacts=contacts_set)


if __name__ == '__main__':
    app.run(port=8000)
