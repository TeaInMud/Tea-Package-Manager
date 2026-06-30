#!/usr/bin/env python3
import sys
import os
import datetime

TEA_DIR = os.path.expanduser("~/.tea")
NOTES_FILE = os.path.join(TEA_DIR, "notes.md")

def init_env():
    """Ensure the hidden tea directory exists."""
    os.makedirs(TEA_DIR, exist_ok=True)

def show_help():
    print("📝 NOTES — Quick Terminal Notebook")
    print("Usage: notes <command> [arguments]\n")
    print("Commands:")
    print("  add \"<text>\"  -> Add a new note with a timestamp")
    print("  view          -> Display all saved notes cleanly")
    print("  clear         -> Wipe out your notes file completely")

def add_note(text):
    init_env()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    try:
        with open(NOTES_FILE, "a") as f:
            f.write(f"- [{timestamp}] {text}\n")
        print(f"✅ Saved note: \"{text}\"")
    except Exception as e:
        print(f"❌ Failed to save note: {e}")

def view_notes():
    if not os.path.exists(NOTES_FILE) or os.stat(NOTES_FILE).st_size == 0:
        print("📋 Your notebook is completely empty!")
        return
    
    print("📋 Saved Notes:")
    print("-" * 40)
    try:
        with open(NOTES_FILE, "r") as f:
            print(f.read().strip())
    except Exception as e:
        print(f"❌ Failed to read notes: {e}")
    print("-" * 40)

def clear_notes():
    if not os.path.exists(NOTES_FILE):
        print("📋 Nothing to clear.")
        return
        
    confirm = input("⚠️ Are you sure you want to delete ALL notes? (y/N): ").strip().lower()
    if confirm == 'y':
        try:
            os.remove(NOTES_FILE)
            print("🧹 Notebook cleared successfully!")
        except Exception as e:
            print(f"❌ Failed to clear notebook: {e}")
    else:
        print("Cancelled.")

def main():
    if len(sys.argv) < 2:
        show_help()
        return

    cmd = sys.argv[1].lower()

    if cmd == "add":
        if len(sys.argv) < 3:
            print("Usage: notes add \"your note text here\"")
            return
        # Combine all subsequent arguments in case the user forgot quotes
        note_text = " ".join(sys.argv[2:])
        add_note(note_text)

    elif cmd == "view":
        view_notes()

    elif cmd == "clear":
        clear_notes()

    else:
        print(f"Unknown command: '{cmd}'")
        show_help()

if __name__ == "__main__":
    main()
