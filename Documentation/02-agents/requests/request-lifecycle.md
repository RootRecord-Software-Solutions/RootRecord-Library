# Request lifecycle

An interaction request lives in Database `System/status/requests/`. It is not committed. Schemas stay in Library.

Fields stay distinct. A later step appends. It does not overwrite `original_request`.

`RECEIVED` → `CLASSIFIED` → `MODE_SELECTED` → `DISCOVERY`.

From discovery the council may set `QUESTIONS_REQUIRED`. An answer appends to the question list and returns to discovery. The fourth unresolved round becomes `NEEDS_DECISION`.

After a draft and council review:

- A standard user, or an authorized principal whose build gate is off, ends at `PENDING_AUTHORIZATION`. `execution.permitted` is false.
- A principal matched on numeric id, with the build gate on and no Carly reject, may reach `READY_FOR_BUILD`.
- Carly `reject` sets `BLOCKED`.
- A missing dependency sets `BLOCKED` or `NEEDS_DECISION`.

A later authorization is a new event on `authorization.events`. `requested_by` stays the original sender.

`READY_FOR_BUILD` with the handoff gate on writes the context package and moves to `CURSOR_HANDOFF`. While `cursor_api` is off, the request stays there. That stop proves the package. It is not a permanent requirement that a person start Cursor.

`cursor_api` on invokes the Cursor API from that package, then the execution report, the verification report, and the state summary.
