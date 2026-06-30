#!/usr/bin/env python3
import sys
import os
import subprocess

def run_cmd(args):
    """Helper to run a shell command and return its output/status."""
    try:
        result = subprocess.run(args, capture_output=True, text=True)
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except FileNotFoundError:
        return -1, "", "Git is not installed on this system."

def check_git_repo():
    """Checks if the current directory is a git repository."""
    code, _, _ = run_cmd(["git", "rev-parse", "--is-inside-work-tree"])
    return code == 0

def show_help():
    print("Better Gut — Easier & Better Git")
    print("Usage: better-git <command> [arguments]\n")
    print("Commands:")
    print("  setup             -> Configure your global Git username, email, or remote repository")
    print("  init              -> Initialize a new local Git repository")
    print("  save \"<message>\"  -> Stage all changes and commit them cleanly")
    print("  sync              -> Push your local saves straight to GitHub")
    print("  pull              -> Pull down the latest updates from GitHub")
    print("  check             -> Show a simplified, clean view of modified files")
    print("  undo              -> Safely unstage files back to your last save")

def main():
    if len(sys.argv) < 2:
        show_help()
        return

    cmd = sys.argv[1].lower()

    # NEW: Setup command that works inside or outside a repo
    if cmd == "setup":
        print("Better Git Configuration Wizard")
        print("1. Set Identity (Fixes 'who you are' errors)")
        print("2. Link a GitHub Remote URL")
        choice = input("Choose an option (1 or 2): ").strip()

        if choice == "1":
            name = input("Enter your GitHub Username: ").strip()
            email = input("Enter your GitHub Email: ").strip()
            if name and email:
                run_cmd(["git", "config", "--global", "user.name", name])
                run_cmd(["git", "config", "--global", "user.email", email])
                print(f"Identity saved globally! Name: {name} | Email: {email}")
            else:
                print("Setup cancelled. Name and email cannot be empty.")
        elif choice == "2":
            if not check_git_repo():
                print("Error: You must run 'better-git init' in this directory before linking a remote repo.")
                return
            url = input("Paste your GitHub repository HTTPS URL: ").strip()
            if url:
                # Remove existing origin if it exists to avoid errors
                run_cmd(["git", "remote", "remove", "origin"])
                code, _, err = run_cmd(["git", "remote", "add", "origin", url])
                if code == 0:
                    print(f"Successfully linked remote repository to: {url}")
                else:
                    print(f"Failed to link remote: {err}")
            else:
                print("Remote URL cannot be empty.")
        else:
            print("Invalid selection.")
        return

    if cmd == "init":
        if check_git_repo():
            print("[!] This directory is already a Git repository.")
            return
        code, _, err = run_cmd(["git", "init"])
        if code == 0:
            run_cmd(["git", "checkout", "-b", "main"])
            print("Initialized a clean local Git repository with branch 'main'.")
            print("Next, run 'better-git setup' to link your GitHub repository URL!")
        else:
            print(f"Failed to initialize repository: {err}")
        return

    # Enforce repo presence for remaining commands
    if not check_git_repo():
        print("Error: Not a Git repository.")
        print("Run 'better-git init' here first to get started!")
        return

    if cmd == "save":
        if len(sys.argv) < 3:
            print("Usage: better-git save \"your commit message\"")
            return
        msg = sys.argv[2]
        
        run_cmd(["git", "add", "."])
        code, out, err = run_cmd(["git", "commit", "-m", msg])
        if code == 0:
            print(f"Save successful!\n{out}")
        elif "nothing to commit" in out or "nothing to commit" in err:
            print("Nothing to save. Everything is already up to date!")
        else:
            print(f"Save failed: {err}\nHint: Try running better-git setup' option 1 first.")

    elif cmd == "sync":
        print("Syncing with GitHub...")
        _, branch, _ = run_cmd(["git", "branch", "--show-current"])
        branch = branch or "main"
        
        code, out, err = run_cmd(["git", "push", "-u", "origin", branch])
        if code == 0:
            print(f"Sync complete! Pushed cleanly to remote branch '{branch}'.")
        else:
            print(f"Sync failed.\n{err}")
            print("\nHOW TO FIX REJECTED PUSHES / AUTH ERRORS:")
            print("1. Run 'better-git setup' to ensure your project's GitHub URL link is correct.")
            print("2. When GitHub asks for your password in the terminal, you CANNOT use your regular login password.")
            print("3. You must use a GitHub Personal Access Token (PAT) as your password instead.")

    elif cmd == "pull":
        print("Pulling updates from GitHub...")
        _, branch, _ = run_cmd(["git", "branch", "--show-current"])
        branch = branch or "main"
        
        code, out, err = run_cmd(["git", "pull", "origin", branch])
        if code == 0:
            print("Successfully pulled latest updates!")
        else:
            print(f"Pull failed: {err}")

    elif cmd == "check":
        code, out, _ = run_cmd(["git", "status", "-s"])
        if code == 0:
            if not out:
                print("Workspace is completely clean!")
            else:
                print("Current changes waiting to be saved:")
                print(out)
        else:
            print("Failed to read workspace status.")

    elif cmd == "undo":
        code, _, err = run_cmd(["git", "reset"])
        if code == 0:
            print("Successfully undid staging. Your files are safe but unsaved.")
        else:
            print(f"Undo failed: {err}")

    else:
        print(f"Unknown command: '{cmd}'")
        show_help()

if __name__ == "__main__":
    main()
