# import main Flask class and request object
from flask import Flask, request
import config

# create the Flask app
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return 'Under construction'

@app.route('/alarm/disarm')
def query_example():
    # Expect: http://localhost:5000/alarm/disarm?code=SECRETCODEFROMCONFIG
    verification_code = request.args.get('code')
    if verification_code == config.expected_verification_code:
        # Execute IQ to disarm alarm
        return 'Alarm has (hopefully) been disarmed'
    else:
        return 'Why are we here? Just to suffer?' 

@app.route('/form-example')
def form_example():
    return 'Form Data Example'

@app.route('/json-example')
def json_example():
    return 'JSON Object Example'

if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)