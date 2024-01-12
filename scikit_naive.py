from sklearn.naive_bayes import BernoulliNB
from sklearn import metrics
from vocab_functions import *
from results import save

positive_test = "test\\pos\\"
negative_test = "test\\neg\\"

positive_train = "train\\pos\\"
negative_train = "train\\neg\\"

batch_size = 2500

handler = vocabHandler(n=100, m=1000, k=10)
vocab = {}

acc1 = []
acc2 = []
x=[]

for i in range(10):
    vocab = handler.create_vocab(i)
    y = []

    rev_list_train = []

    for j, review in enumerate(os.listdir(positive_train)):
        if j >= i * batch_size//2 & j < (i+1) * batch_size//2:
            word_list = handler.review_keywords(positive_train + review)
            vec = handler.populate_vector(word_list)
            rev_list_train.append(vec)
            y.append(1)
    for j, review in enumerate(os.listdir(negative_train)):
        if j >= i * batch_size//2 & j < (i+1) * batch_size//2:
            word_list = handler.review_keywords(negative_train + review)
            vec = handler.populate_vector(word_list)
            rev_list_train.append(vec)
            y.append(0)

    classifier = BernoulliNB()

    classifier.fit(rev_list_train, y)

    prediction_train = classifier.predict(rev_list_train)

    acc1.append(metrics.accuracy_score(y, prediction_train))

    x.append(batch_size*(i+1))

    rev_list_test = []

    for review in os.listdir(positive_test):
        word_list = handler.review_keywords(positive_test + review)
        vec = handler.populate_vector(word_list)
        rev_list_test.append(vec)
    for review in os.listdir(negative_test):
        word_list = handler.review_keywords(negative_test + review)
        vec = handler.populate_vector(word_list)
        rev_list_test.append(vec)

    predictions = classifier.predict(rev_list_test)
    accuracy = metrics.accuracy_score(y, predictions)
    acc2.append(accuracy)
    print(f"Loop {i+1} Complete! Accuracy: {accuracy}")

# Evaluate the performance
save("scikit","bayes_acc",x,acc1,acc2,"test")