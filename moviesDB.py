# Importing Libraries

import pymysql
import pymongo


myclient = None
db = None
dbpaswd = None

#Connects to mysql database. User will be asked for db password
def connect_sql():
    global db
    global dbpaswd
    try:
        
        # Asks user to enter DB password if none has entered yet
        if dbpaswd == None:
            dbpaswd = input("ENTER DB PASSWORD: ")
        db = pymysql.connect(host="localhost", user="root", password=dbpaswd, db="moviesdb", cursorclass=pymysql.cursors.DictCursor)
    
    #If db password is incorrect, exception will be caught and user will be asked for db password again
    #until db password is correct
    except pymysql.err.OperationalError as e:
        while e:
            dbpaswd = input("DB PASSWORD INVALID, TRY AGAIN: ")
            connect_sql()
            break
            
# Creates a connection with mongoDB
def connect_mongo():
    global myclient
    myclient = pymongo.MongoClient()
    myclient.admin.command('ismaster')


def view_movies():
    
    # if not connected to DB, it will connect
    if (not db):
        connect_sql()
    try:
        
        # if DB is not open, it will reconnect
        if not (db.open):
            connect_sql()
    except AttributeError as e:
        print(e)
    
    sql = """
            select F.FilmName, A.ActorName
            from film F
            inner join filmcast FC on FC.CastFilmID = F.FilmID
            inner join actor A on FC.CastActorID = A.ActorID
            order by f.FilmName, A.ActorName
            
          """
    try:
        with db:
            cursor = db.cursor()
            cursor.execute(sql)
            return cursor.fetchall()
    except Exception as e:
        print(e)

def view_act_yob_gender(yob,gender):
    
    # if not connected to DB, it will connect
    if (not db):
        connect_sql()
    
     # if DB is not open, it will reconnect
    if not (db.open):
        connect_sql()
    
    # because where condition is "like", it will either get all actors for specific YOB or all actors for any year of decade
    # as in 1980, or 198x
    sql = """
            select ActorName, ActorDOB, ActorGender
            from actor
            where ActorDOB like %s
            and ActorGender like %s
          """  
    with db:
        cursor = db.cursor()
        cursor.execute(sql, ("%"+yob+"%","%"+gender+"%"))
        return cursor.fetchall()


def view_studios():
    
    # if not connected to DB, it will connect
    if (not db):
        connect_sql()
    
     # if DB is not open, it will reconnect
    if not (db.open):
        connect_sql()
  
    sql = """
            select * from studio
            order by StudioID
        """
    
    with db:
        cursor = db.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

def add_country(CountryID, CountryName):
    
    # if not connected to DB, it will connect
    if (not db):
        connect_sql()
    
    # if DB is not open, it will reconnect
    if not (db.open):
        connect_sql()
    
    
    sql = "insert into country values (%s, %s)"

    with db:
        try:
            cursor = db.cursor()
            cursor.execute(sql, (CountryID, CountryName))
            db.commit()
            print("")
            print("Country:", CountryID, ", ",CountryName, "added to database")

        except pymysql.err.IntegrityError as e:
            print("")
            print("*** ERROR ***: ID and/or Name (", CountryID,", ", CountryName, ") already exists")
        except pymysql.err.DataError as e:
            print(e)
        except Exception as e:
            print(e)


# Checking if language for option 5 exists in mongoDB docs
def find(language):
    
    # Creating mongo query
    mydb = myclient['movieScriptsDB']
    docs = mydb["movieScripts"]
    query = {"subtitles": language}
    people = docs.find(query)
    
    # Creating a list from mongo query with language_id for subtitles codes already in mongo collection
    language_id = []
    for p in people:
        language_id.append(p["_id"])
    
    return(language_id)


def view_movies_subtitles(language):
    
    # if not connected to DB, it will connect
    if (not db):
        connect_sql()
    
    # if DB is not open, it will reconnect
    if not (db.open):
        connect_sql()

    # if MONGO is not connected yet, it will connect
    if (not myclient):
        connect_mongo()
    

    # sql query list from list obtained on the "find" function
    # creates variable "id_tuple" from find function    
    id_tuple = tuple(find(language))
    
    while id_tuple:
        
        sql = """ 
                select FilmName, concat(substring(FilmSynopsis,1,30),'...') as Synopsis
                from film
                where FilmID in %s
                """  

        with db:
            cursor = db.cursor()
            cursor.execute(sql, (id_tuple,))
            return cursor.fetchall()


def add_movscript(film_id, keyword, language):
    
    # if MONGO is not connected yet, it will connect
    if (not myclient):
        connect_mongo()
    
    # Creating mongo query
    mydb = myclient["movieScriptsDB"]
    docs = mydb["movieScripts"]
    x = "_id"
    k = "keywords"
    s = "subtitles"
    

    newDoc = [{x:film_id, k:keyword,s:language}]
    try:
        # Attempting to insert new collection to movieScripts
        docs.insert(newDoc)
        print("MovieScript:",film_id,"added to database")
    except pymongo.errors.BulkWriteError as e:
        print("Error inserting document - check _id values")
    except pymongo.errors.DuplicateKeyError as e:
        print("*** ERROR ***: Movie Script with id:", film_id, "already exists")
    except Exception as e:
        print("Error: ",e)


def check_film_exists(film_id):
    
    # if not connected to DB, it will connect
    if (not db):
        connect_sql()
    
    # if DB is not open, it will reconnect
    if not (db.open):
        connect_sql()

    sql = """
            select FilmID, UPPER(FilmName) from film where FilmID = %s
            
          """  
    with db:
        cursor = db.cursor()
        cursor.execute(sql, (film_id))
        return cursor.fetchall()
    
    
