import nltk, pyodbc, re
from nltk.util import ngrams

con = pyodbc.connect('Trusted Connection = yes', DRIVER = '{SQL Server}', SERVER = 'Ramiro',
    DATABASE = 'ISDS599_NLP_F')
cur = con.cursor()

cur.execute(""" DELETE from Ngrams""")
con.commit()

ng_lst_uni =[]
ng_lst_bi =[]
ng_lst_tri =[]
ng_lst_four =[]
ng_lst_five =[]

def CreateNgs(article_text, id):
    ng_lst_u = []
    ng_lst_b = []
    ng_lst_t = []
    ng_lst_fo = []
    ng_lst_fi = []
    text = str(article_text) #converting the unicode text into string
    text_split = re.split(r'(?<=\w\.)\s',text)
    for i in text_split:
        unigram = nltk.word_tokenize(i)
        if '.' in set(unigram): #here i am using set() because it doesn't have aindex function, so it wont go like '.' in uni[0],[1],[2]...
            unigram = filter(lambda a: a != '.', unigram)
         #removing the fot from the end of the list
        bigrams = ngrams(unigram, 2)
        trigrams = ngrams(unigram, 3)
        fourgrams = ngrams(unigram, 4)
        fivegrams = ngrams(unigram, 5)
        ng_lst_uni.extend(unigram)
        #print set(ng_lst_uni) #to check the ouput
        ng_lst_bi.extend(bigrams)
        ng_lst_tri.extend(trigrams)
        ng_lst_four.extend(fourgrams)
        ng_lst_five.extend(fivegrams)
        ng_lst_u.extend(unigram)# for ngram count article
        ng_lst_b.extend(bigrams)
        ng_lst_t.extend(trigrams)
        ng_lst_fo.extend(fourgrams)
        ng_lst_fi.extend(fivegrams)
    #To calculate and enter the ngramss count to articles table
    q = """UPDATE Articles SET Unigram_Count = ? WHERE Article_ID = ?;"""
    cur.execute(q, (len(ng_lst_u), id,))
    #print set(ng_lst_uni) #to check the
    q = """UPDATE Articles SET Bigram_Count = ? WHERE Article_ID = ?;"""
    cur.execute(q, (len(ng_lst_b), id,))
    q = """UPDATE Articles SET Trigram_Count = ? WHERE Article_ID = ?;"""
    cur.execute(q, (len(ng_lst_t), id,))
    q = """UPDATE Articles SET Fourgram_Count = ? WHERE Article_ID = ?;"""
    cur.execute(q, (len(ng_lst_fo), id,))
    q = """UPDATE Articles SET Fivegram_Count = ? WHERE Article_ID = ?;"""
    cur.execute(q, (len(ng_lst_fi), id,))
    con.commit()

# fetching articles from DB
q = """ SELECT * from Articles"""
cur.execute(q)
row = cur.fetchall()
 # to see the column names
col_names = [c[0] for c in cur.description]
col_names

text =[(i[0], i[3]) for i in row]
for i, j in text:
    CreateNgs(j,i)

def NgsEntry(ngram_lst, ngram_type):
    for i in set(ngram_lst):
        text = " ".join(i)
        q = """INSERT INTO Ngrams(Ngram_Type, Ngram)
            VALUES(?,?);
            """
        cur.execute(q, (ngram_type, text,))
        con.commit()

##### Entering unigrams to DB
for i in set(ng_lst_uni): #set() is used to remove all duplicate values from the list
    q = """INSERT INTO Ngrams(Ngram_Type, Ngram)
        VALUES('Unigram', ?);
        """
    cur.execute(q, (i,))
    con.commit()

### Entering the entire list of ngrams into the DB
NgsEntry(ng_lst_bi, 'Bigram')
NgsEntry(ng_lst_tri, 'Trigram')
NgsEntry(ng_lst_four, 'Fourgram')
NgsEntry(ng_lst_five, 'Fivegram')


con.commit()
con.close()
