import logging
from datetime import datetime
from decimal import Decimal

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

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
    name = db.Column(db.String(50), unique = True, nullable = False)
    class_name = db.Column(db.String(20))
    parent1_name = db.Column(db.String(50))
    parent1_phone = db.Column(db.String(15))
    parent2_name = db.Column(db.String(50))
    parent2_phone = db.Column(db.String(15))
    fee_payable = db.Column(db.Numeric(10, 2))
    fee_status = db.Column(db.String(20))

class Daycare(db.Model):
    __tablename__ = 'daycare'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    parent_1_name = db.Column(db.String(50))
    parent_1_phone = db.Column(db.String(15))
    parent_2_name = db.Column(db.String(50))
    parent_2_phone = db.Column(db.String(15))
    payment_mode = db.Column(db.String(15))
    option = db.Column(db.String(20))
    fee_payable = db.Column(db.Numeric(10, 2))
    fee_paid = db.Column(db.Numeric(10, 2))
    balance = db.Column(db.Numeric(10, 2))
    status = db.Column(db.String(20))

class Fee(db.Model):
    __tablename__ = 'fees'
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String, db.ForeignKey('students.name'))
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
    activity_name = db.Column(db.String(50), unique = True, nullable = False)
    payment_frequency = db.Column(db.String(20))
    fee_amount = db.Column(db.Numeric(10, 2))

class StudentActivity(db.Model):
    __tablename__ = 'student_activities'    
    student_name = db.Column(db.String, db.ForeignKey('students.name'), primary_key=True)
    activity_name = db.Column(db.String, db.ForeignKey('activities.activity_name'), primary_key=True)

class ActivityParticipation(db.Model):
    __tablename__ = 'activity_participation'
    id = db.Column(db.Integer, primary_key=True, autoincrement= True)
    term = db.Column(db.Integer, nullable=False)
    frequency = db.Column(db.String(20))
    student_name = db.Column(db.String(50), db.ForeignKey('students.name'))
    activity_name = db.Column(db.String(50), db.ForeignKey('activities.activity_name'))
    status = db.Column(db.String(20))
    date_paid_for = db.Column(db.Date)
    amount_paid = db.Column(db.Numeric(10, 2))
    balance = db.Column(db.Numeric(10, 2))
    __table_args__ = (db.UniqueConstraint('student_name', 'activity_name', 'term', 'frequency', 'status', name='unique_participation'),)

class Income(db.Model):
    __tablename__='income'
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(50))
    amount = db.Column(db.Numeric(10, 2))
    date = db.Column(db.Date)
    student_name = db.Column(db.String(50), db.ForeignKey('students.name'))


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
            # Create initial fee record
            new_fee = Fee(
                student_name=new_student.name,
                total_fees=new_student.fee_payable,
                amount_paid=0,
                balance=new_student.fee_payable,
                remarks="Initial fee record"
            )
            db.session.add(new_fee)
            db.session.commit()
            
            logging.debug(f"Student added: {new_student}")
            return jsonify({'message': 'Student added successfully!'}), 201
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error adding student: {e}")
            if "UNIQUE constraint failed" in str(e):
                return jsonify({'error': 'A student with this name already exists'}), 400
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


@app.route('/daycare', methods=['GET', 'POST'])
def manage_daycare():
    if request.method == 'POST':
        logging.debug('POST request received at /daycare endpoint')
        data = request.get_json()
        logging.debug(f"Received data: {data}")
        
        if not data:
            logging.error('No data received in POST request')
            return jsonify({'error': 'No data received'}), 400
        
        try:
            new_daycare = Daycare(
                name=data.get('name'),
                parent_1_name=data.get('parent_1_name'),
                parent_1_phone=data.get('parent_1_phone'),
                parent_2_name=data.get('parent_2_name'),
                parent_2_phone=data.get('parent_2_phone'),
                payment_mode=data.get('payment_mode'),
                option=data.get('option'),
                fee_payable=data.get('fee_payable'),
                fee_paid=data.get('fee_paid'),
                balance=data.get('balance'),
                status=data.get('status')
            )
            db.session.add(new_daycare)
            db.session.commit()
            logging.debug(f"Child added: {new_daycare}")
            return jsonify({'message': 'Child added successfully!'}), 201
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error adding child: {e}")            
            return jsonify({'error': str(e)}), 500

    logging.debug('GET request received at /daycare endpoint')
    daycare = Daycare.query.all()
    daycare_list = [{
        'id': daycare.id,
        'name': daycare.name,
        'parent_1_name': daycare.parent_1_name,
        'parent_1_phone': daycare.parent_1_phone,
        'parent_2_name': daycare.parent_2_name,
        'parent_2_phone': daycare.parent_2_phone,
        'payment_mode' : daycare.payment_mode,
        'option' : daycare.option,
        'fee_payable': daycare.fee_payable,
        'fee_paid': daycare.fee_paid,
        'balance' : daycare.balance,
        'status' : daycare.status
    } for daycare in daycare]
    logging.debug(f"Daycare retrieved: {daycare_list}")
    return jsonify(daycare_list)


