from pathlib import Path
import pdftotext
import sys


def main(argv):
    with open('output.txt', 'w') as out:
        path = Path(argv[0]).glob("**/*.pdf")
        for src_file in path:
            print('Processing %s' % src_file.absolute())
            with open(src_file, 'rb') as f:
                pdf = pdftotext.PDF(f)
                for page in pdf:
                    out.write(page)


if __name__ == "__main__":
    main(sys.argv[1:])
