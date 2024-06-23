from flask import Flask, render_template, jsonify, send_file, request
from dotenv import load_dotenv
from app.reports import sanitize_and_process_reports
from app.feedback import sanitize_and_process_feedback
from app.softwareTable import create_software_table

import os
import re
import json
import pandas as pd
from datetime import datetime
app = Flask(__name__)

# Main Route
@app.route("/")
def software_search():
    try:
        df = pd.read_csv("./static/data/softwareTable.csv", keep_default_na=False)
        print("Table found!")
    except FileNotFoundError as e:
        df = create_software_table()
        print(e)
    
    table = df.to_html(classes='table-striped" id = "softwareTable',index=False,border=1).replace('\\n', '<br>')
    return render_template("software_search.html",table=table)

# 'Example Use' Modal Route
@app.route("/example_use/<software_name>")
def get_example_use(software_name):
    
    if software_name == '7-Zip':
        software_name = '7z'

    file_directory = "./dynamicSearch/softwareUse/"
    
    normalize_software_name = re.escape(software_name).lower()

    pattern = re.compile(normalize_software_name, re.IGNORECASE)

    try:
        for filename in os.listdir(file_directory):
            if pattern.search(filename):
                with open(os.path.join(file_directory,filename),'r') as file:
                    file_content = file.read()
                    return(jsonify({"use": file_content}))
        return jsonify({"use": '**Unable to find use case record**'})
    except Exception as e:
        print(e)
        return(jsonify({"use": '**Unable to find use case record**'})), 500

# 'Report Issue' Button Route
@app.route("/report-issue", methods=['POST'])
def report_issue():
    issue_report = request.get_json()

    if issue_report['reportDetails']:
        report = sanitize_and_process_reports(issue_report)
        current_datetime = report['datetime']

        report_folder = os.path.join('reports', current_datetime)
        os.makedirs(report_folder, exist_ok=True)
        report_filename = os.path.join(report_folder, 'report.json')
        with open(report_filename, 'w') as f:
            json.dump(report, f, indent=4)

    else:
        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        report_folder = os.path.join('reports', current_datetime)
        os.makedirs(report_folder, exist_ok=True)
        report_filename = os.path.join(report_folder, 'report.json')
        with open(report_filename, 'w') as f:
            json.dump(issue_report, f, indent=4)

    return jsonify({'message': 'Issue reported successfully'})


## Flask Route Definition for User Feedback Button
## process_feedback() is called anytime a POST is sent to /user-feedback
@app.route("/user-feedback", methods=['POST'])
def process_feedback():
    # Grab Ajax Request
    user_feedback = request.get_json()

    # Sanitize Feedback if necessary
    if user_feedback['feedbackForm']:
        feedback = sanitize_and_process_feedback(user_feedback)
        current_datetime = feedback['datetime']

        # Create folder and make feedback file
        feedback_folder = os.path.join('feedback', current_datetime)
        os.makedirs(feedback_folder, exist_ok=True)
        feedback_filename = os.path.join(feedback_folder, 'feedback.json')
        with open(feedback_filename, 'w') as f:
            json.dump(feedback, f, indent=4)

    else:
        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        feedback_folder = os.path.join('feedback', current_datetime)
        os.makedirs(feedback_folder, exist_ok=True)
        feedback_filename = os.path.join(feedback_folder, 'feedback.json')
        with open(feedback_filename, 'w') as f:
            json.dump(user_feedback, f, indent=4)

    return jsonify({'success': 'Feedback processed successfully'})


# Display Images
@app.route("/images/<filename>")
def get_image(filename):
    if 'png' in filename:
        mimetype = 'image/png'
    elif 'svg' in filename:
        mimetype='image/svg+xml'

    return send_file(f'static/images/{filename}', mimetype=mimetype)


# Flask Bootloader
if __name__ == '__main__':
    load_dotenv()
    app.run(debug=True, host='0.0.0.0', port=8080)