#Importing libraries and functions
import moviesDB
import os
import keyboard
import calendar


# Option 2 - testing if year is an integer value
def get_year():
    while True:
        try:
            n = input("Year of Birth: ")
            n = int(n)
            break
        except ValueError:
            print("invalid year, try again")
    return str(n)


#Option 4 - testing if country ID is an integer value
def get_country_id():
    while True:
        try:
            new_id = input("ID : ")
            new_id = int(new_id)
            break
        except ValueError:
            print("Invalid ID number, try again")
    return (new_id)


#Option 4 - Asks for a country name if none is entered
def get_coutry_name():
    new_country = input("Name : ")
    while new_country in [""]:
        new_country = input("Name : ")
    return(new_country)

    
#Option 2 - Asks for a gender if an invalid gender is entered
def get_gender():
    gender=input("Gender (Male/Female): ")
    while gender not in ['Male', 'Female','']:
        gender=input("Gender (Male/Female): ")
    return(gender)


#Option 5 - Asks for a subtitle name if none is entered
def get_subtitle_name():
    subtitle = input("Enter subtitle Language : ")
    while subtitle in [""]:
        subtitle = input("Enter subtitle Language : ")
    return(subtitle)


# Option 6 - testing if film_id is an integer value
def get_film_id():
    while True:
        try:
            new_id = input("ID : ")
            new_id = int(new_id)
            break
        except ValueError:
            print("Invalid ID number, try again")
    return (new_id)


# Option 6 - Checks if new keyword is entered and creates a list with keywords
def get_keyword():
    
    #initializing list
    nk = []
    new_keyword = input("Keyword (-1 to end): ")
    while new_keyword not in ["-1"]:
        if new_keyword not in[""]:
            
            #recording values already validate into the list
            nk.append(new_keyword)
            new_keyword=input(("Keyword (-1 to end): "))
        
        else:
            #if invalid values are typed
            new_keyword = input("Keyword (-1 to end): ")
    
    return(nk)


# Option 6 - Checks if new subtitle language is entered and creates a list with subtitles language
def get_sub_lang():                   
    
    #initializing list
    ns = []       
    new_subtitle = input("Subtitles Language (-1 to end): ")
    while new_subtitle not in ["-1"]:
        if new_subtitle not in[""]:
            
            #recording values already validate into the list
            ns.append(new_subtitle)
            new_subtitle = input("Subtitles Language (-1 to end): ")
        else:
            #if invalid values are typed
            new_subtitle = input("Subtitles Language (-1 to end): ")

    return(ns)

# creates main menu - function called within all 6 options in main menu
def display_menu():
    print("")
    print("Movies DB")
    print("-"*9)
    print("")
    print("MENU")
    print("="*4)
    print("1 - View Films")
    print("2 - View Actors by Year of Birth & gender")
    print("3 - View Studios")
    print("4 - Add New Country")
    print("5 - View Movie with Subtitles")
    print("6 - Add new MovieScript")
    print("x - Exit")
    print("")




# Creates main menu and calls all functions above
def main():
    display_menu()
    
    #Initializing var dict_created for option 3
    dict_created = False
    
    while True:
        choice = input("Choice: ")
        if (choice == "1"):
            
            # Calling function from moviesDB
            films = moviesDB.view_movies()
            count = 0
            print("")

            try:
                for film in films:
                    print(film["FilmName"], "|", film["ActorName"])
                    count +=1
                
                    # prints movie list in batches of 5
                    # If count mod 5 = 0, asks to press key
                    if (count % 5) == 0:
                        print("-- Quit (q) --")
                        os.system('pause')

                        # Breaks the looping if q is pressed
                        if keyboard.is_pressed('q'): 
                            break  # finishing the loop
            except Exception as e:
                print(e)

            display_menu()

        elif(choice == "2"):

            year_birth = get_year()
            gender = get_gender()
            
            # Calling function from moviesDB
            try:
                yb = moviesDB.view_act_yob_gender(year_birth,gender)
                for actor in yb:
                    
                    #converts actor's DOB into a string
                    month = str(actor["ActorDOB"])
                    
                    #Gets the digits equivalent to month and converts it to a month name (needs calendar library)
                    month_name = (calendar.month_name[int(month[5:7])])
                    
                    print(actor["ActorName"], "|", month_name, "|", actor["ActorGender"])
            except Exception as e:
                print(e)

            display_menu()
            

        elif(choice == "3"):
            
            # Will only go through loopings and connect to DB if list has not been created
            if not dict_created:
                
                # empties list before create it
                studio_list = {}

                # Calling function from moviesDB
                studios = moviesDB.view_studios()
                keys = []
                values = []

                for studio in studios:
                    keys.append(studio["StudioID"])
                    values.append(studio["StudioName"])

                    # Creates a list with studios info
                    studio_list = dict(zip(keys,values))
                dict_created = True
                

            c = 0

            # Printing values from studio_list    
            while c < len(studio_list):
                for keys in studio_list:
                    print(keys, ":", studio_list[keys])
                    c += 1

 
            print("")
            display_menu()

        elif(choice == "4"):
            print("")
            print("Add New Country")
            print("-" * 14)
            new_id = get_country_id()
            new_country = get_coutry_name()

            # Calling function from moviesDB
            try:
                moviesDB.add_country(new_id, new_country)
            except Exception as e:
                print(e)
            
            print("")
            display_menu()

        elif(choice == "5"):
            print("Movies with Subtitles")
            print("-"*21)
            print("")
            language = get_subtitle_name()

            # Calling function from moviesDB
            try:
                show_movies = moviesDB.view_movies_subtitles(language)
                print("Movies with ",language," subtitles")
                
                for item in show_movies:
                    print(item["FilmName"], " | ", item["Synopsis"])
            except:
                print("No movies with subtitle in", language)
            
            print("")
            display_menu()

        elif(choice == "6"):
            print("Add New Movie Script")
            print("-"*20)
            print("")
            film_id = int(get_film_id())

            # Calling function from moviesDB
            try:

                searc_film= moviesDB.check_film_exists(film_id)
                print("")
                
                # Will print film name if film exists in DB
                if len(searc_film) != 0:
                    for x in searc_film:
                        
                        # Displaying film name on screen so as user knows what keys should be entered
                        print("New movie script for: ",x["UPPER(FilmName)"])

                    # Getting keyword and languages for new movie script
                    new_keyword = (get_keyword())
                    new_language = (get_sub_lang())
                    print("")
                    
                    # Calling funcion add_movscript
                    moviesDB.add_movscript(film_id, new_keyword, new_language)
                else:
                    
                    # If movie not found from function "check_film_exists"
                    print("*** ERROR ***: Film with id: ",film_id, "does not exist in moviesDB")
            except Exception as e:
                print(e)

            display_menu()
 
        else:
            if (choice == 'x'):
                break
            else:
                display_menu()



if __name__== "__main__":
    main()