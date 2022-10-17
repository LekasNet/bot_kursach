from random import choice, shuffle
from aiogram import types
import config
import data


def naming(name, repl):
    nn = name.split('.')
    return str(repl) + '.' + nn[-1]


def testKeyboard(words, text):
    buttons = [[types.KeyboardButton(text=words[text]),
                types.KeyboardButton(
                    text=choice(list(words.values()))),
                types.KeyboardButton(
                    text=choice(list(words.values()))),
                types.KeyboardButton(
                    text=choice(list(words.values())))
                ]]
    shuffle(buttons[0])
    buttons = [[buttons[0][0],buttons[0][1]],
               [buttons[0][2],buttons[0][3]]]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder="Как переводится?")
    return keyboard


def keyboardGen(buttons):
    return types.ReplyKeyboardMarkup(
    keyboard=buttons,
    resize_keyboard=True,
    input_field_placeholder="Что будем делать?"
    )


def converter(word, words, message):
    text = choice(list(words.keys()))
    if word != "":
        input_text = message
        print(words[word], input_text)
    if word == "":
        plumbum = ""
    elif input_text in words[word]:
        plumbum = "✅"
    else:
        text = word
        plumbum = "❌"
    return text, plumbum


def month_cycle_gen():
    days = [["❌", "❌", "❌"],[],[],[],[]]

    iterator = 0
    not_buttoned = 0
    for i in range(1, config.DATE):
        if len(days[iterator]) == 7:
            iterator += 1
        days[iterator].append(i)
        not_buttoned = len(days[iterator])
    
    for i in range(not_buttoned, 7):
        days[iterator].append("❌")
    
    if config.DATE > 29:
        days[iterator] += ["1️⃣","2️⃣"]
    return days