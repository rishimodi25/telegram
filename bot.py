from telethon import TelegramClient
import schedule
import asyncio
import time

api_id = 123729016
api_hash = "fdd914d1be8d30e6aed32dc98cf79f5b"

source_chat = "https://t.me/freecourseez"
target_channel = "https://t.me/freecourseez"

client = TelegramClient("userbot", api_id, api_hash)


async def resend_messages():
    async with client:
        messages = await client.get_messages(source_chat, limit=5)

        for msg in reversed(messages):
            if msg.text:
                await client.send_message(target_channel, msg.text)


def job():
    asyncio.run(resend_messages())


# Schedule times
schedule.every().day.at("09:00").do(job)
schedule.every().day.at("13:00").do(job)
schedule.every().day.at("17:00").do(job)


print("Userbot started...")

while True:
    schedule.run_pending()
    time.sleep(30)
