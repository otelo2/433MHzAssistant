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
    # Get the code from the URL
    verification_code = request.args.get('code')
    # Check if the code is correct
    if verification_code == config.expected_verification_code:
        # Check if the OS where this script is running is Linux
        output = ""
        if platform == "linux":
            # Run the disarm script
            command = f"{config.commands_directory}/disableAlarm.sh"
            output = subprocess.getoutput(command)
        else:
            return "Not supported on this platform"
        
        # Return the output of the disarm script
        if "End of file" in output:
            html_output = f"<h1> Alarm (maybe) disarmed. </h1> <h2>Confirm with your ears.</h2>"
        else:
            html_output = f"Alarm (maybe) not disarmed. An error probably happened. Check logs."
            
        html_output += f"Here is the output from the command: \n {output}"	
        return html_output
    else:
        return 'Why are we here? Just to suffer?' 

if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(host="0.0.0.0", debug=True, port=5000)