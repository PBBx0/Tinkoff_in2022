import argparse
import pickle
import random


parser = argparse.ArgumentParser(description="Generating module")
parser.add_argument('--model', dest='model_file', help='path to model')
parser.add_argument('--prefix', dest='prefix', nargs='+', help='start of the sentence')
parser.add_argument('--length', dest='length', type=int, help='quantity of words to generate if unset then generates before \'.\' sigh')

args = parser.parse_args()
nxt = dict()
with open(args.model_file, 'rb') as stream:
    nxt = pickle.load(stream)

def get_next_word(words):
    while words not in nxt.keys():
        words = words[1:]
        if len(words) == 0:
            print("Something's wrong")
            return '.'
    probability = random.random() * sum(nxt[words].values())
    for w, p in nxt[words].items():
        probability -= p
        if probability <= 0:
            return w
        
def get_next(words):
    while words not in nxt.keys():
        words = words[1:]
        if len(words) == 0:
            print("Something's wrong")
            return '.'
    w = get_next_word(words)
    tmp = list(words)
    tmp.append(w)
    return tuple(tmp)

def print_sentence(prefix):
    print(*prefix, end=' ')
    while prefix[-1] != '.':
        prefix = get_next(prefix)
        print(prefix[-1], end=' ')
    print('\n')


def print_word_sequence(k, prefix):
    print(*prefix, end=' ')
    for i in range(k):
        prefix = get_next(prefix)
        print(prefix[-1], end=' ')
    print('\n')
    
if args.prefix == None:
    args.prefix = tuple((get_next_word(tuple('.')),))
    args.length -= 1

if args.length == None:
    print_sentence(tuple(args.prefix))
else:
    print_word_sequence(args.length, tuple(args.prefix))