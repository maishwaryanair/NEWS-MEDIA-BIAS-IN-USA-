import pyodbc

# this is for a windows authenticated MS SQL server / Management studio
# for a database authentication we need to add UID and PWD
con = pyodbc.connect('Trusted Connection = yes', DRIVER = '{SQL Server}', SERVER = 'Ramiro',
    DATABASE = 'ISDS599_NLP_F')
cur = con.cursor()


###############################################################################
###########Delete the table in the beginning, if any:
cur.execute("""IF OBJECT_ID('ArticleNgrams') is NOT NULL DROP TABLE ArticleNgrams;
                IF OBJECT_ID('Articles') is NOT NULL DROP TABLE Articles;
                IF OBJECT_ID('Ngrams') is NOT NULL DROP TABLE Ngrams;""")
con.commit()


tab1 = """
CREATE TABLE Articles(
Article_ID int IDENTITY(1,1),
Source_ nvarchar(30) NOT NULL,
Raw_Text nvarchar(MAX) NOT NULL,
Processed_Text nvarchar(MAX) NOT NULL,
Unigram_Count int,
CONSTRAINT articleIDpk PRIMARY KEY(Article_ID)
);
"""
cur.execute(tab1)
con.commit()

tab2 = """
CREATE TABLE Ngrams(
Ngram_ID int IDENTITY(1,1),
Ngram_Type nvarchar(10) NOT NULL,
Ngram nvarchar(MAX) NOT NULL,
CONSTRAINT ngramIDpk PRIMARY KEY(Ngram_ID)
);
"""
cur.execute(tab2)
con.commit()

#incase we are starting the data update all over again, this helps to start the primary key from 1 again for the below tables
cur.execute("""DBCC CHECKIDENT ('Articles', RESEED, 1);
                DBCC CHECKINDENT ('Ngrams', RESEED, 1);""")

tab3 = """
CREATE TABLE ArticleNgrams(
/*ArticleNgram_ID int IDENTITY(1,1) Primary key,*/
Article_ID int,
Ngram_ID int,
Frequency Integer,
Std_Frequency Float /*NOT NULL - removed this because for now i am adding this values later*/,
CONSTRAINT articlengramIDpk PRIMARY KEY(Article_ID, Ngram_ID),
CONSTRAINT articleIDfk FOREIGN KEY(Article_ID) REFERENCES Articles(Article_ID) /*ON DELETE CASCADE*/ ON UPDATE CASCADE,
CONSTRAINT ngramIDfk FOREIGN KEY(Ngram_ID) REFERENCES Ngrams(Ngram_ID) /*ON DELETE CASCADE*/ ON UPDATE CASCADE
);
"""
cur.execute(tab3)
con.commit()

con.close()
