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
            # Parse the date
            date_obj = datetime.strptime(data['date'], '%a, %d %b %Y').date()
            
            # Create and add new income record
            new_income = Income(
                source=data['source'],
                amount=Decimal(str(data['amount'])),
                date=date_obj,
                student_name=data['student_name']
            )
            db.session.add(new_income)
            db.session.flush()  # This will assign an ID to new_income if it's using auto-increment

            # If the source is Daycare, update the daycare table
            updated_daycare = None
            if data['source'] == "Daycare":
                daycare_record = Daycare.query.filter_by(name=data['student_name']).first()
                if daycare_record:
                    daycare_record.fee_paid += Decimal(str(data['amount']))
                    daycare_record.balance = daycare_record.fee_payable - daycare_record.fee_paid
                    daycare_record.status = 'Paid' if daycare_record.balance <= 0 else 'Incomplete'
                    updated_daycare = {
                        'name': daycare_record.name,
                        'fee_payable': float(daycare_record.fee_payable),
                        'fee_paid': float(daycare_record.fee_paid),
                        'balance': float(daycare_record.balance),
                        'status': daycare_record.status
                    }
                else:
                    logging.warning(f"Daycare record not found for child: {data['student_name']}")

            db.session.commit()
            
            response_data = {
                'message': 'Income record added successfully!',
                'income_id': new_income.id
            }
            if updated_daycare:
                response_data['updated_daycare'] = updated_daycare

            logging.debug(f"Income record added: {new_income}")
            return jsonify(response_data), 201

        except IntegrityError as e:
            db.session.rollback()
            logging.error(f"IntegrityError: {str(e)}")
            return jsonify({"error": "Duplicate entry. This income already exists."}), 409
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error adding income record: {e}")
            return jsonify({'error': str(e)}), 500

    # GET method remains the same
    ...