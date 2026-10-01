# CouncilPersona

Not an identity pack.

Pacific `Communications/CouncilPersona/scripts/personas.py` reads Library `Agent Context/{Ava,Bruce,Carly,Global-Updater}-Agent-Context/` at reply time. It does not keep a prompt copy, and nothing syncs the packs onto the server. Telegram still requests only ava, bruce, and carly.

The short `prompts/*.md` files that briefly lived in that folder were a second editable persona. They are gone from the working tree. Git history still has them. Do not restore them as a source of truth.
