import html
import re
from setup.settings import preprocessing


# inspired by https://github.com/moses-smt/mosesdecoder/blob/master/scripts/tokenizer/tokenizer.perl used in nmt's examples

# Load list of protected words/phrases (those will remain unbreaked, will be not tokenised)
protected_phrases_regex = []
with open(preprocessing['protected_phrases_file'], 'r', encoding='utf-8') as protected_file:
    protected_phrases_regex = list(filter(lambda word: False if word[0] == '#' else True, filter(None, protected_file.read().split("\n"))))

# Tokenize sentense
def tokenize(sentence):
    # Remove special tokens
    sentence = re.sub('<unk>|<s>|</s>', '', sentence, flags=re.IGNORECASE)

    # Decode entities
    sentence = html.unescape(sentence)

    # Strip white charactes
    sentence = sentence.strip()

    # Remove white characters inside sentence
    sentence = re.sub(r'\s+', ' ', sentence)
    sentence = re.sub(r'[\x00-\x1f]', '', sentence)

    # Regex-based protected phrases
    protected_phrases_regex_replacements = []
    for phrase in protected_phrases_regex:

        diffrence = 0
        replacement = 0;

        # If phrase was found in sentence
        if re.search(phrase, sentence):

            # Search for all occurrences and iterate thru them
            regex = re.compile(phrase)
            for p in regex.finditer(sentence):

                # Calculate data
                replace_from = p.groups()[0]
                replace_to = p.groups()[0].replace(" ", "")
                position = p.start(1) + diffrence
                diffrence += -len(replace_from) + len(replace_to)

                # Remove spaces
                sentence = sentence[:position] + sentence[position:].replace(replace_from, ' PROTECTEDREGEXPHRASE{}PROTECTEDREGEXPHRASE '.format(replacement), 1)
                protected_phrases_regex_replacements.append(replace_to)
                replacement += 1

    # Strip spaces and remove multi-spaces
    sentence = sentence.strip()
    sentence = re.sub(r'\s+', ' ', sentence)

    # Protect multi-periods
    m = re.findall('\.{2,}', sentence)
    if m:
        for dots in list(set(m)):
            sentence = sentence.replace(dots, ' PROTECTEDPERIODS{}PROTECTEDPERIODS '.format(len(dots)))

    # Normalize `->' and '' ->"
    sentence = re.sub(r'\`', '\'', sentence)
    sentence = re.sub(r'\'\'', '"', sentence)

    # Separate some special charactes
    sentence = re.sub(r'([^\w\s\.])', r' \1 ', sentence)

    # Separate digits in numbers
    sentence = re.sub(r'([\d])', ' \\1 ', sentence)

    # Split sentence into words
    words = sentence.split()
    sentence = []

    # For every word
    for word in words:

        # Find if it ends with period
        m = re.match('(.+)\.$', word)
        if m:
            m = m.group(1)
            # If string still includes period
            if re.search('\.', m) and re.search(r'[^\w\d_]', m):
                pass

            else:
                word = m + ' .'

        # Add word to a sentence
        sentence.append(word)

    # Join words as a sentence again
    sentence = " ".join(sentence)

    # Strip spaces and remove multi-spaces
    sentence = sentence.strip()
    sentence = re.sub(r'\s+', ' ', sentence)

    # Restore protected phrases and multidots
    sentence = re.sub(r'PROTECTEDREGEXPHRASE([\d\s]+?)PROTECTEDREGEXPHRASE', lambda number: protected_phrases_regex_replacements[int(number.group(1).replace(" ", ""))] , sentence)
    sentence = re.sub(r'PROTECTEDPERIODS([\d\s]+?)PROTECTEDPERIODS', lambda number: ("." * int(number.group(1).replace(" ", ""))), sentence)

    return sentence

# list with regex-based detokenizer rules
answers_detokenize_regex = None

# Load detokenizer rules
with open(preprocessing['answers_detokenize_file'], 'r', encoding='utf-8') as answers_detokenize_file:
    answers_detokenize_regex = list(filter(lambda word: False if word[0] == '#' else True, filter(None, answers_detokenize_file.read().split("\n"))))

# Returns detokenizes sentences
def detokenize(answers):

    detokenized_answers = []

    # For every answer
    for answer in answers:

        # And every regex rule
        for detokenize_regex in answers_detokenize_regex:

            diffrence = 0

            # If detokenize_regex was found in answer
            if re.search(detokenize_regex, answer):

                # Search for all occurrences and iterate thru them
                regex = re.compile(detokenize_regex)
                for p in regex.finditer(answer):

                    # If there are more groups - process spaces that should stay in response
                    if len(p.groups()) > 1:
                        groups = p.groups()[1:]

                        # Replace spaces that should stay with temporary placeholder
                        for i, group in enumerate(groups):
                            position = p.start(i+2) + (i)*22
                            answer = answer[:position] + answer[position:].replace(" ", "##DONOTTOUCHTHISSPACE##", 1)

                        # Update reges to match placeholders as spaces
                        detokenize_regex = detokenize_regex.replace(' ', '(?: |##DONOTTOUCHTHISSPACE##)')

                # Search for all occurrences and iterate thru them again
                regex = re.compile(detokenize_regex)
                for p in regex.finditer(answer):

                    # Calculate data
                    replace_from = p.groups()[0]
                    replace_to = p.groups()[0].replace(" ", "")
                    position = p.start(1) + diffrence
                    diffrence += -len(replace_from) + len(replace_to)

                    # Remove spaces
                    answer = answer[:position] + answer[position:].replace(replace_from, replace_to, 1)

        # Change placeholders back to spaces
        answer = answer.replace("##DONOTTOUCHTHISSPACE##", ' ')

        detokenized_answers.append(answer)

    return detokenized_answers