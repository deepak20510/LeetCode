import json
import re
import urllib.request
import urllib.error
from collections import defaultdict
from pathlib import Path


# =========================================================
# Configuration
# =========================================================

ROOT = Path(__file__).resolve().parent.parent
README_FILE = ROOT / "README.md"
TOPICS_CACHE_FILE = ROOT / "scripts" / "topics_cache.json"

REPOSITORY_URL = "https://github.com/deepak20510/LeetCode"

LEETCODE_GRAPHQL_URL = "https://leetcode.com/graphql"


LANGUAGES = {
    ".java": "Java",
    ".py": "Python",
    ".cpp": "C++",
    ".c": "C",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".go": "Go",
    ".rs": "Rust",
    ".kt": "Kotlin",
    ".cs": "C#",
    ".sql": "SQL",
    ".swift": "Swift",
    ".rb": "Ruby",
    ".php": "PHP",
    ".scala": "Scala",
}


# =========================================================
# Topics cache
# =========================================================

def load_topics_cache():
    """
    Load locally cached LeetCode topics.
    Return an empty dictionary if the cache is missing
    or invalid.
    """

    if not TOPICS_CACHE_FILE.exists():
        return {}

    try:
        content = TOPICS_CACHE_FILE.read_text(encoding="utf-8")
        data = json.loads(content)

        if isinstance(data, dict):
            return data

    except (OSError, json.JSONDecodeError) as error:
        print(f"Warning: Could not load topics cache: {error}")

    return {}


