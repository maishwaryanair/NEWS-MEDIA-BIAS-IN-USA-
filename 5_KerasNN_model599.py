import keras
import pyodbc
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
import numpy as np
import sklearn
import h5py, json
from sklearn.model_selection import train_test_split

con = pyodbc.connect('Trusted Connection = yes', DRIVER = '{SQL Server}', SERVER = 'Ramiro',
    DATABASE = 'ISDS599_NLP_F')
cur = con.cursor()

cur.execute("""SELECT a.Article_ID, an.Std_Frequency, a.Source_
                from Articles a JOIN ArticleNgrams an ON a.Article_ID = an.Article_ID
                JOIN Ngrams n ON an.Ngram_ID = n.Ngram_ID
                WHERE n.Ngram_Type = 'Unigram';""")
row = cur.fetchall()

articles = dict()
for r in range(1,205):
    for i in row:
        if i[0] == r:
            articles.setdefault(r, []).append(i[1:3])

articles_lst = []
for i in articles:
    b = articles[i]
    x = [i for sub in b for i in sub]
    if x[-1] == 'Fox News':
        x1 = list(filter(lambda a: a != 'Fox News', x))
        x1.append(0)
        x1.append(1)
    else:
        x1 = list(filter(lambda a: a != 'MSNBC', x))
        x1.append(1)
        x1.append(0)
    articles_lst.append(x1)

dataset = np.array(articles_lst)


#randomly splitting the dataset into training and testing sets(70-30)
train_dataset, test_dataset = train_test_split(dataset, test_size = 0.3, random_state = 1)
# training data
train_inputdata = train_dataset[:,0:9742]
train_output = train_dataset[:,9742:9744]
# testing data
test_inputdata = test_dataset[:,0:9742]
test_output = test_dataset[:,9742:9744]

# creating the model with three layers
model = Sequential()
model.add(Dense(10000, input_dim = 9742, activation ='relu')) # input layer
model.add(Dense(400, activation ='relu')) # hidden layer
model.add(Dense(2, activation ='softmax')) # output layer

# Compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Fit the model
model.fit(train_inputdata, train_output, epochs=100)

# using training set evaluate the model - it is usually 100% since the model has already seen the data
print("\n Now validating the model using training dataset:\n")
scores = model.evaluate(train_inputdata, train_output)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

# evaluate the model with test data
print("\n Now validating the model using test data:\n")
scores = model.evaluate(test_inputdata, test_output)
print("\n%s: %.2f%%\n" % (model.metrics_names[1], scores[1]*100))


con.close()
