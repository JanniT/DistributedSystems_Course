# I used these in help: 
# https://docs.python.org/3/library/xml.etree.elementtree.html
# https://docs.python.org/3/library/re.html

import datetime
import requests
import xml.etree.ElementTree as ET
from xmlrpc.server import SimpleXMLRPCServer

# function to take the timestamp for the note
def timestamp():
    return datetime.datetime.now().strftime("%m/%d/%y - %H:%M:%S")

def userInput(topic, noteName, text, timestamp):
    # Parsing the xml file and getting the root of it
    tree = ET.parse('db.xml')
    root = tree.getroot()

    # checking if the topic already exists in the XML file
    topic_exists = False
    for topic_element in root.findall('topic'):
        if topic_element.attrib['name'] == topic:
            topic_exists = True
            # creating a sub note to the topic
            note = ET.SubElement(topic_element, 'note')
            note.set('name', noteName)
            text_element = ET.SubElement(note, 'text')
            text_element.text = text
            timestamp_element = ET.SubElement(note, 'timestamp')
            timestamp_element.text = timestamp
            break
    
    # if the topic doesn't exist the topic is created
    if not topic_exists:
        new_topic = ET.SubElement(root, 'topic')
        new_topic.set('name', topic)

        note = ET.SubElement(new_topic, 'note')
        note.set('name', noteName)

        text_element = ET.SubElement(note, 'text')
        text_element.text = text

        timestamp_element = ET.SubElement(note, 'timestamp')
        timestamp_element.text = timestamp

    # writing out the file
    tree.write('db.xml')
    return True

def getNotes(topic):
    tree = ET.parse('db.xml')
    root = tree.getroot()
    
    notes = []
    # searching for the given topic to get its' notes
    for topic_element in root.findall('topic'):
        if topic_element.attrib['name'] == topic:

            # going thourgh the notes of the selected topic
            for note_element in topic_element.findall('note'):
                note_name = note_element.attrib.get('name', 'N/A')

                timestamp_element = note_element.find('timestamp')
                if timestamp_element is not None:  
                    timestamp = timestamp_element.text.strip()
                else:
                    timestamp = 'N/A'

                # getting the text of the note and stripping whitespace
                text_element = note_element.find('text')

                # handling the empty texts as wikipedia returns only empty strings
                if text_element is not None and text_element.text is not None:
                    text = text_element.text.strip()
                else:
                    text = ''
                    
                notes.append({'name': note_name, 'timestamp': timestamp, 'text': text})
            break
    return notes

# The wikipedia api should retrieve the data from there but as said on their website
# the descriptions cannot be fetched: 
# "On Wikimedia wikis descriptions are disabled due to performance reasons, so the second array only contains empty strings"
# https://www.mediawiki.org/wiki/API:Opensearch

def wikipediaApi(searchWord, topic):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "opensearch",
        "namespace": "0",
        "search": searchWord,
        "limit": "1",
        "format": "json"
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if len(data) >= 4 and data[3]:
            userInput(topic, searchWord, data[2][0], timestamp())
            return True
        else:
            return False
    except requests.RequestException as e:
        print(f"Error making request: {e}")
        return False

if __name__ == "__main__":
    server = SimpleXMLRPCServer(("localhost", 8000))
    print("Listening on port: 8000")
    # registering all the functions separately as there isn't any classes
    server.register_function(timestamp, "timestamp")
    server.register_function(userInput, "userInput")
    server.register_function(getNotes, "getNotes")
    server.register_function(wikipediaApi, "wikipediaApi")
    server.serve_forever()