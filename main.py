import telebot
from telebot.types import Message 
from model import get_class

bot = telebot.TeleBot('7310900197:AAFCpSi9BSp4XloiGylHzBZNRu5Qv5R16wo')

@bot.message_handler(commands=['start'])
def start_cmd(message: Message):
    bot.send_message(message.chat.id, 'Привет! Этот бот поможет отличить дипфейк от оригинального произведения искусства')

@bot.message_handler(content_types=['photo'])
def photo_cmd(message: Message):
    if not message.photo:
        bot.send_message(message.chat.id, 'Вы не отправили фото')
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    file_name = f"{message.chat.id}.png"
    downloaded_file = bot.download_file(file_info.file_path)
    print('photo_cmd')
    with open(file_name, 'wb') as file:
        file.write(downloaded_file)
    result = get_class(model_path="./keras_model.h5", labels_path="labels.txt", image_path=file_name)
    bot.send_message(message.chat.id, 'Изображение успешно принято в обработку, пожалуйста, ожидайте..')
    print(result)

bot.polling()