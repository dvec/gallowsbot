import logging

from gallowsbot.game import on_message_while_not_playing
from gallowsbot.vk import Vk

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    Vk.run_long_poll(on_message_while_not_playing)
