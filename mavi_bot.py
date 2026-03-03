import os
import re
import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters
from openai import OpenAI

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8272504492:AAE4tfPmzNdsojMNAjs8Txj9Sk-HhzdthBs")

client = OpenAI()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging
