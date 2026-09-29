# Test sheet — Hawaiian place-name pronunciation (Kokoro G3 port)

| Field | Value |
| --- | --- |
| **Date / time (HST)** | 2026-09-29 04:12 HST |
| **Tester** | Grok Bot (executor, overnight build) |
| **Change under test** | G1 `hawaiian_lexicon.py` + `speakable.py` copied verbatim into Pacific `Media/Voice/scripts/` |
| **State** | **PASS** (text path: 99/99 canonical spellings, 99/99 ASCII spellings) · audio by ear **VERIFY PENDING** (Alexander) |
| **Evidence** | G1 unit tests `test_hawaiian_lexicon.py` 13/13 PASS on the G3 copy; this sheet generated from the live module |

## How

Each row: `speakable("<name>.")` with the canonical spelling (ʻokina + kahakō) and with the plain ASCII spelling. Kokoro gets the English respelling, never IPA (Misaki maps ʻ→t). The IPA column is the operator list, kept for reference/diagnose tools only. Ava/Ayeva/Avaivy are fixed separately in `voice_generate.apply_lexicon` (`ˈAvə`, `ˈAvəˈIvi`).

Sources searched (grep hawaiian|okina|kahako|respell|lexicon|pronunciation|ʻ across `old ollama/`, Pacific, Library, `~/Database`): the only pronunciation *settings* are G1 `kokoro/scripts/hawaiian_lexicon.py` (SPEAK_ENGLISH + PLACE_IPA) and the Ava lexicon in `generate.py`; everything else is orthography guidance (history/hawaiian.md: kahakō and ʻokina on canonical names; hurricane-ara-prompt: ʻokina where natural) or the G1 `boot_report.py` filter that strips leaked "Pronounce Kīlauea…" instruction lines. All are applied (lexicon verbatim; `speakable` folds ASCII spellings to canonical first).

## Sheet

