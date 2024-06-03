from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import logging


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/school_management'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#Enable CORS
CORS(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)



class Student(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    class_name = db.Column(db.String(20))
    parent1_name = db.Column(db.String(50))
    parent1_phone = db.Column(db.String(15))
    parent2_name = db.Column(db.String(50))
    parent2_phone = db.Column(db.String(15))
    fee_payable = db.Column(db.Numeric(10, 2))
    fee_status = db.Column(db.String(20))

class Fee(db.Model):
    __tablename__ = 'fees'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    total_fees = db.Column(db.Numeric(10, 2))
    amount_paid = db.Column(db.Numeric(10, 2))
    balance = db.Column(db.Numeric(10, 2))
    remarks = db.Column(db.Text)

class Expenditure(db.Model):
    __tablename__ = 'expenditures'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    item = db.Column(db.String(50))
    category = db.Column(db.String(50))
    vendor = db.Column(db.String(50))
    amount = db.Column(db.Numeric(10, 2))

class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True)
    activity_name = db.Column(db.String(50))
    payment_frequency = db.Column(db.String(20))
    fee_amount = db.Column(db.Numeric(10, 2))

class StudentActivity(db.Model):
    __tablename__ = 'student_activities'
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'), primary_key=True)

class ActivityParticipation(db.Model):
    __tablename__ = 'activity_participation'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'))
    term = db.Column(db.Integer, nullable=False)
    week_or_month = db.Column(db.String(20))
    participation_value = db.Column(db.Integer, nullable=False)
    __table_args__ = (db.UniqueConstraint('student_id', 'activity_id', 'term', 'week_or_month', 'participation_value', name='unique_participation'),)

class Income(db.Model):
    __tablename__='income'
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(50))
    amount = db.Column(db.Numeric(10, 2))
    date = db.Column(db.Date)


# Define routes for each table and handle CRUD operations

@app.route('/students', methods=['GET', 'POST'])
def manage_students():
    if request.method == 'POST':
        logging.debug('POST request received at /students endpoint')
        data = request.get_json()
        logging.debug(f"Received data: {data}")
        
        if not data:
            logging.error('No data received in POST request')
            return jsonify({'error': 'No data received'}), 400
        
        try:
            new_student = Student(
                name=data.get('name'),
                class_name=data.get('class_name'),
                parent1_name=data.get('parent1_name'),
                parent1_phone=data.get('parent1_phone'),
                parent2_name=data.get('parent2_name'),
                parent2_phone=data.get('parent2_phone'),
                fee_payable=data.get('fee_payable'),
                fee_status=data.get('fee_status')
            )
            db.session.add(new_student)
            db.session.commit()
            logging.debug(f"Student added: {new_student}")
            return jsonify({'message': 'Student added successfully!'}), 201
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error adding student: {e}")
            return jsonify({'error': str(e)}), 500

    logging.debug('GET request received at /students endpoint')
    students = Student.query.all()
    student_list = [{
        'id': student.id,
        'name': student.name,
        'class_name': student.class_name,
        'parent1_name': student.parent1_name,
        'parent1_phone': student.parent1_phone,
        'parent2_name': student.parent2_name,
        'parent2_phone': student.parent2_phone,
        'fee_payable': student.fee_payable,
        'fee_status': student.fee_status
    } for student in students]
    logging.debug(f"Students retrieved: {student_list}")
    return jsonify(student_list)


@app.route('/fees', methods=['GET', 'POST'])
def manage_fees():
    if request.method == 'POST':
        logging.debug('POST request received at /fees endpoint')
        data = request.get_json()
        logging.debug(f"Received data: {data}")
        
        if not data:
            logging.error('No data received in POST request')
            return jsonify({'error': 'No data received'}), 400

        try:
            new_fee = Fee(
                student_id=data['student_id'],
                total_fees=data['total_fees'],
                amount_paid=data['amount_paid'],
                balance=data['balance'],
                remarks=data['remarks']
            )
            db.session.add(new_fee)
            db.session.commit()
            logging.debug(f"Fee added: {new_fee}")
            return jsonify({'message': 'Fee record added successfully!'}), 201
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error adding fee: {e}")
            return jsonify({'error': str(e)}), 500

    logging.debug('GET request received at /fees endpoint')
    fees = Fee.query.all()
    fee_list = [{
        'id': fee.id,
        'student_id': fee.student_id,
        'total_fees': fee.total_fees,
        'amount_paid': fee.amount_paid,
        'balance': fee.balance,
        'remarks': fee.remarks
    } for fee in fees]
    logging.debug(f"Fees retrieved: {fee_list}")
    return jsonify(fee_list)


@app.route('/expenditures', methods=['GET', 'POST'])
def manage_expenditures():
    if request.method == 'POST':
        logging.debug('POST request received at /expenditures endpoint')
        data = request.get_json()
        logging.debug(f"Received data: {data}")
        
        if not data:
            logging.error('No data received in POST request')
            return jsonify({'error': 'No data received'}), 400

        try:
            new_expenditure = Expenditure(
                date=data['date'],
                item=data['item'],
                category=data['category'],
                vendor=data['vendor'],
                amount=data['amount']
            )
            db.session.add(new_expenditure)
            db.session.commit()
            logging.debug(f"Expenditure added: {new_expenditure}")
            return jsonify({'message': 'Expenditure added successfully!'}), 201
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error adding expenditure: {e}")
            return jsonify({'error': str(e)}), 500

    logging.debug('GET request received at /expenditures endpoint')
    expenditures = Expenditure.query.all()
    expenditure_list = [{
        'id': expenditure.id,
        'date': expenditure.date,
        'item': expenditure.item,
        'category': expenditure.category,
        'vendor': expenditure.vendor,
        'amount': expenditure.amount
    } for expenditure in expenditures]
    logging.debug(f"Expenditures retrieved: {expenditure_list}")
    return jsonify(expenditure_list)


