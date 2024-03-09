import xmlrpc.client

proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")

def addNote():
    topic = input("Enter topic name: ")
    note = input("Enter note name: ")
    text = input("Enter text to the note: ")
    
    # Calling the functions in the server
    timestamp = proxy.timestamp()
    success = proxy.userInput(topic, note, text, timestamp)

    if (success):
        print("\n----Note added succesfully----\n")
    else: 
        print("\n----Failed to add the note----\n")

def getNotes(topic):
    # Getting the notes from the server side function
    notes = proxy.getNotes(topic)
    return notes

def wikipediaSearch():
    searchWord = input("Enter search word to search from Wikipedia: ")
    topic = input("Enter the topic you want this information to be appended: ")
    success = proxy.wikipediaApi(searchWord, topic)
    if success:
        print("\n----Data found and added to topic----\n")
    else:
        print("\n----There was an error----\n")

if __name__ == "__main__":
    while True:
        print("1. Add a Note")
        print("2. Get Notes")
        print("3. Find from Wikipedia and add to topic")
        print("4. Exit")
        choice = input("Enter your choice (number): ")

        if choice == "1":
            addNote()
        elif choice == "2":
            topic = input("Enter topic to retrieve notes: ")
            notes = getNotes(topic)
            if notes:
                print(f"\nNotes for topic '{topic}':")
                for note in notes:
                    print(f"Note Name: {note['name']},\nTimestamp: {note['timestamp']},\nText: {note['text']}\n")
            else:
                print(f"No notes found for topic '{topic}'.")
        elif choice == "3":
            wikipediaSearch()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")
