import sys
sys.path.insert(0, '../')
from core.tokenizer import detokenize
from colorama import Fore, init


tests = [
    ['¯ \ \ \ _ ( ツ ) _ / ¯', '¯\\\\\\_(ツ)_/¯'],
    ['¯ \ \ _ ( ツ ) _ / ¯', '¯\\\\_(ツ)_/¯'],
    ['¯ \ _ ( ツ ) _ / ¯', '¯\_(ツ)_/¯'],
    ['( ͡ ° ͜ ʖ ͡ ° )', '( ͡° ͜ʖ ͡°)'],
    ['( V ) ( ; , , ; ) ( V )', '(V)(;,,;)(V)'],
    ['< 3', '<3'],
    ['= D', '=D'],
    ['= - D', '=-D'],
    [': )', ':)'],
    ['; )', ';)'],
    [': - )', ':-)'],
    ['; - )', ';-)'],
    [': O', ':O'],
    [': - O', ':-O'],
    [': o', ':o'],
    [': d', ':d'],
    [': D', ':D'],
    [': P', ':P'],
    [': - P', ':-P'],
    [': p', ':p'],
    [': - p', ':-p'],
    [': ]', ':]'],
    [': - ]', ':-]'],
    ['8 )', '8)'],
    ['8 - )', '8-)'],
    ['8 ]', '8]'],
    ['8 - ]', '8-]'],
    ['o . O', 'o.O'],
    ['O . o', 'O.o'],
    ['@ . @', '@.@'],
    ['* . *', '*.*'],
    ['= - )', '=-)'],
    ['= )', '=)'],
    [': (', ':('],
    [': - (', ':-('],
    ['; (', ';('],
    ['; - (', ';-('],
    ['x D', 'xD'],
    ['x - D', 'x-D'],
    ['X D', 'XD'],
    ['X - D', 'X-D'],
    ['@ _ _ @', '@__@'],
    ['@ _ @', '@_@'],
    ['◉ _ ◉', '◉_◉'],
    [': - /', ':-/'],
    ['< / 3', '</3'],
    ['; _ ;', ';_;'],
    ['( ⌐ ■ _ ■ )', '(⌐■_■)'],
    ['( • _ • ) > ⌐ ■ - ■', '( •_•)>⌐■-■'],
    [': \'(', ':\'('],
    ['- _ -', '-_-'],
    ['^ _ ^', '^_^'],
    ['\ \ ( \' u \' ) /', '\\\\(\'u\')/'],
    ['\ ( \' u \' ) /', '\(\'u\')/'],
    ['\ \ ( = ) /', '\\\\(=)/'],
    ['\ ( = ) /', '\(=)/'],
    ['\ \ ( \' - \' ) /', '\\\\(\' - \')/'],
    ['\ ( \' - \' ) /', '\(\' - \')/'],
    ['word . word .', 'word. word.'],
    ['word \' word \'', 'word\'word\''],
    ['word , word ,', 'word, word,'],
    ['word : word :', 'word: word:'],
    ['1 2 3 , 4 5 6', '123,456'],
    ['1 2 3 . 4 5 6', '123.456'],
    ['1 2 3 , abc', '123, abc'],
    ['No . 1 2 3', 'No. 123'],
    ['1 2 3 , abc', '123, abc'],
    ['1 2 3 . abc', '123. abc'],
    ['Hi !', 'Hi!'],
    ['Why ?', 'Why?'],
    ['M . O . R . E .', 'M.O.R.E.'],
    ['word ...', 'word...'],
]

init()

for test in tests:
    detokenized_answers = detokenize([test[0]])
    print('[{}]  {}  ->  {}{}'.format(Fore.GREEN + 'PASS' + Fore.RESET if detokenized_answers[0] == test[1] else Fore.RED + 'FAIL' + Fore.RESET, test[0], test[1], '' if detokenized_answers[0] == test[1] else '  Result: {}'.format(detokenized_answers[0])))
