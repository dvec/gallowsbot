import logging
from threading import Thread

from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, Event, VkEventType

from gallowsbot.config import GROUP_TOKEN


class Vk:
    _interception_mappings = {}
    _sess = VkApi(token=GROUP_TOKEN)
    api = _sess.get_api()
    default_mapping = None

    @classmethod
    def start_mapping(cls, func, user_id):
        cls._interception_mappings[user_id] = func

    @classmethod
    def stop_mapping(cls, user_id):
        if user_id == 0:
            cls._interception_mappings[user_id] = cls.default_mapping
        else:
            del cls._interception_mappings[user_id]

    @classmethod
    def _handle_message(cls, event: Event):
        logging.info('Got new message: "{}" from user with id "{}"'.format(event.text, event.user_id))
        func = cls._interception_mappings.get(event.user_id, cls.default_mapping)

        try:
            message = func(event)
            if type(message) != str:
                raise Exception('message is {}, not str'.format(type(message)))
        except Exception as e:
            logging.exception(e)
            message = 'Произошла какая-то ошибка'

        if message:
            cls.api.messages.send(user_id=event.user_id, message=message)

    @classmethod
    def _listen_long_poll(cls):
        long_poll = VkLongPoll(cls._sess)
        while True:
            try:
                yield from long_poll.listen()
            except Exception as e:
                logging.exception(e)
                long_poll.update_longpoll_server()

    @classmethod
    def run_long_poll(cls, default_mapping):
        cls.default_mapping = default_mapping
        for event in cls._listen_long_poll():
            logging.debug("Got new event: {}".format(event.raw))
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                Thread(target=cls._handle_message, args=[event]).start()
