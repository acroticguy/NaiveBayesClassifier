from IG_Functions import calculate_IGs
import os
import re
import json

class vocabHandler:

    def __init__(self, n, m, k) -> None:
        self.dir_t_pos = os.listdir("train\\pos\\")
        self.dir_t_neg = os.listdir("train\\neg\\")


        self.vocab = {}
        self.n = n
        self.m = m
        self.k = k
        self.sum_mes_neg = 0
        self.sum_mes_pos = 0

    def export_vocab(self, filename):
        with open(filename + ".json", 'w') as json_file:
            json.dump(self.vocab, json_file)

    def import_vocab(filepath):
        try:
            with open(filepath, 'r') as json_file:
                vocab = json.load(json_file)
            return vocab
        except FileNotFoundError:
            return None

    def review_keywords(self, filename):
        try:
            with open(filename, encoding="utf8") as f:
                content = f.read()
        except Exception as e:
            print(f"File Could not be read. Error: {e}")
            return None

        #I noticed a few files had <br> and </br> tags, so I used Regex to remove them, and then kept all occurences of words, excluding punctuation and special characters
        content = re.sub(r'<br\s*\/?>', '', content)

        #returning a Set, in order to remove duplicates
        return set(re.findall(r'\b\w+\b', content.lower()))

    def create_vocab(self, i):

        for index in range(int(len(self.dir_t_pos) * i * 10/100), int(len(self.dir_t_pos) * (i+1) * 10/100)):
            word_list = self.review_keywords("train\\pos\\" + self.dir_t_pos[index])

            if (word_list):
                for key in word_list:
                    #Dictionaries have method get(), where you can set a default value if the key doesn't yet exist. In our case, we set vocab[key] to [0,0] by default, and always add +1 on word occurences.
                    #Since all of our words here belong in positive reviews, we also add +1 to our second element of the list, indicating that the word showed up in a positive review
                    self.vocab[key] = [self.vocab.get(key, [0, 0])[0] + 1, self.vocab.get(key, [0, 0])[1] + 1]
                self.sum_mes_pos += 1

        for index in range(int(len(self.dir_t_neg) * i * 10/100), int(len(self.dir_t_neg) * (i+1) * 10/100)):
            word_list = self.review_keywords("train\\neg\\" + self.dir_t_neg[index])

            if (word_list):
                for key in word_list:
                    #In the case of negative reviews, we only add occurences of the words, and never add to the second element of the list.
                    #Similarily, using get(), we either get the value of vocab[key], or [0,0], then add 1 to the first element of the list.
                    self.vocab[key] = [self.vocab.get(key, [0, 0])[0] + 1, self.vocab.get(key, [0, 0])[1]]
                self.sum_mes_neg += 1

        #REMOVE TOP N AND BOTTOM K WORDS FROM VOCAB, THEN RETURN M TOP WORDS FROM THE RESULT
        self.vocab = dict(sorted(self.vocab.items(), key=lambda item: item[1][0], reverse=True))

        # self.vocab = dict(list(self.vocab.items())[self.n:]) # remove n first elements
        # self.vocab = dict(list(self.vocab.items())[:-self.k]) # remove k last elements

        self.vocab_ig = calculate_IGs(self.vocab, self.get_sum(), self.sum_mes_pos)

        self.vocab_ig = dict(list(self.vocab_ig.items())[:self.m]) # keep m first elements from the resulting list

        self.vocab = {key: [self.vocab[key][0], self.vocab[key][1]] for key in self.vocab.keys() if key in self.vocab_ig.keys()}
        self.vocab_list = {key: i for i, key in enumerate(self.vocab.keys())}
        return self.vocab

    def populate_vector(self, review):
        vector = [0 for i in range(len(self.vocab_list))]
        for word in review:
            if word in self.vocab_list:
                vector[self.vocab_list[word]] = 1
        return vector
    
    def clear(self):
        self.sum_mes_neg = 0
        self.sum_mes_pos = 0
        self.vocab = {}

    def get_sum(self):
        return self.sum_mes_neg + self.sum_mes_pos