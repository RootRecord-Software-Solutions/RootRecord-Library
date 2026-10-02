# Test record — <title>

| Field | Value |
| --- | --- |
| **Date / time (HST)** | YYYY-MM-DD HH:MM–HH:MM HST |
| **Tester** | <agent / operator> |
| **Change under test** | <what changed; WO link> |
| **State** | LANDED · VERIFY PENDING · PASS · FAIL · BLOCKED · RETIRED · PROPOSED · KEPT |
| **Evidence** | `2 - RootRecord-Database/Logs/Migration/<file>.md` |
| **Commits** | Pacific `<sha>` · Database `<sha>` · Library `<sha>` (each checked with `git log --oneline \| grep <sha>`) |
| **Backup** | `/home/rootrecord/Database/GITHUB/<name>.bak-YYYYMMDD-HHMMSS/` |

## What was tested

## How (exact commands / procedure)

```bash
# one test per change; no retry loops
```

## Pass criteria (written before running)

1.

## Result

## Resource impact

| When | Load (1/5/15) | MemAvailable | Swap used | Peak RSS |
| --- | --- | --- | --- | --- |
| before | | | | |
| during | | | | |
| after | | | | |

## Cleanup confirmation

- [ ] no test process left (`pgrep …` = 0)
- [ ] ports closed, lock IDLE
- [ ] no resident model (`ollama ps` empty; no `flm serve`)

## Open items / caveats
