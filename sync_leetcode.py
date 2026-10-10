
import os
import re
import json
import time
import getpass
import subprocess
from pathlib import Path
from datetime import datetime, timezone

import requests

ROOT = Path(__file__).resolve().parent
API = "https://leetcode.com/graphql/"
REPO_URL = "https://github.com/ShivamGupta0802/LEETCODE.git"
PAGE_SIZE = 20
FAILURE_LOG = ROOT / "retrieval_failures.jsonl"


def git(*args, env=None, check=True):
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
    )
    if check and result.returncode:
        raise RuntimeError(result.stderr or result.stdout)
    return result


def setup_git():
    if not (ROOT / ".git").is_dir():
        raise RuntimeError(
            f"No Git repository found at {ROOT}. Nothing was reset."
        )

    if not git("config", "user.name", check=False).stdout.strip():
        git("config", "user.name", input("Git author name: ").strip())

    if not git("config", "user.email", check=False).stdout.strip():
        email = input("GitHub-linked email: ").strip()
        if not email:
            raise RuntimeError("Git author email is required.")
        git("config", "user.email", email)

    remotes = git("remote").stdout.split()
    if "origin" in remotes:
        git("remote", "set-url", "origin", REPO_URL)
    else:
        git("remote", "add", "origin", REPO_URL)


def make_session():
    session_cookie = os.getenv("LEETCODE_SESSION")
    csrf = os.getenv("LEETCODE_CSRF_TOKEN")

    if not session_cookie:
        session_cookie = getpass.getpass("LEETCODE_SESSION: ")
    if not csrf:
        csrf = getpass.getpass("csrftoken: ")

    if not session_cookie.strip() or not csrf.strip():
        raise RuntimeError("Both LeetCode cookies are required.")

    session = requests.Session()
    session.cookies.set(
        "LEETCODE_SESSION", session_cookie.strip(), domain="leetcode.com"
    )
    session.cookies.set("csrftoken", csrf.strip(), domain="leetcode.com")
    session.headers.update({
        "Content-Type": "application/json",
        "Referer": "https://leetcode.com/",
        "Origin": "https://leetcode.com",
        "x-csrftoken": csrf.strip(),
        "User-Agent": "Mozilla/5.0",
    })
    return session


def graphql(session, query, variables):
    response = session.post(
        API,
        json={"query": query, "variables": variables},
        timeout=(10, 30),
    )

    if not response.ok:
        raise RuntimeError(
            f"HTTP {response.status_code}: {response.text[:2000]}"
        )

    try:
        payload = response.json()
    except ValueError:
        raise RuntimeError(
            f"Non-JSON response: {response.text[:1000]}"
        )

    if payload.get("errors"):
        raise RuntimeError(
            json.dumps(payload["errors"], indent=2)[:2500]
        )

    if payload.get("data") is None:
        raise RuntimeError("LeetCode returned no GraphQL data.")

    return payload["data"]


def fetch_all_submissions(session):
    query = """
    query submissionList(
      $offset: Int!,
      $limit: Int!,
      $lastKey: String
    ) {
      submissionList(
        offset: $offset,
        limit: $limit,
        lastKey: $lastKey
      ) {
        lastKey
        hasNext
        submissions {
          id
          title
          titleSlug
          timestamp
          statusDisplay
          lang
          runtime
          memory
        }
      }
    }
    """

    result = []
    seen = set()
    offset = 0
    last_key = None

    while True:
        data = graphql(
            session,
            query,
            {
                "offset": offset,
                "limit": PAGE_SIZE,
                "lastKey": last_key,
            },
        )
        page = data.get("submissionList")

        if not isinstance(page, dict):
            raise RuntimeError("Invalid submissionList response.")

        items = page.get("submissions") or []
        new_count = 0

        for item in items:
            sid = str(item.get("id", ""))
            if sid and sid not in seen:
                seen.add(sid)
                result.append(item)
                new_count += 1

        print(f"Fetched {len(result)} submissions")

        if not page.get("hasNext") or not items or not new_count:
            break

        offset += len(items)
        last_key = page.get("lastKey")
        time.sleep(0.25)

    return result


def fetch_submission_details(session, submission_id):
    query = """
    query submissionDetails($submissionId: Int!) {
      submissionDetails(submissionId: $submissionId) {
        code
        runtime
        memory
        timestamp
        lang {
          name
          verboseName
        }
        question {
          questionId
          title
          titleSlug
          difficulty
        }
      }
    }
    """

    data = graphql(
        session,
        query,
        {"submissionId": int(submission_id)},
    )
    details = data.get("submissionDetails")

    if not details:
        raise RuntimeError("No submission details returned.")

    return details


def slugify(value):
    return re.sub(r"[^a-z0-9-]+", "-", value.lower()).strip("-")


def get_language(details, submission):
    lang = details.get("lang")
    if isinstance(lang, dict):
        lang = lang.get("name") or lang.get("verboseName")
    return str(lang or submission.get("lang") or "unknown")


def extension(language):
    return {
        "java": ".java",
        "python": ".py",
        "python3": ".py",
        "cpp": ".cpp",
        "c++": ".cpp",
        "c": ".c",
        "javascript": ".js",
        "typescript": ".ts",
        "kotlin": ".kt",
        "csharp": ".cs",
        "go": ".go",
        "golang": ".go",
        "rust": ".rs",
        "swift": ".swift",
        "ruby": ".rb",
        "mysql": ".sql",
        "mssql": ".sql",
    }.get(language.lower(), ".txt")


