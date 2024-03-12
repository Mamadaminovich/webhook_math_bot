import telebot
from telebot import types
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import random

WEBHOOK_URL = 'https://a003-213-230-76-133.ngrok-free.app/webhook'
BOT_TOKEN = '6719577695:AAGtoIx7smO8T-fDsPHDgQ3AxDeNL1lzOSc'
bot = telebot.TeleBot(BOT_TOKEN)

total_points = 0
question_count = 0

def home(request):
    return HttpResponse('Salom dunyo')

@bot.message_handler(commands=['start'])
def start_game(message):
    bot.send_message(message.chat.id, "Assalomu Aleykum math bot ga xush kelibsiz!!!")
    ask_question(message)

def ask_question(message):
    global question_count
    global total_points
    if question_count < 5:
        question, answer = generate_question()
        bot.send_message(message.chat.id, question)
        bot.register_next_step_handler(message, lambda msg: check_answer(msg, answer))
        question_count += 1
    else:
        bot.send_message(message.chat.id, f"O'yin tugadi. Jami to'plangan ballar: {total_points}")
        bot.send_message(message.chat.id, f"Qayta o'ynashni xoxlasangiz /start ni bosing!!!")

def check_answer(message, correct_answer):
    global total_points
    user_answer = message.text
    try:
        user_answer = int(user_answer)
    except ValueError:
        bot.send_message(message.chat.id, "Iltimos javobni raqamlar bilan kiriting")
        return
    if user_answer == correct_answer:
        total_points += 1
        bot.send_message(message.chat.id, "To'gri! 🎉")
    else:
        bot.send_message(message.chat.id, f"Hato. Bu masalaning javobi: {correct_answer}.")
    ask_question(message)

def generate_question():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operator = random.choice(['+', '-', '*', '/'])
    if operator == '+':
        answer = num1 + num2
    elif operator == '-':
        answer = num1 - num2
    elif operator == '*':
        answer = num1 * num2
    else:
        answer = num1 / num2
    question = f"Masalaning yechimi nima:\n {num1} {operator} {num2}?"
    return question, answer

@require_POST
@csrf_exempt
def webhook(request):
    update = types.Update.de_json(request.body.decode('utf-8'), bot)
    bot.process_new_updates([update])
    return JsonResponse({'status': 'ok'})


bot.set_webhook(url=WEBHOOK_URL)

def remove_webhook(request):
    bot.remove_webhook()
    return JsonResponse({'status': 'ok'})