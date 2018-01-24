from random import choice

from gallowsbot.config import GROUP_ID
from gallowsbot.utils import units
from gallowsbot.vk import Vk


class Game:
    _MAN = [

        """
____
▏ O 
▏/|\\
▏ /\\
""",
        """
____
▏ O 
▏/|\\
▏ /
""",

        """
____
▏ O 
▏/|\\
▏
""",

        """
____
▏ O 
▏/|
▏
""",
        """
____
▏ O 
▏ |
▏
""",

        """
____
▏ O 
▏
▏
""",
]

    def __init__(self):
        with open('../word_rus.txt') as f:
            self.word = choice(f.readlines()).strip()
        self.mistakes = set()
        self.characters_been = set()
        self.right_answers = [False] * len(self.word)
        self.hints_left = round(len(self.word) / 3)

    def _check_answer(self, character):
        self.characters_been.add(character)
        count = 0
        for i in range(len(self.word)):
            if self.word[i] == character:
                if not self.right_answers[i]:
                    count += 1
                    self.right_answers[i] = True
        if count == 0:
            self.mistakes.add(character)

    def _draw_word(self):
        result = ''
        for i in range(len(self.word)):
            if self.right_answers[i]:
                result += self.word[i]
            else:
                result += '_'
        return result

    def _get_hint(self):
        self.hints_left -= 1
        for i in range(len(self.word)):
            if self.word[i] not in self.characters_been:
                self._check_answer(self.word[i])
                return

    def on_message_while_playing(self, event):
        text = event.text.lower()
        if text == 'подсказка':
            if self.hints_left <= 0:
                return 'Подсказки уже использованы!'
            else:
                self._get_hint()
        else:
            if len(text) != 1:
                return 'Вы должны прислать только одну букву'
            elif text in self.characters_been:
                return 'Эта буква уже была'

            self._check_answer(text)

        if all(self.right_answers):
            Vk.stop_mapping(event.user_id)
            return 'Вы выиграли!'
        elif len(self.mistakes) == len(self._MAN):
            Vk.stop_mapping(event.user_id)
            return 'Вы проиграли! Я загадал слово {}'.format(self.word)
        else:
            return 'У вас {}\n{}\nОшибки: {}\n{}' \
                .format(
                    'осталось {} {}\n'.format(self.hints_left, units(self.hints_left,
                                                                 ['подсказка', 'подсказки', 'подсказок']))
                    if self.hints_left else 'не осталось подсказок',

                    self._MAN[len(self.mistakes)],
                    ', '.join(self.mistakes) if self.mistakes else 'нет', self._draw_word()
            )


def on_message_while_not_playing(event):
    if event.text.lower() == 'игра':
        game = Game()
        Vk.start_mapping(game.on_message_while_playing, event.user_id)

        return 'Игра началась! В слове {} букв'.format(len(game.word))
    else:
        is_user_subscribed = Vk.api.groups.is_member(group_id=GROUP_ID, user_id=event.user_id)
        return 'Напишите "игра" чтобы начать игру.\n{}' \
            .format('Спасибо что подписались на нас!' if is_user_subscribed else
                    'Пожалуйста, подпищитесь на наше сообщество. Вам не сложно, а нам приятно')
