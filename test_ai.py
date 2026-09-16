from Services.ai_analyzer import analyze_complaint


complaint = """
There has been garbage piling up near our apartment
for the last five days. Nobody has collected it.
It is creating a very bad smell and attracting stray animals.
"""


print("Analyzing complaint...")

result = analyze_complaint(complaint)


print("\nAI ANALYSIS")
print("--------------------")

print("Category:", result["category"])
print("Priority:", result["priority"])
print("Department:", result["department"])
print("Summary:", result["summary"])