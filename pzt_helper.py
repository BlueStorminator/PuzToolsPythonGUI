import json
import os
import re
from typing import Generator, Any, List, Tuple, Dict
import webbrowser
import pzt_ancillary as a


#############################################
# MISCELLANEOUS, NUMBER, AND WORD FUNCTIONS #
#############################################


path_to_json_dict = "reference/words_dict.json"


# MISCELLANEOUS FUNCTIONS
def callwebpage(url: str) -> None:
    '''
    open a tab in default browser
    bring browser to focus_force
    '''
    webbrowser.open(url, new=2, autoraise=True)


# NUMBERS FUNCTIONS
def clean_integer(text: str) -> str:
    """make sure no extraneous characters have been entered"""
    if not re.match("[0-9]+$", text) or re.match("[0]+$", text):
        return ''
    return text


def factors(num: int) -> List[int]:
    '''returns all factors of an integer'''
    top = num//2
    return [i for i in range(1, top+1) if num % i == 0]


def generate_fibonacci_sequence(limit: int) -> Generator[int, int, None]:
    '''
    this code snippet adapted from various internet sources
    produces fibonacci sequence using a generator
    '''
    int1, int2 = 0, 1
    while int1 < limit:
        yield int1
        int1, int2 = int2, int1 + int2


def generate_hi_low_primes(low: int, high: int) -> Generator[int, int, None]:
    '''
    this code snippet adapted from various internet sources
    a generator that yields primes between low and high boundaries
    calls is_prime function
    '''
    results: List[int] = []
    if low <= 2:
        yield 2
        low = 3
    if low % 2 == 0:
        low = low + 1
    for num in range(low, high+1):
        if is_prime(num):
            yield num


def get_cube_root(num: int) -> int:
    '''return cube root of an integer'''
    return round(num ** (1/3))


def get_cubes(low: int, high: int) -> List[int]:
    '''return cubes between low and high limits'''
    return [i for i in range(low, high + 1)
            if float.is_integer(round(i ** (1/3), 10))]


def get_fib_nums_in_range(low: int, high: int) -> List[int]:
    '''
    this code snippet adapted from various internet sources
    return fibonacci numbers between low and high limits
    '''
    results: List[int] = []
    data: Generator[int, int, None] = generate_fibonacci_sequence(high+1)
    for fib in sorted(set(data)):
        if fib >= low:
            results.append(fib)
    return results


def get_prime_factors(num: int) -> str:
    '''returns styled string listing all prime factors of a number'''
    pfactors: Dict[int, int] = {}
    n: int = num
    while n % 2 == 0:
        pfactors[2] = pfactors.get(2, 0) + 1
        n = n // 2
    for i in range(3, int(n ** (1/2)) + 1, 2):
        while n % i == 0:
            pfactors[i] = pfactors.get(i, 0) + 1
            n = n // i
    if n > 2:
        pfactors[n] = pfactors.get(n, 0) + 1
    return ' x '.join([str(key)
                       for key, value in pfactors.items()
                       for i in range(0, value)])


def get_primes_in_range(low: int, high: int) -> List[int]:
    '''
    input: low and high boundary
    output: list of primes within the boundaries, inclusive
    calls generator
    '''
    results: List[int] = []
    primes: Generator[int, int, None] = generate_hi_low_primes(low, high)
    for prime in primes:
        if prime <= high:
            results.append(prime)
    return results


def get_square_root(num: int) -> int:
    '''return square root of a number'''
    return round(num ** (1/2))


def get_squares(low: int, high: int) -> List[int]:
    '''return squares between low and high limits'''
    return [i for i in range(low, high+1) if float.is_integer(i ** (1/2))]


def is_cube(num: int) -> bool:
    '''check whether a number is a perfect cube'''
    max: int = round((num ** (1/3)) + 1)
    return any(i * i * i == num for i in range(max))


def is_fibonacci(num: int) -> bool:
    '''check whether a number is a fibonacci number'''
    return bool(is_square(5 * num * num + 4)
                or is_square(5 * num * num - 4))


def is_prime(num: int) -> bool:
    """returns True if num is prime otherwise False"""
    if num == 1:
        return False
    if num == 2:
        return True
    if num % 2 == 0:
        return False
    # now check only odd numbers
    count: int = 0
    for i in range(1, num, 2):
        if (num % (i + 2)) == 0:
            count += 1
            if count > 1:
                return False
    return True


def is_square(num: int) -> bool:
    max: int = round((num ** 0.5) + 1)
    return any(i * i == num for i in range(max))


def is_triangular(num: int) -> bool:
    if num in [0, 1]:
        return True
    triangular_sum = 0
    for i in range(num):
        triangular_sum += i
        if triangular_sum == num:
            return True
        if triangular_sum > num or i == num:
            return False
    return False