@app.route('/activities', methods=['GET', 'POST'])
def manage_activities():
    if request.method == 'POST':
        logging.debug('POST request received at /activities endpoint')
        data = request.get_json()
        logging.debug(f"Received data: {data}")

        if not data:
            logging.error('No data received in POST request')
            return jsonify({'error': 'No data received'}), 400

        try:
            new_activity = Activity(
                activity_name=data['activity_name'],
                payment_frequency=data['payment_frequency'],
                fee_amount=data['fee_amount']
            )
            db.session.add(new_activity)
            db.session.commit()
            logging.debug(f"Activity added: {new_activity}")
            return jsonify({'message': 'Activity added successfully!'}), 201
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error adding activity: {e}")
            return jsonify({'error': str(e)}), 500

    logging.debug('GET request received at /activities endpoint')
    activities = Activity.query.all()
    activity_list = [{
        'id': activity.id,
        'activity_name': activity.activity_name,
        'payment_frequency': activity.payment_frequency,
        'fee_amount': activity.fee_amount
    } for activity in activities]
    logging.debug(f"Activities retrieved: {activity_list}")
    return jsonify(activity_list)


@app.route('/student_activities', methods=['GET', 'POST'])
def manage_student_activities():
    if request.method == 'POST':
        logging.debug('POST request received at /student_activities endpoint')
        data = request.get_json()
        logging.debug(f"Received data: {data}")

        if not data:
            logging.error('No data received in POST request')
            return jsonify({'error': 'No data received'}), 400

        try:
            new_student_activity = StudentActivity(
                student_id=data['student_id'],
                activity_id=data['activity_id']
            )
            db.session.add(new_student_activity)
            db.session.commit()
            logging.debug(f"Student activity added: {new_student_activity}")
            return jsonify({'message': 'Student activity added successfully!'}), 201
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error adding student activity: {e}")
            return jsonify({'error': str(e)}), 500

    logging.debug('GET request received at /student_activities endpoint')
    student_activities = StudentActivity.query.all()
    student_activity_list = [{
        'student_id': student_activity.student_id,
        'activity_id': student_activity.activity_id
    } for student_activity in student_activities]
    logging.debug(f"Student activities retrieved: {student_activity_list}")
    return jsonify(student_activity_list)


@app.route('/activity_participation', methods=['GET', 'POST'])
def manage_activity_participation():
    if request.method == 'POST':
        logging.debug('POST request received at /activity_participation endpoint')
        data = request.get_json()
        logging.debug(f"Received data: {data}")

        if not data:
            logging.error('No data received in POST request')
            return jsonify({'error': 'No data received'}), 400

        try:
            new_activity_participation = ActivityParticipation(
                student_id=data['student_id'],
                activity_id=data['activity_id'],
                term=data['term'],
                week_or_month=data['week_or_month'],
                participation_value=data['participation_value']
            )
            db.session.add(new_activity_participation)
            db.session.commit()
            logging.debug(f"Activity participation added: {new_activity_participation}")
            return jsonify({'message': 'Activity participation added successfully!'}), 201
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error adding activity participation: {e}")
            return jsonify({'error': str(e)}), 500

    logging.debug('GET request received at /activity_participation endpoint')
    activity_participations = ActivityParticipation.query.all()
    activity_participation_list = [{
        'id': activity_participation.id,
        'student_id': activity_participation.student_id,
        'activity_id': activity_participation.activity_id,
        'term': activity_participation.term,
        'week_or_month': activity_participation.week_or_month,
        'participation_value': activity_participation.participation_value
    } for activity_participation in activity_participations]
    logging.debug(f"Activity participations retrieved: {activity_participation_list}")
    return jsonify(activity_participation_list)


@app.route('/income', methods=['GET', 'POST'])
def manage_income():
    if request.method == 'POST':
        logging.debug('POST request received at /income endpoint')
        data = request.get_json()
        logging.debug(f"Received data: {data}")

        if not data:
            logging.error('No data received in POST request')
            return jsonify({'error': 'No data received'}), 400

        try:
            new_income = Income(
                source=data['source'],
                amount=data['amount'],
                date=data['date']
            )
            db.session.add(new_income)
            db.session.commit()
            logging.debug(f"Income record added: {new_income}")
            return jsonify({'message': 'Income record added successfully!'}), 201
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error adding income record: {e}")
            return jsonify({'error': str(e)}), 500

    logging.debug('GET request received at /income endpoint')
    income_records = Income.query.all()
    income_list = [{
        'id': income.id,
        'source': income.source,
        'amount': income.amount,
        'date': income.date
    } for income in income_records]
    logging.debug(f"Income records retrieved: {income_list}")
    return jsonify(income_list)


if __name__ == '__main__':
    app.run(debug=True)
