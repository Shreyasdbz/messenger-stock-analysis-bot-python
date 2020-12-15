import os
import json
from dotenv import load_dotenv
from . import SessionGenerator
import fbchat
# print("------------- Starting FB Chat API -------------")

load_dotenv()

fb_user_name = os.getenv('FB_USER_NAME')
fb_password = os.getenv('FB_PASSWORD')

# Start a session
# Code from https://github.com/xaadu --------------
# Including the Session Generator class
# session = SessionGenerator.SessionGenerator(fb_user_name, fb_password).getSession()
# print(session)
# with open('session.json', 'w') as f:
#     f.write(json.dumps(session))
# ---------------------------------- --------------

client = fbchat.Client(fb_user_name, fb_password)

