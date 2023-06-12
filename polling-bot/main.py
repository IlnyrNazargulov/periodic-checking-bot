import asyncio
import logging.config
import os

import psycopg2
from psycopg2 import errors
from psycopg2.errorcodes import UNIQUE_VIOLATION
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


def write_to_db(chat_id, username):
    connection = connect_to_db()
    cursor = connection.cursor()
    insert_query = "INSERT INTO chats (chat_id, username) VALUES (%s, %s)"
    cursor.execute(insert_query, (chat_id, username))
    connection.commit()
    cursor.close()
    connection.close()


@bot.message_handler(commands=['start'])
async def create_chat(message):
    logger.info("Handle new start message.")
    try:
        chat_id = message.chat.id
        username = message.from_user.username
        logger.info("Message from chat %s.", chat_id)
        write_to_db(chat_id, username)
        await bot.reply_to(message, "You are now receiving responses from the scheduler.")
    except errors.lookup(UNIQUE_VIOLATION):
        logger.info("Chat already exists.")
        await bot.reply_to(message, "You are already enrolled in the planner.")


if __name__ == '__main__':
    logger.info("Start service.")
    asyncio.run(bot.polling())
    logger.info("Shutdown service.")
