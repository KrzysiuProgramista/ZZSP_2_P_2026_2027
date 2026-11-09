# Calculate shipping cost for a positive package weight: up to 1 kg costs 5; over 1 kg and up to 5 kg costs 8; over 5 kg costs 12.
def shipping_cost(weight):
    if weight > 5:
        cost = 12
    elif weight > 1:
        cost = 8
    else:
        cost = 5
    return cost
 
print(shipping_cost(6)) #12
print(shipping_cost(5)) #8
print(shipping_cost(2)) #8
print(shipping_cost(1)) #5
print(shipping_cost(0.5)) #5

# Symptom: The 6kg case returns 8
# Cause: Each if statement is checked independently one after another
# Fix: Change the second if to elif
# 6 returns 12
# 5 returns 8
# 1 returns 5
# 0.5 returns 5