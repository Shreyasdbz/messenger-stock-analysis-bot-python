import os
import json
from dotenv import load_dotenv
from fbchat import Client
# from fbchat.models import *

print("Starting FB Chat API -------------")

load_dotenv()

fb_user_name = os.getenv('FB_USER_NAME')
fb_password = os.getenv('FB_PASSWORD')


