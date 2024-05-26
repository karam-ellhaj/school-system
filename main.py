from flask import Flask,render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
db = SQLAlchemy(app)

class Student(db.Model):
   
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    date_of_enroll = db.Column(db.Date, nullable=False)
    grade = db.Column(db.Integer, nullable=False)
    paid = db.Column(db.Integer,nullable=False)
    total = db.Column(db.Integer,nullable=False)
    # topay = db.Column(db.Integer,nullable=False)

# with app.app_context():
#     db.create_all()
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add-student',methods=['GET','POST'])
def add_student():

    if request.method == 'POST':
        name = request.form['name']
        date_of_enroll = request.form['date']
        year,month,day = date_of_enroll.split('-')
        date_of_enroll=date(year=int(year),month=int(month),day=int(day))
        print(date_of_enroll)
        grade = request.form['grade']
        paid = int(request.form['paid'])
        total = int(request.form['total'])
        student = Student(name=name,date_of_enroll=date_of_enroll,grade=grade,paid=paid,total=total)
        db.session.add(student)
        db.session.commit()
        return redirect('/students')
    return render_template('add-student.html')

@app.route('/edit-student',methods=['GET','POST'])
def edit():
    
    if request.method =='POST':
        id = request.form['id']
        print(id)

        student = Student.query.filter_by(id=id).first()
        # print(student)
        name = request.form['name']
        date_of_enroll = request.form['date']
        year,month,day = date_of_enroll.split('-')
        date_of_enroll=date(year=int(year),month=int(month),day=int(day))
        paid = request.form['paid']
        total = request.form['total']
        grade = request.form['grade']

        student.name = name
        student.date_of_enroll = date_of_enroll
        student.paid = paid 
        student.total = total
        student.grade = grade
        db.session.add(student)
        db.session.commit()
        return redirect('/students')
    
    student = Student.query.filter_by(id=request.args['id']).first()
    return render_template("edit-student.html",student=student)
@app.route('/students')
def students():        

    
    if request.args:
            name = request.args['name'] if 'name' in request.args else ''
            grade = request.args['grade'] if 'grade' in request.args else ''
            students = Student.query.filter(Student.name.like("%"+name+"%")).filter_by(grade=grade).all()
            if not grade:
                students = Student.query.filter(Student.name.like("%"+name+"%"))
    else:
        students = Student.query.filter_by().all()
    
        
    return render_template('students.html',students=students,grades = {
        1:"اولى اساس",
        2:"تانية اساس",
        3:'تالتة اساس',
        4:'رابعة اساس',
        5:'خامسة اساس',
        6: 'سادس اساس',
        7:'اولى متوسط',
        8:'تانية متوسط',
        9:'تالتة متوسط',
        10:'اولى ثانوي',
        11:'تانية ثانوي ',
        12:'تالتة ثانوي '
        })

@app.route('/delete/<id>')
def delete(id):
    db.session.delete(Student.query.filter_by(id=id).first())
    db.session.commit()
    return redirect('/students')
if __name__ == '__main__':
    app.run(debug=True)
