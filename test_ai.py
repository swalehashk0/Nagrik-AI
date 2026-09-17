from Services.ai_analyzer import analyze_complaint

complaint = """
There is a strange problem in our neighborhood and residents are unsure
who is responsible for fixing it. It has been causing inconvenience for
the past few days, but the exact cause of the problem is not known.
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