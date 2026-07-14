import json
import re
import subprocess
import urllib.error
import urllib.parse
import urllib.request

from collections import defaultdict
from datetime import datetime, date, timedelta
from pathlib import Path


# =========================================================
# Configuration
# =========================================================

ROOT = Path(__file__).resolve().parent.parent

README_FILE = ROOT / "README.md"

TOPICS_CACHE_FILE = (
    ROOT / "scripts" / "topics_cache.json"
)

REPOSITORY_URL = (
    "https://github.com/deepak20510/LeetCode"
)

LEETCODE_GRAPHQL_URL = (
    "https://leetcode.com/graphql"
)

# Personal progress goal
PROBLEM_GOAL = 150

# Number of recent solutions displayed
RECENT_PROBLEMS_LIMIT = 10


# =========================================================
# Supported programming languages
# =========================================================

LANGUAGES = {
    ".java": "Java",
    ".py": "Python",
    ".cpp": "C++",
    ".c": "C",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".jsx": "JavaScript",
    ".go": "Go",
    ".rs": "Rust",
    ".kt": "Kotlin",
    ".kts": "Kotlin",
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
    Safely load cached LeetCode topics.
    """

    if not TOPICS_CACHE_FILE.exists():
        return {}

    try:
        content = TOPICS_CACHE_FILE.read_text(
            encoding="utf-8"
        )

        data = json.loads(content)

        if isinstance(data, dict):
            return data

    except (
        OSError,
        json.JSONDecodeError,
    ) as error:

        print(
            f"Warning: Could not load "
            f"topics cache: {error}"
        )

    return {}


def save_topics_cache(cache):
    """
    Save topics cache deterministically.
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
        print(
            f"Warning: Could not save "
            f"topics cache: {error}"
        )


# =========================================================
# Fetch topics from LeetCode
# =========================================================

def fetch_topics_from_leetcode(slug):
    """
    Fetch topic tags from LeetCode GraphQL.

    Failure never stops README generation.
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
        },
    }).encode("utf-8")

    request = urllib.request.Request(
        LEETCODE_GRAPHQL_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
            "Referer": (
                f"https://leetcode.com/problems/{slug}/"
            ),
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
                f"Warning: No topic data "
                f"returned for {slug}."
            )
            return []

        topics = sorted({
            topic.get("name", "").strip()
            for topic in question.get(
                "topicTags",
                []
            )
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
# Parse LeetHub-generated problem README
# =========================================================

def parse_problem_readme(readme_path):
    """
    Extract:
    - Problem number
    - Title
    - LeetCode URL
    - Difficulty
    - Slug
    """

    try:
        content = readme_path.read_text(
            encoding="utf-8"
        )

    except (
        OSError,
        UnicodeDecodeError,
    ) as error:

        print(
            f"Warning: Could not read "
            f"{readme_path}: {error}"
        )

        return None

    problem_match = re.search(
        r'<h2>\s*'
        r'<a\s+href="([^"]+)"[^>]*>'
        r'\s*(\d+)\.\s*(.*?)\s*'
        r'</a>\s*</h2>',
        content,
        re.IGNORECASE | re.DOTALL,
    )

    difficulty_match = re.search(
        r'<h3>\s*'
        r'(Easy|Medium|Hard)'
        r'\s*</h3>',
        content,
        re.IGNORECASE,
    )

    if not problem_match:
        return None

    leetcode_url = (
        problem_match.group(1).strip()
    )

    number = int(
        problem_match.group(2)
    )

    title = re.sub(
        r"<[^>]+>",
        "",
        problem_match.group(3),
    ).strip()

    difficulty = (
        difficulty_match.group(1).capitalize()
        if difficulty_match
        else "Unknown"
    )

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
# Detect solution languages
# =========================================================

def detect_languages(problem_folder):
    """
    Detect programming languages from solution files.
    """

    detected = set()

    for file in problem_folder.iterdir():

        if not file.is_file():
            continue

        extension = file.suffix.lower()

        if extension in LANGUAGES:
            detected.add(
                LANGUAGES[extension]
            )

    return sorted(detected)


# =========================================================
# Git solved-date detection
# =========================================================

def get_problem_solved_date(folder_name):
    """
    Find the earliest Git commit date associated
    with a problem folder.

    Returns a date object or None.
    """

    try:
        result = subprocess.run(
            [
                "git",
                "log",
                "--follow",
                "--format=%aI",
                "--",
                folder_name,
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
            timeout=15,
        )

        if result.returncode != 0:
            return None

        timestamps = [
            line.strip()
            for line in result.stdout.splitlines()
            if line.strip()
        ]

        if not timestamps:
            return None

        dates = []

        for timestamp in timestamps:
            try:
                parsed = datetime.fromisoformat(
                    timestamp.replace(
                        "Z",
                        "+00:00",
                    )
                )

                dates.append(parsed.date())

            except ValueError:
                continue

        return min(dates) if dates else None

    except (
        subprocess.SubprocessError,
        OSError,
    ) as error:

        print(
            f"Warning: Could not determine "
            f"solved date for {folder_name}: "
            f"{error}"
        )

        return None


# =========================================================
# Find all LeetCode problems
# =========================================================

def get_all_problems(topics_cache):
    """
    Scan all LeetHub problem folders.
    """

    folder_pattern = re.compile(
        r"^\d+-.+$"
    )

    problems = []
    cache_changed = False

    for item in ROOT.iterdir():

        if not item.is_dir():
            continue

        if not folder_pattern.match(item.name):
            continue

        problem_readme = (
            item / "README.md"
        )

        if not problem_readme.exists():
            print(
                f"Warning: No README found "
                f"in {item.name}. Skipping."
            )
            continue

        problem = parse_problem_readme(
            problem_readme
        )

        if not problem:
            print(
                f"Warning: Could not parse "
                f"README in {item.name}. "
                f"Skipping."
            )
            continue

        slug = problem["slug"]

        if slug in topics_cache:
            topics = topics_cache[slug]

        else:
            print(
                f"Fetching topics for {slug}..."
            )

            topics = (
                fetch_topics_from_leetcode(slug)
            )

            if topics:
                topics_cache[slug] = topics
                cache_changed = True

        problem["folder"] = item.name

        problem["languages"] = (
            detect_languages(item)
        )

        problem["topics"] = topics

        problem["solved_date"] = (
            get_problem_solved_date(
                item.name
            )
        )

        problems.append(problem)

    return (
        sorted(
            problems,
            key=lambda problem: problem["number"],
        ),
        cache_changed,
    )


# =========================================================
# Difficulty formatting
# =========================================================

def format_difficulty(difficulty):

    labels = {
        "Easy": "🟢 Easy",
        "Medium": "🟡 Medium",
        "Hard": "🔴 Hard",
    }

    return labels.get(
        difficulty,
        "⚪ Unknown",
    )


# =========================================================
# Markdown escaping
# =========================================================

def escape_markdown_table_text(value):
    """
    Prevent table-breaking pipe characters.
    """

    return str(value).replace("|", "\\|")


# =========================================================
# Problem table row
# =========================================================

def create_problem_row(
    problem,
    include_date=False,
):

    title = escape_markdown_table_text(
        problem["title"]
    )

    languages = ", ".join(
        problem["languages"]
    ) or "Unknown"

    languages = escape_markdown_table_text(
        languages
    )

    solution_url = (
        f"{REPOSITORY_URL}/tree/main/"
        f"{urllib.parse.quote(problem['folder'])}"
    )

    row = (
        f"| {problem['number']} "
        f"| [{title}]"
        f"({problem['leetcode_url']}) "
        f"| {format_difficulty(problem['difficulty'])} "
        f"| {languages} "
        f"| [View Solution]({solution_url})"
    )

    if include_date:
        solved_date = (
            problem["solved_date"].strftime(
                "%b %d, %Y"
            )
            if problem["solved_date"]
            else "Unknown"
        )

        row += f" | {solved_date}"

    row += " |"

    return row


# =========================================================
# Progress bar
# =========================================================

def create_progress_bar(
    solved,
    goal,
    length=20,
):

    if goal <= 0:
        return "░" * length

    ratio = min(
        solved / goal,
        1.0,
    )

    filled = round(
        ratio * length
    )

    return (
        "█" * filled
        + "░" * (length - filled)
    )


# =========================================================
# Streak calculations
# =========================================================

def calculate_streaks(problems):
    """
    Calculate current and longest streak from
    unique Git-derived solved dates.
    """

    active_dates = sorted({
        problem["solved_date"]
        for problem in problems
        if problem["solved_date"]
    })

    if not active_dates:
        return 0, 0

    longest = 1
    running = 1

    for index in range(
        1,
        len(active_dates),
    ):

        difference = (
            active_dates[index]
            - active_dates[index - 1]
        ).days

        if difference == 1:
            running += 1
            longest = max(
                longest,
                running,
            )

        else:
            running = 1

    today = date.today()
    latest = active_dates[-1]

    # Allow the current streak to remain alive
    # if the latest activity was today or yesterday.
    if latest not in {
        today,
        today - timedelta(days=1),
    }:
        current = 0

    else:
        current = 1

        for index in range(
            len(active_dates) - 1,
            0,
            -1,
        ):

            difference = (
                active_dates[index]
                - active_dates[index - 1]
            ).days

            if difference == 1:
                current += 1
            else:
                break

    return current, longest


# =========================================================
# Monthly progress
# =========================================================

def calculate_monthly_progress(problems):

    monthly = defaultdict(int)

    for problem in problems:

        solved_date = problem["solved_date"]

        if solved_date:
            key = solved_date.strftime(
                "%Y-%m"
            )

            monthly[key] += 1

    return sorted(
        monthly.items(),
        reverse=True,
    )


# =========================================================
# Badge generation
# =========================================================

def create_badge(label, value, color):

    encoded_label = urllib.parse.quote(
        str(label)
    )

    encoded_value = urllib.parse.quote(
        str(value)
    )

    return (
        f"![{label}]"
        f"(https://img.shields.io/badge/"
        f"{encoded_label}-{encoded_value}-{color})"
    )


# =========================================================
# Add problem table
# =========================================================

def add_problem_table(
    lines,
    problems,
    include_date=False,
):

    if include_date:

        lines.extend([
            "| # | Problem | Difficulty | Language | Solution | Solved |",
            "|---:|---|---|---|---|---|",
        ])

    else:

        lines.extend([
            "| # | Problem | Difficulty | Language | Solution |",
            "|---:|---|---|---|---|",
        ])

    for problem in problems:

        lines.append(
            create_problem_row(
                problem,
                include_date=include_date,
            )
        )


# =========================================================
# Generate root README
# =========================================================

def generate_readme():

    topics_cache = (
        load_topics_cache()
    )

    problems, cache_changed = (
        get_all_problems(
            topics_cache
        )
    )

    if cache_changed:
        save_topics_cache(
            topics_cache
        )

    total = len(problems)

    easy_problems = [
        problem
        for problem in problems
        if problem["difficulty"] == "Easy"
    ]

    medium_problems = [
        problem
        for problem in problems
        if problem["difficulty"] == "Medium"
    ]

    hard_problems = [
        problem
        for problem in problems
        if problem["difficulty"] == "Hard"
    ]

    unknown_problems = [
        problem
        for problem in problems
        if problem["difficulty"] == "Unknown"
    ]

    easy = len(easy_problems)
    medium = len(medium_problems)
    hard = len(hard_problems)

    current_streak, longest_streak = (
        calculate_streaks(problems)
    )

    monthly_progress = (
        calculate_monthly_progress(problems)
    )

    recently_solved = sorted(
        [
            problem
            for problem in problems
            if problem["solved_date"]
        ],
        key=lambda problem: (
            problem["solved_date"]
        ),
        reverse=True,
    )[:RECENT_PROBLEMS_LIMIT]

    progress_percentage = min(
        round(
            (total / PROBLEM_GOAL) * 100,
            1,
        )
        if PROBLEM_GOAL > 0
        else 0,
        100,
    )

    progress_bar = create_progress_bar(
        total,
        PROBLEM_GOAL,
    )


    # -----------------------------------------------------
    # README header
    # -----------------------------------------------------

    lines = [
        "# 🚀 LeetCode Solutions",
        "",
        "A collection of my LeetCode solutions, "
        "automatically synced using LeetHub-3.0 "
        "and tracked with GitHub Actions.",
        "",
        (
            create_badge(
                "Solved",
                total,
                "blue",
            )
            + " "
            + create_badge(
                "Easy",
                easy,
                "brightgreen",
            )
            + " "
            + create_badge(
                "Medium",
                medium,
                "yellow",
            )
            + " "
            + create_badge(
                "Hard",
                hard,
                "red",
            )
        ),
        "",
        (
            create_badge(
                "Current Streak",
                f"{current_streak} days",
                "orange",
            )
            + " "
            + create_badge(
                "Longest Streak",
                f"{longest_streak} days",
                "purple",
            )
        ),
        "",
    ]


    # -----------------------------------------------------
    # Progress section
    # -----------------------------------------------------

    lines.extend([
        "## 📊 Progress",
        "",
        (
            f"**Goal: {total} / "
            f"{PROBLEM_GOAL} problems "
            f"({progress_percentage}%)**"
        ),
        "",
        f"`{progress_bar}`",
        "",
        "| Difficulty | Solved |",
        "|---|---:|",
        f"| 🟢 Easy | {easy} |",
        f"| 🟡 Medium | {medium} |",
        f"| 🔴 Hard | {hard} |",
    ])

    if unknown_problems:
        lines.append(
            f"| ⚪ Unknown | "
            f"{len(unknown_problems)} |"
        )


    # -----------------------------------------------------
    # Streak section
    # -----------------------------------------------------

    lines.extend([
        "",
        "## 🔥 Solution Streak",
        "",
        (
            f"- **Current streak:** "
            f"{current_streak} day"
            f"{'' if current_streak == 1 else 's'}"
        ),
        (
            f"- **Longest streak:** "
            f"{longest_streak} day"
            f"{'' if longest_streak == 1 else 's'}"
        ),
        "",
        "> Streaks are calculated from Git commit dates "
        "associated with problem folders.",
    ])


    # -----------------------------------------------------
    # Recently solved
    # -----------------------------------------------------

    if recently_solved:

        lines.extend([
            "",
            "## 🕐 Recently Solved",
            "",
        ])

        add_problem_table(
            lines,
            recently_solved,
            include_date=True,
        )


    # -----------------------------------------------------
    # Monthly progress
    # -----------------------------------------------------

    if monthly_progress:

        lines.extend([
            "",
            "## 📅 Monthly Progress",
            "",
            "| Month | Problems Solved |",
            "|---|---:|",
        ])

        for month_key, count in monthly_progress:

            month_label = datetime.strptime(
                month_key,
                "%Y-%m",
            ).strftime("%B %Y")

            lines.append(
                f"| {month_label} | {count} |"
            )


    # -----------------------------------------------------
    # All problems
    # -----------------------------------------------------

    lines.extend([
        "",
        "## 📚 All Problems",
        "",
    ])

    add_problem_table(
        lines,
        problems,
    )


    # -----------------------------------------------------
    # Separate difficulty tables
    # -----------------------------------------------------

    if easy_problems:

        lines.extend([
            "",
            "## 🟢 Easy Problems",
            "",
        ])

        add_problem_table(
            lines,
            easy_problems,
        )

    if medium_problems:

        lines.extend([
            "",
            "## 🟡 Medium Problems",
            "",
        ])

        add_problem_table(
            lines,
            medium_problems,
        )

    if hard_problems:

        lines.extend([
            "",
            "## 🔴 Hard Problems",
            "",
        ])

        add_problem_table(
            lines,
            hard_problems,
        )

    if unknown_problems:

        lines.extend([
            "",
            "## ⚪ Unknown Difficulty",
            "",
        ])

        add_problem_table(
            lines,
            unknown_problems,
        )


    # -----------------------------------------------------
    # Topic organization
    # -----------------------------------------------------

    topics = defaultdict(list)
    uncategorized = []

    for problem in problems:

        if problem["topics"]:

            for topic in problem["topics"]:
                topics[topic].append(
                    problem
                )

        else:
            uncategorized.append(
                problem
            )

    if topics or uncategorized:

        lines.extend([
            "",
            "## 🏷️ Topics",
            "",
        ])

        # Better topic organization:
        # topics with more solved problems appear first.
        sorted_topics = sorted(
            topics.items(),
            key=lambda item: (
                -len(item[1]),
                item[0].lower(),
            ),
        )

        for topic, topic_problems in sorted_topics:

            lines.extend([
                (
                    f"### {topic} "
                    f"({len(topic_problems)})"
                ),
                "",
            ])

            add_problem_table(
                lines,
                sorted(
                    topic_problems,
                    key=lambda problem: (
                        problem["number"]
                    ),
                ),
            )

            lines.append("")

        if uncategorized:

            lines.extend([
                (
                    f"### Uncategorized "
                    f"({len(uncategorized)})"
                ),
                "",
            ])

            add_problem_table(
                lines,
                uncategorized,
            )

            lines.append("")


    # -----------------------------------------------------
    # Footer
    # -----------------------------------------------------

    lines.extend([
        "---",
        "",
        "_README automatically updated with "
        "LeetHub-3.0 and GitHub Actions._",
        "",
    ])


    # -----------------------------------------------------
    # Write README
    # -----------------------------------------------------

    README_FILE.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print(
        f"README generated successfully "
        f"with {total} problems."
    )

    print(
        f"Current streak: "
        f"{current_streak} day(s)."
    )

    print(
        f"Longest streak: "
        f"{longest_streak} day(s)."
    )


# =========================================================
# Entry point
# =========================================================

if __name__ == "__main__":
    generate_readme()