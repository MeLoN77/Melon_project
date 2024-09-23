# Dictionary for language translations
MESSAGES = {
    "lang_en": {
        "start": "Hello {user}!"
                 "\nI'm WaterMelon Bot, thank you for chatting with me."
                 "\nFor information please use command /help",
        "hello": "Hello {user}!",
        "help": "Here is the list of commands to run:"
                "\n/start -> start bot"
                "\n/help -> show available commands"
                "\n/language -> set language for bot"
                "\n/menu -> menu list",
        "continue_language": "You can now continue in English language.",
        "select_language": "Please select your language:",
        "menu": {
            "title": "Please select an option:",
            "water": {
                "button_name": "Healthcare: Water Calculator",
                "question_1": "Please write your weight (kg):",
                "answer": "{user} based on your weight ({weight} kg), you should drink water per day:\nminimum: {min} liters\nmaximum: {max} liters\n\nAlso take into consideration your physical activity and season of the year."
            },
            "helpers": {
                "pwd": {
                    "button_name": "Helpers: Password Generator",
                    "question_1": "Enter word (at least 5 letters):",
                    "question_2": "Enter number (at least 5 numbers):",
                    "result": "Here is your password: {password}",
                },
                "qr_code": {
                    "button_name": "Helpers: QR Code Generator",
                    "msg_1": "Please enter link (example: https://www.youtube.com):",
                    "msg_2": "Here is your QR code!",
                    "msg_error": "Text you provided is not URL(LINK).\nHere is example of URL: https://www.instagram.com.\n Please try again."
                }
            }
        },
        "thanks": "{user} are welcome!"
        ""
    },
    "lang_uk": {
        "start": "Привіт {user}!"
                 "\nЯ є БОТ-Кавун, дякую що написав мені."
                 "\nДля довідки використовуй ось цю комадну /help",
        "hello": "Привіт {user}!",
        "help": "Список команд які можна запустити:\n"
                "\n/start -> запускає бота"
                "\n/help -> список можливиї команд"
                "\n/language -> вибрати мову БОТА"
                "\n/menu -> меню можливостей",
        "continue_language": "Тепер ви можете спілкуватися Українською мовою зі мною.",
        "select_language": "Будь ласка виберіть мову:",
        "menu": {
            "title": "Будь-ласка вибери елемент з меню:",
            "water": {
                "button_name": "Здоров'я: К-сть води на добу",
                "question_1": "Введіть вагу тіла (кг):",
                "answer": "{user} виходячи із вашої ваги тіла ({weight} кг), ви повинні випивати води щодня:\n\n    мінімум: {min} літрів\n    максимум: {max} літрів\n\nпшеТакож враховуйте свою фізичну активність і пору року.",
            },
            "helpers": {
                "pwd": {
                    "button_name": "Генератор Паролів",
                    "msg_1": "Вибрано генератор паролів.",
                    "question_1": "Введіть слово (англійською мовою мін. 5 букв у слові):",
                    "question_2": "Введіть цифру (5 цифр мін.):",
                    "result": "Ось ваш новий пароль: {password}",
                },
                "qr_code": {
                    "button_name": "Генератор QR Коду",
                    "msg_1": "Будь ласка введіть посилання (приклад: https://www.youtube.com):",
                    "msg_2": "Ось твій QR код!",
                    "msg_error": "Текст який ти написав не є URL(LINK).\nОсь приклад URL: https://www.instagram.com.\n Спробуй будь ласка ще раз."
                }
            }
        },
        "thanks": "Будь ласка {user}! Звертайся ще 😉"
    }
}
