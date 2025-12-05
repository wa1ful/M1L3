import telebot
from config import token

bot = telebot.TeleBot(token) 

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я бот для управления чатом. Баню за ссылки и нецензурную лексику!")

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status
        
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно забанить администратора.")
        else:
            bot.ban_chat_member(chat_id, user_id)
            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был забанен.")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите забанить.")

@bot.message_handler(content_types=['new_chat_members'])
def make_some(message):
    bot.send_message(message.chat.id, 'I accepted a new user!')
    bot.approve_chat_join_request(message.chat.id, message.from_user.id)

@bot.message_handler(func=lambda message: True)
def check_messages(message):
    if message.from_user.is_bot:
        return
        
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    try:
        user_status = bot.get_chat_member(chat_id, user_id).status
        if user_status in ['administrator', 'creator']:
            return
    except:
        return
    
    # Проверка на ссылки
    if message.text and "https://" in message.text:
        bot.ban_chat_member(chat_id, user_id)
        bot.reply_to(message, f"Пользователь @{message.from_user.username} забанен за отправку ссылки!")

bot.infinity_polling(none_stop=True)