# Client for a notebook application made by Tommi Kunnari
# for a university course about Distributed Systems.
# 29.3.2021

from xmlrpc.client import ServerProxy
from datetime import date, datetime



# Määritetään serverin osoite.

proxy = ServerProxy('http://localhost:5000')


# Päävalikko josta käyttäjän on helppo valita haluamansa toiminto.

def main_menu():
    print("\nWhat do you want to do?\n1 - Send a note\n2 - List topics\n3 - Fetch topics\n4 - Search wikipedia for additional information\n0 - Quit")
    choice = input()
    if (choice == "1"):
        make_note()
    elif (choice == "2"):
        list_topics()
    elif (choice == "3"):
        find_topic()
    elif (choice == "4"):
        search_wikipedia()
    elif (choice == "0"):
        print("Client closing. See you again!")
        exit(0)
    else:
        print("Your choice was invalid.")



# Hakee serveriltä kaikki muistiossa olevat aiheet.

def list_topics():
    print("\nFetching a list of topics in notebook...")
    try:
        topics = proxy.get_topics()
        if topics == []:
            print("\nThe notebook is currently empty. Save some notes and try again!\n")
            return
        print("List of topics in notebook:\n")
    except:
        print("Error while fetching a list of topics. Please contact adminstration for help.")
        return
    for i in topics:
        print(i)



# Etsii kaikki muistiinpanot aiheen mukaan.

def find_topic():
    print("Enter a topic to search: ")
    topic = input()
    notes = proxy.find_topic(topic)

    if notes == []:
        print("No topics on '{}' found.".format(topic))
        return
    elif notes[0] == 'error':
        print("A serverside error has occurred. Please contact the adminstration for support.")
        return

    print("\nNotes on topic '{}':".format(topic))
    for i in notes:
        print("\nNote: {}\nText: {}\nTime: {}".format(i[0],i[1],i[2]))
        


# Ottaa käyttältä tiedot uutta muistiinpanoa varten ja lähettää ne serverille.

def make_note():
    print("Enter the topic:")
    topic = input()
    print("Enter the title:")
    title = input()
    print("Text for the note:")
    text = input()

    note = [topic, title, text, get_time()]

    if proxy.create_topic(note) == False:
        print("Failed to create a note. Please check your connection and try again.")
        return
    print("\nSuccesfully created a note on topic '{}'!".format(topic))



# Kysyy käyttäjältä wikipediasta etsittävän artikkelin tiedot, käskee serverin hakea nämä, ja kysyy haluaako
# käyttäjä tallentaa nämä muistioonsa. Jos kyllä, tehdään juurikin näin.

def search_wikipedia():
    print("What would you like to search for?")
    search = input()
    print("Searching, please wait...")

    try:
        results = proxy.search_wiki(search)
    except:
        print("An error has occurred while searching wikipedia. This is likely a serverside fault. Please contact adminstration for support.")
        return

    if results == []:
        print("Nothing found on '{}'".format(search))
        return
    print("Found the following results on '{}':\n\n{}\n\nWhich would you like to pick? (Select by using list index):".format(search, results))

    while True:
        try:
            choice = int(input())
            break
        except:
            print("You gave an invalid index. The index has to be a round number (int) and be in range of the list. Try again.")

    print("Fetching data from wikipedia, please wait...\n")
    title = results[choice]
    try:
        info = proxy.get_summary(title)
        print(info)
    except:
        print("A serverside error has occurred. Please contact adminstration for help.")
        return

    print("\nWould you like to save this data under a topic? (y/n)\n")
    while True:
        choice = input()
        if choice == "y":
            #try:
            save_wiki_info(title, info)
            print("\nSummary on '{}' from wikipedia succesfully saved as a note!".format(title))
            break
            #except:
            #    print("\nAn error occurred while saving the wikipedia summary. This is likely a serverside fault. Please contact adminstration for support.\n")
            #    return
        elif choice == "n":
            print("Data not saved.")
            return
        else:
            print("Invalid input")
    


# Hakee järjestelmän ajan muistiinpanojen formatointia varten.

def get_time():
    today = date.today().strftime("%d/%m/%Y")
    time = datetime.now().strftime("%H:%M:%S")
    timestamp = "{} - {}".format(today, time)
    return timestamp



# Lähettää aiemmasta wikipedian hakufunktiosta saadut tiedot serverille tallennettavaksi muistioon.

def save_wiki_info(title, info):
    print("Under what topic would you like to save the info?")
    topic = input()
    timestamp = get_time()
    note = [ topic , "Wikipedia entry on '{}'".format(title) , info , timestamp ]
    proxy.create_topic(note)



# Määritetään main_menu funktio ajettavaksi ohjelman käynnistyessä.

if __name__ == '__main__':
    #print(proxy.list_directory(r'D:\Tiedostot\Kouluasiat\Lipasto\distributed_systems\2'))
    print("Client started!\nThis is a notebook application. Enjoy!")
    while(True):
        main_menu()
