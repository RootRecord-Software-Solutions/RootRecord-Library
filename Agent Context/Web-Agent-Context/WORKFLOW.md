# Workflow — Cove

## When Alexander asks for the web seat

1. Read [CONTEXT/SITE.md](CONTEXT/SITE.md). If this pack and the files it names disagree, follow the files.
2. Edit `Website/Home/`. Do not open a second site.
3. If the change is a reading, confirm `telemetry.js` still requests `api.rootrecord.cloud` and still treats a bad response as no data.
4. Open the changed page and use it.
5. Ask Wren when the Library page that describes the site is now wrong. Cove does not invent a second Library folder.

## What this workflow does not do

- It does not run the Ava, Bruce, Carly review chain
- It does not call `run-infer.sh`
- It does not start a local Next server
- It does not copy this pack into Pacific `Communications/`
