from app import app, db
from flask import jsonify, request, render_template, session

@app.route('/testcase', methods=['POST'])
def test():
    selected_data = request.get_json()
    session['selected_data'] = selected_data
    # Redirect to the '/testcase' route
    return jsonify({'result': "sucess"})

@app.route('/testcase', methods=['GET'])
def show_testcase():
    # Retrieve necessary data from the session or elsewhere
    selected_data = session.get('selected_data')
    selected_len = len(selected_data) if selected_data else 0
    # Render the 'testcase.html' template
    return render_template('testcase.html', selected_len=selected_len)