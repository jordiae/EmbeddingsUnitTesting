import sys
import os
import magic


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def is_float(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def check(file_lines):
    if len(file_lines[0].split()) != 2:
        return False, 'First line should have nwords and embeddings dimension'
    nwords, dim = file_lines[0].split()
    if not is_int(nwords) or not is_int(dim):
        return False, 'nwords, embedding dimension are not ints: ' + nwords + ' ' + dim
    nwords, dim = int(nwords), int(dim)
    if nwords <= 0 or dim <= 0:
        return False, 'nwords, embedding dimension must be > 0:' + str(nwords) + ' ' + str(dim)
    if len(file_lines) != nwords + 1:
        return False, 'File has ' + str(len(file_lines)) + ' lines instead of nwords + 1 (' + str(nwords + 1) + ')'
    vocab = set([])
    for index, line in enumerate(file_lines[1:]):
        toks = line.split()
        if len(toks) != dim + 1:
            return False, 'Line ' + str(index+1) + ' has ' + str(len(toks)) +\
                   ' tokens instead of dim + 1 (' + str(dim + 1) + ')' + '\n' + line
        if toks[0] in vocab:
            return False, 'Token ' + toks[0] + ' appears more than once'
        else:
            vocab.add(toks[0])
        for index_tok, tok in enumerate(toks[1:]):
            if not is_float(tok):
                return False,  'Line ' + str(index+1) + ' has a non-float in position ' + str(index_tok) + ': '\
                       + str(tok)
    return True, None


def main():
    if len(sys.argv) == 1:
        print('Usage: python3 main.py [EMBEDDINGS FILEPATH LIST]')
        return
    m = magic.Magic(mime=True)
    for filepath in sys.argv[1:]:
        if not os.path.exists(filepath):
            print('Error:', filepath, 'does not exist')
            continue
        if not os.path.isfile(filepath):
            print('Error:', filepath, ': not a file')
            continue
        if m.from_file(filepath) != 'text/plain':
            print('Error:', filepath, ': not a plain text file')
            continue
        try:
            file_lines = open(filepath, 'r').readlines()
        except BaseException as e:
            print('Error:', filepath, ':', str(e))
            continue
        print('Checking', filepath)
        ok, message = check(file_lines)
        if ok:
            print(filepath, 'seems ok')
        else:
            print(filepath, 'not ok:', message)


if __name__ == '__main__':
    main()