| Place | ASCII | Spoken respelling (to Kokoro) | Operator IPA | Canonical → | ASCII → |
|---|---|---|---|---|---|
| Hawaiʻi | Hawaii | hah wye ee | həˈwɐi.ʔi | PASS | PASS |
| Hawaiian | Hawaiian | hah wye uhn | həˈwɐi.ən | PASS | PASS |
| Oʻahu | Oahu | oh ah hoo | oˈʔɑ.hu | PASS | PASS |
| Maui | Maui | mow ee | ˈmɐu.i | PASS | PASS |
| Kauaʻi | Kauai | kah wah ee | kɐuˈɑ.ʔi | PASS | PASS |
| Molokaʻi | Molokai | moh loh kah ee | moloˈkɑ.ʔi | PASS | PASS |
| Lānaʻi | Lanai | lah nah ee | lɑːˈnɑ.ʔi | PASS | PASS |
| Niʻihau | Niihau | nee ee how | niːˈi.hɐu | PASS | PASS |
| Kahoʻolawe | Kahoolawe | kah hoh oh lah vay | kɑ.ho.ʔoˈlɑ.ve | PASS | PASS |
| Kīlauea | Kilauea | Kill ah way uh | kiː.lɐˈu.e.ɑ | PASS | PASS |
| Mauna Loa | Mauna Loa | mow nah low ah | ˈmɐu.nə ˈlo.ə | PASS | PASS |
| Mauna Kea | Mauna Kea | mow nah kay ah | ˈmɐu.nə ˈke.ə | PASS | PASS |
| Haleakalā | Haleakala | hah leh ah kah lah | hɑ.le.ɑ.kɑˈlɑː | PASS | PASS |
| Hualālai | Hualalai | hoo ah lah lye | hu.ɑˈlɑː.lɑi | PASS | PASS |
| Halemaʻumaʻu | Halemaumau | hah leh mow mow | hɑ.le.mɐˈu.mɐ.ʔu | PASS | PASS |
| Hilo | Hilo | hee loh | ˈhi.lo | PASS | PASS |
| Pāhala | Pahala | pah hah lah | pɑːˈhɑ.lə | PASS | PASS |
| Pāhoa | Pahoa | pah hoh ah | pɑːˈho.ə | PASS | PASS |
| Kailua-Kona | Kailua-Kona | kye loo ah koh nah | kɐiˈlu.ə ˈko.nə | PASS | PASS |
| Kona | Kona | koh nah | ˈko.nə | PASS | PASS |
| Waikoloa | Waikoloa | wye koh low ah | wɐi.koˈlo.ə | PASS | PASS |
| Honokaʻa | Honokaa | hoh noh kah ah | honoˈkɑ.ʔɑ | PASS | PASS |
| Waimea | Waimea | wye may ah | wɐiˈme.ə | PASS | PASS |
| Keaʻau | Keaau | kay ah ow | ke.ɑˈʔɐu | PASS | PASS |
| Hāwī | Hawi | hah vee | ˈhɑː.vi | PASS | PASS |
| Kapaʻau | Kapaau | kah pah ow | kɑˈpɑ.ʔɐu | PASS | PASS |
| Kealakekua | Kealakekua | kay ah lah keh koo ah | ke.ɑ.lɑ.keˈku.ə | PASS | PASS |
| Hōnaunau-Nāpōʻopoʻo | Honaunau-Napoopoo | hoh now now nah poh oh poh oh | hoː.nɑuˈnɑu nɑːˈpoː.ʔo.poː.ʔo | PASS | PASS |
| Hōnaunau | Honaunau | hoh now now | hoː.nɑuˈnɑu | PASS | PASS |
| Nāpōʻopoʻo | Napoopoo | nah poh oh poh oh | nɑːˈpoː.ʔo.poː.ʔo | PASS | PASS |
| Captain Cook | Captain Cook | Captain Cook | ˈkæp.tən kʊk | PASS | PASS |
| Mountain View | Mountain View | Mountain View | ˈmaʊn.tən vjuː | PASS | PASS |
| Hawaiian Paradise Park | Hawaiian Paradise Park | hah wye uhn Paradise Park | həˈwɐi.ən ˈpæɹ.ə.daɪs pɑɹk | PASS | PASS |
| Hawaiian Ocean View | Hawaiian Ocean View | hah wye uhn Ocean View | həˈwɐi.ən ˈoʊ.ʃən vjuː | PASS | PASS |
| Ainaloa | Ainaloa | eye nah low ah | ɑi.nɑˈlo.ə | PASS | PASS |
| Kurtistown | Kurtistown | Kurtistown | ˈkɝː.tɪs.taʊn | PASS | PASS |
| Paukaa | Paukaa | pow kah ah | pɑuˈkɑ.ə | PASS | PASS |
| Pepeekeo | Pepeekeo | peh peh eh kay oh | pe.pe.eˈke.o | PASS | PASS |
| Laupāhoehoe | Laupahoehoe | lau pah hoy hoy | lɑu.pɑː.hoeˈhoe | PASS | PASS |
| Naalehu | Naalehu | nah ah leh hoo | nɑːˈʔɑ.le.hu | PASS | PASS |
| Nāʻālehu | Naalehu | nah ah leh hoo | nɑːˈʔɑ.le.hu | PASS | PASS |
| Puna | Puna | poo nah | ˈpu.nɑ | PASS | PASS |
| Kaʻū | Kau | kah oo | kɑˈʔuː | PASS | PASS |
| Kohala | Kohala | koh hah lah | koˈhɑ.lə | PASS | PASS |
| Hāmākua | Hamakua | hah mah koo ah | hɑːˈmɑː.ku.ə | PASS | PASS |
| Honolulu | Honolulu | hoh noh loo loo | honoˈlu.lu | PASS | PASS |
| Waikīkī | Waikiki | wye kee kee | wɐi.kiːˈkiː | PASS | PASS |
| Kailua | Kailua | kye loo ah | kɐiˈlu.ə | PASS | PASS |
| Kāneʻohe | Kaneohe | kah neh oh heh | kɑː.neˈʔo.he | PASS | PASS |
| Pearl City | Pearl City | Pearl City | pɝːl ˈsɪ.ti | PASS | PASS |
| Waipahu | Waipahu | wye pah hoo | wɐiˈpɑ.hu | PASS | PASS |
| Kapolei | Kapolei | kah poh lay | kɑ.poˈlei | PASS | PASS |
| ʻEwa Beach | Ewa Beach | eh vah Beach | ˈʔe.vɑ biːtʃ | PASS | PASS |
| ʻEwa Gentry | Ewa Gentry | eh vah Gentry | ˈʔe.vɑ ˈdʒen.tɹi | PASS | PASS |
| ʻEwa | Ewa | eh vah | ˈʔe.vɑ | PASS | PASS |
| Mililani | Mililani | mee lee lah nee | mi.liˈlɑ.ni | PASS | PASS |
| Makakilo | Makakilo | mah kah kee loh | mɑ.kɑˈki.lo | PASS | PASS |
| Wahiawā | Wahiawa | wah hee ah vah | wɑ.hi.ɑˈwɑː | PASS | PASS |
| Waiʻanae | Waianae | wye ah nye | wɐiˈɑ.nɑe | PASS | PASS |
| Nānākuli | Nanakuli | nah nah koo lee | nɑː.nɑːˈku.li | PASS | PASS |
| Haleʻiwa | Haleiwa | hah leh ee vah | hɑ.leˈi.vɑ | PASS | PASS |
| Lāʻie | Laie | lah ee eh | lɑːˈʔi.e | PASS | PASS |
| Hauʻula | Hauula | how oo lah | hɑuˈʔu.lə | PASS | PASS |
| Kahuku | Kahuku | kah hoo koo | kɑˈhu.ku | PASS | PASS |
| Pūpūkea | Pupukea | poo poo kay ah | puː.puːˈke.ə | PASS | PASS |
| Aiea | Aiea | eye ay ah | ɑiˈe.ə | PASS | PASS |
| Ahuimanu | Ahuimanu | ah hoo ee mah noo | ɑ.hu.iˈmɑ.nu | PASS | PASS |
| Heʻeia | Heeia | heh ay ah | heˈʔei.ə | PASS | PASS |
| Kahaluʻu | Kahaluu | kah hah loo oo | kɑ.hɑˈlu.ʔu | PASS | PASS |
| Kahului | Kahului | kah hoo loo ee | kɑ.huˈlu.i | PASS | PASS |
| Lāhainā | Lahaina | lah high nah | lɑːˈhɐi.nɑː | PASS | PASS |
| Kīhei | Kihei | kee hay | kiːˈhei | PASS | PASS |
| Wailuku | Wailuku | wye loo koo | wɐiˈlu.ku | PASS | PASS |
| Makawao | Makawao | mah kah wow | mɑ.kɑˈwɐu | PASS | PASS |
| Hāna | Hana | hah nah | ˈhɑː.nɑ | PASS | PASS |
| Pāʻia | Paia | pah ee ah | pɑːˈʔi.ɑ | PASS | PASS |
| Pukalani | Pukalani | poo kah lah nee | pu.kɑˈlɑ.ni | PASS | PASS |
| Haʻikū-Pauwela | Haiku-Pauwela | high koo pow well ah | hɑˈi.kuː pɑuˈwe.lə | PASS | PASS |
| Nāpili-Honokōwai | Napili-Honokowai | nah pee lee hoh noh koh wye | nɑːˈpi.li honoˈkoː.wɐi | PASS | PASS |
| Kula | Kula | koo lah | ˈku.lə | PASS | PASS |
| Wailea | Wailea | wye lay ah | wɐiˈle.ə | PASS | PASS |
| Kaunakakai | Kaunakakai | cow nah kah kye | kɑu.nɑ.kɑˈkɑi | PASS | PASS |
| Lānaʻi City | Lanai City | lah nah ee City | lɑːˈnɑ.ʔi ˈsɪ.ti | PASS | PASS |
| Kāʻanapali | Kaanapali | kah ah nah pah lee | kɑː.ʔɑ.nɑˈpɑ.li | PASS | PASS |
| Līhuʻe | Lihue | lee hoo eh | liːˈhu.ʔe | PASS | PASS |
| Kapaʻa | Kapaa | kah pah ah | kɑˈpɑ.ʔɑ | PASS | PASS |
| Hanalei | Hanalei | hah nah lay | hɑ.nɑˈlei | PASS | PASS |
| Poʻipū | Poipu | poy poo | poˈʔi.puː | PASS | PASS |
| Kōloa | Koloa | koh low ah | koːˈlo.ə | PASS | PASS |
| Kalaheo | Kalaheo | kah lah hay oh | kɑ.lɑˈhe.o | PASS | PASS |
| Hanamāʻulu | Hanamaulu | hah nah mah oo loo | hɑ.nɑ.mɑːˈʔu.lu | PASS | PASS |
| Hanapēpē | Hanapepe | hah nah pay pay | hɑ.nɑˈpeː.peː | PASS | PASS |
| Kekaha | Kekaha | keh kah hah | keˈkɑ.hə | PASS | PASS |
| Princeville | Princeville | Princeville | ˈpɹɪns.vɪl | PASS | PASS |
| Anahola | Anahola | ah nah hoh lah | ɑ.nɑˈho.lə | PASS | PASS |
| ʻEleʻele | Eleele | eh leh eh leh | ʔe.leˈʔe.le | PASS | PASS |
| Aloha | Aloha | ah loh hah | ɑˈlo.hɑ | PASS | PASS |
| Mahalo | Mahalo | mah hah loh | mɑˈhɑ.lo | PASS | PASS |
| Pele | Pele | peh leh | ˈpe.le | PASS | PASS |

IPA entries without an English respelling (not voiced specially): Volcano

## PROPOSED (not applied — needs Alexander's respelling, none invented)

_Update 2026-09-29 04:41 (pass 2): candidate respellings were written from Hawaiian phonology plus the existing IPA sources that were found (Wiktionary in the G1 store; misaki us_gold). They were rendered as **PROPOSED** clips and are still not in the lexicon. See [pronunciation candidates](./2026-09-29-pronunciation-candidates-proposed.md)._

- `Kalākaua` — not in lexicon; appears in G1 history/references/hawaiian.md
- `Liliʻuokalani` — not in lexicon; appears in G1 history/references/hawaiian.md
- `Nuʻuanu` — not in lexicon; appears in G1 history/references/hawaiian.md
- `Niʻihau` — already in lexicon
- `Māhele` — not in lexicon; appears in G1 history/references/hawaiian.md

## Manual listen list
See `2026-09-29-kokoro-phrase-clips-qc.md` (clips where the whisper-tiny round trip scored < 0.8, mostly respelled Hawaiian names).

