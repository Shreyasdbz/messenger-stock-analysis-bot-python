import os
import json
from dotenv import load_dotenv
from fbchat import *

from src import stockBot

load_dotenv()
fb_user_name = os.getenv('FB_USER_NAME')
fb_password = os.getenv('FB_PASSWORD')
thread_shreyas = os.getenv('CHAT_SHREYAS_SANE')
group_moves = os.getenv('CHAT_MOVES')

KNOWN_THREADS = ['2992994787380239',    # $Moves
                '100000837841366',      # Shreyas
                '4065354120160807',     # StockBot Test
                ]

class CustomClient(Client):
    def onMessage(self, mid, author_id, message_object, thread_id, thread_type, ts, metadata, msg, **kwargs):
        msgText = msg['body']
        # Stockbot
        # Also, ignore self authorID
        if(('enas').lower() in msgText.lower() or '@StockBot' in msgText and author_id != 100055918816796):
            returnMsg = stockBot.processStockbotMsg(msg['body'])
            Client.sendMessage(self, message=returnMsg, thread_id=thread_id, thread_type=thread_type)
        else:
            pass

if __name__ == "__main__":
    load_dotenv()

    client = CustomClient(fb_user_name, fb_password)
    client.listen()
