from flask import Flask, request, jsonify
import os
import requests
import json
from tempfile import NamedTemporaryFile

class ReportGenerator:
    def __init__(self, openai_key, formspree_email, pdfco_api_key):
        self.openai_key = openai_key
        self.formspree_email = formspree_email
        self.pdfco_api_key = pdfco_api_key

    def generate_prompt(self, answers, additional_info):
        return (
            f"Generate a business A.I. insights report based on the following answers: {answers}. "
            f"Additional information: {additional_info}. Include actionable insights and potential strategies."
        )

    def generate_report(self, answers, additional_info):
        prompt = self.generate_prompt(answers, additional_info)
        client = OpenAI(api_key=self.openai_key)

        response = client.ChatCompletion.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model="gpt-4o-mini",
        )

        return response.choices[0].message['content']

    def create_pdf(self, content):
        # Using PDF.co API to create a PDF
        url = "https://api.pdf.co/v1/pdf/convert/from/html"
        headers = {
            "x-api-key": self.pdfco_api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "html": f"<html><body>{content}</body></html>",
            "name": "report.pdf"
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response_data = response.json()

        if response.status_code != 200 or not response_data.get("url"):
            raise Exception("Failed to generate PDF")

        return response_data["url"]

    def send_error_report(self, error):
        error_message = f"An error occurred in the A.I. report generation API: {str(error)}"
        data = json.dumps({
            "subject": "A.I. API is down - Business A.I. Insights Report",
            "message": error_message
        }).encode("utf-8")
        req = urllib.request.Request(
            f"https://formspree.io/{self.formspree_email}",
            data=data,
            headers={'content-type': 'application/json'}
        )
        urllib.request.urlopen(req)

app = Flask(__name__)

report_generator = ReportGenerator(
    openai_key=os.getenv("OPENAI_API_KEY"),
    formspree_email=os.getenv("FORMSPREE_EMAIL"),
    pdfco_api_key=os.getenv("PDFCO_API_KEY")
)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'https://dmotts.github.io')
    response.headers.add('Access-Control-Allow-Methods', 'POST')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Content-Security-Policy', "default-src 'self'")
    return response

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
        pdf_url = report_generator.create_pdf(report_content)

        return jsonify({"downloadUrl": pdf_url})

    except Exception as e:
        report_generator.send_error_report(e)
        return jsonify({
            "message": "There was an issue generating your report. We are looking into it.",
            "fallback": "You will receive your business A.I. insights report shortly. Please contact us if you have any questions."
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
