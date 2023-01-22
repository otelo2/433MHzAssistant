# import main Flask class and request object
from flask import Flask, request
from sys import platform
import config
import subprocess
import datetime
import requests

# create the Flask app
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return 'Under construction'

@app.route('/alarm/disarm')
def disarmAlarm():
    output = ""
    action = "disarmed"
    commandName = "disableAlarm.sh"
    ip_addr = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    
    if (code_is_valid(request.args.get('code')) and running_on_linux()):
        output = execute_command(commandName);
        if command_ran_successfully(output):
            html_output = f"<h1> Alarm (maybe) {action}. </h1> <h2>Confirm with your ears.</h2>"
            send_notification(action, request.args.get('sentBy'), ip_addr)
        else:
            html_output = f"Alarm (maybe) not {action}. An error probably happened. Check logs."
        html_output += f"\nHere is the output from the command: \n {output}"
        return html_output
    else:
        snooper_alert_notification(ip_addr)
        return '<h1>Why are we here? Just to suffer?</h1>'
    
@app.route('/alarm/arm/full')
def fullAlarmArm():
    output = ""
    action = "armed full"
    commandName = "enableFullAlarm.sh"
    ip_addr = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    
    if (code_is_valid(request.args.get('code')) and running_on_linux()):
        output = execute_command(commandName);
        if command_ran_successfully(output):
            html_output = f"<h1> Alarm (maybe) {action}. </h1> <h2>Confirm with your ears.</h2>"
            send_notification(action, request.args.get('sentBy'), ip_addr)
        else:
            html_output = f"Alarm (maybe) not {action}. An error probably happened. Check logs."
        html_output += f"\nHere is the output from the command: \n {output}"
        return html_output
    else:
        snooper_alert_notification(ip_addr)
        return '<h1>Why are we here? Just to suffer?</h1>'


@app.route('/alarm/arm/downstairs')
def downstairsAlarmArm():
    output = ""
    action = "armed downstairs"
    commandName = "enableDownstairsAlarm.sh"
    ip_addr = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    
    if (code_is_valid(request.args.get('code')) and running_on_linux()):
        output = execute_command(commandName);
        if command_ran_successfully(output):
            html_output = f"<h1> Alarm (maybe) {action}. </h1> <h2>Confirm with your ears.</h2>"
            send_notification(action, request.args.get('sentBy'), ip_addr)
        else:
            html_output = f"Alarm (maybe) not {action}. An error probably happened. Check logs."
        html_output += f"\nHere is the output from the command: \n {output}"
        return html_output
    else:
        snooper_alert_notification(ip_addr)
        return '<h1>Why are we here? Just to suffer?</h1>'

@app.route('/alarm/emergency')
def emergencyAlarm():
    output = ""
    action = "emergency activated"
    commandName = "enableEmergencyAlarm.sh"
    ip_addr = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    
    if (code_is_valid(request.args.get('code')) and running_on_linux()):
        output = execute_command(commandName);
        if command_ran_successfully(output):
            html_output = f"<h1> Alarm (maybe) {action}. </h1> <h2>Confirm with your ears.</h2>"
            send_notification(action, request.args.get('sentBy'), ip_addr)
        else:
            html_output = f"Alarm (maybe) not {action}. An error probably happened. Check logs."
        html_output += f"\nHere is the output from the command: \n {output}"
        return html_output
    else:
        snooper_alert_notification(ip_addr)
        return '<h1>Why are we here? Just to suffer?</h1>'

# Helper methods start

def execute_command(command):
    # Execute a command and return the output
    command = f"{config.commands_directory}/{command}"
    output = subprocess.getoutput(command)
    return output

def code_is_valid(verification_code):
    # Check if the code is correct using a switch statement
    if verification_code == config.expected_verification_code:
        return True
    else:
        return False
    
def running_on_linux():
    # Check if the OS where this script is running is Linux
    if platform == "linux":
        return True
    else:
        return False
    
def command_ran_successfully(output):
    # Check if the command ran successfully
    if "End of file" in output:
        return True
    else:
        return False
    

# This method sends a notification to ntfy.sh using requests with the time and the name of the person who sent the message
def send_notification(action, senderName, ip):
    tags = ""
    priority = "default"
    
    # Get the current time and format it
    currentTime = datetime.now().strftime("%H:%M:%S")
    
    if action == "disarmed":
        tags = "green_square,speaker"
        priority = "min"
    elif action == "armed downstairs":
        tags = "yellow_square,loud_sound"
    elif action == "armed full":
        tags = "orange_square,loud_sound"
    elif action == "emergency activated":
        tags = "red_square,loudspeaker"
        priority = "urgent"

    requests.post(f"{config.ntfy_url}/alarm_notifications", \
                    data=f"Alarm {action} by {senderName} at {currentTime} from IP: {ip}", \
                    headers={
                        "Title": f"Alarm has been {action}",
                        "Priority": priority,
                        "Tags": tags
                    })
    
def snooper_alert_notification(ip):
    requests.post(f"{config.ntfy_url}/alarm_notifications", \
                    data=f"Snooper alert! From {ip}", \
                    headers={
                        "Title": f"Snooper alert!",
                        "Priority": "low",
                        "Tags": "red_square,loudspeaker"
                    })

# Helper methods end

if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(host="0.0.0.0", debug=False, port=5000)
