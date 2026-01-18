from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, 
                           InlineKeyboardButton, InlineKeyboardMarkup)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Information', callback_data='information')],
    [InlineKeyboardButton(text='Support', callback_data='support')],
    [InlineKeyboardButton(text='Feedback', callback_data='feedback')],
    [InlineKeyboardButton(text='Donate', callback_data='donate')],
])

feedbacky = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Send anonymously', callback_data='anon')],
    [InlineKeyboardButton(text='Send with your username', callback_data='nonanon')],
])

async def infor():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='Button 1', callback_data='button1')),
    builder.row(InlineKeyboardButton(text='About us', callback_data='about')),
    builder.row(InlineKeyboardButton(text='Button 2', callback_data='button2')),
    builder.row(InlineKeyboardButton(text='Go back', callback_data='go_main'))
    return builder.as_markup()

def us_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Go back to information", callback_data='information')]
    ])

def admin_kb(user_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Response", callback_data=f"reply_{user_id}")]
    ])