def record_failure(submission, error):
    record = {
        "submissionId": submission.get("id"),
        "title": submission.get("title"),
        "titleSlug": submission.get("titleSlug"),
        "timestamp": submission.get("timestamp"),
        "error": str(error),
    }
    with FAILURE_LOG.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record, ensure_ascii=False) + "\n")


def select_latest_accepted(submissions):
    latest = {}

    for item in submissions:
        if item.get("statusDisplay") != "Accepted":
            continue
        if not item.get("timestamp") or not item.get("id"):
            continue

        slug = item.get("titleSlug")
        if not slug:
            continue

        current = latest.get(slug)
        if current is None or int(item["timestamp"]) > int(
            current["timestamp"]
        ):
            latest[slug] = item

    return sorted(
        latest.values(),
        key=lambda item: int(item["timestamp"]),
    )


def save_solution(submission, details):
    question = details.get("question") or {}
    slug = (
        question.get("titleSlug")
        or submission.get("titleSlug")
        or f"submission-{submission['id']}"
    )
    title = question.get("title") or submission.get("title") or slug
    question_id = question.get("questionId")

    folder_name = (
        f"{question_id}-{slug}" if question_id else slugify(slug)
    )
    folder = ROOT / slugify(folder_name)
    folder.mkdir(parents=True, exist_ok=True)

    code = details.get("code")
    if not isinstance(code, str) or not code.strip():
        raise RuntimeError("LeetCode returned no source code.")

    language = get_language(details, submission)
    solution_file = folder / f"Solution{extension(language)}"
    solution_file.write_text(code, encoding="utf-8")

    timestamp = int(submission["timestamp"])
    date_text = datetime.fromtimestamp(
        timestamp, timezone.utc
    ).strftime("%Y-%m-%d %H:%M:%S UTC")

    runtime = details.get("runtime") or submission.get("runtime") or "N/A"
    memory = details.get("memory") or submission.get("memory") or "N/A"

    metadata = {
        "submissionId": str(submission["id"]),
        "title": title,
        "titleSlug": slug,
        "questionId": question_id,
        "language": language,
        "timestamp": timestamp,
        "dateUTC": date_text,
        "runtime": runtime,
        "memory": memory,
    }

    (folder / "submission.json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    readme = folder / "README.md"
    if not readme.exists():
        readme.write_text(
            f"""# {title}

- **Problem:** https://leetcode.com/problems/{slug}/
- **Problem ID:** {question_id or "Unknown"}
- **Difficulty:** {question.get("difficulty") or "Unknown"}
- **Language:** {language}
- **Latest Accepted submission:** {date_text}

## Performance

- **Runtime:** {runtime}
- **Memory:** {memory}

## Complexity

- **Time complexity:** Review required.
- **Space complexity:** Review required.

Verify both complexities against the algorithm and input constraints.
""",
            encoding="utf-8",
        )

    return folder, runtime, memory


def commit_solution(folder, submission, runtime, memory):
    relative = folder.relative_to(ROOT).as_posix()
    git("add", "--", relative)

    diff = git("diff", "--cached", "--quiet", check=False)
    if diff.returncode == 0:
        print("  No changes to commit.")
        return False
    if diff.returncode != 1:
        raise RuntimeError("Could not inspect staged changes.")

    message = (
        f"Time: {runtime} (N/A) | Memory: {memory} (N/A) - LeetSync"
    )

    timestamp = int(submission["timestamp"])
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = f"@{timestamp}"
    env["GIT_COMMITTER_DATE"] = f"@{timestamp}"

    git("commit", "-m", message, env=env)
    return True


def main():
    setup_git()
    session = make_session()

    print("\nFetching submission history...")
    try:
        submissions = fetch_all_submissions(session)
    except Exception as error:
        print(f"History retrieval failed: {error}")
        return

    selected = select_latest_accepted(submissions)

    print(f"\nAll submissions found: {len(submissions)}")
    print(f"Unique problems with Accepted submissions: {len(selected)}")

    if not selected:
        print("No accepted problems found.")
        return

    if input(
        "Type LATEST to save only the latest Accepted code per problem: "
    ).strip() != "LATEST":
        print("Cancelled.")
        return

    success = 0
    failures = 0
    commits = 0

    for index, submission in enumerate(selected, 1):
        print(
            f"\n[{index}/{len(selected)}] "
            f"{submission.get('title') or submission.get('titleSlug')} "
            f"(submission {submission['id']})"
        )

        try:
            details = fetch_submission_details(session, submission["id"])
            folder, runtime, memory = save_solution(submission, details)
            success += 1

            if commit_solution(folder, submission, runtime, memory):
                commits += 1
                print("  Latest solution saved and committed.")
            else:
                print("  Files already match; commit skipped.")

        except Exception as error:
            failures += 1
            record_failure(submission, error)
            print(f"  FAILED: {error}")

        time.sleep(0.25)

    print("\n========== SUMMARY ==========")
    print(f"Unique solved problems: {len(selected)}")
    print(f"Latest solutions retrieved: {success}")
    print(f"Failures: {failures}")
    print(f"New commits: {commits}")
    print(f"Failure details: {FAILURE_LOG}")
    print("\nNothing was pushed to GitHub automatically.")


if __name__ == "__main__":
    main()
