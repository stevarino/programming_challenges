# -*- coding: utf-8 -*-

from collections import deque, namedtuple
from bisect import bisect_left

problem_limit = 68e12
problem_exp = ['thousand', 'million', 'billion']

# Part of a word solution - used for lexigraphical tree and value conversion
WordPart = namedtuple('WordPart', ['multiplier', 'value', 'branches'])


class sorted_deque(object):
    """Implements a sorted deque
        http://stackoverflow.com/questions/4098179/anyone-know-this-python-data-structure
    """
    def __init__(self):
        self.__deque = deque()

    def __len__(self):
        return len(self.__deque)

    def head(self):
        return self.__deque.popleft()

    def tail(self):
        return self.__deque.pop()

    def peek(self):
        return self.__deque[-1]

    def insert(self, obj):
        index = bisect_left(self.__deque, obj)
        self.__deque.rotate(-index)
        self.__deque.appendleft(obj)
        self.__deque.rotate(index)


class Word(object):
    ''''word solution that can generate child words'''
    def __init__(self, words):
        '''constructor'''
        self.words = words
        self.word = ''.join(words)

    @property
    def val(self):
        '''Returns the numeric value of the word'''
        group = 0
        total = 0
        for word in self.words:
            word_def = language[word]
            if word_def.multiplier != 1:
                total += group * word_def.multiplier
                group = 0
            else:
                group += word_def.value
        return group + total

    def children(self):
        '''Generator of valid children'''
        word_def = language[self.words[-1]]
        for word in word_def.branches:
            yield Word(self.words+[word])
        for word in words_exp:
            if word in self.words or self.words[-1] in words_exp:
                return
            yield Word(self.words+[word])

    def __lt__(self, other):
        return self.word < other.word


class Shortcut(object):
    '''Represents a memoized shortcut.'''
    def __init__(self, label, size):
        '''constructor - needs label'''
        self.label = label
        self.size = size
        self.is_active = False
        self.prefix = 0         # length of prefix at init
        self.init_char = 0      # char count at init
        self.len = 0            # normal length without prefix
        self.count = 0

    def check(self, word, char_count, limit):
        '''Can we skip this set? Not if this is our first or last time
        through.'''
        if self.label in word.words:
            if self.len > 0:
                return limit > (char_count + self.jump(word))
            self.count += 1
            if not self.is_active:
                self.is_active = True
                self.init_char = char_count
                self.prefix = len(word.word)
                # print('Started', self.label, char_count, self.prefix)
        elif self.is_active:
            self.is_active = False
            self.len = char_count - self.init_char - self.prefix * self.size
            # print("Stopped", self.label, char_count, self.count)
        return False

    def jump(self, word):
        '''Skipping this branch, how many characters?'''
        return self.len + len(word.word) * self.size

# Build our lexigraphical tree.
words_ones = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight',
              'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen',
              'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen']

words_tens = ['twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy',
              'eighty', 'ninety']

words_hundreds = [w+'hundred' for w in words_ones[0:9]]

words_exp = problem_exp
language = {}

for i, w in enumerate(words_ones):
    language[w] = WordPart(1, i+1, [])
for i, w in enumerate(words_tens):
    language[w] = WordPart(1, 10*(i+2), words_ones[0:9])
for i, w in enumerate(words_hundreds):
    language[w] = WordPart(1, 100*(i+1), words_ones+words_tens)
for i, w in enumerate(words_exp):
    language[w] = WordPart(10**(3*(i+1)), 0,
                           words_ones+words_tens+words_hundreds)


def solve(limit):
    '''Start going through the roots and branching out.'''
    root = words_ones+words_tens+words_hundreds
    words = sorted_deque()
    for word in sorted(root):
        words.insert(Word([word]))
    char_count = 0
    word_count = 0

    shortcuts = [Shortcut("billion", 1e9), Shortcut("million", 1e6),
                 Shortcut("thousand", 1e3)]

    while words:
        word = words.head()
        word_count += 1
        jumped = False
        for shortcut in shortcuts:
            if shortcut.check(word, char_count, limit):
                char_count += shortcut.jump(word)
                jumped = True
        if not jumped:
            char_count += len(word.word)
            for child in word.children():
                words.insert(child)
        if char_count >= limit:
            return char_count, word_count, word.val, word

if __name__ == '__main__':
    import time
    t = time.time()
    c, i, v, w = solve(problem_limit)
    t = time.time() - t
    print("char: ", c)
    print("cnt:  ", i)
    print("val:  ", v)
    print("time: ", t)
    print("word: ", ' '.join(w.words))
