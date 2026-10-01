# Test record — PROPOSED pronunciations: Kalākaua, Liliʻuokalani, Nuʻuanu, Māhele

| Field | Value |
| --- | --- |
| **Date / time (HST)** | 2026-09-29 04:27–04:41 HST |
| **Tester** | Grok Bot (executor, overnight build, pass 2) |
| **Change under test** | Pacific `Media/Voice/scripts/clip_catalog.py` `PROPOSED_PRONUNCIATION` (catalog entries `proposed: true` + explicit `spoken`); `voice_generate.py` (stitcher never uses proposed clips). **Not** added to `hawaiian_lexicon.py` |
| **State** | **PROPOSED** (rendered + format QC only; nothing marked PASS by ear; not live) |
| **Evidence** | Database `Media/Audio/Voice/Clips/Ava/proposed_*.wav` (git-ignored) + `clips_manifest.json` entries |
| **Backup** | `/home/rootrecord/Database/GITHUB/g3-voice-reports2.bak-20260929-042153/` |

## Search for existing respellings
Searched G1 (`~/old ollama/old skills`, `~/old ollama/github-history`), G2/G3 (`~/Database`, `~/RootRecord-Ecosystem` incl. Library and Pacific, `~/recovery`), case- and ʻokina/kahakō-insensitive. The two private folders were excluded (`~/Desktop/old txt`, `I'll sort these models tomorrow`).

- **No English respelling** exists for any of the four. G1 `history/references/hawaiian.md` uses the names in text only.
- **Existing phonetic sources found** (IPA, not respellings):

| Name | Source | Pronunciation |
| --- | --- | --- |
| Nuʻuanu | G1 `state/store/hawaiian-dictionary/kaikki.org-dictionary-Hawaiian.jsonl` (Wiktionary) | /nu.ʔuˈa.nu/, [nu.ʔuˈwɐ.nu] |
| Māhele | same (headword `mahele`, no kahakō) | /maˈhe.le/, [məˈhɛ.lɛ] |
| Liliʻuokalani | misaki `us_gold.json` (Kokoro's own G2P lexicon) | lIlˌiəwˌɑkəlˈɑni (English-style "lil-ee-uh-wah-kuh-LAH-nee") |
| Kalākaua | none found | — |

## Candidates (standard Hawaiian phonology: a=ah, e=eh, i=ee, o=oh, u=oo, au=ow; ʻokina = glottal stop, a syllable break here; kahakō = long vowel)
Kokoro has no glottal-stop phoneme (misaki maps ʔ to t), so the ʻokina is a separate syllable. Stress (Hawaiian: penultimate mora, long vowels stressed) cannot be marked in a respelling. "G2P reads" is misaki's phoneme output for the spoken text.

| Clip (Ava af_heart 0.82) | Written | Spoken as | G2P reads | Syllables / note | Duration | QC | State |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `Ava/proposed_kalakaua` | Kalākaua. | kah lah kow ah. | kˈɑ lˈɑ kˈW ˈɑ | ka-LĀ-kau-a | 0.97 s | format PASS | **PROPOSED** |
| `Ava/proposed_liliuokalani` (A) | Liliʻuokalani. | lee lee oo oh kah lah nee. | lˈi lˈi ˈu ˈO kˈɑ lˈɑ nˈi | li-li-ʻu-o-ka-LA-ni | 1.51 s | format PASS | **PROPOSED** |
| `Ava/proposed_liliuokalani_b_misaki` (B) | Liliʻuokalani. | Liliuokalani. (Kokoro native) | lIlˌiəwˌɑkəlˈɑni | existing misaki entry, English-style | 1.26 s | format PASS | **PROPOSED** (compare A/B) |
| `Ava/proposed_nuuanu` | Nuʻuanu. | noo oo ah noo. | nˈu ˈu ˈɑ nˈu | nu-ʻu-A-nu (matches Wiktionary) | 1.03 s | format PASS | **PROPOSED** |
| `Ava/proposed_mahele` (A) | Māhele. | mah heh leh. | mˈɑ hˈɛh lˈA | MĀ-he-le. **Caveat**: the G2P reads the final "leh" as "lay" | 0.90 s | format PASS | **PROPOSED** |
| `Ava/proposed_mahele_b_ipa` (B) | Māhele. | `[Māhele](/mˌɑhˈɛlɛ/)` (inline phonemes) | mˌɑhˈɛlɛ | from Wiktionary [məˈhɛ.lɛ] with a long first a. Needs inline-phoneme support in the live path | 0.74 s | format PASS | **PROPOSED** |

Kokoro-native readings, for comparison only (not rendered): Kalakaua → kˈæləkˌɔə ("KAL-uh-kaw-uh"), Nuuanu → nuˈɑnu (drops the ʻu syllable), Mahele → mˈæhɛl ("MAH-hel"). All three are wrong, which is why the respellings are needed.

## Resources
| Step | Time | rc | Wall | MemAvailable | Load |
| --- | --- | --- | --- | --- | --- |
| 4 A clips (inside the 13-clip batch) | 04:27 | 0 | 12.9 s batch | 9,407 → min 7,965 MB | max 2.17 |
| Liliʻuokalani B | 04:40 | 0 | 6.5 s | 12,161 → 12,173 MB | 1.83 |
| Māhele B | 04:41 | 0 | 6.2 s | 12,092 → 11,898 MB | 1.89 |
| G2P phoneme checks (misaki only, no TTS model) | 04:38–04:40 | 0 | ~3.5 s each | — | — |

## To approve (Alexander, by ear)
Listen to each clip. For an approved candidate, add the name to `hawaiian_lexicon.py`: `PLACE_IPA` (operator IPA), `SPEAK_ENGLISH` (the spoken respelling) and `SPELLING_ALIASES` (unmarked spellings such as "Kalakaua"), then run `test_hawaiian_lexicon.py`. A-style respellings work in the live path today. A B-style choice (inline `[Name](/ipa/)`) is **not** live-compatible as is: G1's `pronounce_places()` deliberately turns existing tags back into English respellings. It would need a documented exception. Then mark it PASS here.

## Cleanup confirmation
- [x] No voice_generate / kokoro processes left; single-flight IDLE. Nothing played or sent.
