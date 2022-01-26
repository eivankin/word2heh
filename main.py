import re
import random
from dataclasses import dataclass
from math import ceil
from typing import Callable

DEBUG = False
HEH_RATE = 1 if DEBUG else .25
HEH_LEVEL = 0.2
VOWELS: set[str] = set('уеыаоэяию')
# Й, Ъ, Ь пропущены, так как с них не может начинаться слог
CONSONANTS: set[str] = set('цкнгшщзхфвпрлджчсмтб')


@dataclass
class Syllable:
    MAX_SIMILARITY = 3
    SIMILAR_VOWELS = {('а', 'я'), ('е', 'э')}
    value: str
    vowel: str

    def __str__(self) -> str:
        return self.value

    def similarity(self, other: 'Syllable') -> int:
        return self.vowel_similarity(other) + \
               ((self.value[-1].lower() in VOWELS) == (other.value[-1].lower() in VOWELS))

    def vowel_similarity(self, other: 'Syllable') -> int:
        return (self.vowel == other.vowel) * 2 + (tuple(
            sorted((self.vowel, other.vowel))) in self.SIMILAR_VOWELS)

    def agree_case_with(self, other_syllable: 'Syllable') -> 'Syllable':
        result = ''
        for my, other in zip(self.value, other_syllable.value + 'а' * (
                len(self.value) - len(other_syllable.value))):
            result += my.upper() if other.isupper() else my.lower()
        return Syllable(result, self.vowel)

    def __hash__(self) -> int:
        return hash((self.value, self.vowel))

    def __eq__(self, other: 'Syllable') -> bool:
        return self.value.lower() == other.value.lower()


HEH_SYLLABLES: set[Syllable] = set(
    Syllable('х' + vowel + end, vowel) for vowel in ('а', 'е', 'и') for end in ('', 'х'))


def normalize_heh_level(level: float, n_syllables: int) -> int:
    return ceil(level * n_syllables)


def word_to_heh(word_match: re.Match, rate: float = HEH_RATE, level: int = HEH_LEVEL,
                seed: int = None) -> str:
    """
    Main function that performs 'hehefication' - replacing some syllables with the new 'heh' ones
    ('хах', 'ха', etc. for Russian language) from 'HEH_SYLLABLES' set.

    :param word_match: match object, where 0 group should be the word;
    :param rate: probability of 'hehefication';
    :param level: percentage of 'hehefized' syllables, at least one syllable will be replaced anyway;
    :param seed: seed for random for reproducible results;
    :return: result word.
    """
    word: str = word_match.group(0)

    if seed is not None:
        random.seed(seed)

    if random.random() < (1 - rate):
        return word

    syllables = word_to_syllables(word)
    if len(syllables) == 0:
        return word

    level = normalize_heh_level(level, len(syllables))
    for i, syl, best_match, similarity in sorted(
            [(i, syl, *get_best_match(syl, HEH_SYLLABLES)) for i, syl in enumerate(syllables)],
            key=lambda p: Syllable.MAX_SIMILARITY - p[-1]):
        if level <= 0:
            break
        level = level - 1 - 0.5 * (best_match.value[-1] not in VOWELS or (
                i + 1 < len(syllables) and syllables[i + 1].value[0].lower() == 'х'))
        syllables[i] = best_match.agree_case_with(syl)

    return ''.join(map(str, generalize_syllables(syllables))).replace('хх', 'х')


def generalize_syllables(syllables: list[Syllable],
                         filter_func: Callable[[Syllable], bool] = lambda s: s in HEH_SYLLABLES,
                         level=HEH_LEVEL) -> list[Syllable]:
    """
    :param syllables: list of syllables to generalize;
    :param filter_func: boolean function to filter syllables from all of them;
    :param level: level of generalization (1 - max, 0 - no generalization);
    :return: list of generalized syllables.
    """

    def gen_step(next_syl: Syllable, reps, idx):
        if prev == curr:
            reps += 1
        elif filter_func(curr):
            if filter_func(prev) and (
                    reps > level or (level < 3 and next_syl is not None
                                     and prev == next_syl) or not level
                    and len(prev.value) > len(curr.value)):
                generalized[idx] = prev
                reps += 1
            else:
                reps = 0
        return reps

    generalized = syllables.copy()
    repeats = 0
    level = normalize_heh_level(1 - level, len(syllables))
    for i in range(1, len(syllables)):
        prev, curr = generalized[i - 1:i + 1]
        repeats = gen_step(None if i + 1 >= len(syllables) else syllables[i + 1], repeats, i)
    repeats = 0
    for i in range(len(syllables) - 1, 0, -1):
        prev, curr = generalized[i - 1:i + 1][::-1]
        repeats = gen_step(None if i <= 0 else syllables[i - 1], repeats, i - 1)
    return generalized


def get_best_match(to: Syllable, from_list: set[Syllable]) -> tuple[Syllable, int]:
    """
    Finds most similar syllable from with 'Syllable.similarity' method.

    :param to: syllable for matching;
    :param from_list: set of possible matches;
    :return: best match and its similarity.
    """
    return max(((syl, syl.similarity(to)) for syl in from_list), key=lambda t: t[-1])


def word_to_syllables(word: str) -> list[Syllable]:
    """
    Splits given word into syllables.
    References: https://slogi.su/pravila.html

    :param word: word to split;
    :return: list of syllables.
    """

    syllables: list[Syllable] = []
    start_ptr = 0
    idx = 0
    vowel = ''
    while idx < len(word):
        letter = word[idx].lower()
        if letter in VOWELS:
            vowel = letter
            idx += 1
            while idx < len(word) and word[idx] not in VOWELS:
                idx += 1
            idx -= 1 * (word[idx - 1] in CONSONANTS)
            syllables.append(Syllable(word[start_ptr:idx + (idx == len(word) - 1)], vowel))
            start_ptr = idx
        idx += 1
    if start_ptr < len(word) - 1:
        syllables.append(Syllable(word[start_ptr:], vowel))
    return syllables


if __name__ == '__main__':
    # Playground
    text = input()
    print(re.sub(f'[А-Яа-я]+', word_to_heh, text))
