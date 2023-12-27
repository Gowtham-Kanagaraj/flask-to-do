from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

class TodoItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(25), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    to_do_list = TodoItem.query.all()
    return render_template('index.html', to_do_list=to_do_list)

@app.route('/add', methods=['POST'])
def add():
    new_item = request.form.get('new_item', '')
    if new_item and len(new_item) <= 25:
        todo = TodoItem(content=new_item)
        db.session.add(todo)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:item_id>')
def delete(item_id):
    todo_to_delete = TodoItem.query.get_or_404(item_id)
    db.session.delete(todo_to_delete)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
