from telethon import TelegramClient, events, functions, types, errors, Button
from telethon.tl.types import Channel, Chat, User
from telethon.tl.functions.users import GetFullUserRequest
from dotenv import load_dotenv
import subprocess, os, asyncio

load_dotenv(dotenv_path=os.getenv('DOTENV_FILE_PATH'))

APP_ID = os.getenv('private_app_id')
APP_HASH = os.getenv('private_app_hash')
TG_BOT_TOKEN = os.getenv('tg_wtbot_token')
TG_BOT_SESSION = os.getenv('tg_wtbot_session')
TG_USER_ID = os.getenv('tg_user_id')
WT_PATH = os.getenv('wt_path')

client = TelegramClient(TG_BOT_SESSION, APP_ID, APP_HASH)

SCRIPT_MAP = {
    b"script1": WT_PATH + ' ir',
    b"script2": WT_PATH + ' kv',
    b"script3": WT_PATH + ' ir d',
    b"script4": WT_PATH + ' kv d',
    b"script5": WT_PATH + ' ir w',
    b"script6": WT_PATH + ' kv w',
}

@client.on(events.NewMessage(pattern='/start', from_users=int(TG_USER_ID)))
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
    command = 'python ' + SCRIPT_MAP.get(event.data)
    answer = subprocess.run(command, shell=True, capture_output=True, text=True).stdout.strip()
    message = await client.send_message(int(TG_USER_ID), answer)
    await asyncio.sleep(20)
    await client.delete_messages(event.chat_id, message.id)

async def main():
    await client.start(bot_token=TG_BOT_TOKEN)
    await client.run_until_disconnected()

asyncio.run(main())
