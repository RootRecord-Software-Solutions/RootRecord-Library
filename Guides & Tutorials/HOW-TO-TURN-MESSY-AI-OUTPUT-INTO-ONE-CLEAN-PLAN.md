# How to Turn a Messy AI Chat Dump Into One Clean, Authoritative Plan

A short guide to a workflow: you have scattered planning material — old chat
transcripts, a half-finished spec from another AI, corrections you made along
the way — and you want one clean document out the other end. This is the
process, distilled from an actual session.

---

## The situation this is for

You recognize this pattern if:

- You've been planning something complex (a migration, an architecture, a
  project) across multiple AI conversations, notes, or drafts.
- Each one has partial context, some wrong assumptions, some good ideas, and
  a lot of noise (UI chrome, "Show more" text, repeated blocks).
- You know more about the actual system than any single document does,
  because you're the one who's been correcting each draft as it goes.
- You want a single reference document a new person (or a new AI session)
  could pick up cold.

You do **not** need to have a clean starting point. Messy input is normal —
that's what step 1 is for.

---

## The workflow

### 1. Dump the raw material in, unedited

Paste the actual mess — old chat exports, half-formed plans, whatever exists
— without cleaning it up first. Don't summarize it yourself before handing
it over; let the assistant do the extraction. The noise (UI text, repeated
paragraphs, false starts) is cheap for an assistant to filter; it's
expensive for you to clean by hand.

### 2. Say "start" — but watch what comes back

The first response will usually try to do too much at once: build a full
schema, write every file, execute every step. This is expected on a first
pass, especially with a large dump. Your job here is just to watch for that.

### 3. Explicitly cap the scope

If the response is trying to do everything at once, say so directly:
*"stop, just understand it and let's go — it's too much."*
This is the single highest-leverage correction in the whole process. It
converts the assistant from "execute the whole plan now" to "confirm
understanding, then wait for direction."

### 4. Ask for the smallest possible first step

Not "the next phase" — the smallest reversible unit of work. ("First
building block only.") This does two things: it gives you something
concrete to check against reality before more is built on top of it, and it
keeps any given step cheap to throw away if it turns out to be wrong.

### 5. Correct facts the moment you notice them — don't let them ride

If the assistant gets a real detail wrong (an architecture model, a naming
scheme, a boundary condition), correct it as soon as you see it, even if it
means discarding work already produced. In this session, an entire schema
was scrapped because the bucket model was wrong — better to lose one
artifact than to build the next ten steps on a wrong foundation. A good
assistant will acknowledge the correction and treat it as authoritative
going forward, not hedge or half-adopt it.

### 6. Ask for consolidation only once the pieces are right

Don't ask for "the clean version" on the first pass — ask for it after the
corrections have landed. ("I'd like to turn this into a super clean plan.")
At that point the assistant should merge everything discussed so far — the
original material, the corrections, the scoped-down plan — into one
document, not just reformat the last message.

### 7. Feed in new source material as it appears — expect it to be merged, not appended

If a new document shows up later (a more formal spec, a second AI's output,
a colleague's notes), hand it over the same way: raw, unedited. The right
move for the assistant is to fold it into the *existing* document —
renumbering sections, refining earlier wording where the new material is
more precise, removing duplication — rather than tacking it on as a
separate block at the end. If you get back two stapled-together documents
instead of one coherent one, ask for it to be merged properly.

### 8. Be direct about delivery format

"As an artifact," "as an md," "as a file I can download" — these are
different things and worth being explicit about. It's a one-line request
and saves a round trip.

### 9. When something can't be done, expect a plain answer — not a workaround that pretends to work

In this session, a private GitHub URL couldn't be fetched. The right
response is to say so plainly and offer the actual alternatives (paste the
tree, run a local command and paste the output) — not to guess at file
contents or pretend the fetch succeeded.

---

## Why this works

The underlying reason this produces a good result: **you are the source of
truth, not the assistant.** The assistant doesn't know your system; you do.
Every correction you make is data the assistant didn't have. The workflow
above is really just a fast loop for transferring what's in your head into
one document, using the assistant as the thing that holds structure and
absorbs the busywork of merging, formatting, and cross-referencing — while
you supply the one thing it can't: whether it's actually right.

The failure mode this avoids is the opposite loop — accepting whatever the
first draft says, building on top of it, and only discovering the wrong
assumption three layers of work later.

---

## Quick reference

| Step | What you do | What you're asking for |
|---|---|---|
| 1 | Paste raw material | Extraction, not summarization |
| 2 | Say "start" | Watch scope |
| 3 | "That's too much" | Understanding before execution |
| 4 | "First building block only" | Smallest reversible step |
| 5 | Correct on sight | Discard-and-rebuild over patch-and-hope |
| 6 | "Make it clean" | One document, not a reformat |
| 7 | Paste new material later | Merge, not append |
| 8 | Name the format | No guessing on delivery |
| 9 | Hit a real limitation | Plain statement, real alternatives |
