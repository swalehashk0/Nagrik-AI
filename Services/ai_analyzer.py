import os
import json

from dotenv import load_dotenv
from google import genai


# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in the .env file")


# Initialize Gemini client
client = genai.Client(api_key=api_key)


def analyze_complaint(complaint_text):
    """
    Analyze a citizen complaint using Gemini AI.

    Returns:
        category
        priority
        department
        summary
        confidence
    """

    if not complaint_text or not complaint_text.strip():
        raise ValueError("Complaint text cannot be empty")

    prompt = f"""
You are an AI system that analyzes public complaints submitted by citizens.

Analyze the following complaint:

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

Also create a short, factual summary of the complaint.
Also extract the location mentioned in the complaint.
If no specific location is mentioned, return "Not specified".
Also suggest one short, practical action that the responsible department
could take to address this complaint.
Also provide a confidence score between 0 and 1 representing your confidence
in the overall classification.
Also provide a short reason explaining why the selected priority
level is appropriate for this complaint.

Confidence guidelines:

- 0.90 to 1.00 = very clear complaint
- 0.75 to 0.89 = reasonably clear complaint
- 0.50 to 0.74 = somewhat ambiguous complaint
- below 0.50 = highly ambiguous complaint

Important:
Confidence represents how certain the AI is about its classification.
It does NOT represent the seriousness of the complaint.

Return ONLY valid JSON in exactly this format:

{{
    "category": "Waste Management",
    "priority": "High",
    "department": "Waste Management Department",
    "summary": "Short summary here",
    "confidence": 0.94,
    "urgency_reason": "Short reason for the selected priority",
    "location": "MG Road, Pune",
    "suggested_action": "Short practical action here"
}}

The confidence value must be a number between 0 and 1.

Do not add markdown.
Do not add explanations outside the JSON.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        result = response.text.strip()
        

    except Exception as e:
        raise RuntimeError(f"AI analysis failed: {e}")


    # Remove markdown code fences if Gemini happens to return them
    if result.startswith("```"):
        result = result.replace("```json", "")
        result = result.replace("```", "")
        result = result.strip()


    # Convert JSON text into Python dictionary
    try:
        result = json.loads(result)

    except json.JSONDecodeError:
        print("Gemini returned:")
        print(result)
        raise ValueError("Gemini returned invalid JSON")


    # Validate required fields
    required_fields = {
        "category",
        "priority",
        "department",
        "summary",
        "confidence",
        "urgency_reason",
        "location",
        "suggested_action",
    }

    missing_fields = required_fields - result.keys()

    if missing_fields:
        raise ValueError(
            f"AI response is missing required fields: {missing_fields}"
        )


    # Allowed categories
    allowed_categories = {
        "Road",
        "Waste Management",
        "Water",
        "Electricity",
        "Drainage",
        "Public Safety",
        "Other"
    }


    # Allowed priorities
    allowed_priorities = {
        "Low",
        "Medium",
        "High",
        "Urgent"
    }


    # Allowed departments
    allowed_departments = {
        "Road Department",
        "Waste Management Department",
        "Water Department",
        "Electrical Department",
        "Drainage Department",
        "Public Safety Department",
        "General Administration Department"
    }


    # Validate category
    if result["category"] not in allowed_categories:
        raise ValueError("Invalid category returned by AI")


    # Validate priority
    if result["priority"] not in allowed_priorities:
        raise ValueError("Invalid priority returned by AI")


    # Validate department
    if result["department"] not in allowed_departments:
        raise ValueError("Invalid department returned by AI")


    # Validate confidence score
    confidence = result.get("confidence")

    if not isinstance(confidence, (int, float)):
        raise ValueError("Invalid confidence score returned by AI")

    if not 0 <= confidence <= 1:
        raise ValueError("Confidence score must be between 0 and 1")


    return result