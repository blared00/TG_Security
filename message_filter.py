import random

import Levenshtein

try:
    import config
except ImportError:
    config = {
        x: ()
        for x in (
            "BAD_WORDS",
            "HELLO_WORD",
            "POLL_QUESTION",
            "POLL_OPTIONS",
            "LINK_WIKI",
            "COMMANDS",
        )
    }


def start_message(message):
    """Приветствие и обработка матов"""
    if message.text:
        if message.text.lower() in config.HELLO_WORD:
            return "{}, уважаемые. \nПовоюем? Запускай опрос - /poll\nЕсли хочешь просветиться -/wiki".format(
                random.choice(config.HELLO_WORD).title()
            )

        if message.text.lower() in config.BAD_WORDS:
            return "Ты матершинник, {}".format(message["from"].first_name)
        if find_command(message.text, config.CALL_BOT):
            return "{}\nКомандуй\n/poll - опрос;\n/wiki - библиотека знаний.".format(random.choice(config.ANSWER_IN_CALL))

def find_command(text, command):
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
    return config.LINK_WIKI.format(config.COMMANDS[command[1:]])
