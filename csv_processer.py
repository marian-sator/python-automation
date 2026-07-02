# CSV Processor - validates and processes CSV data with error reporting
# Author: Marian Sator

import csv
import io 
import time

data = """name,email,age,type
  Marian ,MARIAN@GMAIL.COM,35,customer
Anna,anna@gmail.com,,employee
BOB,bob@gmail.com,42,customer
  Clara  ,CLARA@GMAIL.COM,28,customer
David,invalid-email,31,customer
Eva,eva@gmail.com,17,
"""

def process_data(data):
    
    if not isinstance(data, str):
        raise ValueError("data must be a string value.")
    
    if len(data) == 0:
        raise ValueError("data must not be an empty string.")
        
    start = time.time()

    reader = csv.DictReader(io.StringIO(data))
     
    processed = {}

    for row in reader:
        
        # strip and lowercase to normalize inconsistent input data
        customer_name = row["name"].strip().lower()
        customer_email = row["email"].strip().lower()
        customer_age = row["age"].strip()
        customer_type = row["type"].strip()
        
        if not customer_name:
            continue 
            
        # dictionary lookup to detect duplicates in O(1)
        if processed.get(customer_name, False):
            print(f"{customer_name} - INVALID - multiple entries.")
            continue
            
        if not customer_email:
            print(f"{customer_name} - INVALID - email missing.")
            continue 
        
        # basic email validation
        if "@" not in customer_email:
            print(f"{customer_name} - INVALID - invalid email.")
            continue
        
        if not customer_age:
            print(f"{customer_name} - INVALID - age missing.")
            continue
        
        # age restriction check
        if int(customer_age) < 18:
            print(f"{customer_name} - INVALID - under 18.")
            continue
            
        if not customer_type:
            print(f"{customer_name} - INVALID - type missing.")
            continue     
            
        processed[customer_name] = {
            "email": customer_email,
            "age": int(customer_age),
            "type": customer_type
        }
        
    processing_time = (time.time() - start) * 1000

    return processed, processing_time
    
# Example usage 
processed, processing_time = process_data(data)

print(f"Processing took {processing_time:.2f}ms.")
print(f"Valid entries: {len(processed)}.")
for name, details in processed.items():
    print(f"{name}: {details['email']}, {details['age']}, {details['type']}")
