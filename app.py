# import main Flask class and request object
from flask import Flask, request
from sys import platform
import config
import subprocess

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
        user = subprocess.getoutput("whoami")
        
        sudoTest = ""
        if platform == "linux":
            # linux
            sudoTest =+ subprocess.getoutput("sudo whoami")
        
        html_output = f"Hi, you are running as {user} and you have successfully disarmed the alarm"
        return html_output + sudoTest
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
    app.run(host="0.0.0.0", debug=True, port=5000)