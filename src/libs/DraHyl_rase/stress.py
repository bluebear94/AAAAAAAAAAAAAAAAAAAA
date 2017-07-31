from typing import Optional, Tuple

SHORT = 0
LONG = 1
DIPHTHONG_LG = 2
DIPHTHONG_RG = 3

NO_ACCENT = 0 # none or circumflex
VARIANT_ACCENT = 1 # acute
VARIANT_ACCENT_2 = 2 # macron or overdot

A = 0
E = 1
I = 2
O = 3
U = 4
Y = 5

def vowel_constant_to_short(n: int) -> str:
  return "aeiouy"[n]
def vowel_constant_to_long(n: int) -> str:
  return "âêîôûŷ"[n]
def vowel_constant_to_glide(n: int) -> str:
  return "##j#wẏ"[n]
def vowel_constant_to_short_stress(n: int) -> str:
  return "áéíóúý"[n]
def vowel_constant_to_long_lax(n: int) -> str:
  return "āēīōūȳ"[n]
# Used only in times of desperation.
def vowel_constant_to_short_lax(n: int) -> str:
  return "ȧėịȯụẏ"[n]

vowels = "aeiouyâêîôûŷáéíóúýāēīōūȳȧėịȯụẏ"
CLS_SHORT = 0
CLS_LONG = 1
CLS_SHORT_STRESS = 2
CLS_LONG_LAX = 3
CLS_SHORT_LAX = 4

def get_vowel_code(vowel: str) -> Tuple[int, int]:
  index = vowels.index(vowel)
  return (index / 6, index % 6)
def is_vowel(vowel: str) -> bool:
  return vowels.find(vowel) != -1

class Nucleus:
  pass

class Short(Nucleus):
  def __init__(self, vowel: int):
    self.vowel = vowel
  def typ(self) -> int:
    return SHORT
  def decode(self, mode: int) -> Optional[str]:
    if mode == NO_ACCENT:
      return vowel_constant_to_short(self.vowel)
    if mode == VARIANT_ACCENT:
      return vowel_constant_to_short_stress(self.vowel)
  def raised(self) -> Nucleus:
    return Short(self.vowel + (self.vowel % 3 != 2))

class Long(Nucleus):
  def __init__(self, vowel: int):
    self.vowel = vowel
  def typ(self) -> int:
    return LONG
  def decode(self, mode: int) -> Optional[str]:
    if mode == NO_ACCENT:
      return vowel_constant_to_long(self.vowel)
    if mode == VARIANT_ACCENT_2:
      return vowel_constant_to_long_lax(self.vowel)
  def raised(self) -> Nucleus:
    return Long(self.vowel + (self.vowel % 3 != 2))

class DiphthongLG(Nucleus):
  def __init__(self, glide: int, vowel: int):
    self.glide = glide
    self.vowel = vowel
  def typ(self) -> int:
    return DIPHTHONG_LG
  def decode(self, mode: int) -> Optional[str]:
    n = ""
    if mode == NO_ACCENT:
      n = vowel_constant_to_short(self.vowel)
    if mode == VARIANT_ACCENT:
      n = vowel_constant_to_short_stress(self.vowel)
    if mode == VARIANT_ACCENT_2:
      n = vowel_constant_to_short_lax(self.vowel)
    return vowel_constant_to_glide(glide) + n
  def raised(self) -> Nucleus:
    newVowel = self.vowel + (self.vowel % 3 != 2)
    if newVowel == self.glide: return Long(newVowel)
    return DiphthongLG(self.glide, newVowel)

class DiphthongRG(Nucleus):
  def __init__(self, vowel: int, glide: int):
    self.vowel = vowel
    self.glide = glide
  def typ(self) -> int:
    return DIPHTHONG_RG
  def decode(self, mode: int) -> Optional[str]:
    n = ""
    if mode == NO_ACCENT:
      n = vowel_constant_to_short(self.vowel)
    if mode == VARIANT_ACCENT:
      n = vowel_constant_to_short_stress(self.vowel)
    if mode == VARIANT_ACCENT_2:
      n = vowel_constant_to_short_lax(self.vowel)
    return n + vowel_constant_to_glide(glide)
  def raised(self) -> Nucleus:
    newVowel = self.vowel + (self.vowel % 3 != 2)
    if newVowel == self.glide: return Long(newVowel)
    return DiphthongRG(newVowel, self.glide)

# def string_to_nucleus

class MalformedSyllableException(Exception):
  def __init__(self, message):
    self.message = message

valid_short_codas = {
  "p", "t", "ṫ", "k",
  "f", "s", "ṡ", "ḣ", "ħ", "h",
  "m", "n", "ṅ",
  "r", "l"
}

def is_valid_coda_to_short(coda: str) -> bool:
  return coda in valid_short_codas

class Syllable:
  def __init__(self, onset: str, nucleus: Nucleus, coda: str = ""):
    # A syllable cannot have both a diphthong nucleus and a coda
    if nucleus.typ() >= DIPHTHONG_LG and coda != "":
      raise MalformedSyllableException("Can't have both diphthong nucleus and coda!")
    if nucleus.typ() == SHORT and not is_valid_coda_to_short(coda) and coda != "":
      raise MalformedSyllableException(coda + " is not a valid coda to a short vowel!")
    self.onset = onset
    self.nucleus = nucleus
    self.coda = coda
  def decode(self, mode: int) -> Optional[str]:
    nstr = self.nucleus.decode(mode)
    if nstr is None: return None
    return self.onset + nstr + self.coda

exsyll = Syllable("b", Short(I), "m")
exsyll2 = Syllable("b", Long(O))
print(exsyll.decode(NO_ACCENT) + exsyll2.decode(VARIANT_ACCENT_2))