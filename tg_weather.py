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
    script_name = 'python ' + SCRIPT_MAP.get(event.data)
    subprocess.run(script_name, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    with open(REPORT) as f:
        message = '\n'.join(f.read().split('\n')) 
    message = await client.send_message(int(TG_USER_ID), message)
    msg_ids.append(message.id)
    subprocess.run(f'rm {REPORT}', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

msg_ids = []

@client.on(events.NewMessage(pattern='/clear', from_users=int(TG_USER_ID)))
async def clear_handler(event):
    msg_ids.append(event.message.id)
    try:
        to_delete = msg_ids[:]
        msg_ids.clear()
        await client.delete_messages(event.chat_id, to_delete)
    except errors.MessageDeleteForbiddenError:
        await event.respond("Can't delete old messages!!!")
    except errors.RPCError as e:
        print(f"An error occurred: {e}")
        await event.respond(f"An error occurred: {e}")
        print(f"An error occurred: {e}")

async def main():
    await client.start(bot_token=TG_BOT_TOKEN)
    await client.run_until_disconnected()

asyncio.run(main())
