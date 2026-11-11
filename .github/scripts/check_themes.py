#!/usr/bin/env python3
"""
Checks every theme in this repository against the rules in CONTRIBUTING.md:

- Layout: <username>/<theme>/, both lowercase letters, numbers, and hyphens.
- Each theme has theme.css (starting with a "/* Name: description */" comment), README.md, and a
  screenshot (screenshot.jpg or screenshot.png).
- Only files Outpost serves for themes (CSS, fonts, images), plus README.md and font license files.
- url() and @import point only inside the theme's folder, at another theme by the same person
  (../<theme>/), or at a theme built into Outpost (../../<theme>/). Nothing from other sites.
- Fonts come with a license file.

Run it from the repository root: python3 .github/scripts/check_themes.py
Uses only Python's standard library. Exits with 1 if anything is wrong.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

NAME = r"[a-z0-9-]+"
PATH_PART = r"[A-Za-z0-9_-][A-Za-z0-9._-]*"
SERVED = {"css", "woff2", "woff", "ttf", "otf", "png", "jpg", "jpeg", "gif", "webp", "avif", "svg"}
FONTS = {"woff2", "woff", "ttf", "otf"}
# Themes built into Outpost, which a theme can build on with ../../<name>/
BUILT_IN = {"retro-crt", "amber-terminal", "command-center", "modern-dark", "field-station", "atomic-broadcast", "ink"}
# Files and folders at the top of the repository that are not username folders
REPOSITORY_FILES = {"README.md", "CONTRIBUTING.md", "LICENSE", ".github", ".git", ".gitattributes", ".gitignore"}

MAX_FILE_BYTES = 2 * 1024 * 1024
MAX_SCREENSHOT_BYTES = 1024 * 1024
NAME_COMMENT = re.compile(r"\s*/\*\s*([^:*\n]{1,40}?)\s*:")  # the same rule Outpost uses for the switcher


def is_license(path: Path) -> bool:
    return path.suffix.lower() in {".txt", ".md"} and re.search(r"licen[sc]e|ofl", path.name, re.IGNORECASE) is not None


def check_references(theme: Path, css_path: Path, problems: list) -> None:
    owner = theme.parent
    css = css_path.read_text(encoding="utf-8", errors="replace")
    for match in re.finditer(r"""(?:url\(\s*['"]?|@import\s+['"])([^'")\s]+)""", css):
        target = match.group(1)
        where = f"{css_path.relative_to(ROOT).as_posix()}: {target}"
        if re.match(r"^[a-z][a-z0-9+.-]*:|^//", target, re.IGNORECASE):
            problems.append(f"{where}: files from other sites (and data: URLs) are blocked by Outpost; put the file in the theme's folder")
            continue
        if target.startswith("/"):
            problems.append(f"{where}: use a path relative to the theme's folder")
            continue
        if target.startswith("../../"):
            built_in = target[len("../../"):].split("/")[0]
            if built_in not in BUILT_IN:
                problems.append(f"{where}: ../../ reaches a theme built into Outpost, and '{built_in}' is not one ({', '.join(sorted(BUILT_IN))})")
            continue
        resolved = (css_path.parent / target).resolve()
        if owner.resolve() not in resolved.parents:
            problems.append(f"{where}: points outside your username folder")
        elif not resolved.is_file():
            problems.append(f"{where}: file not found")


def check_theme(theme: Path, problems: list) -> None:
    label = theme.relative_to(ROOT).as_posix()
    if not re.fullmatch(NAME, theme.name):
        problems.append(f"{label}: theme folder names use only lowercase letters, numbers, and hyphens")
        return
    css_path = theme / "theme.css"
    if not css_path.is_file():
        problems.append(f"{label}: no theme.css")
        return
    css = css_path.read_text(encoding="utf-8", errors="replace")
    if not NAME_COMMENT.match(css):
        problems.append(f"{label}/theme.css: start with a comment that names the theme, like /* My Theme: what it looks like */")
    if not (theme / "README.md").is_file():
        problems.append(f"{label}: no README.md")
    screenshots = [theme / name for name in ("screenshot.jpg", "screenshot.png") if (theme / name).is_file()]
    if not screenshots:
        problems.append(f"{label}: no screenshot.jpg or screenshot.png")
    for shot in screenshots:
        if shot.stat().st_size > MAX_SCREENSHOT_BYTES:
            problems.append(f"{label}/{shot.name}: keep the screenshot under 1 MB (a JPEG works well)")

    fonts = False
    for path in sorted(p for p in theme.rglob("*") if p.is_file()):
        relative = path.relative_to(theme)
        shown = f"{label}/{relative.as_posix()}"
        if not all(re.fullmatch(PATH_PART, part) for part in relative.parts):
            problems.append(f"{shown}: file and folder names use letters, numbers, dots, hyphens, and underscores, and do not start with a dot")
            continue
        extension = path.suffix.lower().lstrip(".")
        if extension in FONTS:
            fonts = True
        if relative.as_posix() == "README.md" or is_license(path):
            continue
        if extension not in SERVED:
            problems.append(f"{shown}: Outpost does not serve .{extension} files; themes hold only CSS, fonts, and images")
        elif path.stat().st_size > MAX_FILE_BYTES:
            problems.append(f"{shown}: larger than 2 MB")
        if extension == "css":
            check_references(theme, path, problems)

    if fonts and not any(is_license(p) for p in theme.rglob("*") if p.is_file()):
        problems.append(f"{label}: has fonts but no license file for them (for example OFL.txt)")


def main() -> int:
    problems: list = []
    themes = 0
    for entry in sorted(ROOT.iterdir()):
        if entry.name in REPOSITORY_FILES:
            continue
        if not entry.is_dir():
            problems.append(f"{entry.name}: only username folders go at the top of the repository")
            continue
        if not re.fullmatch(NAME, entry.name):
            problems.append(f"{entry.name}/: name the folder after your GitHub username in lowercase")
            continue
        for child in sorted(entry.iterdir()):
            if child.is_dir():
                themes += 1
                check_theme(child, problems)
            elif child.name != "README.md":
                problems.append(f"{entry.name}/{child.name}: files go inside a theme folder")

    for problem in problems:
        print(f"FAIL {problem}")
    print(f"\n{themes} themes checked, {len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
