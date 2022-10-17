from config import AVAILABLE_TESTS as at
from generators import month_cycle_gen
from aiogram import types


days = month_cycle_gen()


buttons_commands = [[types.KeyboardButton(text='Найти'), 
                     types.KeyboardButton(text='Загрузить'),
                  types.KeyboardButton(text='Тест')]]


buttons_days = [[types.KeyboardButton(text=f"{j}") for j in i] for i in days]


buttons_lesson = [[types.KeyboardButton(text=f"{j}") for j in i] for i in [
                  ["тех.инд.п", "Алг.реш. прик.", "Информатика", "Проф. деят."],
                  ["Физика", "Лин.ал", "Матан"],
                  ["Ин.яз", "Истоия", "Право"]]]


buttons_adding = [[types.KeyboardButton(text='Добавить'), 
                     types.KeyboardButton(text='Отправить')]]

print(at.keys())
buttons_test_choice = [[types.KeyboardButton(text=i) for i in at.keys()]]
print(buttons_test_choice)