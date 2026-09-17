# Miyako trip — independent editorial cross-check

Review date: 2026-09-16 (Asia/Taipei). Sample reread: 22:05. Owner: independent editorial QA.

## Outcome and scope

Sixteen completed entry-level rewrites were sampled across `new-north`, `new-south`, `existing-1`, `existing-2`, and `existing-4`. Their reports contained story claims and their YAMLs were in `review`, **not approved**. This is a risk-selected sample, not a release certificate or an assertion that all 16 pass.

Highest-priority handoff: substantiate or remove Pinza-Abu's assumed public interpretation/viewing position (F01); state Kuninaka's documented prohibition rather than merely uncertain access (F02). Also fix municipal attribution, unresolved-place titles, an unsupported family-tomb embellishment, and several visibility/audio issues. Historical numbers and myths were checked individually; supported details are recorded below rather than silently classified as errors.

Read `AGENTS.md`, `LOCATION_REVIEW.md`, `CONTRIBUTING.md`, the five batch reports, and the sampled YAML narratives, summaries, observation prompts, hints, sources, and review notes. Opened the actual source pages/PDF text independently, rather than relying on agents' `supports` claims or search snippets. Additional primary material uncovered a specific sacred-access rule and resolved a suspected visual-detail gap.

Only this Markdown file is written by this reviewer. No source, tools, schema, public files, network settings, credentials, commits, seals, builds, releases, or publishing were changed. No browser was installed and no live Google Maps research was performed. Coordinates and shared Maps claims are not independently certified here.

## Actionable findings

### F01 — High: assumed public viewing facility at Pinza-Abu

