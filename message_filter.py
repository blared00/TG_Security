import random

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
    if message.text.lower() in config.HELLO_WORD:
        return "{}, уважаемые. \nПовоюем? Запускай опрос - /poll\nЕсли хочешь просветиться -/wiki".format(
            random.choice(config.HELLO_WORD).title()
        )
    if message.text in config.BAD_WORDS:
        return "Ты матершинник, {}".format(message["from"].first_name)


def create_poll():
    """Создание опроса"""
    question = random.choice(config.POLL_QUESTION)
    options = config.POLL_OPTIONS
    is_anonimus = False
    return (question, options, is_anonimus)


def get_link_wiki(command):
    """Возвращает страницу с википедии"""
    return config.LINK_WIKI.format(config.COMMANDS[command[1:]])
