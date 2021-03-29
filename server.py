# Server for a notebook application made by Tommi Kunnari
# for a university course about Distributed Systems.
# 29.3.2021

from xmlrpc.server import SimpleXMLRPCServer
from datetime import date, datetime
import xml.etree.ElementTree as ET
import os
import wikipedia
import threading

tree = ET.parse('db.xml')
root = tree.getroot()



# Määritetään serveri

server = SimpleXMLRPCServer(('127.0.0.1', 5000), logRequests=True, allow_none=True)



# Määritetään funktiot

# Funktio, joka etsii käyttäjän syötteenmukaiset muistiinpanot aiheen perusteella ja palauttaa ne käyttäjälle.
def find_topic(topic):
    print("{}: Fetching topics...".format(get_time()))
    try:
        r_topics = []
        topics = tree.findall('topic')
        for i in topics:
            if (topic == i.attrib.get('name')):
                notes = i.findall('note')
                for x in notes:
                    r_notes = []
                    r_notes.append(x.attrib.get('name').strip())
                    r_notes.append(x.find('text').text.strip())
                    r_notes.append(x.find('timestamp').text.strip())
                #    print(text.strip(),time.strip())
                    r_topics.append(r_notes)
        print("{}: Successfully fetched topics!".format(get_time()))
        return r_topics
    except:
        print("{}: Error while fetching topics.".format(get_time()))
        return r_topics


# Hakee kaikki aiheet xml-tiedostosta ja palauttaa ne käyttäjälle.
def get_topics():
    print("{}: Getting current topics...".format(get_time()))
    r_topics = []
    topics = tree.findall('topic')
    for i in topics:
        r_topics.append(i.attrib.get('name').strip())
    print("{}: Successfully returned topics!".format(get_time()))
    return r_topics


# Luo uuden muistiinpanon. Jos muistiinpanon aihetta ei ole, luodaan uusi aihe.
def create_topic(note):
    try:
        for i in tree.findall('topic'):
            if i.attrib.get('name') == note[0]:
                print("{}: Appending an existing topic...".format(get_time()))
                new_note = ET.SubElement(i,'note', name=note[1])
                ET.SubElement(new_note, 'text').text = note[2]
                ET.SubElement(new_note, 'timestamp').text = note[3]
                tree.write('db.xml', encoding='UTF-8', xml_declaration=True)
                print("{}: Successfully appended topic!".format(get_time()))
                return True
        print("{}: Creating a new topic...".format(get_time()))
        new_topic = ET.SubElement(root,'topic', name=note[0])
        new_note = ET.SubElement(new_topic,'note', name=note[1])
        ET.SubElement(new_note, 'text').text = note[2]
        ET.SubElement(new_note, 'timestamp').text = note[3]
        tree.write('db.xml', encoding='UTF-8', xml_declaration=True)
        print("{}: Successfully created a new topic!".format(get_time()))
        return True
    except:
        print("{}: Error while creating a note.".format(get_time()))
        return False


# Etsii wikipediasta artikkelia käyttäjän syötteen mukaan.
def search_wiki(search):
    print("{}: Searching wikipedia for '{}'...".format(get_time(), search))
    try:
        result = wikipedia.search(search)
        print("{}: Successfully searched wikipedia!".format(get_time()))
        return result
    except:
        print("{}: An error has occurred while searching wikipedia for '{}'".format(get_time(), search))
        return Exception


# Hakee wikipedia-artikkelin yhteenvedon käyttäjän syötteen mukaan.
def get_summary(search):
    print("{}: Fetching data from wikipedia on '{}'...".format(get_time(),search))
    try:
        result = wikipedia.summary(search)
        print("{}: Successfully fetched data from wikipedia!")
        return result
    except:
        print("{}: Error while fetching wikipedia.".format(get_time()))
        return Exception

# Hakee serverin ajan logia varten.
def get_time():
    today = date.today().strftime("%d/%m/%Y")
    time = datetime.now().strftime("%H:%M:%S")
    timestamp = "[{} - {}]".format(today, time)
    return timestamp



# Rekisteröidään funktiot serverin käytettäväksi

server.register_function(find_topic)
server.register_function(create_topic)
server.register_function(search_wiki)
server.register_function(get_summary)
server.register_function(get_topics)



# Käynnistetään serveri ohjelman käynnistyessä ja ajetaan se omalla
# säikeellään usean käyttäjien pyyntöjen yhtäaikaisen käsittelyn mahdollistamiseksi.

if __name__ == '__main__':
    try:
        print('{}: Server commissioned.'.format(get_time()))
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.start()
    except KeyboardInterrupt:
        print('{}: Quitting server'.format(get_time()))

