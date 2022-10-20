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
        
        output = ""
        if platform == "linux":
            # linux
            command = f"sudo /home/pi/rpitx/sendiq -s 250000 -f 434.0e6 -t u8 -i {config.IQ_directory}/disableAlarm-b2.iq"
            print(command)
            usingSH = f"{config.commands_directory}/disableAlarm.sh"
            hmm = subprocess.getoutput(usingSH)
            print(hmm)
            output = subprocess.run([sudo, "/home/pi/rpitx/sendiq", -s, 250000, -f, 434.0e6, -t, u8, -i, "{config.IQ_directory}/disableAlarm-b2.iq"], capture_output=True)
        
        html_output = f"Hi, you are running as {user} and you have successfully disarmed the alarm. Here is the output from the command: {output} or {hmm}"	
        return html_output
    else:
        return 'Why are we here? Just to suffer?' 

if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(host="0.0.0.0", debug=True, port=5000)