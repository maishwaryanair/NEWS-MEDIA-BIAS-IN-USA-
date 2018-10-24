import re, pyodbc
con = pyodbc.connect('Trusted Connection = yes', DRIVER = '{SQL Server}', SERVER = 'Ramiro',
    DATABASE = 'ISDS599_NLP_F')
cur = con.cursor()

cur.execute("""DELETE FROM Articles;""")
con.commit()
#Creating dict for appostrophes
Appo = {"'s" : "is", "it\'s" : "it is", "you\'re" : "you are", "they\'ve" : "they have", "i'm" : "I am", "i\'m" : "i am", "it\'s" : "it is", "i've" : "I have", "i\'ve" : "i have",
        "haven\'t" : "have not", "didn\'t" : "did not", "isn\'t" : "is not", "hasn\'t": "has not",
        "wasn\'t" : "was not", "doesn\'t" : "does not", "hadn\'t" : "had not", "aren\'t" : "are not", "\'ll" : "will" }

#for FOX NEWS Articles
for i in range(01,103):
    string = open('file%s.txt' %i).read().lower()
    string = re.sub('\s+', ' ', string) #pleacing a dot at the end of the sentence with a new line break
    text = string.split()
    r_text = [Appo[j] if j in Appo else j for j in text] #replacing the appostrophes
    r_text = " ".join(r_text)
    #string = r_text.replace('["?!;:,]', '.') # this is not working!!
    new_s = re.sub('[^a-zA-Z\n\.?!;:,'']', ' ', string) # special characters = [^a-zA-Z0-9\n\.]
    new_s = re.sub('[";?:!,]', '.', new_s)
    new_s = re.sub('\s+', ' ', new_s)
    #new_string = new_string.replace('.','').lower()
    open('pfile%s.txt' %i, 'w').write(new_s)
#for MSNBC Articles
for i in range(01,103):
    string = open('nfile%s.txt' %i).read().lower()
    string = re.sub('\s+', ' ', string)
    text = string.split()
    r_text = [Appo[j] if j in Appo else j for j in text]
    r_text = " ".join(r_text)
    #string = r_text.replace('["?!;:,]', '.') # this is not working!!
    new_s = re.sub('[^a-zA-Z\n\.?!;:,'']', ' ', string) # special characters = [^a-zA-Z0-9\n\.]
    new_s = re.sub('[";?:!,]', '.', new_s)
    new_s = re.sub('\s+', ' ', new_s)
    #new_string = new_string.replace('.','').lower()
    open('pnfile%s.txt' %i, 'w').write(new_s)

import io # codecs it reads all encoding without mentioning them in open() but not able parse to SQL

#for FOX NEWS articles:
for i in range(1,103):
    try:
        f = io.open('file%s.txt' %i, 'r').read() #Added exception handling for different types of encoding of Articles
    except UnicodeDecodeError:
        f = io.open('file%s.txt' %i, 'r', encoding = 'utf-8').read()
    else:
        f = io.open('file%s.txt' %i, 'r', encoding = 'CP1252').read()
    g = open('pfile%s.txt' %i, 'r').read()
    c = len(g.split())
    q = """INSERT INTO Articles(Source_, Raw_Text, Processed_Text, Unigram_Count)
    VALUES('Fox News', ?, ?, ?);"""
    #ID = "Fox_%s" %i  ## initially had an idea to form a primay key with char in it
    cur.execute(q,(f,g,c,))

# for MSNBC articles:
for i in range(1,103):
    try:
        f = io.open('nfile%s.txt' %i, 'r').read() #Added exception handling for different types of encoding of Articles
    except UnicodeDecodeError:
        f = io.open('nfile%s.txt' %i, 'r', encoding = 'utf-8').read()
    else:
        f = io.open('nfile%s.txt' %i, 'r', encoding = 'CP1252').read()
    g = open('pnfile%s.txt' %i, 'r').read()
    c = len(g.split())
    q = """INSERT INTO Articles(Source_, Raw_Text, Processed_Text, Unigram_Count)
    VALUES('MSNBC', ?, ?, ?);"""
    #ID = "Fox_%s" %i  ## initially had an idea to form a primay key with char in it
    cur.execute(q,(f,g,c,))

con.commit()

con.close()
