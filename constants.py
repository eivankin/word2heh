DEBUG = True
HEH_RATE = 1 if DEBUG else .25
HEH_LEVEL = 0.4
VOWELS: set[str] = set('уеыаоэяию')
# Й, Ъ, Ь пропущены, так как с них не может начинаться слог
CONSONANTS: set[str] = set('цкнгшщзхфвпрлджчсмтб')
