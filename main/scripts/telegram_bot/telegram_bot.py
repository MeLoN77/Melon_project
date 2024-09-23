from typing import Coroutine, Any

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    MessageHandler,
    CallbackQueryHandler,
    filters, Application,
)
from main.logs.melon_logs import log
from main.scripts.telegram_bot.bot_messages import MESSAGES
from main.scripts.telegram_bot.constants import *
from main.scripts.telegram_bot.helpers import *
from main.scripts.telegram_bot.health_care import calculate_water
from main.scripts.password_generator import PasswordGenerator


class MelonBot:

    def __init__(self, token: str = ""):
        # Builder
        log.debug("Starting Bot . . .")
        self.user_name = ""
        self.user_tag = ""
        self.chat_id = ""
        self.token = token
        self.user_language = {}
        self.app = Application.builder().token(self.token).build()

        # Password Generator
        self._pwd_word = ""
        self._pwd_numbers = ""

        # Languages
        self._lang_ukr = LANGUAGE['lang_uk']
        self._lang_eng = LANGUAGE['lang_en']

        # Commands
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("language", self.set_language))
        self.app.add_handler(CommandHandler("menu", self.menu_command))

        # Callback handler for button clicks
        self.app.add_handler(CallbackQueryHandler(self.button))

        # Messages
        self.app.add_handler(MessageHandler(filters.TEXT, self.handle_message))

        # Errors
        self.app.add_error_handler(self.error)

        log.debug("Start Polling")
        self.app.run_polling(poll_interval=3)

    # Commands
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        self.chat_id = update.effective_chat.id
        self.user_name = f"{update.effective_user.first_name} {update.effective_user.last_name}"
        self.user_tag = update.effective_user.username

        # Create inline keyboard with language options
        keyboard = [
            [InlineKeyboardButton(self._lang_eng, callback_data='lang_en')],
            [InlineKeyboardButton(self._lang_ukr, callback_data='lang_uk')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        user_lang = self.user_language.get(self.chat_id, 'lang_en')
        await update.message.reply_text(MESSAGES[user_lang]['select_language'], reply_markup=reply_markup)

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user_lang = self.user_language.get(self.chat_id, 'lang_en')
        await update.message.reply_text(MESSAGES[user_lang]['help'])

    async def set_language(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        # Create inline keyboard with language options
        keyboard = [
            [InlineKeyboardButton(self._lang_eng, callback_data='lang_en')],
            [InlineKeyboardButton(self._lang_ukr, callback_data='lang_uk')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        user_lang = self.user_language.get(self.chat_id, 'lang_en')
        await update.message.reply_text(MESSAGES[user_lang]['select_language'], reply_markup=reply_markup)

    # /menu command to show list of blocks
    async def menu_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        _user_lang = self.user_language.get(self.chat_id)
        keyboard = [
            [InlineKeyboardButton(MESSAGES[_user_lang]['menu']['water']['button_name'],
                                  callback_data='health_water')],
            [InlineKeyboardButton(MESSAGES[_user_lang]['menu']['helpers']['pwd']['button_name'],
                                  callback_data='helper_password')],
            [InlineKeyboardButton(MESSAGES[_user_lang]['menu']['helpers']['qr_code']['button_name'],
                                  callback_data='helper_qrcode')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(MESSAGES[_user_lang]['menu']['title'], reply_markup=reply_markup)

    async def button(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        _data = query.data
        await query.answer()
        _user_lang = self.user_language.get(self.chat_id)

        # Handling language selection
        if _data in ['lang_en', 'lang_uk']:
            # Set user's language choice
            _user_lang = _data
            self.user_language[self.chat_id] = _user_lang
            # Confirm language selection
            await query.edit_message_text(MESSAGES[_user_lang]['continue_language'])
            await query.message.reply_text(MESSAGES[_user_lang]['help'])

        # Handling menu options
        elif _data == 'health_water':
            await query.edit_message_text(MESSAGES[_user_lang]['menu']['water']['question_1'])
            context.user_data['expecting_weight'] = True  # Flag for input capture

        elif _data == 'helper_password':
            await query.edit_message_text(MESSAGES[_user_lang]['menu']['helpers']['pwd']['question_1'])
            context.user_data['password_word'] = True

        elif _data == 'helper_qrcode':
            await query.edit_message_text(MESSAGES[_user_lang]['menu']['helpers']['qr_code']['msg_1'])
            context.user_data['qrcode'] = True

    async def handle_response(self, update: Update, text: str, context: ContextTypes.DEFAULT_TYPE) -> Any:
        processed: str = text.lower()
        chat_id = update.effective_chat.id
        log.debug(update)
        log.debug(context)
        _context = context.user_data

        user_lang = self.user_language.get(chat_id, 'lang_en')

        if _context.get('expecting_weight'):
            _weight = int(text)
            _result = calculate_water(_weight)
            _msg = MESSAGES[user_lang]['menu']['water']['answer'].format(user=self.user_name,
                                                                         weight=_weight,
                                                                         min=_result[0],
                                                                         max=_result[1])
            return _msg

        if _context.get('password_word'):
            self._pwd_word = text
            context.user_data['password_word'] = False
            context.user_data['password_number'] = True
            await update.message.reply_text(
                MESSAGES[self.user_language[self.chat_id]]['menu']['helpers']['pwd']['question_2'])
            return ''
        if _context.get('password_number'):
            self._pwd_numbers = text
            context.user_data['password_number'] = False
            __password_generator = PasswordGenerator(word=self._pwd_word, numbers=self._pwd_numbers)
            __new_password = __password_generator.password()
            log.debug(__new_password)
            return MESSAGES[self.user_language[self.chat_id]]['menu']['helpers']['pwd']['result'].format(
                password=__new_password
            )

        if _context.get('qrcode'):
            context.user_data['qrcode'] = False
            if 'http' not in text:
                return MESSAGES[self.user_language[self.chat_id]]['menu']['helpers']['qr_code']['msg_error']

            _qrcode_path = qr_code(link=text, chat_id=self.chat_id)
            _caption = MESSAGES[self.user_language[self.chat_id]]['menu']['helpers']['qr_code']['msg_2']
            with open(_qrcode_path, 'rb') as _qr_image:
                await update.message.reply_photo(photo=_qr_image, caption=_caption)
            remove_qr_codes()
            return

        if 'hello' in processed or 'привіт' in processed:
            return f"{MESSAGES[user_lang]['hello'].format(user=self.user_name)}"

        if 'дякую' in processed or 'thank' in processed:
            return f"{MESSAGES[user_lang]['thanks'].format(user=self.user_name)}"

        elif 'бубочка' in processed or 'bubochka' in processed:
            return f"Я знаю що це ти Оксанка-бубочка 😊️️️️️️. Цьомаю тебе 💋"

        return 'I do not have such command or do not understand you. Sorry.'

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message_type: str = update.message.chat.type
        text: str = update.message.text
        _context: dict = context.user_data

        log.info(f"Username: {self.user_name}"
                 f" | User: {update.message.chat.id}"
                 f" | Channel: {message_type}"
                 f" | Text: {text}"
                 f" | Context: {context.user_data}")

        if message_type == "group":
            if BOT_USERNAME in text:
                new_text: str = text.replace(BOT_USERNAME, "").strip()
                response: str = await self.handle_response(update=update, text=new_text, context=context)
            else:
                return
        else:
            response: str = await self.handle_response(update=update, text=text, context=context)
            # Reset flags
            if 'expecting_weight' in _context:
                context.user_data['expecting_weight'] = False

        if response:
            await update.message.reply_text(response)

        log.info(f"Bot: {response}")

    async def error(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        log.error(f"Update: {update} caused error {context.error}")


if __name__ == "__main__":
    melon_bot = MelonBot(TOKEN)
