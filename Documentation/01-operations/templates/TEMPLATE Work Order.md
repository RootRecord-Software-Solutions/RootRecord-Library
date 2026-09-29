# WORK ORDER — {{TITLE}}

| Field | Value |
| --- | --- |
| **Work Order ID** | WO-{{CODE}}-{{YYYY-MM-DD}} |
| **Date** | {{YYYY-MM-DD}} (HST) |
| **Status** | OPEN — {{short status}} |
| **Owner** | RootRecord |
| **Related** | {{links or none}} |

**Scope:** {{One paragraph — what is in scope and what is not.}}

---

## 1. Intent

{{Why this work exists.}}

---

## 2. Current reality

### 2.1 What exists

| Item | Location / status |
| --- | --- |
| {{Item}} | {{Where / state}} |

### 2.2 Completed so far

- [x] {{Done}}
- [ ] {{Not done}}

### 2.3 Known friction

- {{Friction}}

---

## 3. Tasks

1. {{Task}}
2. {{Task}}
3. {{Task}}

---

## 4. Non-goals

- {{Non-goal}}
- {{Non-goal}}

---

## 5. Key file / path reference

| Path | Role |
|------|------|
| {{path}} | {{role}} |

---

## 6. Open items

**Additional requirements:**

- 
- 
- 

---

## 7. Notes & constraints

- No force-push.
- Secrets stay out of git.
- Prefer small reversible steps.
- {{Domain-specific constraint}}

---

*Work order prepared {{YYYY-MM-DD}} HST. Update status when closed.*

---

## Archive / location note

**Active / accepted WOs** — filename when saved:

```text
{{Short_Name}}_Work_Order_WO-{{CODE}}-{{YYYY-MM-DD}}.md
# or
WO-{{CODE}}-{{short-title}}.md
```

Location:

```text
Documentation/06-development/Work-Orders/
```

**Drafts (not on active index)** — use:

```text
Documentation/06-development/Work-Orders/drafts/
```

See `drafts/README.md` and WO-WOGEN-001. Do not auto-promote.

**Closed WOs:** set Status → COMPLETE/CLOSED → `git mv` into:

```text
Documentation/06-development/Work-Orders/Complete/
```

Human session logs archive under `Documentation/01-operations/archive/YYYY-Www/` (WO-ARCH) — separate from closed work orders.
