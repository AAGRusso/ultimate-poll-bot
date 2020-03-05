"""User related callback handler."""
from pollbot.i18n import i18n
from pollbot.helper.update import remove_poll_messages
from pollbot.display.creation import get_init_text
from pollbot.display.settings import get_user_settings_text
from pollbot.display.misc import (
    get_poll_list,
    get_help_text_and_keyboard,
)
from pollbot.models import Poll
from pollbot.telegram.keyboard import (
    get_main_keyboard,
    get_init_keyboard,
    get_user_settings_keyboard,
    get_user_language_keyboard,
    get_cancel_creation_keyboard,
    get_donations_keyboard,
    get_delete_all_confirmation_keyboard,
)


def open_main_menu(session, context):
    """Open the main menu."""
    keyboard = get_main_keyboard(context.user)
    context.query.message.edit_text(
        i18n.t('misc.start', locale=context.user.locale),
        reply_markup=keyboard,
        parse_mode='Markdown',
        disable_web_page_preview=True,
    )


def open_user_settings(session, context):
    """Open the user settings."""
    keyboard = get_user_settings_keyboard(context.user)
    text = get_user_settings_text(context.user)
    context.query.message.edit_text(text, reply_markup=keyboard,
                                    parse_mode='Markdown')


def open_language_menu(session, context):
    """Open the user language selection menu."""
    keyboard = get_user_language_keyboard(context.user)
    context.query.message.edit_text(
        i18n.t('settings.change_language', locale=context.user.locale),
        parse_mode='markdown',
        reply_markup=keyboard,
    )


def list_polls(session, context):
    """List all open polls of a user."""
    text, keyboard = get_poll_list(session, context.user)
    context.query.message.chat.send_message(text, reply_markup=keyboard)


def list_closed_polls(session, context):
    """List all open polls of a user."""
    text, keyboard = get_poll_list(session, context.user, closed=True)
    context.query.message.chat.send_message(text, reply_markup=keyboard)


def open_donation(session, context):
    """Open the donations text."""
    context.query.message.edit_text(
        i18n.t('misc.donation', locale=context.user.locale),
        parse_mode='Markdown',
        reply_markup=get_donations_keyboard(context.user),
    )


def open_help(session, context):
    """Open the donations text."""
    text, keyboard = get_help_text_and_keyboard(context.user, 'intro')
    context.query.message.edit_text(
        text,
        parse_mode='Markdown',
        reply_markup=keyboard,
        disable_web_page_preview=True,
    )


def init_poll(session, context):
    """Start the creation of a new poll."""
    user = context.user
    chat = context.query.message.chat
    if user.current_poll is not None and not user.current_poll.created:
        chat.send_message(
            i18n.t('creation.already_creating', locale=user.locale),
            reply_markup=get_cancel_creation_keyboard(user.current_poll))
        return

    poll = Poll.create(user, session)
    text = get_init_text(poll)
    keyboard = get_init_keyboard(poll)

    chat.send_message(
        text,
        parse_mode='markdown',
        reply_markup=keyboard,
        disable_web_page_preview=True,
    )


def toggle_notification(session, context):
    """Toggle the notification settings of the user."""
    user = context.user
    user.notifications_enabled = not user.notifications_enabled
    session.commit()
    open_user_settings(session, context)


def change_user_language(session, context):
    """Open the language picker."""
    context.user.locale = context.action
    session.commit()
    open_user_settings(session, context)
    return i18n.t('user.language_changed', locale=context.user.locale)


def delete_all_confirmation(session, context):
    keyboard = get_delete_all_confirmation_keyboard(context.user)
    context.query.message.edit_text(
        i18n.t('settings.user.delete_all_confirmation',
               locale=context.user.locale),
        parse_mode='markdown',
        reply_markup=keyboard,
    )


def delete_closed_confirmation(session, context):
    keyboard = get_delete_all_confirmation_keyboard(context.user, closed=True)
    context.query.message.edit_text(
        i18n.t('settings.user.delete_all_confirmation',
               locale=context.user.locale),
        parse_mode='markdown',
        reply_markup=keyboard,
    )


def delete_all(session, context):
    """Delete all polls of the user."""
    for poll in context.user.polls:
        remove_poll_messages(session, context.bot, poll)
        session.delete(poll)
        session.commit()

    open_user_settings(session, context)
    return i18n.t('deleted.polls', locale=context.user.locale)


def delete_closed(session, context):
    """Delete all closed polls of the user."""
    for poll in context.user.polls:
        if poll.closed:
            remove_poll_messages(session, context.bot, poll)
            session.delete(poll)
            session.commit()

    open_user_settings(session, context)
    return i18n.t('deleted.closed_polls', locale=context.user.locale)
