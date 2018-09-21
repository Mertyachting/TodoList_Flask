from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)

#Implemtierung der Datenbanl
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/todo.db'

db = SQLAlchemy(app)

#Modelieren einer Tabelle in der Datenbank
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    complete = db.Column(db.Boolean)

#Startseite soll Alle Todos in den zuständen Complete und incomplete anzeigen
@app.route('/')
def index():
    incomplete = Todo.query.filter_by(complete=False).all()
    complete = Todo.query.filter_by(complete=True).all()

    return render_template('index.html', incomplete=incomplete, complete=complete)

# Die Seite add hat die Funktion ein Todo in die datenbank einzufügen, dann leitet es an die Startseite weiter
@app.route('/add', methods=['POST'])
def add():
    todo = Todo(text=request.form['todoitem'], complete=False)
    db.session.add(todo)
    db.session.commit()

    return redirect(url_for('index'))

# Search zeigt auf einer anderen Seite alle Items an, wenn man ohne input auf search klickt oder man kann nach speziellen Todos suchen
@app.route('/search', methods=['POST'])
def search():

    search = request.form.get('search')
    todo_list = db.session.query(Todo).filter(Todo.text.like("%" + search + "%")).all()
    return render_template('search.html', todo_list=todo_list )

# Complete Id wird dank dynamic routing wird die ID der todo genommen und in complete gelegt
@app.route('/complete/<id>')
def complete(id):

    todo = Todo.query.filter_by(id=int(id)).first()
    todo.complete = True
    db.session.commit()

    return redirect(url_for('index'))

# delete ebenfalls dynamic die ID wird genommen und das entsprechende element aus der datenbank gelöscht
@app.route('/delete/<id>')
def delete(id):

    todo = Todo.query.filter_by(id=int(id)).delete()
    db.session.commit()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)