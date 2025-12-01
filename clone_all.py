import os
import subprocess

# Path to repo list
REPO_FILE = "repo_names.txt"

# Create output folder
os.makedirs("repos", exist_ok=True)

# Read repos
with open(REPO_FILE, "r") as f:
    repos = [line.strip() for line in f.readlines() if line.strip()]

# Clone each repo
for repo in repos:
    print(f"\n=== Cloning {repo} ===")
    url = f"https://github.com/{repo}.git"

    # Replace "/" because Windows cannot use it in folder names
    folder_name = repo.replace("/", "_")
    dest = os.path.join("repos", folder_name)

    # Skip if already cloned
    if os.path.exists(dest):
        print(f"Skipping {repo}, folder already exists.")
        continue

    subprocess.run(["git", "clone", url, dest])

print("\nDONE! All repositories cloned.")
