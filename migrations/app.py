from flask import Flask, render_template, request, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy
from models import User,Question,Answer
from sqlalchemy import or_
app = Flask(__name__)
app.config['SECRET_KEY']='123456'
app.config['SQLALCHEMY_DATABASE_URI']="mysql+pymysql://root:root@localhost:3306/demo3"
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db= SQLAlchemy(app)


@app.route('/')
def index():
    context = {
        'questions':Question.query.order_by('-create_time').all()
    }
    return render_template('index.html', **context)


@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        passworld = request.form.get('password')
        user = User.query.filter(User.telephone==telephone,User.password==passworld).first()
        if user:
            session['user_id'] = user.id
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return "手机号码或者密码错误"

@app.route('/regist/', methods=['GET', 'POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return "该手机号码已经被注册"
        else:
            if password1 != password2:
                return "两次密码不一致，请核对后重新注册"
            else:
                user = User(telephone=telephone,username=username,password=password1)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))
@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/question/',methods=['GET','POST'])
def question():
    if session.get('user_id'):
        if request.method == 'GET':
            return render_template('question.html')
        else:
            from models import db
            title = request.form.get('title')
            content = request.form.get('content')
            question = Question(title=title, content=content)
            user_id = session.get('user_id')
            user = User.query.filter(User.id == user_id).first()
            question.auther = user
            db.session.add(question)
            db.session.commit()
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))

@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user':user}
    return {}

@app.route('/detail/<question_id>/')
def detail(question_id):
    question_model = Question.query.filter(Question.id == question_id).first()
    return render_template('detail.html', question=question_model)

@app.route('/add_answer/',methods=['POST'])
def add_answer():
    from models import db
    content = request.form.get('answer_content')
    question_id = request.form.get('question_id')
    answer = Answer(content=content)
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        answer.auther = user
        question = Question.query.filter(Question.id == question_id).first()
        answer.question = question
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for('detail', question_id=question_id))
    else:
        return redirect(url_for('login'))
@app.route('/search/')
def search():
    q = request.args.get('q')
    questions = Question.query.filter(or_(Question.title.contains(q),Question.content.contains(q))).order_by('-create_time')
    return render_template('index.html', questions=questions)

if __name__ == '__main__':
    app.run(host='192.168.0.173', port=5000, debug='True')
