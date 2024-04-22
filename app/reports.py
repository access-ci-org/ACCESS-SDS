from datetime import datetime

def sanitize_and_process_reports(issue_report):
    feedback = issue_report['feedback']
    report_details = issue_report['reportDetails']
    page_url = report_details['pageUrl']
    element_type = report_details['elementType']
    element_id = report_details['elementId']
    element_class = report_details['elementClass']
    element_text = report_details['elementText']
    table_cell_info = report_details['tableCellInfo']
    capture_data_url = report_details['captureDataUrl']

    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    capture_filename = f"issue_{current_datetime}.png"

    report = {
        "datetime": current_datetime,
        "pageUrl": page_url,
        "elementType": element_type,
        "elementId": element_id,
        "elementClass": element_class,
        "elementText": element_text,
        "tableCellInfo": table_cell_info,
        "feedback": feedback,
        "captureFilename": capture_filename
    }

    return report, capture_data_url