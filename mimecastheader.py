import os
from dotenv import load_dotenv
import datetime
import hashlib
import hmac
import base64

# Mimecast API credentials
load_dotenv()
mimecast_api_key = os.getenv('MIMECAST_API_KEY')
mimecast_secret_key = os.getenv('MIMECAST_SECRET_KEY')
mimecast_domain = os.getenv('MIMECAST_DOMAIN')
ACCESS_KEY = mimecast_api_key
SECRET_KEY = mimecast_secret_key
APP_ID = mimecast_api_key
APP_KEY = mimecast_secret_key

# Generate required headers
request_id = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
date_str = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S UTC")

secret_bytes = base64.b64decode(SECRET_KEY)
data_to_sign = f"{date_str}:{request_id}".encode('utf-8')
signature = hmac.new(secret_bytes, data_to_sign, digestmod=hashlib.sha1).digest()
signature_b64 = base64.b64encode(signature).decode()

print("x-mc-date:", date_str)
print("x-mc-req-id:", request_id)
print("Authorization:", f"MC {ACCESS_KEY}:{signature_b64}")
