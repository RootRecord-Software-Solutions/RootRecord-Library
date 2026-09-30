# For an AI

Read this before you edit Pacific code. It is the short class. The standing rule, with the copy-paste blocks, is [How to read and edit code](../../prompts/How-To-Read-And-Edit-Code.md).

You are helping Alexander on one desk. The live tree is:

`/home/rootrecord/RootRecord-Ecosystem/1 - Servers/1 - RootRecord-Pacific-Solar-Server`

Library, Pacific, and Database are folders inside one git root. They are not three clones.

## How a file is meant to be read

Open the file. Do not ask for a tour of the whole repo first.

1. The banner at the top says what the file is.
2. The `# SECTION:` banner above a function or a list says what that block does, and that you edit only that block.
3. The `# info:` note at the end of a code line says what that line does.

When you change a line, change its `# info:` note in the same edit. When you change what a function does, change the `What it does:` line in its banner. Do not strip banners to make a diff smaller.

A new function starts from the banner in the standing rule. A new poller job is copied from the TEMPLATE at the bottom of the matching list in `Automations/scripts/jobs.py`. Paste it above the template. Leave `enabled` false. Do not delete the template.

## What you leave alone

These are facts, not suggestions.

- Delta 2 does not transmit. A quiet Delta 2 read is normal. Do not schedule a test that tries to drive it.
- Do not create `3 - RootRecord-Website`, and do not bind port 3001. `https://rootserver.rootrecord.cloud/` is the poller, not a website.
- Do not turn on `RR_*` gates, Telegram replies, voice playback, or speaker output. Alexander names the one he wants.
- Do not restart the poller, the relay, or the cameras unless he asks.
- Do not retire a legacy tree unless he names that tree. Byte-identical skills copies were already removed. Unique skills files and the old 27 GB skills tree stay.
- Vendor folders, virtualenvs, and `node_modules` do not get teaching comments.

## Where to look next

| Question | Page |
| --- | --- |
| What does the window show? | [Root Monitor handbook](../Root-Monitor-Operators-Handbook/Root-Monitor-Operators-Handbook.md) |
| What is still Alexander's decision? | [What's left](../../Documentation/01-operations/2026-09-30-whats-left-for-alexander.md) |
| How does he want a messy plan cleaned up? | [One clean plan](../HOW-TO-TURN-MESSY-AI-OUTPUT-INTO-ONE-CLEAN-PLAN.md) |
| What would a new person learn after this? | [For a new person](./For-a-new-person.md) and the [course map](./Course-map.md) |

After an edit, compile the Python file you touched, or run `bash -n` on the shell script. A comment inside a string or a heredoc is a broken edit, not documentation.
