"""All keyboards for external users that don't own the poll."""
from telegram import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from pollbot.telegram.keyboard import get_back_to_menu_button
from pollbot.i18n import i18n
from pollbot.helper.enums import CallbackType


def get_help_keyboard(user, categories, current_category):
    """Get the done keyboard for options during poll creation."""
    rows = []
    current_row = []
    while len(categories) > 0:
        category = categories.pop(0)
        payload = f'{CallbackType.switch_help.value}:0:{category}'
        text = i18n.t(f'keyboard.help.{category}', locale=user.locale)
        if category == current_category:
            text = f'[ {text} ]'
        button = InlineKeyboardButton(text, callback_data=payload)

        if len(current_row) < 3:
            current_row.append(button)
        else:
            rows.append(current_row)
            current_row = [button]

    rows.append(current_row)
    rows.append([get_back_to_menu_button(user)])

    return InlineKeyboardMarkup(rows)


def get_donations_keyboard(user):
    buttons = [
        [InlineKeyboardButton(text='☺️ Buy me a coffee',
                              url='https://www.buymeacoffee.com/Nukesor')],
        [InlineKeyboardButton(text='❤️ Patreon ❤️',
                              url='https://patreon.com/nukesor')],
        [InlineKeyboardButton(text='Paypal',
                              url='https://paypal.me/arnebeer/')],
        [get_back_to_menu_button(user)]
    ]

    return InlineKeyboardMarkup(buttons)
