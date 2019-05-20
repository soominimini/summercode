from flask import Flask, render_template, request, flash, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = "random string"
db = SQLAlchemy(app)


class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    contents = db.Column(db.String(100))
    priority = db.Column(db.Integer)
    done = db.Column(db.String(20))
    due = db.Column(db.Integer)

    def __init__(self, title, contents, priority, done, due):
        self.title = title
        self.contents = contents
        self.priority = priority
        self.done = done
        self.due = due

@app.route("/show_list/", methods=['GET', 'POST'])
def List_show():
    list = List.query.order_by(List.priority).all()
    return render_template('show_all.html', list=list)

@app.route("/creat/", methods=['GET', 'POST'])
def TODO_create():
    if request.method == 'POST':
        if not request.form['title'] or not request.form['contents'] or not request.form['priority']:
            flash('Please enter all the fields', 'error')

        else:
            list = List(request.form['title'], request.form['contents'],
                        request.form['priority'], request.form['done'], request.form['due'])

            db.session.add(list)
            db.session.commit()
            flash('Record was successfully added')
            return redirect(url_for('List_show'))

    else:
        return render_template('create.html')


@app.route("/update/<id>/", methods=['GET', 'POST'])
def user_update(id):
    if request.method == 'POST':

        update_title_val = request.form['update_title']
        update_contents_val = request.form['update_contents']
        update_priority_val = request.form['update_priority']
        update_done_val = request.form['update_done']
        if not update_title_val == '':
            sql = List.query.get(id)
            sql.title = update_title_val
            db.session.commit()
        if not update_contents_val == '':
            sql = List.query.get(id)
            sql.contents = update_contents_val
            db.session.commit()
        if not update_priority_val == '':
            sql = List.query.get(id)
            sql.priority = update_priority_val
            db.session.commit()
        if not update_done_val == '':
            sql = List.query.get(id)
            sql.done = update_done_val
            db.session.commit()
        flash('Record was successfully added')
        return redirect(url_for('List_show'))

    else:
        return render_template('update.html')

@app.route("/delete/<id>/", methods=['GET'])
def user_delete(id):
    if request.method == 'GET':
        List.query.filter(List.id == id).delete()
        db.session.commit()
        flash('Record was successfully added')
        return redirect(url_for('List_show'))


if __name__ == '__main__':
    # db.drop_all() 맨 처음에 시작할 때 테이블 drop 하려면 이 코드 쓰고 아니면 쓰지 말고
    db.create_all()
    app.run(debug=True)
