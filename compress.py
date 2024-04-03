import random
import string
import nltk
from collections import Counter

# give truth to each three letter combination of letters
truth_table = {}

lowercase_letters = string.ascii_lowercase

word_dict = nltk.corpus.words.words()

# all words should be lowercase
word_dict = [word.lower() for word in word_dict]
# remove symbols
word_dict = [word for word in word_dict if word.isalpha()]

# build a table that maps X to the most common characters next to XXX
next_to_x = {}

for i in lowercase_letters:
    for j in lowercase_letters:
        for k in lowercase_letters:
            for l in lowercase_letters:
                next_to_x[i + j + k + l] = Counter()

for word in word_dict:
    for i in range(len(word) - 4):
        next_to_x[word[i:i+4]][word[i+4]] += 1

# trigger .most_common for each
for key in next_to_x:
    next_to_x[key] = next_to_x[key].most_common()

# print(next_to_x)

# trith table should be every combination of 3 lowercase letters
for i in lowercase_letters:
    for j in lowercase_letters:
        for k in lowercase_letters:
            for l in lowercase_letters:
                # use the most common letter that comes after i, j, k
                if len(next_to_x[i + j + k + l]) > 0:
                    truth_table[i + j + k + l] = next_to_x[i + j + k + l][0][0]
                else:
                    truth_table[i + j + k + l] = random.choice(lowercase_letters)

K = 5

word_count_for_each_state = {w: 0 for w in truth_table.values()}

# nodes = [random.choice(lowercase_letters) for _ in range(K)]
nodes = list("baaab")

connections = {
    k: [random.randint(0, K - 1) for k in range(4)] for k in range(K)
}
# coffee = 291
# aaaaa = 1111
# zzzzz = 908
# 10m iters w/ aaaaa as seeed = 3458

found_words = set(nltk.corpus.words.words())

unique_words = {}
state_counts = {}

# count # of words of length K
total_words_to_find = 0

for word in found_words:
    if len(word) == K:
        total_words_to_find += 1

iters = 0

with open("output.txt", "w") as f:
    while iters < 10000: # 10_000_000:
        new_nodes = nodes.copy()

        for i in range(K):
            inputs = "".join([str(nodes[k]) for k in connections[i]])
            new_nodes[i] = truth_table[inputs]

        nodes = new_nodes

        iters += 1
        state = "".join(nodes)
        if state not in state_counts:
            state_counts[state] = 0

        state_counts[state] += 1
        # flip a random bit if state count > 10
        if state_counts[state] > 3: # or state in found_words:
            print("Flipping a random bit for state", state)
            idx = random.randint(0, K - 1)
            # get 2nd most common letter if available
            if next_to_x.get(state[idx-2:idx+1]) and len(next_to_x[state[idx-2:idx+1]]) > 1:
                print("Getting nth most common letter")
                word_count_for_each_state[state[idx]] += 1
                nth_common = word_count_for_each_state[state[idx]]
                # if nth common exceeds the number of common letters, reset to 0
                if nth_common >= len(next_to_x[state[idx-2:idx+1]]):
                    nth_common = 0
                    word_count_for_each_state[state[idx]] = 0
                new_nodes[idx] = next_to_x[state[idx-2:idx+1]][nth_common][0]
            # else:
            #     new_nodes[idx] = random.choice(lowercase_letters)
            state_counts[state] = 0
        
        #add to unique words
        if state in found_words:
            unique_words[state] = iters

        print(len(unique_words),  total_words_to_find)

    for word, iteration in unique_words.items():
        f.write(f"{word}, {iteration}\n")