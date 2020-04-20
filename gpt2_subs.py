"""
Processes subtitles in SRT format
"""

import re
import sys
import chardet


def srt_to_gpt2(argv):
    with open(argv[0], 'rb') as inp:
        content = inp.read()
        encoding = chardet.detect(content)['encoding']
        content = content.decode(encoding)
        content = re.sub(r'\r\n', '\n', content, flags=re.MULTILINE)  # removes empty lines
        content = re.sub(r'[0-9]{2}:.*\n', '', content, flags=re.MULTILINE)  # removes time codes 00:09:34,400
        content = re.sub(r'^[0-9]+\n', '', content, flags=re.MULTILINE)  # removes line with just numbers
        content = re.sub(r'<i>', '', content, flags=re.MULTILINE)
        content = re.sub(r'</i>', '', content, flags=re.MULTILINE)
        # Line starting with capital letter is considered beginning of sentence
        content = re.sub(r'^([А-Я]|-)', '<BOS>\g<1>', content, flags=re.MULTILINE)
        # Line ending with '.' or '?' or '!' is considered end of sentence
        content = re.sub(r'([.?!])\n', '\g<1><EOS>', content, flags=re.MULTILINE)
        with open(argv[1], 'w', encoding='utf-8') as out:
            out.write(content)


if __name__ == '__main__':
    srt_to_gpt2(sys.argv[1:])
