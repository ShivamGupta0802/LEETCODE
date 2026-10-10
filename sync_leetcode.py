
import os
import re
import time
import subprocess
from pathlib import Path

import requests

ROOT = Path(r"C:\Users\ayush\LEETCODE")
API = "https://leetcode.com/graphql/"

SESSION = os.getenv("LEETCODE_SESSION")
CSRF = os.getenv("LEETCODE_CSRF_TOKEN", "")

if not SESSION:
    raise SystemExit("Set LEETCODE_SESSION in PowerShell first.")

http = requests.Session()
http.headers.update({
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://leetcode.com/",
    "Origin": "https://leetcode.com",
    "Content-Type": "application/json",
})
http.cookies.set("LEETCODE_SESSION", SESSION, domain=".leetcode.com")

if CSRF:
    http.cookies.set("csrftoken", CSRF, domain=".leetcode.com")
    http.headers["x-csrftoken"] = CSRF


def graphql(query, variables, operation):
    response = http.post(
        API,
        json={
            "query": query,
            "variables": variables,
            "operationName": operation,
        },
        timeout=30,
    )

    if not response.ok:
        raise RuntimeError(
            f"HTTP {response.status_code}: {response.text[:500]}"
        )

    result = response.json()

    if result.get("errors"):
        raise RuntimeError(str(result["errors"])[:1000])

    if not result.get("data"):
        raise RuntimeError("LeetCode returned no data.")

    return result["data"]


USER_QUERY = """
query globalData {
  userStatus {
    username
    isSignedIn
  }
}
"""

RECENT_QUERY = """
query recentAcSubmissions($username: String!, $limit: Int!) {
  recentAcSubmissionList(username: $username, limit: $limit) {
    id
    title
    titleSlug
    timestamp
  }
}
"""

DETAIL_QUERY = """
query submissionDetails($submissionId: Int!) {
  submissionDetails(submissionId: $submissionId) {
    runtimeDisplay
    runtimePercentile
    memoryDisplay
    memoryPercentile
    statusCode
    code
    timestamp
    lang {
      name
    }
    question {
      questionFrontendId
      title
      titleSlug
    }
  }
}
"""


def get_username():
    user = graphql(USER_QUERY, {}, "globalData").get("userStatus") or {}

    if not user.get("isSignedIn") or not user.get("username"):
        raise RuntimeError("LeetCode session is not authenticated.")

    return user["username"]


def slug_from_readme(folder):
    readme = folder / "README.md"
    if not readme.exists():
        return None

    content = readme.read_text(encoding="utf-8", errors="replace")

    match = re.search(
        r"leetcode\.com/problems/([a-z0-9-]+)",
        content,
        re.IGNORECASE,
    )
    if match:
        return match.group(1).lower()

    # Fall back to folder names such as 278-first-bad-version.
    match = re.match(r"^\d+-(.+)$", folder.name)
    return match.group(1).lower() if match else None


def format_percentile(value):
    if value is None:
        return "N/A"

    try:
        return f"{float(value):.2f}%"
    except (TypeError, ValueError):
        return "N/A"


def update_readme(folder, details):
    readme = folder / "README.md"

    if not readme.exists():
        print("Skipped: README missing:", folder.name)
        return None

    runtime = details.get("runtimeDisplay")
    memory = details.get("memoryDisplay")
    runtime_pct = format_percentile(details.get("runtimePercentile"))
    memory_pct = format_percentile(details.get("memoryPercentile"))

    if not runtime or not memory:
        print("Skipped: statistics unavailable:", folder.name)
        return None

    submission_id = details.get("submissionId")
    url = f"https://leetcode.com/submissions/detail/{submission_id}/"

    line = (
        f"[Time: {runtime} ({runtime_pct}) | "
        f"Memory: {memory} ({memory_pct})]({url})"
    )

    old = readme.read_text(encoding="utf-8", errors="replace")

    # Replace an existing statistics line instead of duplicating it.
    pattern = re.compile(
        r"^\[Time:.*?\]\(https?://leetcode\.com/submissions/detail/.*?\)$",
        re.MULTILINE,
    )

    if pattern.search(old):
        new = pattern.sub(line, old, count=1)
    else:
        new = line + "\n\n" + old

    if new == old:
        return None

    readme.write_text(new, encoding="utf-8")
    return line


def main():
    if not (ROOT / ".git").exists():
        raise RuntimeError(f"Not a Git repository: {ROOT}")

    os.chdir(ROOT)

    # This script updates files; commit/push only after review.
    username = get_username()
    print("Authenticated as:", username)

    submissions = graphql(
        RECENT_QUERY,
        {"username": username, "limit": 100},
        "recentAcSubmissions",
    ).get("recentAcSubmissionList")

    if submissions is None:
        raise RuntimeError("Recent submissions list is unavailable.")

    # Use the newest returned accepted submission for each problem.
    latest = {}
    for item in submissions:
        slug = item.get("titleSlug")
        if slug:
            latest.setdefault(slug.lower(), item)

    folders = [p for p in ROOT.iterdir() if p.is_dir() and p.name != ".git"]
    changed = []

    for folder in folders:
        slug = slug_from_readme(folder)
        if not slug or slug not in latest:
            continue

        submission = latest[slug]

        try:
            details = graphql(
                DETAIL_QUERY,
                {"submissionId": int(submission["id"])},
                "submissionDetails",
            ).get("submissionDetails")

            if not details:
                print("No details:", slug)
                continue

            # Only update statistics for Java submissions.
            language = (details.get("lang") or {}).get("name", "")
            if "java" not in language.lower():
                print(f"Skipped non-Java submission: {slug} ({language})")
                continue

            if details.get("statusCode") not in (10, "10"):
                print("Skipped submission not marked accepted:", slug)
                continue

            details["submissionId"] = submission["id"]
            line = update_readme(folder, details)

            if line:
                changed.append((folder, line))
                print("Updated:", folder.name, line)
            else:
                print("No update needed:", folder.name)

        except Exception as exc:
            print("Failed:", slug, exc)

        time.sleep(0.3)

    print(f"\nUpdated {len(changed)} README files.")

    if not changed:
        print("No changes to commit.")
        return

    print("\nReview your changes with: git diff")
    answer = input("Commit all README updates and push? (y/n): ")

    if answer.strip().lower() != "y":
        print("Changes saved locally only.")
        return

    subprocess.run(["git", "add", "."], check=True)

    if subprocess.run(["git", "diff", "--cached", "--quiet"]).returncode == 0:
        print("No staged changes.")
        return

    subprocess.run(
        ["git", "commit", "-m", "Update LeetCode runtime and memory stats"],
        check=True,
    )
    subprocess.run(["git", "push"], check=True)
    print("README updates pushed successfully.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("\nFAILED:", exc)
