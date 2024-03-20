from flask import Flask, redirect, request, render_template, flash
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


@app.route('/contacts/new', methods=['GET'])
def new_contact_form():
    return render_template('new.html', contact=Contact())


@app.route('/contacts/new', methods=['POST'])
def new_contact():
    c = Contact(
        first=request.form['first_name'],
        last=request.form['last_name'],
        email=request.form['email'],
        phone=request.form['phone']
    )
    if c.save():
        # flash('Created New Contact!')
        return redirect('/contacts')
    return render_template('new.html', contact=c)


@app.route('/contacts/<contact_id>', methods=['GET'])
def get_contact(contact_id=0):
    c = Contact.find(int(contact_id))
    return render_template('show.html', contact=c)


if __name__ == '__main__':
    Contact.load_db()
    app.run(port=8000)
