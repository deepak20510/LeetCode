import re
from pathlib import Path


# =========================================================
# Configuration
# =========================================================

ROOT = Path(__file__).resolve().parent.parent
README_FILE = ROOT / "README.md"

REPOSITORY_URL = "https://github.com/deepak20510/LeetCode"


# Supported programming languages
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
# Parse problem README
# =========================================================

def parse_problem_readme(readme_path):
    """
    Extract problem number, title, LeetCode URL,
    and difficulty from a LeetHub-generated README.
    """

    try:
        content = readme_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        print(f"Warning: Could not read {readme_path}: {error}")
        return None

    # Example:
    # <h2><a href="https://leetcode.com/problems/valid-palindrome">
    # 125. Valid Palindrome
    # </a></h2>

    problem_match = re.search(
        r'<h2>\s*<a\s+href="([^"]+)"[^>]*>\s*(\d+)\.\s*(.*?)\s*</a>\s*</h2>',
        content,
        re.IGNORECASE | re.DOTALL,
    )

    # Example:
    # <h3>Easy</h3>

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

    return {
        "number": number,
        "title": title,
        "leetcode_url": leetcode_url,
        "difficulty": difficulty,
    }


# =========================================================
# Detect programming languages
# =========================================================

def detect_languages(problem_folder):
    """
    Detect solution languages from files inside
    a LeetCode problem folder.
    """

    detected = set()

    for file in problem_folder.iterdir():

        if not file.is_file():
            continue

        extension = file.suffix.lower()

        if extension in LANGUAGES:
            detected.add(LANGUAGES[extension])

    return sorted(detected)


# =========================================================
# Find all LeetCode problems
# =========================================================

def get_all_problems():
    """
    Scan repository root for LeetHub problem folders.
    """

    folder_pattern = re.compile(r"^\d+-.+$")

    problems = []

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

        problem["folder"] = item.name
        problem["languages"] = detect_languages(item)

        problems.append(problem)

    return sorted(
        problems,
        key=lambda problem: problem["number"]
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
        "⚪ Unknown"
    )


# =========================================================
# Generate problem table row
# =========================================================

def create_problem_row(problem):

    number = problem["number"]
    title = problem["title"]
    leetcode_url = problem["leetcode_url"]
    difficulty = format_difficulty(
        problem["difficulty"]
    )

    languages = ", ".join(
        problem["languages"]
    ) or "Unknown"

    solution_url = (
        f"{REPOSITORY_URL}/tree/main/"
        f"{problem['folder']}"
    )

    return (
        f"| {number} "
        f"| [{title}]({leetcode_url}) "
        f"| {difficulty} "
        f"| {languages} "
        f"| [View Solution]({solution_url}) |"
    )


# =========================================================
# Generate root README
# =========================================================

def generate_readme():

    problems = get_all_problems()

    total = len(problems)

    easy = sum(
        1 for problem in problems
        if problem["difficulty"] == "Easy"
    )

    medium = sum(
        1 for problem in problems
        if problem["difficulty"] == "Medium"
    )

    hard = sum(
        1 for problem in problems
        if problem["difficulty"] == "Hard"
    )

    unknown = sum(
        1 for problem in problems
        if problem["difficulty"] == "Unknown"
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
        lines.append(
            create_problem_row(problem)
        )

    lines.extend([
        "",
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
        f"README generated successfully with {total} problems."
    )


# =========================================================
# Entry point
# =========================================================

if __name__ == "__main__":
    generate_readme()