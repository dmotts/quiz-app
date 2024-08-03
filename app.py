from flask import Flask, request, jsonify
from openai import OpenAI
import os
import json
import urllib.request
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

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
        """
        prompt = self.generate_prompt(answers, additional_info)
        client = OpenAI(
            api_key=self.openai_key
        )

        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-4o-mini",
        )

        print("Response: ", response.choices[0].message.content)

        return response.choices[0].message.content
    """

        return "# Business A.I. Insights Report\n\n## Objective\nTo leverage AI technologies aimed at increasing sales and enhancing customer service within a timeframe of 1-3 months.\n\n---\n\n### Overview\n\nThe insights provided in this report are rooted in the goal of increasing sales while simultaneously elevating customer service levels. In an increasingly competitive marketplace, employing artificial intelligence can streamline operations, personalize customer experiences, and gain deeper insights into consumer behavior. \n\n### Key Opportunities\n\n1. **Personalized Marketing Campaigns**\n   - **Actionable Insight**: Utilize AI algorithms to analyze customer data (purchase history, browsing behavior) to craft tailored marketing campaigns.\n   - **Strategies**:\n     - Implement segmentation techniques to identify high-value customer groups.\n     - Develop targeted email campaigns or social media ads featuring products that align with customer preferences and past purchases.\n\n2. **Chatbots for Customer Service**\n   - **Actionable Insight**: Deploy AI chatbots to handle routine customer inquiries and support requests, freeing up human resources for complex queries.\n   - **Strategies**:\n     - Train chatbots with a comprehensive FAQ database to provide instant responses.\n     - Continuously improve the chatbot's knowledge base based on customer interactions, ensuring it learns over time.\n\n3. **Predictive Sales Analytics**\n   - **Actionable Insight**: Implement predictive analytics tools to forecast sales demand and customer purchasing behavior.\n   - **Strategies**:\n     - Analyze historical sales data to identify patterns and trends.\n     - Use these insights to optimize inventory management and plan promotional strategies, thus minimizing stockouts or excess inventory.\n\n4. **Customer Feedback Analysis**\n   - **Actionable Insight**: Utilize sentiment analysis tools to evaluate customer feedback from various channels (social media, reviews, surveys) and make informed decisions.\n   - **Strategies**:\n     - Regularly collect and analyze feedback to identify pain points in the customer journey.\n     - Adapt business practices or product offerings based on insights gathered to improve customer satisfaction.\n\n5. **Enhanced Customer Journey mapping**\n   - **Actionable Insight**: Utilize AI to map out customer journeys in real-time, identifying drop-off points and opportunities for engagement.\n   - **Strategies**:\n     - Implement analytics tools that visualize customer interactions with the business at every touchpoint.\n     - Identify barriers to sales conversion and create relevant touchpoints that drive engagement and purchases.\n\n### Implementation Timeline (1-3 Months)\n\n#### Month 1:\n- **Tool Assessment**: Research and select AI tools that best fit your business needs (e.g., chatbot platforms, predictive analytics software).\n- **Data Gathering**: Begin gathering and cleaning customer data across platforms to enhance the AI algorithm's effectiveness.\n\n#### Month 2:\n- **Deployment of Chatbots**: Set up and test the chatbot, implementing the FAQ database and ensuring integration with existing customer service tools.\n- **Market Segmentation**: Utilize AI analytics to segment your customer base and start designing personalized marketing materials.\n\n#### Month 3:\n- **Launch Campaigns**: Roll out targeted marketing campaigns and introduce the AI chatbot online.\n- **Feedback Loop**: Begin collecting customer feedback on the new services and analyze using sentiment analysis tools. Adjust strategies based on findings.\n\n---\n\n### Conclusion\n\nBy capitalizing on AI technologies in a structured approach, businesses can enhance sales outcomes and significantly improve customer service efficiency within a short period. Focused efforts on personalized marketing, AI-driven customer support, and analytics will pave the way for fulfilling the outlined objectives.\n\nInvesting in these strategies places businesses in a favorable position to not only meet but exceed customer expectations, ultimately resulting in improved sales performance."

    def create_pdf(self, content):
        url = "https://api.pdf.co/v1/pdf/convert/from/html"
        headers = {
            "x-api-key": str(self.pdfco_api_key),
            "Content-Type": "application/json"
        }
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Business A.I. Insights Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            line-height: 1.6;
        }}
        header {{
            text-align: center;
            margin-bottom: 40px;
        }}
        header h1 {{
            font-size: 2.5em;
            margin: 0;
        }}
        section {{
            margin-bottom: 20px;
        }}
        h2, h3 {{
            color: #2c3e50;
        }}
        .section-title {{
            border-bottom: 2px solid #2980b9;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        .insight {{
            margin-bottom: 10px;
        }}
        .insight-title {{
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .insight-content {{
            margin-left: 20px;
        }}
        .strategies {{
            list-style-type: disc;
            margin-left: 40px;
        }}
        .timeline {{
            border-left: 3px solid #2980b9;
            padding-left: 15px;
            margin-left: 10px;
        }}
        .timeline-item {{
            margin-bottom: 20px;
        }}
    </style>
</head>
<body>
    <header>
        <h1>Business A.I. Insights Report</h1>
        <p>To leverage AI technologies aimed at increasing sales and enhancing customer service within a timeframe of 1-3 months.</p>
    </header>
    <section>
        <div class="section-title">
            <h2>Overview</h2>
        </div>
        <p>The insights provided in this report are rooted in the goal of increasing sales while simultaneously elevating customer service levels. In an increasingly competitive marketplace, employing artificial intelligence can streamline operations, personalize customer experiences, and gain deeper insights into consumer behavior.</p>
    </section>
    <section>
        <div class="section-title">
            <h2>Key Opportunities</h2>
        </div>
        {content}
    </section>
    <section>
        <div class="section-title">
            <h2>Implementation Timeline (1-3 Months)</h2>
        </div>
        <div class="timeline">
            <div class="timeline-item">
                <h3>Month 1:</h3>
                <ul>
                    <li><strong>Tool Assessment:</strong> Research and select AI tools that best fit your business needs (e.g., chatbot platforms, predictive analytics software).</li>
                    <li><strong>Data Gathering:</strong> Begin gathering and cleaning customer data across platforms to enhance the AI algorithm's effectiveness.</li>
                </ul>
            </div>
            <div class="timeline-item">
                <h3>Month 2:</h3>
                <ul>
                    <li><strong>Deployment of Chatbots:</strong> Set up and test the chatbot, implementing the FAQ database and ensuring integration with existing customer service tools.</li>
                    <li><strong>Market Segmentation:</strong> Utilize AI analytics to segment your customer base and start designing personalized marketing materials.</li>
                </ul>
            </div>
            <div class="timeline-item">
                <h3>Month 3:</h3>
                <ul>
                    <li><strong>Launch Campaigns:</strong> Roll out targeted marketing campaigns and introduce the AI chatbot online.</li>
                    <li><strong>Feedback Loop:</strong> Begin collecting customer feedback on the new services and analyze using sentiment analysis tools. Adjust strategies based on findings.</li>
                </ul>
            </div>
        </div>
    </section>
    <section>
        <div class="section-title">
            <h2>Conclusion</h2>
        </div>
        <p>By capitalizing on AI technologies in a structured approach, businesses can enhance sales outcomes and significantly improve customer service efficiency within a short period. Focused efforts on personalized marketing, AI-driven customer support, and analytics will pave the way for fulfilling the outlined objectives.</p>
        <p>Investing in these strategies places businesses in a favorable position to not only meet but exceed customer expectations, ultimately resulting in improved sales performance.</p>
    </section>
</body>
</html>
    """
        
        payload = json.dumps({
            "html": html_content,
            "name": "report.pdf"
        }).encode("utf-8")
    
        # Log the request for debugging
        logging.debug(f"Creating PDF with payload: {payload.decode('utf-8')}")
    
        req = urllib.request.Request(url, data=payload, headers=headers, method='POST')
        with urllib.request.urlopen(req) as response:
            response_data = response.read()
            response_json = json.loads(response_data)
    
        # Log the response for debugging
        logging.debug(f"Received response: {response_json}")
    
        if response_json.get("error"):
            raise Exception(f"PDF generation error: {response_json['message']}")
            
        
        return response_json["url"]

    def send_error_report(self, error):
        error_message = f"An error occurred in the A.I. report generation API: {str(error)}"
        data = json.dumps({
            "subject": "A.I. API is down - Business A.I. Insights Report",
            "message": error_message
        }).encode("utf-8")
        req = urllib.request.Request(
            f"https://formspree.io/{self.formspree_email}",
            data=data,
            headers={'Content-Type': 'application/json'}
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
        logging.error(f"Error generating report: {e}")
        report_generator.send_error_report(e)
        return jsonify({
            "message": "There was an issue generating your report. We are looking into it.",
            "fallback": "You will receive your business A.I. insights report shortly. Please contact us if you have any questions."
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
