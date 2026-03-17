from telethon import TelegramClient, events, functions, types, errors, Button
from telethon.tl.types import Channel, Chat, User
from telethon.tl.functions.users import GetFullUserRequest
from dotenv import load_dotenv
import subprocess, os, asyncio

load_dotenv()

APP_ID = os.getenv('app_id')
APP_HASH = os.getenv('app_hash')
TG_BOT_TOKEN = os.getenv('tg_bot_token')
TG_BOT_SESSION = os.getenv('tg_bot_session')
AUTHORIZED_USER_ID = os.getenv('authorized_user_id')
WT_PATH = os.getenv('wt_path')
REPORT = os.getenv('report')

client = TelegramClient(TG_BOT_SESSION, APP_ID, APP_HASH)

SCRIPT_MAP = {
    b"script1": WT_PATH + ' ir',
    b"script2": WT_PATH + ' kv',
    b"script3": WT_PATH + ' ir d',
    b"script4": WT_PATH + ' kv d',
    b"script5": WT_PATH + ' ir w',
    b"script6": WT_PATH + ' kv w',
}

msg_ids = []

@client.on(events.NewMessage(pattern='/start', from_users=int(AUTHORIZED_USER_ID)))
async def start(event):
    await event.respond(
        "WEATHER FORECAST",
        buttons=[
            [Button.inline("HOME CURRENT", b"script1"),
            Button.inline("WORK CURRENT", b"script2")],
            [Button.inline("HOME DAILY", b"script3"),
            Button.inline("WORK DAILY", b"script4")],
            [Button.inline("HOME WEEKLY", b"script5"),
            Button.inline("WORK WEEKLY", b"script6")],
        ])

@client.on(events.CallbackQuery)
async def handler(event):
    script_name = 'python ' + SCRIPT_MAP.get(event.data)
    subprocess.run(script_name, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    with open(REPORT) as f:
        message = '\n'.join(f.read().split('\n')) 
    message = await client.send_message(int(AUTHORIZED_USER_ID), message)
    msg_ids.append(message.id)
    msg_ids.append(message.id+1)
    subprocess.run(f'rm {REPORT}', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


@client.on(events.NewMessage(pattern='/clear', from_users=int(AUTHORIZED_USER_ID)))
async def clear_handler(event):
    current_id = event.message.id
    chat = event.peer_id.user_id
    await client.delete_messages(chat, msg_ids)
    msg_ids.clear()

async def main():
    await client.start(bot_token=TG_BOT_TOKEN)
    await client.run_until_disconnected()

asyncio.run(main())

