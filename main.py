import datetime
import json
import os # For backup functionality

class Note:
    def __init__(self, title, content, timestamp=None):
        self.title = title
        self.content = content
        if timestamp is None:
            self.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.timestamp = timestamp

    def __str__(self):
        return f"Title: {self.title}\nContent: {self.content}\nTimestamp: {self.timestamp}"

    def to_dict(self):
        return {
            "title": self.title,
            "content": self.content,
            "timestamp": self.timestamp
        }

class NoteManager:
    def __init__(self, filename="notes.json"):
        self.filename = filename
        self.notes = []
        self.load_notes()

    def add_note(self, title, content):
        if not title.strip() or not content.strip():
            print("Error: Title and content cannot be empty.")
            return False
        note = Note(title, content)
        self.notes.append(note)
        print("Note added successfully!")
        return True

    def view_notes(self):
        if not self.notes:
            print("No notes to display.")
            return
        print("\n--- Your Notes ---")
        for i, note in enumerate(self.notes):
            print(f"{i + 1}. Title: {note.title}")
            print(f"   Timestamp: {note.timestamp}")
            print("------------------")

    def get_note_details(self, index):
        if 0 <= index < len(self.notes):
            return self.notes[index]
        return None

    def edit_note(self, index, new_title, new_content):
        if not new_title.strip() or not new_content.strip():
            print("Error: Title and content cannot be empty.")
            return False
        if 0 <= index < len(self.notes):
            self.notes[index].title = new_title
            self.notes[index].content = new_content
            self.notes[index].timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("Note updated successfully!")
            return True
        else:
            print("Invalid note number.")
            return False

    def delete_note(self, index):
        if 0 <= index < len(self.notes):
            deleted_note = self.notes.pop(index)
            print(f"Note \'{deleted_note.title}\' deleted successfully!")
            return True
        else:
            print("Invalid note number.")
            return False

    def search_notes(self, search_term):
        if not search_term.strip():
            print("Search term cannot be empty.")
            return
        found_notes = []
        search_term_lower = search_term.lower()
        for i, note in enumerate(self.notes):
            if search_term_lower in note.title.lower() or search_term_lower in note.content.lower():
                found_notes.append((i, note))
        
        if not found_notes:
            print(f"No notes found matching \'{search_term}\'")
            return
        
        print(f"\n--- Search Results for \'{search_term}\' ---")
        for i, note in found_notes:
            print(f"{i + 1}. Title: {note.title}")
            print(f"   Content: {note.content[:70]}...") # Truncate for display
            print(f"   Timestamp: {note.timestamp}")
            print("------------------")

    def save_notes(self):
        try:
            # Backup existing notes.json before saving new data
            if os.path.exists(self.filename):
                os.rename(self.filename, "notes_backup.json")
                print("Created notes_backup.json")

            with open(self.filename, "w") as f:
                notes_as_dicts = [note.to_dict() for note in self.notes]
                json.dump(notes_as_dicts, f, indent=4)
            print(f"Notes saved to {self.filename}")
        except Exception as e:
            print(f"An error occurred while saving notes: {e}")

    def load_notes(self):
        try:
            with open(self.filename, "r") as f:
                notes_as_dicts = json.load(f)
                self.notes = [Note(d["title"], d["content"], d["timestamp"]) for d in notes_as_dicts]
            print(f"Notes loaded from {self.filename}")
        except FileNotFoundError:
            print("No saved notes file found. Starting with an empty list.")
            self.notes = []
        except json.JSONDecodeError:
            print("Error decoding notes file. It might be corrupted. Starting with an empty list.")
            self.notes = []
        except Exception as e:
            print(f"An unexpected error occurred while loading notes: {e}")
            self.notes = []


def display_menu():
    print("\n--- Note-Taking Application Menu ---")
    print("1. Add Note")
    print("2. View Notes")
    print("3. Edit Note")
    print("4. Delete Note")
    print("5. Search Notes")
    print("6. Exit")
    print("------------------------------------")

def get_user_choice():
    attempts = 0
    while attempts < 3:
        display_menu()
        choice = input("Enter your choice (1-6): ")
        if choice.isdigit() and 1 <= int(choice) <= 6:
            return choice
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")
            attempts += 1
    print("Too many invalid attempts. Exiting application.")
    return '6' # Return exit choice if attempts exhausted

def main():
    note_manager = NoteManager()

    while True:
        choice = get_user_choice()

        if choice == '1':
            while True:
                title = input("Enter note title: ")
                content = input("Enter note content: ")
                if note_manager.add_note(title, content):
                    break
        elif choice == '2':
            note_manager.view_notes()
            if note_manager.notes:
                while True:
                    try:
                        detail_choice = input("Enter note number to view details (or press Enter to return): ")
                        if not detail_choice:
                            break
                        note_index = int(detail_choice) - 1
                        note = note_manager.get_note_details(note_index)
                        if note:
                            print("\n--- Note Details ---")
                            print(note)
                            print("------------------")
                        else:
                            print("Invalid note number.")
                    except ValueError:
                        print("Invalid input. Please enter a number or press Enter.")
        elif choice == '3':
            note_manager.view_notes()
            if not note_manager.notes:
                continue
            attempts = 0
            while attempts < 3:
                try:
                    note_index = int(input("Enter the number of the note to edit: ")) - 1
                    if 0 <= note_index < len(note_manager.notes):
                        current_note = note_manager.get_note_details(note_index)
                        print(f"Editing note: {current_note.title}")
                        new_title = input(f"Enter new title (current: \'{current_note.title}\'): ")
                        new_content = input(f"Enter new content (current: \'{current_note.content}\'): ")
                        if note_manager.edit_note(note_index, new_title, new_content):
                            break
                    else:
                        print("Invalid note number.")
                        attempts += 1
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    attempts += 1
            if attempts == 3:
                print("Too many invalid attempts. Returning to main menu.")
        elif choice == '4':
            note_manager.view_notes()
            if not note_manager.notes:
                continue
            attempts = 0
            while attempts < 3:
                try:
                    note_index = int(input("Enter the number of the note to delete: ")) - 1
                    if 0 <= note_index < len(note_manager.notes):
                        confirm = input(f"Are you sure you want to delete note \'{note_manager.notes[note_index].title}\'? (y/n): ").lower()
                        if confirm == 'y':
                            note_manager.delete_note(note_index)
                        else:
                            print("Note deletion cancelled.")
                        break
                    else:
                        print("Invalid note number.")
                        attempts += 1
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    attempts += 1
            if attempts == 3:
                print("Too many invalid attempts. Returning to main menu.")
        elif choice == '5':
            search_term = input("Enter search term: ")
            note_manager.search_notes(search_term)
        elif choice == '6':
            print("Exiting application. Goodbye!")
            note_manager.save_notes()
            break

if __name__ == "__main__":
    main()