- Owner / ID: `new-south` — `jp-miyakojima-pinza-abu-site`.
- Fields / exact wording: title `Pinza-Abu遺跡（洞外解說）`; narration `面前的洞口` and `請把參觀留在洞外公共解說位置`; observation prompt `在洞外公開解說位置`; location hint `只在洞外公共解說位置觀看`.
- Evidence: [heritage description](https://miyakojimabunkazai.jp/bunkazaiinfo834/) identifies the 1980 excavation and human/animal remains. The independently opened [city inventory, ピンザアブ遺跡 section](https://www.city.miyakojima.lg.jp/kanko/bunkazai/miyakojimabunkazai/shiseki2.html) also describes the research and preservation value. Neither text establishes a public interpretation area, present-day public access, or a safe outside position with the stated view. The heritage page was additionally fetched directly, HTTP 200.
- Classification: **unsupported access/visibility assumption, not proof that no sign or viewing area exists**. The no-entry/no-collecting precautions are appropriate, but do not supply evidence for the place where visitors are told to stand.
- Recommendation: retain the archaeological story and no-cave-entry rule; remove the assumed facility from title/narration/prompt/hint unless the owner has identifiable access evidence. Suggested conditional instruction: `若現場設有開放的洞外解說位置，可依標示閱讀；未確認開放前不接近洞口、不入洞。` Avoid opening with `面前` for an unverified sightline. A landmark pin must not imply a verified public viewing point.

### F02 — High: Kuninaka's actual no-entry rule is now available

- Owner / ID: `new-north` — `jp-miyakojima-kuninaka-sacred-grove`.
- Current wording: `這些是資料中的空間描述，不表示旅客能走進參觀`; prompt `未確認公共接近點前不入林`; hint says access involves ritual restrictions. Current YAML is already `unresolved`, with navigation withheld; that safeguard should remain.
- New primary evidence: [city Irabu guide](https://www.city.miyakojima.lg.jp/soshiki/kyouiku/syougaigakusyu/syougaikakusyu/files/aya_irabujima.pdf), printed pp. 52–53, PDF page 28 (zero-based 27), explicitly says entry is not permitted outside ritual use. Relevant short wording: `祭祀以外で中に入ることはできません`.
- Why this matters: the existing [heritage page](https://miyakojimabunkazai.jp/bunkazaiinfo635/) describes a 90 m approach and shrine, but a spatial description is not visitor permission. The report's “PDF original pending” gap can now be closed with the actual text. Access is not merely unknown until somebody finds a better pin.
- Recommendation: add the city PDF to the story evidence and say `市府導覽明載御嶽內部不供一般遊客進入；本項僅供背景閱讀。` Do not imply that visitors may attend rites or enter after finding an approach. Any future outside viewpoint still requires separate public-access evidence. The 60-species/near-natural-forest description is supported.

### F03 — Medium: wrong municipal name in four narratives

- Owner: `new-north`.
- IDs and exact phrases: `jp-miyakojima-yamato-well` — `宮古市的文化財解說`; `jp-miyakojima-susabi-myahka` — `宮古市將`; `jp-miyakojima-kuninaka-sacred-grove` — `宮古市文化財解說`; `jp-miyakojima-obi-iwa` — `宮古市的文化財解說`.
- Evidence: issuing authority on their [Yamato](https://miyakojimabunkazai.jp/bunkazaiinfo84/), [Susabi](https://miyakojimabunkazai.jp/bunkazaiinfo557/), [Kuninaka](https://miyakojimabunkazai.jp/bunkazaiinfo635/), and [Obi-iwa](https://miyakojimabunkazai.jp/bunkazaiinfo588/) pages is **宮古島市教育委員会**.
- Recommendation: change these attributions to `宮古島市` or `宮古島市教育委員會`. This is a concrete attribution correction, not a request to rewrite supported history.

### F04 — Medium: unresolved names still look like confirmed attractions in titles

- IDs / owners: `jp-miyakojima-sunayama-sunset` (`existing-4`) and `jp-miyakojima-hora-cave` (`existing-1`). Related confirmed-place comparison: `jp-miyakojima-sunayama-beach`.
- Exact issue: `砂山展望台（日落景點）` remains the title, although its own summary/narration says the separate platform has not been established. `保良泉鍾乳洞` likewise lacks the old-name/identity qualification that appears later in its narration. Both correctly withhold navigation.
- Sources: the [tourism association's Sunayama page](https://miyako-guide.net/spots/spots-804/) establishes the beach and sand dune, not a separate public observatory. The [local sunset article](https://www.tanoshima.jp/facilities/detail/sunayamabeach?category=spot) also describes the beach, not the former draft's wooden platform. For Bora, the [operator's actual page](https://boraga-pool.com/kayak/index.html) specifically markets Pumpkin cave kayaking; the [city notice](https://www.city.miyakojima.lg.jp/soshiki/shityo/kankosyoukou/kankou/oshirase/borakubakundai.html) refers to 保良クバクンダイ. Those pages do not by themselves establish the old dataset name's exact identity or public entrance.
- Recommendation: qualify titles, e.g. `砂山夕景／舊展望台名稱待確認` and `保良泉鍾乳洞（舊名待確認）`; retain immutable IDs. Keep the sunset record a non-navigating explanatory cross-reference, not a second verified stop. This is unresolved-identity/duplicate-presentation risk, **not a finding that two currently enabled GPS triggers duplicate each other**.

### F05 — Medium: Susabi adds a family claim and overpromises a combined view

- Owner / ID: `new-north` — `jp-miyakojima-susabi-myahka`.
- Exact claims: `大塊石材把家族的安息之所圍了起來`; closing invitation `把大石與薄石板放在同一個視野裡`.
- Evidence: [heritage page](https://miyakojimabunkazai.jp/bunkazaiinfo557/) supports an estimated date around 1600, double walls, outer dimensions, and stone-coffin construction. It does not identify a family. The [city museum's children's field-trip material](https://www.city.miyakojima.lg.jp/soshiki/kyouiku/syougaigakusyu/hakubutsukan/files/h28oono01.pdf), PDF page 5 (zero-based 4), explicitly treats whose tomb it is and why it was built there as unanswered questions.
- Recommendation: replace `家族的安息之所` with `墓葬空間`. The construction detail is not invented, but simultaneous visibility of outer blocks and inner thin slabs from the permitted exterior was not established. Keep the preceding distinction between documentary knowledge and physical viewing; finish with `若從開放外側看得到，可比較石塊尺度；內部構造以官方解說理解。` Do not entice visitors to climb a wall to obtain the promised view.

### F06 — Medium: Tomori's wear marks are real documentary evidence; the exact surface viewing setup is not established

- Owner / ID: `new-south` — `jp-miyakojima-tomori-amaga`.
- Exact wording to qualify: `先在地面看看井口和向下延伸的石階` and `上方可安全觀看的井口、石階走向與解說牌`.
- Evidence: [heritage page](https://miyakojimabunkazai.jp/bunkazaiinfo563/), also fetched directly with HTTP 200, explicitly supports approximately 20 m depth, use before the 1965 water supply, women/children carrying water, and worn rock beside descending steps. Thus **do not delete the wear marks as an invented embellishment**. Neither that text nor the [city prefectural-properties entry](https://www.city.miyakojima.lg.jp/kanko/bunkazai/miyakojimabunkazai/ken.html) establishes the present-day surface sightline or the named interpretation board.
- Recommendation: retain the historical facts with attribution; change the visitor instruction to `若在現場允許停留的地面位置看得到井口或石階，可留意其走向；看不到也不要下井。` Refer to `現場如有解說牌` unless the owner supplies identifiable evidence for the board. The existing no-descent/no-fence-crossing rule is sensible and should stay.

### F07 — Low/medium: narration assumes a photograph that the entry does not provide

- IDs: `jp-miyakojima-maou-palace-cave` (`existing-2`), `jp-miyakojima-hora-cave` (`existing-1`). Both have `media: []` in this sample.
- Wording: Maou begins `先看介紹照片裡亮與暗的交界`; Bora begins `看到洞穴照片裡的鐘乳石`. Maou's observation prompt also requests a photograph instead of something physically visible at the site.
- Evidence: the [OCVB dive page](https://www.okinawastory.jp/feature/activity/diving) and [Bora operator page](https://boraga-pool.com/kayak/index.html) have externally hosted pictures, but those are not attached dataset media and their availability to an offline audio listener was not established. `CONTRIBUTING.md` asks for physically visible observation prompts.
- Recommendation: start from the place/activity distinction without assuming an on-screen picture. If a pre-trip photo exercise is intentional, explicitly say `若另行開啟業者的具名潛點照片…`, and document the non-point/pre-trip exception instead of presenting it as an on-site prompt. Do not add an unlicensed image to satisfy the prose. Maou's 27 m, boat-entry, intermediate-or-above, and advance-qualification source claims are supported; the operator suitability caveat should remain.

### F08 — Low: nine narrations exceed the requested sentence range; unresolved records read like audit logs

- Local standard: `CONTRIBUTING.md` requests natural spoken narration of 2–5 sentences. Counting Chinese sentence-ending punctuation in the 22:05 sample gives: `jp-miyakojima-kuninaka-sacred-grove` 6; `jp-miyakojima-obi-iwa` 6; `jp-miyakojima-maiga-sacred-tree` 6; `jp-miyakojima-city-museum` 7; `jp-miyakojima-harimizu-utaki` 7; `jp-miyakojima-head-tax-stone` 8; `jp-miyakojima-hora-cave` 7; `jp-miyakojima-maou-palace-cave` 6; `jp-miyakojima-toriki-ike-pools` 6. This is a punctuation-based editorial aid, not an audio-duration test.
- Repeated pattern: a visual opener, official-source attribution, a “not X” correction, an observation request, and a moral/conceptual wrap-up. Individually reasonable; repetitive in a multi-stop listening sequence.
- Especially awkward: Sunayama sunset says `實際地圖搜尋還混入…`; Bora says `所以沒有替它安上一個海灘座標`; Toriike says `這個地標pin不是潛水入口`. These expose dataset maintenance mechanics instead of telling a compact travel story.
- Recommendation: move research process to review notes; keep a short, direct traveler-facing identity/access warning. For Toriike, `這裡只從開放步道觀察，不是入水點` is clearer than `地標pin`. Shorten by removing redundant meta-commentary, not the no-entry, no-water-entry, closure, or myth-attribution safeguards. For supported content, use the source URLs in the coverage table below.

## Sample coverage — exact IDs and source comparison

“Supported” here means the listed claim matches the opened source, not that every fact, sightline, safety condition, or future opening is certified.

| Batch | Exact ID | Independently checked claim / result | Primary source actually opened |
| --- | --- | --- | --- |
| new-north | `jp-miyakojima-yamato-well` | Circa-1720 estimate based on the 1727 record; circular masonry/steps; officials, gates and guards properly marked as tradition. Supported; F03 attribution correction. | [大和井](https://miyakojimabunkazai.jp/bunkazaiinfo84/) |
| new-north | `jp-miyakojima-susabi-myahka` | Circa-1600 estimate, double walls, 10.8 × 7.2 m outer plan and coffin drainage detail supported. Family identity/viewing promise require qualification (F05); F03. | [スサビミャーカ](https://miyakojimabunkazai.jp/bunkazaiinfo557/); [museum handout, PDF p.5](https://www.city.miyakojima.lg.jp/soshiki/kyouiku/syougaigakusyu/hakubutsukan/files/h28oono01.pdf) |
| new-north | `jp-miyakojima-kuninaka-sacred-grove` | 90 m approach, shrine/lions and approximately 60 plant species supported as descriptions, not visitor access. Additional primary PDF establishes the prohibition (F02); F03/F08. | [植物群落](https://miyakojimabunkazai.jp/bunkazaiinfo635/); [city bilingual description](https://www.city.miyakojima.lg.jp/soshiki/kyouiku/syougaigakusyu/syougaikakusyu/bunkazai-KuninakaPlantCommunity.html); [Irabu guide, printed pp.52–53](https://www.city.miyakojima.lg.jp/soshiki/kyouiku/syougaigakusyu/syougaikakusyu/files/aya_irabujima.pdf) |
| new-north | `jp-miyakojima-obi-iwa` | 12.5 m / estimated 20,000 tonnes supported. The 1771 emplacement story remains attributed, not presented as established dating. Independent city PDF supports the narrowed middle/name: not an invented feature. Add that source for this claim; F03/F08. | [下地島巨岩](https://miyakojimabunkazai.jp/bunkazaiinfo588/); [Irabu guide, printed pp.46–47 / PDF p.25](https://www.city.miyakojima.lg.jp/soshiki/kyouiku/syougaigakusyu/syougaikakusyu/files/aya_irabujima.pdf) |
| new-south | `jp-miyakojima-tomori-amaga` | Approximately 20 m, 1965 waterworks, water-carrying labor and worn rock explicitly supported. Public sightline/board remains an evidence gap (F06), not a proven fabrication. | [友利のあま井](https://miyakojimabunkazai.jp/bunkazaiinfo563/); [city prefectural-property entry](https://www.city.miyakojima.lg.jp/kanko/bunkazai/miyakojimabunkazai/ken.html) |
| new-south | `jp-miyakojima-pinza-abu-site` | 1980 excavation, Hasegawa and human/rodent/deer/snake remains supported. No unsupported modern population-ancestry claim found. Public interpretation position needs evidence (F01). | [ピンザアブ](https://miyakojimabunkazai.jp/bunkazaiinfo834/); [city inventory](https://www.city.miyakojima.lg.jp/kanko/bunkazai/miyakojimabunkazai/shiseki2.html) |
| new-south | `jp-miyakojima-maiga-sacred-tree` | September 1919 conversion, slow flow/ramie work while waiting, and a tree joined with another tree all appear in the source. The tree detail is not invented. The source names アコウ; retain that name if botanical precision matters. Current outside-only guidance is not a proof of today's access. F08. | [前井と御神木](https://miyakojimabunkazai.jp/bunkazaiinfo696/) |
| existing-1 | `jp-miyakojima-city-museum` | Limestone entrance/tomb-inspired design and historical-life models supported. September 23 closure is a valid inference from two official sources, explicitly subject to notices. July restriction is correctly described as an earlier notice, not a September site visit. F08. | [city building description](https://www.city.miyakojima.lg.jp/kanko/annai/sisetsu.html); [museum rules](https://www.city.miyakojima.lg.jp/soshiki/kyouiku/syougaigakusyu/hakubutsukan/index.html); [July reopening notice](https://www.city.miyakojima.lg.jp/soshiki/kyouiku/syougaigakusyu/hakubutsukan/oshirase/2026-0714-0903-198.html); [Cabinet Office 2026 holidays](https://www8.cao.go.jp/chosei/shukujitsu/gaiyou.html) |
| existing-1 | `jp-miyakojima-harimizu-utaki` | Creation/human-snake marriage kept as myths; 1500 vow/wall story correctly attributed to genealogy; popular labor is explicitly recognized by source. No residual promotion of myth into historical fact found. F08. | [漲水御嶽と石垣](https://miyakojimabunkazai.jp/bunkazaiinfo738/) |
| existing-1 | `jp-miyakojima-head-tax-stone` | OCVB supports 1.43 m, 1637–1903, ages 15–50 and grain/cloth. Heritage page supports 30-plus villages and four delegates. OCVB mixes the height story into its account; the rewrite prudently calls it tradition, not verified tax mechanics. This is source inconsistency, not grounds to restore literal height taxation. F08. | [OCVB 人頭税石](https://www.okinawastory.jp/spot/20340903); [鏡原馬場跡](https://miyakojimabunkazai.jp/bunkazaiinfo749/) |
| existing-1 | `jp-miyakojima-hora-cave` | Actual operator describes kayaking to Pumpkin cave, tide-dependent times and cancellation conditions; city recommends conservation-agreement operators. Supports a guided activity example, not proof that the old record name identifies its entrance. F04/F07/F08. | [operator](https://boraga-pool.com/kayak/index.html); [city conservation/safety notice](https://www.city.miyakojima.lg.jp/soshiki/shityo/kankosyoukou/kankou/oshirase/borakubakundai.html) |
| existing-2 | `jp-miyakojima-kamama-ridge-park` | 1976 park conversion, shisa slide, Shinohara teaching history and named monuments supported on the cited city PDF's third page, printed pp.24–25. **No evacuation-destination assertion survives in the sampled narrative.** The guide's disaster-stockpile/observatory label is not, by itself, a current tsunami-evacuation designation. | [city park guide, PDF p.3](https://www.city.miyakojima.lg.jp/soshiki/kyouiku/syougaigakusyu/syougaikakusyu/files/18hiraraminami_kugai_2.pdf) |
| existing-2 | `jp-miyakojima-maou-palace-cave` | Shimoji identity, narrow/dark passages, larger vertical chamber, boat entry, 27 m, intermediate-or-above and advance requirement match the named section. No land entrance or guaranteed sunlight promised. F07/F08. | [OCVB dive guide, 魔王の宮殿 section](https://www.okinawastory.jp/feature/activity/diving) |
| existing-4 | `jp-miyakojima-sunayama-beach` | Dune approach, left-side limestone arch, sudden offshore depth and restricted arch access supported. No instruction to pass under the arch survives. Current rewrite sensibly prioritizes shore viewing. | [tourism association](https://miyako-guide.net/spots/spots-804/); [JTBF resource survey](https://tabi.jtb.or.jp/res/470063-) |
| existing-4 | `jp-miyakojima-sunayama-sunset` | Dune/beach sunset sources do not establish a separate observatory. Wooden platform/boardwalk claims have been removed, and navigation is null. Remaining title/duplicate-presentation concern F04; audit-style prose F08. | [tourism association](https://miyako-guide.net/spots/spots-804/); [local article, supplementary rather than official authority](https://www.tanoshima.jp/facilities/detail/sunayamabeach?category=spot) |
| existing-4 | `jp-miyakojima-toriki-ike-pools` | Approximately 75/55 m pools, cave connection to sea, tidal depth changes and collapsed roof explanation supported. Sea-spirit story explicitly labeled legend. No swimming or self-guided underwater route survives. F08. | [city heritage description](https://miyakojimabunkazai.jp/bunkazaiinfo142/); [tourism association](https://miyako-island.net/beach_and_spot/beach_spot_014/) |

## Limits and handoff

- Sources were independently opened through the web reader, which can return cached page representations. Direct HTTP GET additionally confirmed the Pinza-Abu heritage page, Tomori heritage page, and current museum rules (all HTTP 200). This is not a claim that every source was freshly downloaded from its origin at the same instant.
- PDF findings use extracted page text. Attempts to retrieve page screenshots returned cache errors; no PDF illustration, sightline, photograph, current fence, or physical condition is visually certified. No installation or workaround that changes settings was used.
- The Hirara-north supplementary PDF `https://www.city.miyakojima.lg.jp/soshiki/kyouiku/syougaigakusyu/syougaikakusyu/files/aya_hirarakita01.pdf` could not be opened successfully and was **not used as evidence**. The head-tax story is not a comprehensive historical-tax-system review.
- An official historical description can support masonry, a tree, or an excavation without establishing present public access. Conversely, absent access text is not proof of closure or private ownership. Findings F01/F06 deliberately retain that distinction.
- No September 23–27 opening, tide, weather, guide availability, dive fitness, land ownership, evacuation route, designated shelter, or on-device behavior is certified. No blanket assurance of safe water/cave access is given. Myth attribution was evaluated as wording, not as verification that the legendary events happened.
- Three unresolved records and one non-point record are included because they have completed editorial rewrites: Kuninaka, Bora old cave name, Sunayama sunset, and Maou respectively. Their unavailable on-site prompts should not be “fixed” by inventing a scene or enabling a pin.
- Other agents are still writing. Findings apply to the quoted sample and the fingerprints below; owners must compare their latest text and record corrections in their own work. Nothing here approves later edits, all records in a batch, omitted sources, media rights, or a final package. Do not reseal merely because this report exists.

## Sample fingerprints at 2026-09-16 22:05 +08:00

These identify the read snapshots, not an approval seal.

| Exact ID | Source YAML SHA-256 |
| --- | --- |
| `jp-miyakojima-yamato-well` | `f4c557352a7f9d92ece7209a2af0d7d9ee8a10eac44f00c7e807694bdc607c73` |
| `jp-miyakojima-susabi-myahka` | `4627ef8fbf337f34b7713dc232e8d535af3ad509db4e78234eb4ce510da33091` |
| `jp-miyakojima-kuninaka-sacred-grove` | `c2f26373a39af69748dbb0dd3918174d5625897134fd1803219e43059f96c577` |
| `jp-miyakojima-obi-iwa` | `7fdaeac7dfe9a0a31f4aac2c29473c96c869942d26a8d64dcc3b385b4653654b` |
| `jp-miyakojima-tomori-amaga` | `40dbf2eee3b294d8f6aec63ade827972da3ff25ca8a393e5315c251c1ebfbce6` |
| `jp-miyakojima-pinza-abu-site` | `0aae59665ba45ed9b1d99f285a143a7143bbc26121bf27dd2259729aa8b863da` |
| `jp-miyakojima-maiga-sacred-tree` | `f61bf7b53883cff04267e112cb766a4994cb753f0d40756f5a29b29eb0bcec7f` |
| `jp-miyakojima-city-museum` | `f8699a286fc3140241e0d0a168cc34f1c027eb5001fa6a709a9b596fd4c4c053` |
| `jp-miyakojima-harimizu-utaki` | `03a750fcb724d38f4860bc48002bd26b84d38b388dce40fba180750659431b63` |
| `jp-miyakojima-head-tax-stone` | `762230404a4569c1ecf7dc50c9b4537f99df24cc8e3f05954cf5a4d3f547d61d` |
| `jp-miyakojima-hora-cave` | `bcc093ab6165f38ba34ab9d8d6c28a13d7d6b8b3ab123b15961c70f788c642fb` |
| `jp-miyakojima-kamama-ridge-park` | `3c4fb859b931a3c3043a85e2dab723acae73abf316eea600f696bd283aa265c0` |
| `jp-miyakojima-maou-palace-cave` | `ad3511ebaf02e118f224c949274b2c73b31aa8a6a252836638e4403f2b7100f9` |
| `jp-miyakojima-sunayama-beach` | `07497d41b3b4d49aa9175ef391d710ca5ae658dc108b9e747d144d74f85d5a6a` |
| `jp-miyakojima-sunayama-sunset` | `8f7aff3ce4c1646b2fff116a17c134be2ba7c8462c40dcf133813bdb20572eba` |
| `jp-miyakojima-toriki-ike-pools` | `28d9a6ada665bcc8e797b8ef729ca79ef857553afbc621fe390a01b5a5fd3f3c` |
