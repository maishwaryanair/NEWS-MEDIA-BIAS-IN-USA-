## trail for extracting data from database and then inserting them:
import re, pyodbc

con = pyodbc.connect('Trusted Connection = yes', DRIVER = '{SQL Server}', SERVER = 'Ramiro',
    DATABASE = 'ISDS599_NLP_F')
cur = con.cursor()

def freq_entry(article_ID, article):
    q = """INSERT INTO ArticleNgrams(Article_ID, Ngram_ID, Frequency)
        VALUES (?, ?, ?)
        """
    for x,y in ng_lst:
        #match = re.search(y, article) # matching the ngrams of the article with the ngram list
        match = re.findall(r'\b%s\b' % y, article)
        if match:
            #f = len(re.findall(r'\b%s\b' % y, article))
            f = len(match)
            cur.execute(q, (article_ID, x, f))
            con.commit()
        else:
            f = 0
            cur.execute(q, (article_ID, x, f))
            con.commit()

##cur.description - shows the details of the table on which the command is executed
##columns = [column[0] for column in cursor.description] - very useful info ###

#extracting ngramss from the DB
q1 = """ SELECT * from Ngrams;"""
cur.execute(q1)
row1 = cur.fetchall()
 # to see the column names
col_names1 = [c[0] for c in cur.description]
col_names1

ng_lst = [(i[0], i[2]) for i in row1]

#extracting articles from the DB:
q2 = """ SELECT * from Articles;"""
cur.execute(q2)
row = cur.fetchall()
 # to see the column names
col_names = [c[0] for c in cur.description]
col_names

arti_text =[(i[0], i[3]) for i in row]
#freq_entry(text[28]) # just to text the 29th file
for (i, j) in arti_text:
    freq_entry(i, j)


#"""UPDATE TABLE ArticleNgrams SET Frequency = 0 WHERE """
for (i, j) in arti_text:
    alter2 = """UPDATE ArticleNgrams
            SET Std_Frequency = (CAST(Frequency AS float)/(SELECT sum(Frequency) FROM ArticleNgrams WHERE Article_ID = ?))
            WHERE Article_ID = ?;
        """
    #INSERT INTO ArticleNgrams(Std_Frequency) (SELECT an.Frequency/a.Word_Count FROM ArticleNgrams As an, Articles As a WHERE an.Article_ID = a.Article_ID);
    cur.execute(alter2, (i, i,))
    con.commit()

con.close()
