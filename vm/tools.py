# -*- coding: utf-8 -*-

import random
import string


def random_string(string_length):
    """
    Generate a random string with the combination of lowercase and uppercase letters (52 possibility per char)

    :param string_length: int to specify which number of character will be the random string
    :return: [a-zA-Z]{string_length}
    """

    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(string_length))
