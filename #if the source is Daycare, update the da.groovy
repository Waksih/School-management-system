#if the source is Daycare, update the daycare table
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

