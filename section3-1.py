import json
import datetime
import csv

notes = [] # Global list to store notes
NOTE_FILE = "notes.json"

def display_menu():
    print("\n--- Note-Taking Application Menu ---")
    print("1. Add Note")
    print("2. View Notes")
    print("3. Edit Note")
    print("4. Delete Note")
    print("5. Save Notes")
    print("6. Load Notes")
    print("7. Exit")
    print("8. Export to CSV")
    print("------------------------------------")

def get_user_choice():
    while True:
        display_menu()
        choice = input("Enter your choice (1-8): ")
        if choice.isdigit() and 1 <= int(choice) <= 8:
            return choice
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

def add_note():
    title = input("Enter note title: ")
    content = input("Enter note content: ")
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    note = {"title": title, "content": content, "timestamp": timestamp}
    notes.append(note)
    print("Note added successfully!")

def view_notes():
    if not notes:
        print("No notes to display.")
        return
    print("\n--- Your Notes ---")
    for i, note in enumerate(notes):
        print(f"{i + 1}. Title: {note["title"]}")
        print(f"   Content: {note["content"][:50]}...") # Truncate content
        print(f"   Timestamp: {note["timestamp"]}")
        print("------------------")

def edit_note():
    view_notes()
    if not notes:
        return
    while True:
        try:
            note_index = int(input("Enter the number of the note to edit: ")) - 1
            if 0 <= note_index < len(notes):
                new_title = input(f"Enter new title for note {note_index + 1} (current: \'{notes[note_index]["title"]}\'): ")
                new_content = input(f"Enter new content for note {note_index + 1} (current: \'{notes[note_index]["content"]}\'): ")
                notes[note_index]["title"] = new_title
                notes[note_index]["content"] = new_content
                notes[note_index]["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print("Note updated successfully!")
                break
            else:
                print("Invalid note number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def delete_note():
    view_notes()
    if not notes:
        return
    while True:
        try:
            note_index = int(input("Enter the number of the note to delete: ")) - 1
            if 0 <= note_index < len(notes):
                deleted_note = notes.pop(note_index)
                print(f"Note \'{deleted_note["title"]}\' deleted successfully!")
                break
            else:
                print("Invalid note number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def save_notes():
    with open(NOTE_FILE, "w") as f:
        json.dump(notes, f, indent=4)
    print(f"Notes saved to {NOTE_FILE}")

def load_notes():
    global notes # Declare that we are modifying the global 'notes' list
    try:
        with open(NOTE_FILE, "r") as f:
            notes = json.load(f)
        print(f"Notes loaded from {NOTE_FILE}")
    except FileNotFoundError:
        print("No saved notes found. Starting with an empty list.")
        notes = [] # Initialize notes as empty if file not found
    except json.JSONDecodeError:
        print("Error decoding notes file. Starting with an empty list.")
        notes = [] # Initialize notes as empty if JSON is invalid

def export_to_csv():
    if not notes:
        print("No notes to export")
        return
    with open("note.csv", "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["title", "content", "timestamp"])
        writer.writeheader()
        writer.writerows(notes)
    print("Notes exported to notes.csv")

def main():
    load_notes() # Load notes when the application starts
    while True:
        choice = get_user_choice()

        if choice == '1':
            add_note()
        elif choice == '2':
            view_notes()
        elif choice == '3':
            edit_note()
        elif choice == '4':
            delete_note()
        elif choice == '5':
            save_notes()
        elif choice == '6':
            load_notes()
        elif choice == '7':
            print("Exiting application. Goodbye!")
            save_notes() # Save notes before exiting
            break
        elif choice == '8':
            export_to_csv()

if __name__ == "__main__":
    main()