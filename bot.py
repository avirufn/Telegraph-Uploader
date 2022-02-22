import os
from telegraph import upload_file
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

semsy = Client(
   "SWTelegraph",
   api_id=API_ID,
   api_hash=API_HASH,
   bot_token=BOT_TOKEN)


@semsy.on_message(filters.command(["start"]))
async def home(client, message):
  buttons = [[
        InlineKeyboardButton('Help', callback_data='help')
    ],
    [
        InlineKeyboardButton('Our Channel', url='https://t.me/swbots'),
        InlineKeyboardButton('Groups', url='https://t.me/semsychat')
    ]]
  reply_markup = InlineKeyboardMarkup(buttons)
  await semsy.send_message(
        chat_id=message.chat.id,
        text=f""" Hello dear,
I'm Telegraph Uploader bot, you can upload any file telegraph with me.

Made by @swbots
        """,
        reply_markup=reply_markup,
        reply_to_message_id=message.message_id)

@semsy.on_message(filters.command(["help"]))
async def help(client, message):
  buttons = [[
        InlineKeyboardButton('Back', callback_data='home')
    ]]
  reply_markup = InlineKeyboardMarkup(buttons)
  await semsy.send_message(
        chat_id=message.chat.id,
        text="""       
Just Send Me A Video/gif/photo Upto 5mb.
I'll upload it to telegraph and give you the direct link""",
        reply_markup=reply_markup,
        parse_mode="html",
        reply_to_message_id=message.message_id
    ) 

@semsy.on_message(filters.photo)
async def uploadphoto(client, message):
  msg = await message.reply_text("Downloading...")
  userid = str(message.chat.id)
  img_path = (f"./DOWNLOADS/{userid}.jpg")
  img_path = await client.download_media(message=message, file_name=img_path)
  await msg.edit_text("Uploading...")
  try:
    tlink = upload_file(img_path)
  except:
    await msg.edit_text("Something went wrong") 
  else:
    await msg.edit_text(f"https://telegra.ph{tlink[0]}")     
    os.remove(img_path) 

@semsy.on_message(filters.animation)
async def uploadgif(client, message):
  if(message.animation.file_size < 5242880):
    msg = await message.reply_text("Downloading...")
    userid = str(message.chat.id)
    gif_path = (f"./DOWNLOADS/{userid}.mp4")
    gif_path = await client.download_media(message=message, file_name=gif_path)
    await msg.edit_text("Uploading...")
    try:
      tlink = upload_file(gif_path)
      await msg.edit_text(f"https://telegra.ph{tlink[0]}")   
      os.remove(gif_path)   
    except:
      await msg.edit_text("Something really Happend Wrong...") 
  else:
    await message.reply_text("Size Should Be Less Than 5 mb")

@semsy.on_message(filters.video)
async def uploadvid(client, message):
  if(message.video.file_size < 5242880):
    msg = await message.reply_text("Downloading...")
    userid = str(message.chat.id)
    vid_path = (f"./DOWNLOADS/{userid}.mp4")
    vid_path = await client.download_media(message=message, file_name=vid_path)
    await msg.edit_text("Uploading...")
    try:
      tlink = upload_file(vid_path)
      await msg.edit_text(f"https://telegra.ph{tlink[0]}")     
      os.remove(vid_path)   
    except:
      await msg.edit_text("Something really Happend Wrong...") 
  else:
    await message.reply_text("Size Should Be Less Than 5 mb")
                          
@semsy.on_callback_query()
async def button(semsy, update):
      cb_data = update.data
      if "help" in cb_data:
        await update.message.delete()
        await help(semsy, update.message)
      elif "close" in cb_data:
        await update.message.delete() 
      elif "home" in cb_data:
        await update.message.delete()
        await home(semsy, update.message)

semsy.run()
