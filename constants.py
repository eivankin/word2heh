DEBUG = True
HEH_RATE = 1 if DEBUG else .3
HEH_LEVEL = 1
VOWELS: set[str] = set('уеыаоэяиюё')
# Й, Ъ, Ь пропущены, так как с них не может начинаться слог
CONSONANTS: set[str] = set('цкнгшщзхфвпрлджчсмтб')
