from flask import Flask, request, jsonify, send_file
import openai
from utils.generate_pdf import create_pdf
from utils.send_email import send_report_email
import os

app = Flask(__name__)

openai.api_key = 'YOUR_OPENAI_API_KEY'

@app.route('/generate-insights', methods=['POST'])
def generate_insights():
    data = request.json
    prompt = f"""
    You are an A.I. consultant generating a comprehensive Business A.I. Insights Report based on the following client details:

    User Name: {data['name']}
    Company Name: {data['company']}
    Business Industry: {data['industry']}
    Business Size: {data['size']}
    Primary Business Challenge: {data['challenge']}
    Current Use of Technology: {data['technology']}
    Goals: {data['goals']}

    Provide a detailed analysis and recommendations for the following areas:

    1. A.I. Opportunities: Identify key opportunities where A.I. can be implemented to solve the primary business challenge and enhance operational efficiency.

    2. Technology Integration: Suggest ways to integrate A.I. with the current technology stack to optimize processes and achieve the company's goals.

    3. Actionable Steps: Provide a step-by-step plan for implementing A.I. solutions, including potential tools, platforms, and technologies that would be most effective.

    4. Expected Benefits: Describe the expected benefits of implementing these A.I. solutions, focusing on improving efficiency, productivity, and overall business performance.

    5. Future Trends: Highlight future A.I. trends relevant to the client's industry that they should be aware of and prepared for.

    Create a personalized and insightful report that positions the client as a forward-thinking and innovative company ready to leverage A.I. for business success.
    """

    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=1500
    )

    report = response.choices[0].text.strip()

    # Generate PDF
    pdf_path = create_pdf(data['name'], report)

    # Send email with PDF attachment
    send_report_email(data['email'], pdf_path)

    return jsonify({'report': report, 'pdf_path': pdf_path})

@app.route('/download-pdf', methods=['GET'])
def download_pdf():
    pdf_path = request.args.get('pdf_path')
    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
