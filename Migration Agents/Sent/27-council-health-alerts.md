# Agent 27 — Council health alerts

Wave: D. One send pipe, then the messages

Discord, Slack, and Telegram posts share a pipe. Economy brief waits on Discord and MySQL. The inbox waits on D1.

This file is the full instruction for this agent. The other 46 agents have their own files in this same folder and are running the same way.

Plan the migration of one function only: Council health alerts.

Execution order: 27 of 47. Wave D. One send pipe, then the messages.
Write this draft now. When building, pause if these Folders are not in place yet: 3. Council persona prompts; 25. Council quake Telegram posts.
No later function in this list depends on this one.

Other agents are doing this same job for the other functions. Stay in your Folder and your one work order. Do not edit their files. If a shared file (jobs.py, the Vercel app shell, or master-key.env) is already being edited, pause. If a function you depend on has no Folder yet when you are told to build, pause and name that function. Do not build it yourself.
Alexander will accept every draft first, then start the builds together. Write the draft so it can run in parallel. Pause only when a real dependency is missing.

Five phases. Do not skip ahead.
1. Before any code: copy 5 - RootRecord-Library/Documentation/01-operations/templates/TEMPLATE Work Order.md into 5 - RootRecord-Library/Documentation/06-development/Work-Orders/drafts/. Fill every section from that template. Status stays OPEN — draft, not accepted for execution. Do not promote it onto the active index. Filename: Council_health_alerts_Work_Order_WO-MIG-27-2026-09-29.md. This draft is the before-documentation.
2. Stop. Wait until Alexander accepts that draft and tells you to build. Until then, do not edit runtime files, restart services, send messages, actuate hardware, or spend cloud money.
3. Build only this function. Do not import system-generated data into the live Folders. That means logs, samples, last-state files, generated reports, collected images, radar frames, zip archives of collected data, database dumps, caches, virtualenvs, node_modules, and __pycache__. Bring source, templates, and prompts. Runtime output stays out of Pacific, Database, the website, and git.
4. After the migration works, and before you update the Library: copy every old-repo file that belonged to this function and is no longer needed into /home/rootrecord/RootRecord-Ecosystem/Old repos deleted and merged/<old-repo-name>/, keeping the path it had inside the old repo. Generated data that lived beside that source goes into this archive too, and still does not go into the live Folders. After the archive copy is on disk, delete those same files from the old repo on this machine and on GitHub. Commit that deletion and push it. Do not force-push. Do not delete the GitHub repository. If a file is shared with another agent's function, leave it and name it in the work order. If the archive copy fails, do not delete.
5. Then update that same work order with what changed, the archive path, the GitHub deletion, and the new status. Correct only the Library pages this function made stale. Do not rewrite unrelated work orders.

Authority: /home/rootrecord/RootRecord-Ecosystem is the live system. New code wins. If a newer version of this function already exists, enhance that version. Do not copy old code over it.

Function: Council health alerts
Old home: council-health
Why it is absent: Needs the three bot tokens, a model probe, and a send.
How to add it: Health check that posts through the current relay.

Read only the old source for this function and the current Ecosystem files that should receive it. Do not survey the other missing functions or re-read the work-order pile.

Exact format (match Geology and Energy; do not invent another layout):
- If this function is not installed, create one capitalized Folder for it. Use that same name in all three places below. No lowercase twin folder and no symlink.
- Code: 1 - Servers/1 - RootRecord-Pacific-Solar-Server/<Folder>/scripts (config/ only if it needs config). The Python package name matches <Folder>. Do not put a Logs/ directory on the server.
- Database: 2 - RootRecord-Database/<Folder>/ for samples, last files, and stores.
- Logs: 2 - RootRecord-Database/Logs/<Folder>/ only.
- If it clearly belongs in an existing domain (Energy, Geology, Weather, Reports, Security, Communications, System, Media), add a subfolder of this function inside that domain, and mirror that subfolder under Database and Logs. Do not open a second top-level domain for it.
- Secrets: /home/rootrecord/master/master-key.env only. Follow Energy/lib/envload.py: an allowlist of key names, never print values, never add a second env file, never commit secrets. The plan lists key names, not values.
- Docs and the plan write-up: 5 - RootRecord-Library
- Website UI, when this function has a public page: 3 - RootRecord-Website, still one Vercel app. Its data and logs still use the Database paths above.
- Android apps already in 6 - Android Development stay there. Do not re-import Kilauea, RootMC, Account Hub, Weather, Tokens, Business, Farms, Goals, or Ava Ops.

Rules:
- One function. The draft work order is the only file you write until Alexander says to build.
- The plan names the Folder and writes the three paths (code, database, logs) before any other file list.
- New periodic jobs stay gated off. Do not edit jobs.py unless the plan only proposes a gated block.
- Do not delete a whole GitHub repository. Phase 4 removes only this function's old files, and only after they are in Old repos deleted and merged. Do not restore files under ~/.ollama/skills/energy, automations, or coms/ssh/local-data-globe.
- EcoFlow BLE, the poller, Hawaiʻi weather, the globe collector, camera grabs, Kokoro, and geology_collect.py are live. Do not replace them.
- Sends, speaker playback, OBS, hardware switching, deletion of live Ecosystem files, and cloud spend require Alexander's sign-off. Put that gate in the plan. Do not do those things. Phase 4 is already ordered: archive the old function's files, then remove them from the old repo locally and on GitHub.

Put this inside the work-order sections, not in a separate format:
1. Intent: what the old function did, and what the live system already does that must be kept.
2. Current reality: the Folder name and the three paths (server code, Database data, Database logs), plus master-key.env key names if any.
3. Tasks: the build steps, in order, including the pause if a dependency Folder is missing.
4. Non-goals: files that must not be overwritten, and the other agents' functions.
5. Key paths: every file you will add or extend.
6. Notes: sign-off gates, and one small test that proves the new behavior.
7. After phase 4, add a short result note to that work order (what landed, what was archived, what was removed on GitHub) and correct the Library pages that are now wrong.
