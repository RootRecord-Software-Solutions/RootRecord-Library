# How to read and edit RootRecord code

**Standing instruction for every future agent and for Alexander.**  
**Applies to:** first-party Pacific `.py` and `.sh` files under `1 - Servers/1 - RootRecord-Pacific-Solar-Server/`.  
**Does not apply to:** `.venv`, `vendor`, `node_modules`, generated logs, or third-party trees. Do not "document" those by rewriting them.

The code is written so a person can open one file and see what each block is for, and what each line does, without asking an AI to explain it first.

## What you will see in a file

1. A **file banner** at the top (`FILE:` or the older `INFO — MUST HAVE` banner). It says what the file is and where the copy-paste pattern lives.
2. A **SECTION banner** immediately above every function, class, and long top-level list:

```text
# ====================================================
# SECTION: function ecoflow_command
# What it does: build the flock-wrapped bash command for one EcoFlow action script.
# Edit this block only. Leave this banner in place and update the What-it-does line if the behavior changes.
# ====================================================
```

3. An **`# info:` note at the end of every code line** that did not already have a comment. The note says what that line does. Example: `PACIFIC = "..."` ends with `# info: set PACIFIC`.

## How to edit

1. Find the SECTION banner for the function or list you need. Do not hunt by guessing.
2. Change the code line.
3. Change the `# info:` note on that **same line** so it still matches the code. A stale note is worse than no note.
4. If the function's behavior changed, rewrite the `What it does:` line in the banner.
5. Do not delete banners or `# info:` notes to "clean up" a file.
6. Do not add a second banner above a block that already has one.

## How to add a function

Copy this block, paste it above the new function, and fill the two names.

```text
# ====================================================
# SECTION: function your_function_name
# What it does: one sentence, including what it must not do (send, spend, restart, play audio).
# Edit this block only. Leave this banner in place and update the What-it-does line if the behavior changes.
# ====================================================
def your_function_name(arg):  # info: def your_function_name
    return arg  # info: return arg
```

Shell functions use the same banner, with `SECTION: function your_function_name`, placed on the lines directly above `your_function_name()`.

## How to add a poller job (`Automations/scripts/jobs.py`)

This file is the schedule. Each list (`ON_BOOT`, `ONCE_AT_START`, `EVERY_SECONDS`, `EVERY_MINUTE`, `EVERY_HOUR`, `ON_AT`) ends with a commented **TEMPLATE**.

1. Open the list that matches when the job should run.
2. Copy the TEMPLATE from the `# {` line through the `# },` line.
3. Paste it **above** the TEMPLATE, still inside the list.
4. Remove the leading `#` and the leading space that followed it, so the dict is real Python.
5. Set `id`, `description`, `command`, and the schedule field (`priority`, `interval_sec`, `only_at_minutes`, `only_at_hours`, or `at_times`).
6. Leave `"enabled": False` until Alexander names that job. Gates that send, spend, move hardware, or play audio stay `RR_SOMETHING=1` checks, not `True`.
7. Quote every path that contains a space. `PACIFIC` contains spaces.
8. Do not delete the TEMPLATE. The next job is copied from it.

A new job does not start until the poller process loads this file. Do not restart the poller unless Alexander asks.

## What not to do

- Do not comment `.venv`, `Energy/lib/vendor`, or `node_modules`.
- Do not put secrets in banners or `# info:` notes.
- Do not enable a gated job, send a message, spend money, or play audio while documenting code.
- Do not rewrite a line's `# info:` note into a novel. Keep it to what that line does.

## Check after an edit

- Python: `python3 -m compileall -q` on the file you changed. It must compile.
- Shell: `bash -n` on the script you changed. It must parse.
- A comment-only edit must not change runtime behavior. If the check fails, the note was inserted inside a string or a heredoc. Move it out.
