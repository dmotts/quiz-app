from flask import Flask, request, jsonify, make_response
import openai
import os
import pdfkit
from tempfile import NamedTemporaryFile
import urllib.request
import json

class ReportGenerator:
    def __init__(self, openai_key, formspree_email):
        self.openai_key = openai_key
        self.formspree_email = formspree_email

    def generate_prompt(self, answers, additional_info):
        return (
            f"Generate a business A.I. insights report based on the following answers: {answers}. "
            f"Additional information: {additional_info}. Include actionable insights and potential strategies."
        )

    def generate_report(self, answers, additional_info):
        prompt = self.generate_prompt(answers, additional_info)

        openai.api_key = self.openai_key
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1500
        )

        return response.choices[0].text.strip()

    def create_pdf(self, content):
        with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            pdfkit.from_string(content, temp_file.name)
            return temp_file.name

    def send_error_report(self, error):
        error_message = f"An error occurred in the A.I. report generation API: {str(error)}"
        data = json.dumps({
            "subject": "A.I. API is down - Business A.I. Insights Report",
            "message": error_message
        }).encode("utf-8")
        req = urllib.request.Request(f"https://formspree.io/{self.formspree_email}", data=data, headers={'content-type': 'application/json'})
        urllib.request.urlopen(req)

app = Flask(__name__)

# CORS handling manually
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'https://0a60d95d-49f5-432e-be40-14ddbdf973c5-00-5w0n7hthz700.picard.replit.dev')
    response.headers.add('Access-Control-Allow-Methods', 'POST')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response

report_generator = ReportGenerator(os.getenv("OPENAI_API_KEY"), "YOUR_FORMSPREE_EMAIL")

@app.route('/', methods=['GET'])
def frontpage():
    return "API is online!"

@app.route('/generate-report', methods=['POST'])
def generate_report():
    try:
        data = request.json
        answers = data.get('answers')
        additional_info = data.get('additionalInfo')

        if not answers:
            return jsonify({"error": "Missing answers"}), 400

        report_content = report_generator.generate_report(answers, additional_info)
        temp_file_path = report_generator.create_pdf(report_content)

        # For simplicity, we assume you have a method to upload this PDF to a service
        download_url = "https://your-cloud-storage-service.com/path/to/generated_report.pdf"

        return jsonify({"downloadUrl": download_url})

    except Exception as e:
        report_generator.send_error_report(e)
        return jsonify({
            "message": "There was an issue generating your report. We are looking into it.",
            "fallback": "You will receive your business A.I. insights report shortly. Please contact us if you have any questions."
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
