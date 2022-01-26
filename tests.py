from main import word_to_syllables, generalize_syllables, Syllable, HEH_SYLLABLES

WORDS = ('разъезд', 'абоба', 'купил', 'майка', 'хех', 'в', 'а')
RAW_SYLLABLES = (['разъ', 'езд'], ['а', 'бо', 'ба'], ['ку', 'пил'],
                 ['май', 'ка'], ['хех'], [], ['а'])

SYLLABLES = ([Syllable('хе', 'е'), Syllable('ха', 'а'), Syllable('хе', 'е')],
             [Syllable('хе', 'е'), Syllable('хе', 'е'), Syllable('ха', 'а')],
             [Syllable('ха', 'а'), Syllable('хе', 'е'), Syllable('хе', 'е')])
GENERALIZED_SYLLABLES = ([Syllable('хе', 'е')] * 3,) * 3


def test_word_to_syllables():
    for test, result in zip(WORDS, RAW_SYLLABLES):
        assert [s.value for s in word_to_syllables(test)] == result


def test_generalize_syllables():
    for test, result in zip(SYLLABLES, GENERALIZED_SYLLABLES):
        assert generalize_syllables(test) == result
