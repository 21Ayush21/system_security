import os
import json
import pandas as pd

# Set absolute output directory to avoid missing files
INPUT_DIR = "sca_results"            # <--- your folder with 55 JSONs
OUTPUT_DIR = "./output"                

os.makedirs(OUTPUT_DIR, exist_ok=True)

PARSED_FILE = os.path.join(OUTPUT_DIR, "parsed_results.csv")
DEP_SUMMARY_FILE = os.path.join(OUTPUT_DIR, "dependency_summary.csv")
PROJECT_SUMMARY_FILE = os.path.join(OUTPUT_DIR, "project_summary.csv")


def flatten_vuln(project, dep, vuln):
    return {
        "project": project,
        "dependency": dep.get("name"),
        "dependency_version": dep.get("version"),
        "direct_dependency": dep.get("direct", False),
        "cve_id": vuln.get("cve_id"),
        "cwe_id": vuln.get("cwe_id"),
        "release_date": vuln.get("release_date"),
        "description": vuln.get("description"),
        "security_level_id": vuln.get("security_level_id"),
        "exploit_level_id": vuln.get("exploit_level_id")
    }


def walk(node, project, rows):
    if isinstance(node, dict):
        # Identify dependency nodes
        if "name" in node and "language" in node:
            if "vulnerabilities" in node and node["vulnerabilities"]:
                for vuln in node["vulnerabilities"]:
                    rows.append(flatten_vuln(project, node, vuln))

        for key, value in node.items():
            walk(value, project, rows)

    elif isinstance(node, list):
        for item in node:
            walk(item, project, rows)


def parse_file(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    project = data.get("task_info", {}).get("app_name", os.path.basename(path))
    rows = []
    walk(data, project, rows)
    return rows


def main():
    all_rows = []

    print("\n=== STARTING PARSE ===")
    print("Reading from:", os.path.abspath(INPUT_DIR))
    print("Writing outputs to:", os.path.abspath(OUTPUT_DIR))

    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".json"):
            path = os.path.join(INPUT_DIR, filename)
            print("Parsing:", filename)

            try:
                rows = parse_file(path)
                all_rows.extend(rows)
                print(f"  → Extracted {len(rows)} rows.")
            except Exception as e:
                print("ERROR parsing", filename, ":", e)

    df = pd.DataFrame(all_rows)
    df.to_csv(PARSED_FILE, index=False)

    print("\n=== RESULTS ===")
    print("Total vulnerability rows:", len(df))
    print("parsed_results.csv saved to:", PARSED_FILE)

    if len(df) == 0:
        print("\nWARNING: parsed_results.csv is empty. No summaries created.")
        return

    # Dependency summary
    dep_summary = df.groupby("dependency").agg(
        projects=("project", "nunique"),
        total_cves=("cve_id", "nunique"),
        rows=("cve_id", "count")
    ).reset_index()

    dep_summary.to_csv(DEP_SUMMARY_FILE, index=False)
    print("dependency_summary.csv saved to:", DEP_SUMMARY_FILE)

    # Project summary
    project_summary = df.groupby("project").agg(
        vulnerable_dependencies=("dependency", "nunique"),
        total_cves=("cve_id", "nunique"),
        rows=("cve_id", "count")
    ).reset_index()

    project_summary.to_csv(PROJECT_SUMMARY_FILE, index=False)
    print("project_summary.csv saved to:", PROJECT_SUMMARY_FILE)


if __name__ == "__main__":
    main()

