# Purchase Summary - calculates and ranks customer spending by purchase amount
# Author: Marian Sator

transactions = [
    {"customer": "Marian", "amount": 100, "type": "purchase"},
    {"customer": "Anna", "amount": 200, "type": "refund"},
    {"customer": "Marian", "amount": 50, "type": "purchase"},
    {"customer": "Bob", "amount": 150, "type": "purchase"},
    {"customer": "Anna", "amount": 75, "type": "purchase"},
]

def get_purchase_summary(transactions):
    result = {}
    
    for entry in transactions:
        if entry["type"] == "purchase":
            result[entry["customer"]] = result.get(entry["customer"], 0) + entry["amount"]
            
    sorted_result = sorted(result.items(), key = lambda entry: entry[1], reverse = True)
            
    return result, sorted_result
    
    
result, sorted_result = get_purchase_summary(transactions)

# Lookup Marian:
total = result.get("Marian", 0)
print(f"Marian spent {total}€")

# Ranking:
for customer, total in sorted_result:
    print(f"{customer} spent {total}€")
