from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, LinkPreviewOptions
import app.keyboards as kb
from app.keyboards import main, admin_kb, feedbacky, us_kb
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import json
import os
from dotenv import load_dotenv

# Need for feedback check
alredy_used = "already.json"

async def saver():
    if not os.path.exists(alredy_used) or os.path.getsize(alredy_used) == 0:
        with open(alredy_used, "w") as file:
            json.dump({"usrs": []}, file)
        
    try:
        with open(alredy_used, "r") as f:
            data = json.load(f)
            return data.get("usrs", [])
    except (json.JSONDecodeError, KeyError):
        return []

load_dotenv()

ADMIN_ID = os.getenv("ADMIN_ID")

admin_id = ADMIN_ID=ADMIN_ID
router = Router()

already_voted = None

already_voted = set()

# For support part
class user_message(StatesGroup):
    contex = State()

# For feedback
class user_fb(StatesGroup):
    fb_cont = State()

# Admin class
class admin(StatesGroup):
    admin_context = State()

# /start
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply(f"Welcome, {message.from_user.username}!\nHow we can help you",  
                        reply_markup=kb.main)

# just auto-response on your phrase
@router.message(F.text == 'your pharse')
async def howyou(message: Message):
    await message.reply("Response")

# Button "Information"
@router.callback_query(F.data == 'information')
async def catalog(callback: CallbackQuery):
    await callback.message.answer("Select action:", reply_markup=await kb.infor())

# Support (write user message)
@router.callback_query(F.data == 'support')
async def sup(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Support Text",
    parse_mode="Markdown",
    link_preview_options=LinkPreviewOptions(is_disabled=True)
    )
    await state.set_state(user_message.contex)
    await callback.answer()

# Support (send user message to admin)
@router.message(user_message.contex)
async def send_admin(message: Message, state: FSMContext):
    await message.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"New message from:\nID: {message.from_user.id}\nUsername: {message.from_user.username}; Name: {message.from_user.first_name}\nContent:\n\n{message.text}",
        reply_markup=admin_kb(message.from_user.id)),
    await message.answer("Send to admin! Wait!")
    await state.clear()
    await message.answer("Select action:", reply_markup=main)

# Feedback (collect message)
@router.callback_query(F.data == 'feedback')
async def fedbak(callback: CallbackQuery, state: FSMContext):
    if not os.path.exists(alredy_used) or os.path.getsize(alredy_used) == 0:
        with open(alredy_used, "w") as f:
            json.dump({"usrs": []}, f)
        already_voted = []
    else:
        try:
            with open(alredy_used, "r") as file:
                data = json.load(file)
                already_voted = data.get("usrs", [])
        except json.JSONDecodeError:
            already_voted = []
        print("ID`s is loaded")

    if callback.from_user.id in already_voted:
        await callback.answer("You already left! Thanks!")
        return
    await callback.message.answer("What you think about us?")
    await state.set_state(user_fb.fb_cont)

# Feedback (select variant of send)
@router.message(user_fb.fb_cont)
async def send_fb(message: Message, state: FSMContext):
    await state.update_data(fb_text=message.text)
    await message.answer("How send your review?", reply_markup=feedbacky)

# Anonymously
@router.callback_query(F.data == "anon")
async def send_anon_fb(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text1 = data.get("fb_text")
    try:
        await callback.bot.send_message(
            # Warning! Put here your own channel (or your user) ID
            chat_id=admin_id,
            text=f"New anonimous feedback!\nContent:\n\n{text1}"
            )
        already_voted.add(callback.from_user.id)
    except Exception as e:
        print(f"Error in send {e}")
        await callback.answer("Error!")
    await callback.message.edit_text("Select action:", reply_markup=main)
    await callback.answer("Send anonymously")
    voted = await saver()
    if callback.from_user.id not in voted:
        voted.append(callback.from_user.id)
        with open(alredy_used, "w") as file:
            json.dump({"usrs": voted}, file, indent=4)
            print(f"ID {callback.from_user.id} is successfully saved!")
    await state.clear()

# Not anonymously
    
@router.callback_query(F.data == "nonanon")
async def send_anon_fb(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    text1 = data.get("fb_text")
    try:
        await callback.bot.send_message(
            # Warning! Put here your own channel (or your user) ID
            chat_id=admin_id,
            text=f"New feedback from: {callback.from_user.first_name}!\nContent:\n\n{text1}"
            )
        already_voted.add(callback.from_user.id)
    except Exception as e:
        print(f"Error in send {e}")
        await callback.answer("Error!")
    await callback.message.edit_text("Select action:", reply_markup=main)
    await callback.answer("Send! Thanks!")
    # Save ID after review on already.json
    voted = await saver()
    if callback.from_user.id not in voted:
        voted.append(callback.from_user.id)
        with open(alredy_used, "w") as file:
            json.dump({"usrs": voted}, file, indent=4)
    print(f"ID {callback.from_user.id} is successfully saved!")
    await state.clear()

# Response of admin (support)
@router.callback_query(F.data.startswith("reply_"))
async def admin_reply(callback: CallbackQuery, state: FSMContext):
    user_id = int(callback.data.split("_")[1])
    await state.update_data(target_user_id=user_id)
    await callback.message.answer(f"Answer to {user_id}:")
    await state.set_state(admin.admin_context)
    await callback.answer()

# Response of admin (support (send answer to user))
@router.message(admin.admin_context)
async def for_user(message: Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get("target_user_id")
    await message.bot.send_message(chat_id=user_id, text=f"Response of your appeal:\n\n{message.text}")
    await message.answer("Answer send!")
    await state.clear()

# About
@router.callback_query(F.data == 'about')
async def catalog(callback: CallbackQuery):
    await callback.message.edit_text("Here can be your text",
        reply_markup=us_kb())

# Text 1
@router.callback_query(F.data == 'button1')
async def catalog(callback: CallbackQuery):
    await callback.message.edit_text("Text",
        reply_markup=us_kb())

# Text 2
@router.callback_query(F.data == 'button2')
async def catalog(callback: CallbackQuery):
    await callback.message.edit_text("Text2",
        reply_markup=us_kb())

# Go back to menu
@router.callback_query(F.data == 'go_main')
async def catalog(callback: CallbackQuery):
    await callback.message.edit_text("Select action:", reply_markup=main)
    await callback.answer()

# /help
@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer("How we can help you?")

# /status (can delete)

@router.message(Command('status'))
async def get_help(message: Message):
    await message.answer("Bot already work!")
