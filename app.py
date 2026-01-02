from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# ----------------------
# App configuration
# ----------------------
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # database file
app.config['SECRET_KEY'] = 'your_secret_key'  # for forms if needed

db = SQLAlchemy(app)

# ----------------------
# Database model
# ----------------------
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    course = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Student {self.name}>"

# ----------------------
# Routes
# ----------------------

# Home / List students
@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

# Add student
@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        course = request.form['course']

        new_student = Student(name=name, age=age, course=course)
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add_student.html')

# Edit student
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        student.name = request.form['name']
        student.age = request.form['age']
        student.course = request.form['course']
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit_student.html', student=student)

# Delete student
@app.route('/delete/<int:id>')
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('index'))

# ----------------------
# Run the app
# ----------------------
if __name__ == "__main__":
    # Create database inside application context
    with app.app_context():
        db.create_all()  # database.db will be created automatically
    app.run(debug=True)
