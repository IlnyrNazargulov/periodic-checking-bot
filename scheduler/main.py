import asyncio
import logging.config
import os

import psycopg2
import requests
from telebot.async_telebot import AsyncTeleBot

logger = logging.getLogger(__name__)
bot = AsyncTeleBot(os.getenv('BOT_TOKEN'))


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


async def make_request_and_send_result():
    logger.info("Start request to service.")
    response = requests.get(os.getenv('SERVICE_URL'))
    response.raise_for_status()
    data = response.json()
    appointments = data["result"]["specialities"][0]["doctors"][0]["appointments"]
    if len(appointments) != 0:  # sending condition
        for chat_id in get_all_chat_ids():
            await bot.send_message(chat_id, "There is a free place for an appointment with a doctor.")


async def schedule_task():
    logger.info("Start schedule task.")
    while True:
        await make_request_and_send_result()
        await asyncio.sleep(300)


async def create_task():
    asyncio.create_task(schedule_task())
    while True:
        await asyncio.sleep(1)


if __name__ == '__main__':
    logger.info("Start service.")
    asyncio.run(create_task())
    logger.info("Shutdown service.")
