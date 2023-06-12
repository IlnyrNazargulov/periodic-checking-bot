import asyncio
import logging

import psycopg2
import requests
from telebot.async_telebot import AsyncTeleBot

from config import SERVICE_URL, BOT_TOKEN

bot = AsyncTeleBot(BOT_TOKEN)

root = logging.getLogger()
root.setLevel(logging.INFO)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def connect_to_db():
    connection = psycopg2.connect(
        user="telegrambot",
        password="telegrambot",
        host="db",
        port="5432",
        database="telegrambot"
    )
    return connection


def get_all_chat_ids():
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute('SELECT chat_id FROM chats')
    records = [r[0] for r in cursor.fetchall()]
    cursor.close()
    connection.close()
    return records


def write_to_db(chat_id, username):
    connection = connect_to_db()
    cursor = connection.cursor()
    insert_query = "INSERT INTO chats (chat_id, username) VALUES (%s, %s)"
    cursor.execute(insert_query, (chat_id, username))
    connection.commit()
    cursor.close()
    connection.close()


async def make_request_and_send_result():
    logger.info("Start request to service.")
    response = requests.get(SERVICE_URL)
    response.raise_for_status()
    data = response.json()
    appointments = data["result"]["specialities"][0]["doctors"][0]["appointments"]
    # if len(appointments) != 0:
    for chat_id in get_all_chat_ids():
        await bot.send_message(chat_id, "There is a free place for an appointment with a doctor.")


async def schedule_task():
    logger.info("Start schedule task.")
    while True:
        await make_request_and_send_result()
        await asyncio.sleep(10)


async def create_task():
    asyncio.create_task(schedule_task())
    while True:
        await asyncio.sleep(1)


if __name__ == '__main__':
    logger.info("Start service.")
    asyncio.run(create_task())
    logger.info("Shutdown service.")
