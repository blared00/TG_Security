import random

import Levenshtein
import config

COMMANDS_LIST = {
    "прочее": config.OTHER,
    "other": config.OTHER,
    "фото": config.GOOD_PHOTO,
    "photo": config.GOOD_PHOTO,
    "эквип": config.EQUIPMENT,
    "equipment": config.EQUIPMENT,
    'снаряжение': config.EQUIPMENT,
    "призраки": config.GHOSTS,
    "ghost": config.GHOSTS,
    "вики": config.COMMANDS,
    "wiki": config.COMMANDS
}


def start_message(message):
    """Приветствие и обработка матов"""
    if message.text:
        if message.text.lower() in config.HELLO_WORD:
            return "{}, уважаемые. \nПовоюем? Запускай опрос - /poll\nЕсли хочешь просветиться -/wiki".format(
                random.choice(config.HELLO_WORD).title()
            )
        for bad in config.BAD_WORDS:
            if bad in message.text.lower():
                return "Ты матершинник, {}".format(message["from"].first_name)
        if find_command(message.text, config.CALL_BOT):
            return "{}\nКомандуй\n/poll - опрос;\n/wiki - библиотека знаний.".format(
                random.choice(config.ANSWER_IN_CALL)
            )


def find_command(text, command):
    """Функция для проверки сообщения на совпадение с фразой для вызова бота"""
    percent_coincidence = 1 - Levenshtein.distance(text, command) / max(
        len(text), len(command)
    )
    if percent_coincidence >= 0.75:
        return True


def create_poll():
    """Создание опроса"""
    question = random.choice(config.POLL_QUESTION)
    options = config.POLL_OPTIONS
    is_anonimus = False

    return (question, options, is_anonimus)


def get_link_wiki(command):
    """Возвращает страницу с википедии"""
    return (
        "[{}]({})".format(command.title(), config.LINK_WIKI.format(command))
    )


def get_list_wiki(command):
    """Возвращает команды для вики"""
    if command not in ("вики", 'wiki'):
        return "Доступные команды для вики:\n!" + "\n!".join(map(lambda x: get_link_wiki(x), COMMANDS_LIST[command]))
    return "Доступные команды для вики:\n!" + "\n!".join(map(lambda x: x, COMMANDS_LIST[command]))
