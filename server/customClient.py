import os
import json
from dotenv import load_dotenv
from fbchat import *

load_dotenv()
thread_shreyas = os.getenv('CHAT_SHREYAS_SANE')
group_moves = os.getenv('CHAT_MOVES')


class CustomClient(Client):
    def onMessage(self, mid, author_id, message_object, thread_id, thread_type, ts, metadata, msg, **kwargs):
        # Do something with message_object here
        print("Message from: {} of type {}".format(thread_id, thread_type))
        pass