def save_topics_cache(cache):
    """
    Save topic metadata in a deterministic format.
    """

    try:
        TOPICS_CACHE_FILE.write_text(
            json.dumps(
                cache,
                indent=2,
                ensure_ascii=False,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )

    except OSError as error:
        print(f"Warning: Could not save topics cache: {error}")


# =========================================================
# Fetch topics from LeetCode
# =========================================================

def fetch_topics_from_leetcode(slug):
    """
    Fetch topic tags for one problem from LeetCode GraphQL.

    If anything fails, return an empty list so README
    generation can continue safely.
    """

    query = """
    query getQuestionDetail($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        topicTags {
          name
          slug
        }
      }
    }
    """

    payload = json.dumps({
        "query": query,
        "variables": {
            "titleSlug": slug
        }
    }).encode("utf-8")

    request = urllib.request.Request(
        LEETCODE_GRAPHQL_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
            "Referer": f"https://leetcode.com/problems/{slug}/",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=10,
        ) as response:

            response_data = json.loads(
                response.read().decode("utf-8")
            )

        question = (
            response_data
            .get("data", {})
            .get("question")
        )

        if not question:
            print(
                f"Warning: No topic data returned for {slug}."
            )
            return []

        topic_tags = question.get("topicTags", [])

        topics = sorted({
            topic.get("name", "").strip()
            for topic in topic_tags
            if topic.get("name", "").strip()
        })

        return topics

    except (
        urllib.error.URLError,
        urllib.error.HTTPError,
        TimeoutError,
        json.JSONDecodeError,
        OSError,
    ) as error:

        print(
            f"Warning: Could not fetch topics "
            f"for {slug}: {error}"
        )

        return []


# =========================================================
# Parse problem README
# =========================================================

def parse_problem_readme(readme_path):
    """
    Extract problem number, title, LeetCode URL,
    difficulty and slug from a LeetHub-generated README.
    """

    try:
        content = readme_path.read_text(encoding="utf-8")

    except (OSError, UnicodeDecodeError) as error:
        print(f"Warning: Could not read {readme_path}: {error}")
        return None

    problem_match = re.search(
        r'<h2>\s*<a\s+href="([^"]+)"[^>]*>'
        r'\s*(\d+)\.\s*(.*?)\s*</a>\s*</h2>',
        content,
        re.IGNORECASE | re.DOTALL,
    )

    difficulty_match = re.search(
        r'<h3>\s*(Easy|Medium|Hard)\s*</h3>',
        content,
        re.IGNORECASE,
    )

    if not problem_match:
        return None

    leetcode_url = problem_match.group(1).strip()
    number = int(problem_match.group(2))

    title = re.sub(
        r"<[^>]+>",
        "",
        problem_match.group(3),
    ).strip()

    if difficulty_match:
        difficulty = difficulty_match.group(1).capitalize()
    else:
        difficulty = "Unknown"

    # Extract slug from URL:
    # https://leetcode.com/problems/valid-palindrome
    slug_match = re.search(
        r"leetcode\.com/problems/([^/?#]+)",
        leetcode_url,
        re.IGNORECASE,
    )

    if not slug_match:
        return None

    slug = slug_match.group(1)

    return {
        "number": number,
        "title": title,
        "leetcode_url": leetcode_url,
        "difficulty": difficulty,
        "slug": slug,
    }


# =========================================================
# Detect programming languages
# =========================================================

def detect_languages(problem_folder):

    detected = set()

    for file in problem_folder.iterdir():

        if not file.is_file():
            continue

        extension = file.suffix.lower()

        if extension in LANGUAGES:
            detected.add(LANGUAGES[extension])

    return sorted(detected)


# =========================================================
# Find all problems
# =========================================================

def get_all_problems(topics_cache):

    folder_pattern = re.compile(r"^\d+-.+$")

    problems = []
    cache_changed = False

    for item in ROOT.iterdir():

        if not item.is_dir():
            continue

        if not folder_pattern.match(item.name):
            continue

        problem_readme = item / "README.md"

        if not problem_readme.exists():
            print(
                f"Warning: No README found in {item.name}. "
                "Skipping this folder."
            )
            continue

        problem = parse_problem_readme(problem_readme)

        if not problem:
            print(
                f"Warning: Could not parse README in {item.name}. "
                "Skipping this folder."
            )
            continue

        slug = problem["slug"]

        # Use cached topics when available.
        if slug in topics_cache:
            topics = topics_cache[slug]

        else:
            print(f"Fetching topics for {slug}...")

            topics = fetch_topics_from_leetcode(slug)

            # Cache only successful, non-empty results.
            # Failed lookups can be retried on the next workflow run.
            if topics:
                topics_cache[slug] = topics
                cache_changed = True

        problem["folder"] = item.name
        problem["languages"] = detect_languages(item)
        problem["topics"] = topics

        problems.append(problem)

    return (
        sorted(
            problems,
            key=lambda problem: problem["number"]
        ),
        cache_changed,
    )


# =========================================================
# Formatting
# =========================================================

def format_difficulty(difficulty):

    labels = {
        "Easy": "🟢 Easy",
        "Medium": "🟡 Medium",
        "Hard": "🔴 Hard",
    }

    return labels.get(difficulty, "⚪ Unknown")


def create_problem_row(problem):

    languages = ", ".join(
        problem["languages"]
    ) or "Unknown"

    solution_url = (
        f"{REPOSITORY_URL}/tree/main/"
        f"{problem['folder']}"
    )

    return (
        f"| {problem['number']} "
        f"| [{problem['title']}]"
        f"({problem['leetcode_url']}) "
        f"| {format_difficulty(problem['difficulty'])} "
        f"| {languages} "
        f"| [View Solution]({solution_url}) |"
    )


# =========================================================
# README generation
# =========================================================

def generate_readme():

    topics_cache = load_topics_cache()

    problems, cache_changed = get_all_problems(
        topics_cache
    )

    if cache_changed:
        save_topics_cache(topics_cache)

    total = len(problems)

    easy = sum(
        problem["difficulty"] == "Easy"
        for problem in problems
    )

    medium = sum(
        problem["difficulty"] == "Medium"
        for problem in problems
    )

    hard = sum(
        problem["difficulty"] == "Hard"
        for problem in problems
    )

    unknown = sum(
        problem["difficulty"] == "Unknown"
        for problem in problems
    )

    lines = [
        "# 🚀 LeetCode Solutions",
        "",
        "A collection of my LeetCode solutions, automatically synced "
        "using LeetHub-3.0 and tracked with GitHub Actions.",
        "",
        "## 📊 Progress",
        "",
        f"**Total Problems Solved: {total}**",
        "",
        "| Difficulty | Solved |",
        "|---|---:|",
        f"| 🟢 Easy | {easy} |",
        f"| 🟡 Medium | {medium} |",
        f"| 🔴 Hard | {hard} |",
    ]

    if unknown > 0:
        lines.append(
            f"| ⚪ Unknown | {unknown} |"
        )

    lines.extend([
        "",
        "## 📚 All Problems",
        "",
        "| # | Problem | Difficulty | Language | Solution |",
        "|---:|---|---|---|---|",
    ])

    for problem in problems:
        lines.append(create_problem_row(problem))

    # Group problems by topic
    topics = defaultdict(list)
    uncategorized = []

    for problem in problems:

        if problem["topics"]:

            for topic in problem["topics"]:
                topics[topic].append(problem)

        else:
            uncategorized.append(problem)

    if topics or uncategorized:

        lines.extend([
            "",
            "## 🏷️ Topics",
            "",
        ])

        for topic in sorted(topics):

            lines.extend([
                f"### {topic}",
                "",
                "| # | Problem | Difficulty | Language | Solution |",
                "|---:|---|---|---|---|",
            ])

            for problem in topics[topic]:
                lines.append(
                    create_problem_row(problem)
                )

            lines.append("")

        if uncategorized:

            lines.extend([
                "### Uncategorized",
                "",
                "| # | Problem | Difficulty | Language | Solution |",
                "|---:|---|---|---|---|",
            ])

            for problem in uncategorized:
                lines.append(
                    create_problem_row(problem)
                )

            lines.append("")

    lines.extend([
        "---",
        "",
        "_README automatically updated with GitHub Actions._",
        "",
    ])

    README_FILE.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print(
        f"README generated successfully with "
        f"{total} problems."
    )


if __name__ == "__main__":
    generate_readme()