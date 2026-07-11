# from pathlib import Path
# import os

# ROOT = Path(".").resolve()
# OUTPUT_FILE = ROOT / "project_dump.txt"

# # -------------------------------
# # Directories to ignore
# # -------------------------------

# IGNORE_DIRS = {
#     ".git",
#     ".venv",
#     "venv",
#     "__pycache__",
#     ".pytest_cache",
#     ".mypy_cache",
#     ".idea",
#     ".vscode",
#     "node_modules",
#     "dist",
#     "build",
#     ".ruff_cache",
#     ".cache",
#     "models",          # GGUFs
#     "output",
#     "evaluation/reports",
# }

# # -------------------------------
# # File extensions to ignore
# # -------------------------------

# IGNORE_EXTENSIONS = {
#     ".pyc",
#     ".pyo",
#     ".pyd",
#     ".so",
#     ".dll",
#     ".exe",
#     ".bin",
#     ".gguf",
#     ".png",
#     ".jpg",
#     ".jpeg",
#     ".gif",
#     ".bmp",
#     ".ico",
#     ".pdf",
#     ".zip",
#     ".tar",
#     ".gz",
#     ".7z",
#     ".mp4",
#     ".mov",
#     ".avi",
#     ".wav",
#     ".mp3",
#     ".csv",
#     ".sqlite",
#     ".db",
#     ".log",
# }

# # -------------------------------
# # Specific files to ignore
# # -------------------------------

# IGNORE_FILES = {
#     "project_dump.txt",
#     ".DS_Store",
# }

# MAX_FILE_SIZE = 1024 * 1024  # 1 MB


# def should_skip(path: Path):
#     parts = set(path.parts)

#     if parts & IGNORE_DIRS:
#         return True

#     if path.name in IGNORE_FILES:
#         return True

#     if path.suffix.lower() in IGNORE_EXTENSIONS:
#         return True

#     if not path.is_file():
#         return True

#     try:
#         if path.stat().st_size > MAX_FILE_SIZE:
#             return True
#     except Exception:
#         return True

#     return False


# def write_separator(f):
#     f.write("\n")
#     f.write("=" * 120)
#     f.write("\n\n")


# with open(OUTPUT_FILE, "w", encoding="utf-8") as out:

#     out.write("# PROJECT DUMP\n")
#     out.write(f"# Root: {ROOT}\n\n")

#     files = sorted(ROOT.rglob("*"))

#     for file in files:

#         if should_skip(file):
#             continue

#         relative = file.relative_to(ROOT)

#         print(relative)

#         write_separator(out)

#         out.write(f"FILE: {relative}\n")

#         write_separator(out)

#         try:
#             text = file.read_text(encoding="utf-8")

#         except UnicodeDecodeError:
#             out.write("[Binary / Non UTF-8 File]\n")
#             continue

#         except Exception as e:
#             out.write(f"[Could not read file: {e}]\n")
#             continue

#         out.write(text)

#         if not text.endswith("\n"):
#             out.write("\n")

# print(f"\nDone!\nOutput written to:\n{OUTPUT_FILE}")

from pathlib import Path

ROOT = Path(".").resolve()
OUTPUT_FILE = ROOT / "project_dump.txt"

# -------------------------------
# Specific files to include
# -------------------------------
TARGET_FILES = [
    "config.py",
    "core/pipeline.py",
    "routing/router.py",
    "inference/factory.py",
    "inference/client.py",
    "inference/fireworks.py",
    "local/client.py",
    "local/provider.py",
    "validation/local_validator.py",
    "telemetry/decision_logger.py",
]

def write_separator(f):
    f.write("\n")
    f.write("=" * 120)
    f.write("\n\n")

with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
    out.write("# PROJECT DUMP\n")
    out.write(f"# Root: {ROOT}\n\n")

    for relative_path in TARGET_FILES:
        file = ROOT / relative_path

        # Check if the file actually exists before trying to read it
        if not file.is_file():
            print(f"Skipping (not found): {relative_path}")
            continue

        print(f"Processing: {relative_path}")

        write_separator(out)
        out.write(f"FILE: {relative_path}\n")
        write_separator(out)

        try:
            text = file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            out.write("[Binary / Non UTF-8 File]\n")
            continue
        except Exception as e:
            out.write(f"[Could not read file: {e}]\n")
            continue

        out.write(text)

        if not text.endswith("\n"):
            out.write("\n")

print(f"\nDone!\nOutput written to:\n{OUTPUT_FILE}")