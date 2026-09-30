# 0002 — Council inference stays on the NPU

Date: 2026-09-30.

## Decision

The relay sets `RR_NPU_ONLY=1`, `RR_NPU_PERSONA=1`, and `FLM_MODEL` default `llama3.2:3b`. Context stays 4096. The model loads for a reply and then stops. Personas are JSON files under Database `AI/FLM/Personas/`, not one generic prompt.

## Reason

The council should use the NPU. A resident 3B process at context 8192 OOM'd this desk on 2026-09-29. Ollama remains installed for other work. It is not the council fallback while `RR_NPU_ONLY=1`.

## Drift

`Automations/scripts/jobs.py` still says `llama3.2:1b` and an Ollama fallback. That line is older than this decision. The state aggregator reports `configuration_drift` instead of hiding one of them. Fixing the comment is a documentation edit. Changing the relay model is not.

## Do not remove without reconsidering

- Memory headroom on this desk
- One-model-at-a-time inference
- The difference between the jobs comment and the running relay
