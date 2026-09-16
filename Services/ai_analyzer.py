import os
import json

from dotenv import load_dotenv
from google import genai


# Load the API key from .env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in the .env file")


# Create Gemini client
client = genai.Client(api_key=api_key)


def analyze_complaint(complaint_text):
    """
    Analyze a citizen complaint using Gemini AI.

    Returns:
        category
        priority
        department
        summary
    """

    prompt = f"""
You are an AI system that analyzes public complaints submitted by citizens.

Analyze this complaint:

"{complaint_text}"

Choose ONE category from:

- Road
- Waste Management
- Water
- Electricity
- Drainage
- Public Safety
- Other

Choose ONE priority:

- Low
- Medium
- High
- Urgent

Choose the most suitable department from:

- Road Department
- Waste Management Department
- Water Department
- Electrical Department
- Drainage Department
- Public Safety Department
- General Administration Department

Also create a short summary of the complaint.

Return ONLY valid JSON in exactly this format:

{{
    "category": "Waste Management",
    "priority": "High",
    "department": "Waste Management Department",
    "summary": "Short summary here"
}}

Do not add markdown.
Do not add explanations outside the JSON.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    result = response.text.strip()

    # Remove markdown code fences if Gemini happens to return them
    if result.startswith("```"):
        result = result.replace("```json", "")
        result = result.replace("```", "")
        result = result.strip()

    try:
        return json.loads(result)

    except json.JSONDecodeError:
        print("Gemini returned:")
        print(result)
        raise ValueError("Gemini returned invalid JSON")