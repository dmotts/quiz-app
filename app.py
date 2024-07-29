from flask import Flask, request, jsonify
import openai
import os
import pdfkit
from tempfile import NamedTemporaryFile

app = Flask(__name__)

@app.after_request
def apply_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "https://0a60d95d-49f5-432e-be40-14ddbdf973c5-00-5w0n7hthz700.picard.replit.dev"
    response.headers["Access-Control-Allow-Methods"] = "POST"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

@app.route('/', methods=['GET'])
def frontpage():
    return "API is online!"

@app.route('/generate-report', methods=['POST'])
def generate_report():
    try:
        # Extract data from request
        data = request.json
        print(data)
        answers = data.get('answers')
        additional_info = data.get('additionalInfo')

        if not answers:
            return jsonify({"error": "Missing answers"}), 400

        # Construct the prompt for GPT-3.5
        prompt = (
            f"Generate a business A.I. insights report based on the following answers: {answers}. "
            f"Additional information: {additional_info}. Include actionable insights and potential strategies."
        )

        # Generate the report using OpenAI GPT-3.5
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1500
        )

        report_content = response.choices[0].text.strip()

        # Create a temporary PDF file
        with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            pdfkit.from_string(report_content, temp_file.name)
            temp_file_path = temp_file.name

        # For simplicity, we assume you have a method to upload this PDF to a service
        # Here we will just return a placeholder URL
        download_url = "https://your-cloud-storage-service.com/path/to/generated_report.pdf"

        return jsonify({"downloadUrl": download_url})

    except Exception as e:
        # Handle errors by sending an email via Formspree and notify the user
        send_error_report(e)
        return jsonify({
            "message": "There was an issue generating your report. We are looking into it.",
            "fallback": "You will receive your business A.I. insights report shortly. Please contact us if you have any questions."
        }), 500

def send_error_report(error):
    formspree_url = "https://formspree.io/YOUR_FORMSPREE_EMAIL"
    error_message = f"An error occurred in the A.I. report generation API: {str(error)}"
    request.post(formspree_url, json={
        "subject": "A.I. API is down - Business A.I. Insights Report",
        "message": error_message
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
