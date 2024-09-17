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

