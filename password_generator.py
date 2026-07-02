# Password Generator - generates secure passwords with customizable character sets
# Author: Marian Sator

import random 
import string

def generate_password(length=16, use_lowercase=True, use_uppercase=True, use_digits=True, use_special=True):
    
    if not isinstance(length, int):
        raise TypeError("Length must be an integer.")
    
    if length < 8:
        raise ValueError("Password must be at least 8 characters.")
        
    chars = "" 
    chars += string.ascii_lowercase if use_lowercase else "" 
    chars += string.ascii_uppercase if use_uppercase else "" 
    chars += string.digits if use_digits else "" 
    chars += string.punctuation if use_special else "" 
    
    if len(chars) == 0:
        raise ValueError("At least one character set must be enabled.")
    
    password = ""
    
    for _ in range(length):
        password = password + random.choice(chars)
        
    return password 
    
# Example usage
print(generate_password())
print(generate_password(length = 16, use_special=False))
print(generate_password(length = 32, use_uppercase=False, use_digits=False))
