import json
import datetime
import os
import csv
from colorama import Fore, Style
import uuid

NOTE_FILE = "notes_old.json"
MIN_COUNT = 3

class InvalidNoteError(Exception):
    pass

class Note:
    def __init__(self, title, content, timestamp=None, id=None,):
        self.id = id if id is not None else str(uuid.uuid4())
        self.title = title
        self.content = content
        if timestamp is None:
            self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.timestamp = timestamp

    def __str__(self):
        # The __str__ method provides a user-friendly string representation of the object
        return f"ID: {self.id}\nTitle: {self.title}\nContent: {self.content}\nTimestamp: {self.timestamp}"

    def to_dict(self):
        # This method will be useful for JSON serialization
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "timestamp": self.timestamp,
        }

class NoteManager:
    def __init__(self, filename="notes_old.json"):
        self.filename = filename
        self.notes = []
        self.load_notes()

    def add_note(self, title, content):
        # 空だった場合は再入力
        if not title.strip() or not content.strip():
            print(Fore.RED + "Title and content cannot be empty.")
            print(Style.RESET_ALL)
            return False
        
        # 長さチェック
        if len(title) < MIN_COUNT or len(content) < MIN_COUNT:
            raise InvalidNoteError(Fore.RED + f"Title and content have at least {MIN_COUNT} characters")
            print(Style.RESET_ALL)
            return False

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        note = Note(title, content, timestamp)
        self.notes.append(note)
        print(Fore.GREEN + f"Note added successfully!")
        print(Style.RESET_ALL)
        return True

    def view_notes(self, index=None):
        if not self.notes:
            print("No notes to display.")
            return False
        if index is None:
            for i, note in enumerate(self.notes):
                print(f"{i + 1}. Title: {note.title}")
                print(f"   Content: {note.content[:50]}...")
                print(f"   Timestamp: {note.timestamp}")
                print("------------------")
        else:
            if 0 <= index < len(self.notes):
                shown_note = self.notes[index]
                print("\n--- Your Notes ---")
                print(f"{index + 1}. Title: {shown_note.title}")
                print(f"   Content: {shown_note.content}") # Truncate content
                print(f"   Timestamp: {shown_note.timestamp}")
                print("------------------")
                return True
            else:
                print(f"No note found with number {index + 1}.")
            

    MAX_ATTEMPTS = 3

    def edit_note(self, index, new_title, new_content):
        self.view_notes()
        if not self.notes:
            return
        attempt = 0
        while attempt < MAX_ATTEMPTS:
            try:
                if 0 <= index < len(self.notes):
                    self.notes[index].title = new_title
                    self.notes[index].content = new_content
                    self.notes[index].timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print("Note updated successfully!")
                    return
                else:
                    print("Invalid note number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
            attempt += 1
        print("Return to the main menu.")

    def delete_note(self, index):
        if 0 <= index < len(self.notes):
            deleted_note = self.notes.pop(index)
            print(f"Note \'{deleted_note["title"]}\' deleted successfully!")
        else:
            print("Invalid note number.")

    def save_notes(self):
        try:
            with open(self.filename, "w") as f:
                # Convert list of Note objects to list of dictionaries
                notes_as_dicts = [note.to_dict() for note in self.notes]
                json.dump(notes_as_dicts, f, indent=4)
            print(f"Notes saved to {self.filename}")
        except Exception as e:
            print(f"An error occurred while saving notes: {e}")

    def load_notes(self):
        try:
            with open(self.filename, "r") as f:
                notes_as_dicts = json.load(f)
                # Convert list of dictionaries back to list of Note objects
                self.notes = [Note(d["id"], d["title"], d["content"], d["timestamp"]) for d in notes_as_dicts]
            print(f"Notes loaded from {self.filename}")
        except FileNotFoundError:
            print("No saved notes file found. Starting with an empty list.")
            notes = []
        except json.JSONDecodeError:
            print("Error decoding notes file. It might be corrupted. Starting with an empty list.")
            notes = []
        except Exception as e:
            print(f"An unexpected error occurred while loading notes: {e}")
            notes = []

    def export_to_csv(self):
        if not self.notes:
            print("No notes to export")
            return
        with open("note.csv", "w", newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=["tite", "content", "timestamp"])
            writer.writeheader()
            # writer.writerrows(self.notes)
        print("Notes exported to notes.csv")
    
    def search_notes(self, search_term):
        for i, note in enumerate(self.notes):
            if search_term.lower() in note.title.lower() or search_term.lower() in note.content.lower():
                print(f"{i + 1}. Title: {note.title}")
                print(f"   Content: {note.content[:50]}...") # Truncate content
                print(f"   Timestamp: {note.timestamp}")
                print("------------------")
                return True
            else:
                print(f"No match with {search_term}")
                return False

def display_menu():
    print("\n--- Note-Taking Application Menu ---")
    print("1. Add Note")
    print("2. View Notes")
    print("3. Edit Note")
    print("4. Delete Note")
    print("5. Save Notes")
    print("6. Load Notes")
    print("7. Search Notes")
    print("8. Exit")
    print("------------------------------------")


def get_user_choice():
    while True:
        display_menu()
        choice = input("Enter your choice (1-8): ")
        if choice.isdigit() and 1 <= int(choice) <= 8:
            return choice
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")

def main():
    note_manager = NoteManager(NOTE_FILE)
    while True: # 8でexitするまで動く
        choice = get_user_choice()
        if choice == '1':
            title = input("Enter note title: ").strip()
            content = input("Enter note content: ").strip()
            try:
                note_manager.add_note(title, content)
            except InvalidNoteError as e:
                print(e)
        elif choice == '2':
            note_manager.view_notes()
            user_input = input("Enter the number of the note to view, or press Enter to return: ").strip()
            if user_input == "":
                continue
            try:
                shown_index = int(user_input) - 1
                note_manager.view_notes(shown_index)
            except ValueError:
                print("Invalid input. Please enter a valid number or just press Enter.")
        elif choice == '3':
            note_manager.view_notes()
            if not note_manager.notes:
                continue
            index = int(input("Enter the number of the note to edit: ")) - 1
            new_title = input(f"Enter new title for note {index + 1} (current: \'{note_manager.notes[index]["title"]}\'): ")
            new_content = input(f"Enter new content for note {index + 1} (current: \'{note_manager.notes[index]["content"]}\'): ")
            note_manager.edit_note(index, new_title, new_content)
        elif choice == '4':
            index = int(input("Enter the number of the note to delete: ")) - 1
            note_manager.delete_note(index)
        elif choice == '5':
            note_manager.save_notes()
        elif choice == '6':
            note_manager.load_notes()
        elif choice == '7':
            search_term = (input("Enter the term to search: "))
            note_manager.search_notes(search_term)
        elif choice == '8':
            print("Exiting application. Goodbye!")
            note_manager.save_notes() # Save notes before exiting
            break

if __name__ == "__main__":
    main()