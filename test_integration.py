from Services.ai_analyzer import analyze_complaint

complaint = """
There is a large pothole on the main road near our college.
It is making it difficult for vehicles and students to travel safely.
"""

result = analyze_complaint(complaint)

print("AI integration test successful!")
print()
print("Category:", result["category"])
print("Priority:", result["priority"])
print("Department:", result["department"])
print("Summary:", result["summary"])
print("Confidence:", result["confidence"])
print("Urgency Reason:", result["urgency_reason"])
print("Location:", result["location"])
print("Suggested Action:", result["suggested_action"])