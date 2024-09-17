@app.route('/daycare', methods=['GET', 'POST'])
@app.route('/daycare/<name>', methods=['GET', 'PUT'])
def manage_daycare(name=None):
    if request.method == 'GET':
        if name:
            # Fetch daycare record for a specific child
            logging.debug(f"Fetching daycare record for child: {name}")
            daycare_record = Daycare.query.filter_by(name=name).first()
            if daycare_record:
                logging.debug(f"Daycare record found: {daycare_record}")
                return jsonify({
                    'name': daycare_record.name,
                    'parent_1_name': daycare_record.parent_1_name,
                    'parent_1_phone': daycare_record.parent_1_phone,
                    'parent_2_name': daycare_record.parent_2_name,
                    'parent_2_phone': daycare_record.parent_2_phone,
                    'payment_mode': daycare_record.payment_mode,
                    'option': daycare_record.option,
                    'fee_payable': daycare_record.fee_payable,
                    'fee_paid': daycare_record.fee_paid,
                    'balance': daycare_record.balance,
                    'status': daycare_record.status
                })
            else:
                logging.error(f"Daycare record not found for child: {name}")
                return jsonify({'error': 'Daycare record not found'}), 404
        else:
            logging.debug('GET request received at /daycare endpoint')
            daycare = Daycare.query.all()
            daycare_list = [{
                'id': daycare.id,
                'name': daycare.name,
                'parent_1_name': daycare.parent_1_name,
                'parent_1_phone': daycare.parent_1_phone,
                'parent_2_name': daycare.parent_2_name,
                'parent_2_phone': daycare.parent_2_phone,
                'payment_mode': daycare.payment_mode,
                'option': daycare.option,
                'fee_payable': daycare.fee_payable,
                'fee_paid': daycare.fee_paid,
                'balance': daycare.balance,
                'status': daycare.status
            } for daycare in daycare]
            logging.debug(f"Daycare retrieved: {daycare_list}")
            return jsonify(daycare_list)

    elif request.method == 'POST':
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
                fee_payable=Decimal(str(data.get('fee_payable'))),
                fee_paid=Decimal('0'),  # Initialize to 0
                balance=Decimal(str(data.get('fee_payable'))),  # Initialize to fee_payable
                status='Unpaid'  # Initialize status
            )
            db.session.add(new_daycare)
            db.session.commit()
            logging.debug(f"Child added: {new_daycare}")
            return jsonify({'message': 'Child added successfully!'}), 201
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error adding child: {e}")            
            return jsonify({'error': str(e)}), 500

    elif request.method == 'PUT':
        logging.debug(f"PUT request received to update daycare record for child: {name}")
        
        # Update daycare record for a specific child
        daycare_record = Daycare.query.filter_by(name=name).first()
        if not daycare_record:
            logging.error(f"Daycare record not found for child: {name}")
            return jsonify({'error':'Daycare record not found'}), 404
        
        data = request.get_json()
        if not data:
            logging.error('No data received in PUT request')
            return jsonify({'error':'No data received'}), 400

        try:
            logging.debug(f"Current daycare record: {daycare_record}")
            
            daycare_record.parent_1_name = data.get('parent_1_name', daycare_record.parent_1_name)
            daycare_record.parent_1_phone = data.get('parent_1_phone', daycare_record.parent_1_phone)
            daycare_record.parent_2_name = data.get('parent_2_name', daycare_record.parent_2_name)
            daycare_record.parent_2_phone = data.get('parent_2_phone', daycare_record.parent_2_phone)
            daycare_record.payment_mode = data.get('payment_mode', daycare_record.payment_mode)
            daycare_record.option = data.get('option', daycare_record.option)
            daycare_record.fee_payable = Decimal(str(data.get('fee_payable', daycare_record.fee_payable)))
            daycare_record.fee_paid = Decimal(str(data.get('fee_paid', daycare_record.fee_paid)))
            
            # Recalculate balance and status
            daycare_record.balance = daycare_record.fee_payable - daycare_record.fee_paid
            daycare_record.status = 'Paid' if daycare_record.balance <= 0 else 'Incomplete'
            
            db.session.commit()
            logging.debug(f"Daycare record updated: {daycare_record}")
            return jsonify({'message': 'Daycare record updated successfully'}), 200
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error updating daycare record: {e}")
            return jsonify({'error': str(e)}), 500



if data['source'] == "Daycare":
                logging.debug(f"Attempting to update daycare record for child: {data['student_name']}")
                daycare_record = Daycare.query.filter_by(name=data['student_name']).first()
                if daycare_record:
                    logging.debug(f"Daycare record found. Current fee_paid: {daycare_record.fee_paid}")
                    daycare_record.fee_paid += Decimal(str(data['amount']))
                    daycare_record.balance = daycare_record.fee_payable - daycare_record.fee_paid
                    daycare_record.status = 'Paid' if daycare_record.balance <= 0 else 'Incomplete' 
                    db.session.commit()
                    logging.debug(f"Daycare record updated. New fee_paid: {daycare_record.fee_paid}, New balance: {daycare_record.balance}")
                    
                    return jsonify({
                        'message': 'Income record added and daycare record updated successfully!',
                        'updated_daycare': {
                            'name': daycare_record.name,
                            'fee_payable': daycare_record.fee_payable,
                            'fee_paid': daycare_record.fee_paid,
                            'balance': daycare_record.balance,
                            'status': daycare_record.status
                        }
                    }), 201
                else:
                    logging.error(f"Daycare record not found for child: {data['student_name']}")
                    return jsonify({'error': 'Daycare record not found for this child'}), 404