# WORDS functions
def caesar_all(text: str) -> List[Tuple[int, str]]:
    """returns all 26 Caesar rotations of an input string
    returns a list of tuples with rotation # and the new string
    """
    final_text: str = ''.join(char
                              for char in text.lower()
                              if "a" <= char <= "z" or char == ' ')
    english_words: set[str] = load_words()
    english: List[str] = []
    resultlist: List[Tuple[int, str]] = []
    for key in range(0, 26):
        newstr = ''
        for char in final_text:
            if ord(char) == 32:
                newchar = 32
            else:
                newchar = ord(char) + key
                if newchar > 122:
                    newchar = newchar - 26
            newstr += chr(newchar)
        resultlist.append((key, newstr.upper()))
    return resultlist


def check_english(word_list: str) -> List[str]:
    english_words = load_words()
    return [word for word in word_list if word.lower() in english_words]


def check_for_anagram(s1: str, s2: str) -> Tuple[str, str, str, str, str]:
    s1 = ''.join(char for char in s1.upper() if "A" <= char <= "Z")
    s2 = ''.join(char for char in s2.upper() if "A" <= char <= "Z")
    d1: Dict[str, int] = {}
    d2: Dict[str, int] = {}
    common: Dict[str, int] = {}
    for char in s1:
        d1[char] = d1.get(char, 0) + 1
    for char in s2:
        d2[char] = d2.get(char, 0) + 1
    for char in s1:
        if char in d2.keys() and d2[char] > 0:
            common[char] = common.get(char, 0) + 1
            d2[char] = d2[char] - 1
            d1[char] = d1[char] - 1
    incommon: str = dict_to_list_by_value(common)
    s1only: str = dict_to_list_by_value(d1)
    s2only: str = dict_to_list_by_value(d2)
    return s1, s2, incommon, s1only, s2only


def dict_to_list_by_value(d: Dict[str, int]) -> str:
    '''
    input = a dictionary
    output = a string in alpha order with each dict key repeated value times
    '''
    result: List[str] = []
    for key in sorted(d.keys()):
        result.append(key * d[key])
    return ''.join(result)


def get_words_with_set_value(wordvalue: int, scale: str) -> List[str]:
    '''
    input1: wordvalue (an integer)
    input2: scale (a string - A1-Z26, A26-Z1, Scrabble)
    output: a list of words of given wordvalue according to the given scale
    '''
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    dict_file = os.path.join(THIS_FOLDER, path_to_json_dict)
    with open(dict_file, "r") as word_dict_file:
        word_dict = json.load(word_dict_file)
        if 'A1' in scale:
            return [word for word in word_dict
                    if simple_word_value_calc(word) == int(wordvalue)]
        elif 'A26' in scale:
            return [word for word in word_dict
                    if reverse_word_value_calc(word) == int(wordvalue)]
        elif 'Scrabble' in scale:
            return [word for word in word_dict
                    if scrabble_word_value_calc(word) == int(wordvalue)]
    return ['']


def load_words() -> Any:
    '''
    opens a json english dictionary and returns the keys (valid words)
    with initial set-up of correct path
    source: "https://github.com/dwyl/english-words
    '''
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    dict_file = os.path.join(THIS_FOLDER, path_to_json_dict)
    with open(dict_file, "r") as word_dict_file:
        word_dict = json.load(word_dict_file)
    return word_dict.keys()


def reverse_word_value_calc(word: str) -> int:
    '''
    input: string
    output:  word value using scale A26-Z1
    '''
    wv: int = 0
    word = word.lower()
    for char in word:
        if "a" <= char <= "z":
            wv += 27 - (ord(char) - 96)
    return wv


def scrabble_word_value_calc(word: str) -> int:
    '''
    input: string
    output: word value using standard Scrabble dictionary values
    '''
    wv: int = 0
    word = word.upper()
    for char in word:
        if "A" <= char <= "Z":
            wv += a.SCRABBLE_POINT_DICTIONARY[char]
    return wv


def simple_word_value_calc(word: str) -> int:
    '''
    input: string
    output:  word value using scale A1-Z26
    '''
    wv: int = 0
    word = word.lower()
    for char in word:
        if "a" <= char <= "z":
            wv += ord(char) - 96
    return wv


def triple_word_value_calc(raw_word: str) -> Tuple[str, List[Tuple[str, int]]]:
    """
    input: a string
    output: string in upper case stripped of non-alpha characters
            + 3 word values:
            regular A-Z, reverse A-Z, Scrabble points in a list of tuples
    """
    final_word: str = ''.join(char
                              for char in raw_word.upper()
                              if "A" <= char <= "Z")
    AZ_value: int = 0
    ZA_value: int = 0
    scrb_value: int = 0
    for char in final_word:
        AZ_value += ord(char) - 64
        ZA_value += 27 - (ord(char)-64)
        scrb_value += a.SCRABBLE_POINT_DICTIONARY[char]
    return final_word, [("A1-Z26", AZ_value),
                        ("Z1-A26", ZA_value),
                        ("Scrabble", scrb_value)]
