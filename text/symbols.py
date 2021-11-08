""" from https://github.com/keithito/tacotron """

"""
Defines the set of symbols used in text input to the model.

The default is a set of ASCII characters that works well for English or text that has been run through Unidecode. For other data, you can modify _characters. See TRAINING_DATA.md for details. """

from text import cmudict, pinyin, globalphone
import ipapy

_pad = "_"
_punctuation = "!'(),.:;? "
_special = "-"
_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
_silences = ["@sp", "@spn", "@sil"]

# Prepend "@" to ARPAbet symbols to ensure uniqueness (some are the same as uppercase letters):
_arpabet = ["@" + s for s in cmudict.valid_symbols]
_pinyin = ["@" + s for s in pinyin.valid_symbols]
_globalphone = ["@" + s for s in globalphone.valid_symbols]

# Export all symbols:
"""
symbols = (
    [_pad]
    + list(_special)
    + list(_punctuation)
    + list(_letters)
    + _arpabet
    + _pinyin
    + _silences
    + _globalphone
)
"""

actual_symbols = ['ʀ', 'spn', 'y', 'h', 'ŋ', 'j', 'yː', 'ɡ', 'l̪', 'ə', 'æ', 'ɪ', 'b', 'eː', 'ɞ', 's', 'ø', 'ʃ̺', 'œ', 'ʊ', 'iː', 'm', 'aʊ', 'd̪', 'n̪', 't̪', 'aː', 'v', 'ɑ', 'ç', 'aɪ', 'χ', 'z', 'f', 'ɔɪ', 'p', 'oː', 'ɔ', 'uː', 'ɛ', 'ts', 'k']

symbols = (
    [_pad] 
    + [str(c) for c in ipapy.IPA_CHARS]
    + _silences
)

for s in actual_symbols:
    if s not in symbols:
        print(f"{s} not in symbols, appending")
        symbols.append(s)