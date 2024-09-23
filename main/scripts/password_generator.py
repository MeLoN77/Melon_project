import string
import random
from typing import List
from main.logs.melon_logs import log

# abcdefghijklmnopqrstuvwxyz
LETTERS_LOWERCASE = string.ascii_lowercase

# ABCDEFGHIJKLMNOPQRSTUVWXYZ
LETTERS_UPPERCASE = string.ascii_uppercase

SPECIAL_SYMBOLS = "@~!#$%^&*()_[]<>."


class PasswordGenerator:

    def __init__(self, word: str, numbers: str):
        self.word = word.lower()
        self.numbers = numbers
        if not self._checker():
            exit(0)

    def _checker(self) -> str | bool:
        if len(self.word) < 4:
            log.warning("Please write word at least 5 letters.")
            return "Please write word at least 5 letters."
        elif not isinstance(self.word, str):
            log.warning("Please write word as string.")
            return "Please write word as string."
        elif len(self.numbers) < 4:
            log.warning("Please enter at least 5 numbers.")
            return "Please enter at least 5 numbers."

        return True

    @classmethod
    def __find_right_number(cls, count: int, a_list: List) -> List:
        """
        This function is slicing count number by length of the list and adding elements to the new list.
        Returns new list depends on the count.
        :param count: 15
        :param a_list: ["@", A, a]
        :return: ["@", A, a, "@", A]
        """
        _r_count = count
        _list_counter = 1
        _element_counter = 0
        new_a_list = []
        while True:
            if _r_count == 0:
                break

            if not _list_counter % len(a_list):
                new_a_list.append(a_list[_element_counter])
                _list_counter = 1
                _element_counter = 0
                _r_count -= 1
                continue

            if _r_count > 0:
                new_a_list.append(a_list[_element_counter])
                _list_counter += 1
                _element_counter += 1
            _r_count -= 1
        return new_a_list

    def __find_a_count(self) -> List[str] | bool:
        """
        Function is finding letter "A" in the word to set different spec symbols into password
        :return:
        """
        _at = SPECIAL_SYMBOLS[SPECIAL_SYMBOLS.index("@")]
        _a = LETTERS_LOWERCASE[0]
        _a_list = [_at, _a.upper(), _a]
        _count = self.word.lower().count("a")
        if _count == 0:
            return False

        elif _count == 1:
            return [_at]

        elif _count == 2:
            return [_at, _a.upper()]

        elif _count == 3:
            return [_at, _a.upper(), _a]

        else:
            return self.__find_right_number(count=_count, a_list=[_at, _a.upper(), _a])

    @classmethod
    def __check_longer(cls, word: str, number: str):
        """
        Check which variable length is longer
        :param word:
        :param number:
        :return: str
        """
        log.debug(f"Checking which variable is longer: -->>\t[{word}] vs [{number}]\n")
        if len(word) > len(number):
            return word

        elif len(word) == len(number):
            return number

        else:
            return number

    def __looper_puper(self, longer_item: str, shorter_item: str, a_count: list) -> str:
        """
        Loop to generate password
        :return:
        """
        _password = ""
        _longer = longer_item
        _shorter = shorter_item
        _letter_a = a_count
        log.debug("Generating password. . .\n")
        n = 0
        while True:
            if not _longer:
                break

            shorter_element = ""
            longer_element = _longer[0]
            if _shorter:
                shorter_element = _shorter[0]
            if longer_element.isdigit():
                _password += longer_element
                if shorter_element:
                    if n == 0 and isinstance(shorter_element, int) is False:
                        _password += shorter_element.upper()
                    else:
                        if shorter_element == LETTERS_LOWERCASE[0]:
                            _password += _letter_a[0]

                            # Remove used element
                            _letter_a.pop(0)
                        else:
                            _password += shorter_element
            else:
                if shorter_element:
                    if n == 0 and isinstance(shorter_element, int) is False:
                        _password += shorter_element.upper()
                    else:
                        _password += shorter_element

                elif n == 0 and isinstance(longer_element, str) is True:
                    _password += longer_element.upper()
                else:
                    if longer_element == LETTERS_LOWERCASE[0]:
                        _password += _letter_a[0]

                        # Remove used element
                        _letter_a.pop(0)
                    else:
                        _password += longer_element

            # Removing used characters from variable
            _longer = _longer[1::]
            if _shorter:
                _shorter = _shorter[1::]

            n += 1

        return _password

    @classmethod
    def __generator(cls) -> str:
        """
        Generate random part of password to make it more complex
        :return: prepared radom string
        """
        _upper = random.choice(LETTERS_UPPERCASE)
        _lower = random.choice(LETTERS_LOWERCASE)
        _spec_symbol = random.choice(SPECIAL_SYMBOLS)
        return f"{_upper}{_lower}{_spec_symbol}"

    def password(self) -> str:
        """
        Function generating new password based on passed word and number
        :return: "n23$@2nisb1$*()"
        """
        a_count = self.__find_a_count()
        _numbers = self.numbers
        _word = self.word
        __longer_item = self.__check_longer(word=_word,
                                            number=_numbers)
        if __longer_item == _word:
            password = self.__looper_puper(longer_item=__longer_item,
                                           shorter_item=_numbers,
                                           a_count=a_count)
        else:
            password = self.__looper_puper(longer_item=_numbers,
                                           shorter_item=_word,
                                           a_count=a_count)

        password = password + self.__generator()
        log.debug(f"Password has been successfully generated:\t>[ {password} ]<\t\n")
        return password


# How to use:
word_1 = "Oxana"
number_1 = "12345"
# _pwd = PasswordGenerator(word=word_1, numbers=number_1).password()
# log.debug(_pwd)
# Do anything you want with new pwd. Take care and good luck!
