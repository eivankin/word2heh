from main import word_to_syllables, generalize_syllables, Syllable

WORDS = ('разъезд', 'абоба', 'купил', 'майка', 'хех', 'в', 'а',
         'психология', 'ааа', 'реальность', 'Я', 'ЛИГА', 'ЗаБоР')
RAW_SYLLABLES = (['разъ', 'езд'], ['а', 'бо', 'ба'], ['ку', 'пил'],
                 ['май', 'ка'], ['хех'], [], ['а'], ['пси', 'хо', 'ло', 'ги', 'я'],
                 ['а'] * 3, ['ре', 'аль', 'ность'], ['Я'], ['ЛИ', 'ГА'], ['За', 'БоР'])

SYLLABLES = ([Syllable('хе', 'е'), Syllable('ха', 'а'), Syllable('хе', 'е')],
             [Syllable('хе', 'е'), Syllable('хе', 'е'), Syllable('ха', 'а')],
             [Syllable('ха', 'а'), Syllable('хе', 'е'), Syllable('хе', 'е')],
             [Syllable('ха', 'а'), Syllable('хех', 'е')])
GENERALIZED_SYLLABLES = ([Syllable('хе', 'е')] * 3,) * 3 + \
                        ([Syllable('хе', 'е'), Syllable('хех', 'е')],)


def test_word_to_syllables():
    for test, result in zip(WORDS, RAW_SYLLABLES):
        output = word_to_syllables(test)
        assert [s.value for s in output] == result
        assert all(s.vowel for s in output)


def test_generalize_syllables():
    for test, result in zip(SYLLABLES, GENERALIZED_SYLLABLES):
        assert generalize_syllables(test, level=1) == result
