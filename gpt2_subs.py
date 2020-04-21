"""
Processes subtitles in SRT format
"""

import re
import sys
import chardet

EOS = 'EOS'
BOS = 'BOS'


def srt_to_gpt2(argv):
    if argv[0] == 'validate':
        with open(argv[1], 'r', encoding='UTF-8') as inp:
            detect_mismatches("".join(inp.readlines()))
            return 0

    with open(argv[0], 'rb') as inp:
        content = inp.read()
        encoding = chardet.detect(content)['encoding']
        content = content.decode(encoding)
        content = re.sub(r'\r\n', '\n', content, flags=re.MULTILINE)  # removes empty lines
        content = re.sub(r'[0-9]{2}:.*\n', '', content, flags=re.MULTILINE)  # removes time codes 00:09:34,400
        content = re.sub(r'^[0-9]+\n', '', content, flags=re.MULTILINE)  # removes line with just numbers
        content = re.sub(r'(\n)\.\s*', '\g<1>', content, flags=re.MULTILINE)  # removes leading dot symbol and all subsequent whitespaces
        content = re.sub(r'<i>', '', content, flags=re.MULTILINE)
        content = re.sub(r'</i>', '', content, flags=re.MULTILINE)
        # Line starting with capital letter is considered beginning of sentence
        #content = re.sub(r'^([А-Я]|-)', '<BOS>\g<1>', content, flags=re.MULTILINE)
        # Line ending with '.' or '?' or '!' is considered end of sentence (but not trailing '...')
        content = re.sub(r'([.?!]\n)(?<!([.]{3}\n))', '\g<1><EOS>\n<BOS>', content, flags=re.MULTILINE)
        with open(argv[1], 'w', encoding='utf-8') as out:
            out.write(content)

        detect_mismatches(content)


def detect_mismatches(content):
    unmatched = 0
    token = EOS
    for m in re.finditer(r'([BE]OS)', content):
        if token == BOS and m.group(1) != EOS:
            unmatched += 1
            print('>{}~~~>{}<~~~<'.format(unmatched, content[m.start() - 20: m.end() + 20:]))
        elif token == EOS and m.group(1) != BOS:
            unmatched += 1
            print('>{}~~~>{}<~~~<'.format(unmatched, content[m.start() - 20: m.end() + 20:]))
        else:
            if token == BOS:
                token = EOS
            else:
                token = BOS
    print('Unmatched BOS/EOS pairs {}'.format(unmatched))


if __name__ == '__main__':
    srt_to_gpt2(sys.argv[1:])
