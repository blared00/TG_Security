import random

try:
    import config
except ImportError:
    config = {x: () for x in ('BAD_WORDS', 'HELLO_WORD')}


def start_message(message):
    if message.text in config.HELLO_WORD:
        return "{}, уважаемые. \nПовоюем?".format(random.choice(config.HELLO_WORD))
    if message.text in config.BAD_WORDS:
        return "Ты матершинник, {}".format(message.chat.first_name)



