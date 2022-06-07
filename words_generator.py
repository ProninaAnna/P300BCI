import random
filename = r"\\5_letter_words.txt"

def get_words_list(filename):
    with open(filename, 'r') as f:
        lines=f.readlines()
    words=[]
    for line in lines:
        words.extend(line.split())
    l=[]
    for word in words:
        l.append(word)
    return l

def generate_words_sample(filename, seed=None):
    words= get_words_list(filename)
    if seed:
        random.seed(seed)            
    sample=random.sample(words, 4)
    return sample

print(generate_words_sample(filename))