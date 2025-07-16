import datetime
import json
import uuid
from colorama import Fore, Style

class Note:
    def __init__(self, title, content, id=None, timestamp=None):
        self.id = id if id is not None else str(uuid.uuid4())
        self.title = title
        self.content = content
        self.timestamp = timestamp if timestamp is not None else datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "timestamp": self.timestamp
        }
    # def test_fun(self):
    #     print(f"{self.title} and {self.content}")

class NoteManager:
    def __init__(self, filename="notes.json"):
        self.filename="notes.json"
        self.notes = []
        self.load_notes()
    
    def load_notes(self):
        try:
            with open(self.filename, "r") as f:
                # # [{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}, ...], 苦手
                notes_as_dicts = json.load(f)
                self.notes = [Note(d["id"], d["title"], d["content"], d["timestamp"]) for d in notes_as_dicts]
            print(f"Notes loaded from {self.filename}")
        except FileNotFoundError:
            print("No saved notes file found. Starting with an empty list.")
            self.notes = []
        except json.JSONDecodeError:
             print("Error decoding notes file. Starting with an empty list.")
             self.notes = []
        except Exception as e:
            print(f"An unexpected error occurred while loading notes: {e}")
            self.notes = []
    
    def add_note(self, title, content):
        MIN_CHA_NUMBER = 3
        if not title or not content:
            print(Fore.RED + "Error: Title and content cannot be empty.")
            print(Style.RESET_ALL)
            # False -> break?, True -> main menu
            return False
        if len(title) <= MIN_CHA_NUMBER or len(content) <= MIN_CHA_NUMBER:
            print(Fore.RED + f"Title and content must be at least {MIN_CHA_NUMBER} characters long.")
            print(Style.RESET_ALL)
            return False
        note = Note(title, content)
        self.notes.append(note)
        print("Note added successfully!")
        return True
    
    def view_note(self):
        if not self.notes:
            print("No notes to display.")
            return
        print("\n--- Your Notes ---")
        for i, note in enumerate(self.notes):
            print(f"{i + 1}. Title: {note.title}")
            print(f"   Timestamp: {note.timestamp}")
            print("------------------")
    
    def get_note_detail(self, index):
        if index < 0 or len(self.notes) - 1 < index:
            print(f"There are {len(self.notes)} notes.")
            return
        else:
            return self.notes[index]
        
    def save_notes(self):
        try:
            with open(self.filename, "w") as f:
                notes_as_dicts = [note.to_dict() for note in self.notes]
                json.dump(notes_as_dicts, f, indent=4)
            print(f"Notes saved to {self.filename}")
        except Exception as e:
            print(f"An error occurred while saving notes: {e}")



# 苦手
class InvalidCharacterNumber(Exception):
    def __init__(self, message="Title or content is too short"):
        super().__init__(message)



MAX_MENU_NUMBER = 7
def display_menu():
    print("\n--- Note-Taking Application Menu ---")
    print("1. Add Note")
    print("2. View Notes")
    print("3. Edit Note")
    print("4. Delete Note")
    print("5. Search Notes")
    print("6. Convert to CSV")
    print("7. Exit")
    print("------------------------------------")

def get_user_choice():
    # userが正しい数字を選択するまで実行し続ける
    while True:
        display_menu()
        choice = input(f"Enter your choice (1-{MAX_MENU_NUMBER}): ")
        if choice.isdigit() and 1 <= int(choice) <= MAX_MENU_NUMBER:
            return choice
        else:
            print(f"Invalid choice. Please enter a number between 1 and {MAX_MENU_NUMBER}.")

def main():
    note_manager = NoteManager()
    
    while True:
        choice = get_user_choice()
        if choice == '1':
            title = input("Enter note title: ").strip()
            content = input("Enter note content: ").strip()
            note_manager.add_note(title, content)
        elif choice == '2':
            note_manager.view_note()
            if note_manager.notes:
                while True:
                    try:
                        detail_choice = input("Enter note number to view details (or press Enter to return): ")
                        if not detail_choice:
                            break
                        note_index = int(detail_choice) - 1
                        note = note_manager.get_note_detail(note_index)
                        if note:
                            print("\n--- Note Details ---")
                            print(note.content)
                            print("------------------")
                        else:
                            print("Invalid note number.")
                    except ValueError:
                        print("Invalid input. Please enter a number or press Enter.")
        elif choice == '3':
            note_manager.edit_note(new_title, new_content)
        elif choice == '4':
            note_manager.delete_note(note_number)
        elif choice == '5':
            note_manager.search_note(search_term)
        elif choice == '6':
            note_manager.convert_to_csv()
        elif choice == '7':
            note_manager.save_notes()
            print("Exiting application. Goodbye!")
            break

# Note: choice3-6 and 6.1 Exercises

if __name__ == "__main__":
    main()