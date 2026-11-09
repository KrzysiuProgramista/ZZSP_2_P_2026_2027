def emergency_contact(person):
    try:
        return person["contact"]["name"]
    except KeyError:
        return "Not provided"
 
print(emergency_contact({"name": "Sam"}))
print(emergency_contact({"contact": {"name": "Alex"}}))
print(emergency_contact({"contact": {}}))

# Symptom: Program crashes with KeyError
# Cause: Direct dictionary access assumes all keys exist.
# Tests: emergency_contact({"name": "Sam"}) returns Not provided
# emergency_contact({"contact": {"name": "Alex"}}) returns Alex
# emergency_contact({"contact": {}}) returns Not provided