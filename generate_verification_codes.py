import pymongo
import os
from dotenv import load_dotenv
import secrets
import string

# Fetch the MongoDB URI from environment variables
load_dotenv()
mongo_url = os.getenv("MongoDB_URI")

client = pymongo.MongoClient(mongo_url)
db = client['traffic_logins']
verification_codes_collection = db['verification_codes']

def generate_complex_verification_code(length=16):
    # Define the character set including upper and lower case letters, digits, and special characters
    charset = string.ascii_uppercase + string.ascii_lowercase + string.digits + "!@#$%^&*()-_=+[]{}|;:,.<>?/~"
    
    # Use secrets.choice for cryptographically secure random selection
    return ''.join(secrets.choice(charset) for _ in range(length))

def generate_verification_codes_with_locations():
    locations = ['Mumbra', 'Taloja', 'Panvel']
    codes = []
    
    for location in locations:
        for _ in range(10):  
            code = generate_complex_verification_code()
            codes.append({'code': code, 'location': location})
    
    verification_codes_collection.insert_many(codes)
    print("Complex verification codes and locations have been stored.")

if __name__ == '__main__':
    generate_verification_codes_with_locations()
