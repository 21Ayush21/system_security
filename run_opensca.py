import os
import subprocess

OPEN_SCA_PATH = r".\opensca\opensca-cli.exe"
REPOS_DIR = "repos"
RESULTS_DIR = "sca_results"

OPEN_SCA_TOKEN = "1934ea2c-71fd-4a26-95f2-d441ad040555"  # don't commit this

os.makedirs(RESULTS_DIR, exist_ok=True)

repo_names = [
    name for name in os.listdir(REPOS_DIR)
    if os.path.isdir(os.path.join(REPOS_DIR, name))
]

print(f"Found {len(repo_names)} repositories to scan.")

for repo_name in repo_names:
    repo_path = os.path.join(REPOS_DIR, repo_name)
    out_file = os.path.join(RESULTS_DIR, f"{repo_name}.json")

    if os.path.exists(out_file):
        print(f"[SKIP] {repo_name} -> result already exists")
        continue

    print(f"\n[SCAN] {repo_name}")
    cmd = [
        OPEN_SCA_PATH,
        "-token", OPEN_SCA_TOKEN,
        "-path", repo_path,
        "-out", out_file,
    ]
    print("Running:", " ".join(cmd))

    subprocess.run(cmd)

print("\nAll scans finished (for repos that did not have results yet).")
