from Services.ai_analyzer import analyze_complaint

complaint = """
There is a large pothole on the main road near our school.
It is causing difficulty for vehicles and could lead to accidents.
"""

print("Analyzing complaint...")

result = analyze_complaint(complaint)

print("\nAI ANALYSIS")
print("--------------------")
print("Category:", result["category"])
print("Priority:", result["priority"])
print("Department:", result["department"])
print("Summary:", result["summary"])


print("Confidence:", result["confidence"])
print("Urgency Reason:", result["urgency_reason"])
print("Location:", result["location"])
print("Suggested Action:", result["suggested_action"])