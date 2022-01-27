from dataclasses import dataclass

from constants import VOWELS, CONSONANTS

MAX_SIMILARITY = 3
SIMILAR_VOWELS = {('а', 'я'), ('е', 'э')}


@dataclass
class Syllable:
    value: str
    vowel: str

    def __str__(self) -> str:
        return self.value

    def similarity(self, other: 'Syllable') -> int:
        return self.vowel_similarity(other) + \
               ((self.value[-1].lower() in VOWELS) == (other.value[-1].lower() in VOWELS))

    def vowel_similarity(self, other: 'Syllable') -> int:
        return (self.vowel == other.vowel) * 2 + (tuple(
            sorted((self.vowel, other.vowel))) in SIMILAR_VOWELS)

    def agree_case_with(self, other: 'Syllable') -> 'Syllable':
        result = ''
        for my_letter, other_letter in zip(self.value, other.value + 'а' * (
                len(self.value) - len(other.value))):
            result += my_letter.upper() if other_letter.isupper() else my_letter.lower()
        return Syllable(result, self.vowel)

    def agree_closeness_with_heh(self, other: 'Syllable') -> 'Syllable':
        value = self.value
        if other.is_close() != self.is_close():
            value = value[:-1] if self.is_close() else value + 'х'
        return Syllable(value, self.vowel)

    def is_close(self) -> bool:
        return self.value[-1] in CONSONANTS

    def __hash__(self) -> int:
        return hash((self.value.lower(), self.vowel))

    def __eq__(self, other: 'Syllable') -> bool:
        return self.value.lower() == other.value.lower()


HEH_SYLLABLES: set[Syllable] = set(
    Syllable('х' + vowel + end, vowel) for vowel in ('а', 'е', 'и') for end in ('', 'х'))
