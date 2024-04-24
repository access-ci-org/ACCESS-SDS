from flask import Flask, render_template, jsonify, send_file, request
from dotenv import load_dotenv
from app.softwareStatic import create_static_table
from app.reports import sanitize_and_process_reports
import os
import re
import json
import pandas as pd
import numpy as np
from datetime import datetime
from urllib.request import urlopen
app = Flask(__name__)

@app.route("/")
def software_search():
    try:
        df = pd.read_csv("./staticSearch/ACCESS Software.csv", keep_default_na=False)
    except FileNotFoundError as e:

        df = create_static_table()
        print(e)
    
    table = df.to_html(classes='table-striped" id = "softwareTable',index=False,border=1)

    return render_template("software_search.html",table=table)

@app.route("/dynamic")
def software_search_dynamic():
    df = pd.read_csv('./dynamicSearch/combined_data.csv',keep_default_na=False)
    df.insert(10,"Example Use",np.nan)
    df.fillna('',inplace=True)
    table = df.to_html(classes='table-striped" id = "softwareTableDynamic',index=False,border=1)
    return render_template("software_search.html", table=table)

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

@app.route("/report-issue", methods=['POST'])
def report_issue():
    issue_report = request.get_json()

    if issue_report['reportDetails']:
        report = sanitize_and_process_reports(issue_report)
        current_datetime = report['datetime']

        capture_data_url = report['captureDataUrl']
        report.pop('captureDataUrl')

        report_folder = os.path.join('reports', current_datetime)
        os.makedirs(report_folder, exist_ok=True)
        report_filename = os.path.join(report_folder, 'report.json')
        with open(report_filename, 'w') as f:
            json.dump(report, f, indent=4)

        capture_data = urlopen(capture_data_url).read()
        capture_filename = os.path.join(report_folder, report['captureFilename'])
        with open(capture_filename, 'wb') as f:
            f.write(capture_data)
    else:
        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        report_folder = os.path.join('reports', current_datetime)
        os.makedirs(report_folder, exist_ok=True)
        report_filename = os.path.join(report_folder, 'report.json')
        with open(report_filename, 'w') as f:
            json.dump(issue_report, f, indent=4)

    return jsonify({'message': 'Issue reported successfully'})

@app.route("/images/<filename>")
def get_image(filename):
    if 'png' in filename:
        mimetype = 'image/png'
    elif 'svg' in filename:
        mimetype='image/svg+xml'

    return send_file(f'static/images/{filename}', mimetype=mimetype)

if __name__ == '__main__':
    load_dotenv()
    app.run(debug=True, host='0.0.0.0', port=8080)
