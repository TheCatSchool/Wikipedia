import random
import os
import socket
import subprocess
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)


def git_pull(repo_path):
    try:
        result = subprocess.run(
            ["git", "pull"],
            cwd=repo_path,
            text=True,
            capture_output=True,
            check=True
        )
        print("Pull successful:\n", result.stdout)
    except subprocess.CalledProcessError as e:
            print("Error during pull:\n", e.stderr)
def git_push(repo_path, commit_message="Auto commit"):
    try:
        subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
        subprocess.run(["git", "commit", "-m", commit_message], cwd=repo_path, check=True)
        result = subprocess.run(
            ["git", "push"],
            cwd=repo_path,
            text=True,
            capture_output=True,
            check=True
        )
        print("Push successful:\n", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error during push:\n", e.stderr)
        
def cmd(x):
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    if x == 1:
        print("Running git pull...")
        git_pull(repo_dir)
        menu()
    elif x == 2:
        print("Running git push...")
        updmsg = str(input("commit msg? "))
        git_push(repo_dir, updmsg)
        menu() 
def menu(): 

    print( "     === GITACT MENU ===")
    print("  ")
    print("    == cmd1 (git pull) ==")
    print("    == cmd2 (git push) ==" )
    choice = int(input("      execute cmd?"))
    cmd(choice)

menu()