@app.route('/fees', methods=['GET',])
@app.route('/fees/<student_name>', methods=['GET', 'PUT'])
def manage_fees(student_name = None):
    if request.method == 'GET':
        if student_name:
            #fetch fee record for a specific student
            logging.debug(f"Fetching fee record for student: {student_name}")
            
            fee_record = Fee.query.filter_by(student_name=student_name).first()
            if fee_record:
                logging.debug(f"Fee record found: {fee_record}")
                
                return jsonify({
                    'student_name': fee_record.student_name,
                    'total_fees': fee_record.total_fees,
                    'amount_paid': fee_record.amount_paid,
                    'balance': fee_record.balance,
                    'remarks': fee_record.remarks
                })
            else:
                logging.error(f"Fee record not found for student: {student_name}")
                
                return jsonify ({'error': 'Fee record not found'}), 404
        else:
            logging.debug('GET request received at /fees endpoint')
            fees = Fee.query.all()
            fee_list = [{
                'id': fee.id,
                'student_name': fee.student_name,
                'total_fees': fee.total_fees,
                'amount_paid': fee.amount_paid,
                'balance': fee.balance,
                'remarks': fee.remarks
            } for fee in fees]
            logging.debug(f"Fees retrieved: {fee_list}")
            return jsonify(fee_list)
    elif request.method == 'PUT':
        logging.debug(f"PUT request received to update fee record for student: {student_name}")
        
        #Update fee record for a specific student
        fee_record = Fee.query.filter_by(student_name=student_name).first()
        if not fee_record:
            logging.error(f"Fee record not found for student: {student_name}")
            
            return jsonify({'error':'Fee record not found'}),404
        data = request.get_json()
        if not data:
            logging.error('No data received in PUT request')
           
            return jsonify({'error':'No data received'}), 400

        try:
            logging.debug(f"Current fee record: {fee_record}")
            
            fee_record.total_fees = data.get('total_fees', fee_record.total_fees)
            fee_record.amount_paid = data.get('amount_paid', fee_record.amount_paid)
            fee_record.balance = data.get('balance', fee_record.balance)
            fee_record.remarks = data.get('remarks', fee_record.remarks)
            
            db.session.commit()
            logging.debug(f"Fee record updated: {fee_record}")
            return jsonify({'message': 'Fee record updated successfully'}), 200
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error updating fee: {e}")
            return jsonify({'error': str(e)}), 500


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
            date_obj = datetime.strptime(data['date'], '%a, %d %b %Y').date()
            new_expenditure = Expenditure(
                date=date_obj,
                item=data['item'],
                category=data['category'],
                vendor=data['vendor'],
                amount=data['amount']
            )
            db.session.add(new_expenditure)
            db.session.commit()
            logging.debug(f"Expenditure added: {new_expenditure}")
            return jsonify({'message': 'Expenditure added successfully!'}), 201
        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "Duplicate entry. This expenditure already exists."}), 409
            
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
            # Check if student and activity exist
            student_exists = db.session.query(Student).filter_by(name=data.get('student_name')).first()
            activity_exists = db.session.query(Activity).filter_by(activity_name=data.get('activity_name')).first()

            if not student_exists or not activity_exists:
                logging.error('Student or Activity does not exist')
                return jsonify({'error': 'Student or Activity does not exist'}), 400

            new_student_activity = StudentActivity(
                student_name=data.get('student_name'),
                activity_name=data.get('activity_name')
            )
            db.session.add(new_student_activity)
            db.session.commit()
            logging.debug(f"Student activity added: {new_student_activity}")
            return jsonify({'message': 'Student activity added successfully!'}), 201
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error adding student activity: {e}")
            return jsonify({'error': f"{str(e)}; Data: {data}"}), 500
        
    logging.debug('GET request received at /student_activities endpoint')
    student_activities = StudentActivity.query.all()
    student_activity_list = [{
        'student_name': student_activity.student_name,
        'activity_name': student_activity.activity_name
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
            # Check if student and activity exist
            student_exists = db.session.query(Student).filter_by(name=data.get('student_name')).first()
            activity_exists = db.session.query(Activity).filter_by(activity_name=data.get('activity_name')).first()

            if not student_exists or not activity_exists:
                logging.error('Student or Activity does not exist')
                return jsonify({'error': 'Student or Activity does not exist'}), 400

            new_activity_participation = ActivityParticipation(
               student_name=data['student_name'],
                activity_name=data['activity_name'],
                term=data['term'],
                frequency=data['frequency'],
                status=data['status'],
                date_paid_for=data['date_paid_for'],
                amount_paid=data['amount_paid'],
                balance=data['balance']
            )
            db.session.add(new_activity_participation)
            db.session.commit()
            logging.debug(f"Activity participation added: {new_activity_participation}")
            return jsonify({'message': 'Participation recorded successfully!'}), 201
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error adding participation record: {e}")
            return jsonify({'error': str(e)}), 500

    logging.debug('GET request received at /activity_participation endpoint')
    activity_participations = ActivityParticipation.query.all()
    activity_participation_list = [{
        'id': activity_participation.id,
        'student_name': activity_participation.student_name,
        'activity_name': activity_participation.activity_name,
        'term': activity_participation.term,
        'frequency': activity_participation.frequency,
        'status': activity_participation.status,
        'date_paid_for': activity_participation.date_paid_for,
        'amount_paid': activity_participation.amount_paid,
        'balance': activity_participation.balance
    } for activity_participation in activity_participations]
    logging.debug(f"Participation records retrieved: {activity_participation_list}")
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
            date_obj = datetime.strptime(data['date'], '%a, %d %b %Y').date()
            new_income = Income(
                source=data['source'],
                amount=Decimal(str(data['amount'])),
                date=date_obj,
                student_name=data['student_name']
            )
            db.session.add(new_income)
            db.session.commit()

            #if the source is fees, update the fees table
            if data['source'] == "Fees":
                logging.debug(f"Attempting to update fee record for student: {data['student_name']}")               
                fee_record = Fee.query.filter_by(student_name=data['student_name']).first()
                if fee_record:
                    logging.debug(f"Fee record found. Current amount_paid: {fee_record.amount_paid}")                   
                    fee_record.amount_paid += Decimal(str(data['amount']))
                    fee_record.balance = fee_record.total_fees - fee_record.amount_paid
                    db.session.commit()
                    logging.debug(f"Fee record updated. New amount_paid: {fee_record.amount_paid}, New balance: {fee_record.balance}")
                   
                    return jsonify({
                        'message': 'Income record added and fee record updated successfully!',
                        'updated_fee': {
                            'student_name': fee_record.student_name,
                            'total_fees': fee_record.total_fees,
                            'amount_paid': fee_record.amount_paid,
                            'balance': fee_record.balance
                        }
                    }), 201
                else:
                    logging.error(f"Fee record not found for student: {data['student_name']}")
                   
                    return jsonify({'error': 'Fee record not found for this student'}), 404


            logging.debug(f"Income record added: {new_income}")
            return jsonify({'message': 'Income record added successfully!'}), 201
        except IntegrityError as e:
            db.session.rollback()
            logging.error(f"IntegrityError: {str(e)}")
            
            return jsonify({"error": "Duplicate entry. This income already exists."}), 409
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
        'date': income.date,
        'student_name': income.student_name
    } for income in income_records]
    logging.debug(f"Income records retrieved: {income_list}")
    return jsonify(income_list)


if __name__ == '__main__':
    app.run(debug=True)
