# © BugHunterCodeLabs ™
# © bughunter0
# 2021
# Copyright - https://en.m.wikipedia.org/wiki/Fair_use

import os , glob
from os import error
import logging
import pyrogram
import time
import math
from decouple import config
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.types import User, Message, Sticker, Document

    
bughunter0 = Client(
    "Sticker-Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)

START_STRING = """ Hi {}, I'm Sticker Bot. 

I can Provide all Kind of Sticker Options Here """


JOIN_BUTTON = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('↗ Join Here ↗', url='https://t.me/BughunterBots')
        ]]
    )

DOWNLOAD_LOCATION = os.environ.get("DOWNLOAD_LOCATION", "./DOWNLOADS/")
FINISHED_PROGRESS_STR = "█"
UN_FINISHED_PROGRESS_STR = "░"

@bughunter0.on_message(filters.command(["start"]))
async def start(bot, update):
    text = START_STRING.format(update.from_user.mention)
    reply_markup = JOIN_BUTTON
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup,
        quote=True
    )

@bughunter0.on_message(filters.command(["ping"]))
async def ping(bot, message):
    start_t = time.time()
    rm = await message.reply_text("Checking")
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await rm.edit(f"Pong!\n{time_taken_s:.3f} ms")


@bughunter0.on_message(filters.private & filters.command(["getsticker"]))
async def getsticker(bot, message):  
    tx = await message.reply_text("Checking Sticker")
    await tx.edit("Validating sticker..")
    await tx.delete()
    if message.reply_to_message is None: 
            tx =  await tx.edit("Reply to a Sticker File!")       
    else :
          if message.reply_to_message.sticker.is_animated:
             try :
                   tx = await message.reply_text("Downloading...")
                   file_path = DOWNLOAD_LOCATION + f"{message.chat.id}.tgs"
                   await message.reply_to_message.download(file_path,progress=progress_for_pyrogram)  
                   await tx.edit("Downloaded") 
                #   zip_path= ZipFile.write("")
                   await tx.edit("Uploading...")
                   await message.reply_document(file_path,caption="©@BugHunterBots",progress=progress_for_pyrogram)
                   await tx.delete()   
                   os.remove(file_path)
                #   os.remove(zip_path)
             except Exception as error:
                   print(error)
 
          elif message.reply_to_message.sticker.is_animated is False:        
             try : 
                   tx = await message.reply_text("Downloading...")
                   file_path = DOWNLOAD_LOCATION + f"{message.chat.id}.png"
                   await message.reply_to_message.download(file_path,progress=progress_for_pyrogram)   
                   await tx.edit("Downloaded")
                   await tx.edit("Uploading...")
                   await message.reply_document(file_path,caption="©@BugHunterBots",progress=progress_for_pyrogram)
                   await tx.delete()   
                   os.remove(file_path)
             except Exception as error:
                   print(error)

@bughunter0.on_message(filters.private & filters.command(["clearcache"]))
async def clearcache(bot, message):   
    # Found some Files showing error while Uploading, So a method to Remove it !!  
    txt = await message.reply_text("Checking Cache")
    await txt.edit("Clearing cache")
    dir = DOWNLOAD_LOCATION
    filelist = glob.glob(os.path.join(dir, "*"))
    for f in filelist:
           i =1
           txt = await txt.edit("Clearing " + i + "File")
           os.remove(f)
           i=i+1
           await txt.edit("Cleared "+ i + "File") 
    await txt.edit("Successfully Cleared")
    await txt.delete()
    
@bughunter0.on_message(filters.command(["stickerid"]))
async def stickerid(bot, message):   
    if message.reply_to_message.sticker:
       await message.reply(f"**Sticker ID is**  \n `{message.reply_to_message.sticker.file_id}` \n \n ** Unique ID is ** \n\n`{message.reply_to_message.sticker.file_unique_id}`", quote=True)
    else: 
       await message.reply("Oops !! Not a sticker file")



async def progress_for_pyrogram(current,total,ud_type,message,start):
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        # if round(current / total * 100, 0) % 5 == 0:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = TimeFormatter(milliseconds=elapsed_time)
        estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)

        progress = "[{0}{1}] \nP: {2}%\n".format(
            ''.join(
                
                    FINISHED_PROGRESS_STR for _ in range(
                        math.floor(percentage / 5)
                    )
                
            ),
            ''.join(
                
                    UN_FINISHED_PROGRESS_STR for _ in range(
                        20 - math.floor(percentage / 5)
                    )
                
            ),
            round(percentage, 2))

        tmp = progress + "{0} of {1}\nSpeed: {2}/s\nETA: {3}\n".format(
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),
            # elapsed_time if elapsed_time != '' else "0 s",
            estimated_total_time if estimated_total_time != '' else "0 s"
        )
        try:
            await message.edit(
                "{}\n {}".format(
                    ud_type,
                    tmp
                )
            )
        except:
            pass


def humanbytes(size):
    # https://stackoverflow.com/a/49361727/4723940
    # 2**10 = 1024
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s, ") if seconds else "") + \
        ((str(milliseconds) + "ms, ") if milliseconds else "")
    return tmp[:-2]

bughunter0.run()
