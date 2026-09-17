from Services.ai_analyzer import analyze_complaint

complaint = """
There has been no water supply in our building since yesterday.
Residents are unable to get enough water for their basic needs.
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