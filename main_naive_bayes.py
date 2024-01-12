from vocab_functions import *
from naive_bayes import calc_prob, naive_bayes_run
from results import plot_results

handler = vocabHandler(n=100,m=1000,k=10)

batch_size = 2500

positive_test = "test\\pos\\"
negative_test = "test\\neg\\"

positive_train = "train\\pos\\"
negative_train = "train\\neg\\"

x = []
rev_list = []
res_tests = []
res_trs = []
label = []

for i in range(10):
    vocab = handler.create_vocab(i)
    print(f"Total mes: {handler.get_sum()}")
    print(f"Total pos mes: {handler.sum_mes_pos}")
    feat_prob = calc_prob(vocab, handler.get_sum(), handler.sum_mes_pos)

    for review in os.listdir(positive_train):
        word_list = handler.review_keywords(positive_train + review)
        vec = handler.populate_vector(word_list)
        rev_list.append(vec)
        label.append("pos")
    for review in os.listdir(negative_train):
        word_list = handler.review_keywords(negative_train + review)
        vec = handler.populate_vector(word_list)
        rev_list.append(vec)
        label.append("neg")

    res_tr, ans_tr = naive_bayes_run(rev_list, label, feat_prob, handler.vocab_list)
    res_trs.append(res_tr)

    x.append(batch_size*(i+1))

    rev_list.clear()

    for review in os.listdir(positive_test):
        word_list = handler.review_keywords(positive_test + review)
        vec = handler.populate_vector(word_list)
        rev_list.append(vec)
    for review in os.listdir(negative_test):
        word_list = handler.review_keywords(negative_test + review)
        vec = handler.populate_vector(word_list)
        rev_list.append(vec)
    
    res_test, ans_test = naive_bayes_run(rev_list, label, feat_prob, handler.vocab_list)
    res_tests.append(res_test)

    rev_list.clear()
    label.clear()
    print(f"Loop {i+1} complete! Accuracy: {(res_test[0][0]+res_test[1][1])/(res_test[0][0]+res_test[0][1]+res_test[1][0]+res_test[1][1])}")

plot_results("test", "naive", x, res_tests, res_trs)