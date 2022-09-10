import argparse
import re
import os
import pickle

parser = argparse.ArgumentParser(description="Training module")
parser.add_argument('--input-dir', dest='data_folder', help='path to data')
parser.add_argument('--model', dest='model_file', help='path to model')
parser.add_argument('--new', dest='new', type=bool, help='to learn from the very beginning', default=False)
parser.add_argument('--k', dest='k', type=int, help='maximum length of prefix (default 4)', default=4)

args = parser.parse_args()

text = ''
if args.data_folder == None:
    text = input()
else:
    for filename in os.listdir(os.path.join(os.getcwd(), args.data_folder)):
        with open(os.path.join(os.getcwd(), args.data_folder, filename), 'r') as f:
            text += f.read() + ' '
l = []
sentences = text.split('.')
for sentence in sentences:
    tmp = list(map(lambda s: s.lower(), re.findall(r'[\w]+', sentence)))
    tmp.append('.')
    l.extend(tmp)

    
    
if args.new or args.model_file == None:
    nxt = dict()
else:
    with open(args.model_file, 'rb') as stream:
        nxt = pickle.load(stream)
        
        
        
def add_k_grammas(k):
    for i in range(len(l) - k + 1):
        nxt[tuple([l[j] for j in range(i, i + k)])] = dict()
    for i in range(len(l) - k):
        nxt[tuple([l[j] for j in range(i, i + k)])][l[i + k]] = \
        nxt[tuple([l[j] for j in range(i, i + k)])].get(l[i + k], 0) + 1
        

for i in range(1, args.k):
    add_k_grammas(i)

    
    
if args.model_file != None:
    with open(args.model_file, 'wb') as stream:
        pickle.dump(nxt, stream)
