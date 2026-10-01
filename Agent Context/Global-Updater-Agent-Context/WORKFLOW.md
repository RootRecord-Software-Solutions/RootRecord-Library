# Workflow — Root Record Global Updater

## Discord reply

1. A person mentions Root Record Global Updater in a configured professional guild channel.
2. Load this pack through `Communications/CouncilPersona/scripts/personas.py`.
3. Read recorded observations that already exist. Do not sample the host from Discord.
4. Attach the matching documentation section when the question is covered by this pack.
5. Ask `run-infer.sh` once, as the voice `global-updater`.
6. Check the reply. Drop invented measurements, other-agent identities, and instruction leaks.
7. Post only when `RR_DISCORD_POST=1`. The updater gate `RR_GLOBAL_UPDATER` stays off until that send is signed off.

Other channel traffic is left alone. Direct messages are left alone. The Minecraft Discord is out of scope.

## When a source is missing

Say that the measurement or the answer is unavailable. Do not guess a service is running because a host sample exists. Do not guess a host figure because a document describes the server.

## What this workflow does not do

- It does not run the Ava, Bruce, Carly review chain
- It does not call Telegram
- It does not enable the Discord poller job
- It does not copy this pack into `Communications/Discord/`
