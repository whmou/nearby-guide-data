# Miyako Google Maps independent crosscheck

**Latest covered source: 2026-09-16T22:12:15.603978+08:00 — 105 IDs (71 legacy + 34 new). Wetland P1 is fixed in current YAML. Remaining owner follow-ups: Nishi-Hennazaki arrival precision; Imgya missing captured numeric link; candidate-only `named_listing` claims for textile centre, Shiratorisaki park and newly added Irabu seaside station. See final supplement for four additions and fixed wetland. No source/JSON/code/media edits by this reviewer.**

## Priority handoff — main must resolve before publication

- **P1 `jp-miyakojima-ikema-wetland`: adopt the visitor lookout, not the wetland centre.** At 2026-09-16 22:02 +08:00 YAML uses `24.9323891,125.242831`, `landmark`, with an 80 m trigger and a hint explicitly admitting that the pin is the wetland centre and may not trigger from the lookout. The actually opened **池間湿原 展望台** is `24.9348056,125.2424515`, **271 m** away. Recommend `anchorType: viewpoint`, title **池間湿原（展望台）**, and consistent `location`, `googleMapsUrl`, `verifiedLocation`, hint, narration and review evidence. Do not enlarge the trigger or retain an inaccessible centre merely because its numbers come from an official page. Main owns the source change; this audit makes none.
- Suggested hint: 「導航至池間湿原展望台的觀察位置，不是濕地中心或停車場入口。沿道路與現場『池間湿原』指標抵達；只在開放的觀察設施停留，勿穿越濕地、翻越圍欄或為觸發而離開通行區。遇封閉標示不進入；不保證旅期開放或鳥況。」
- Numeric evidence: `../../../viewer-qa/maps-selected-results.json`, ID `jp-miyakojima-ikema-wetland`, `checkedAt=2026-09-16T13:45:39.074Z`; selected title and heading **池間湿原 展望台**, category **展望台**, address **沖縄県宮古島市平良池間**. Both opened and resolved-share URLs carry `!3d24.9348056!4d125.2424515`, place ID `0x34f44d8f94853d7d:0xbbb7730993487d50`. [Observed named listing](https://www.google.com/maps/place/%E6%B1%A0%E9%96%93%E6%B9%BF%E5%8E%9F+%E5%B1%95%E6%9C%9B%E5%8F%B0/data=!4m7!3m6!1s0x34f44d8f94853d7d:0xbbb7730993487d50!8m2!3d24.9348056!4d125.2424515!16s%2Fg%2F11j4xq3fjl!19sChIJfT2FlI9N9DQRUH1Ikwlzt7s).
- Access/identity evidence fetched through the web tool on 2026-09-16: [Okinawa environmental department — 池間湿原（ユニムイ）](https://www.midorihana-okinawa.jp/?page_id=2739) expressly describes observing birds/aquatic plants from a lookout, while its numeric table is the different centre above. [Ikema Tourism Association — イーヌブー（池間湿原）に行ってみよう！](https://ameblo.jp/ikemajimakankoukyoukai/entry-12251672830.html) describes following the road opposite Funakusu parking, then wetland signs, to a birdwatching shelter. This supports a visitor observation facility reached along roads, not a route through the wetland. Linking the shelter to Google's named lookout is a corroborated inference, not an independently surveyed building footprint. The article is historical; no guarantee of current road condition, parking permission, opening hours or 2026-09-23 access follows.
- [Apple Maps lead](https://maps.apple.com/place?place-id=I5576A91A2140E6A7) was attempted but returned a fetch/cache error; **not counted as independently retrieved coordinate evidence**. Direct shell HTTP attempts also failed; no permissions or installs were changed. No screenshot or site photograph was visually inspected.

## Scope and method

- Read root `AGENTS.md`/`GEMINI.md` and data `AGENTS.md`, `LOCATION_REVIEW.md`, `CONTRIBUTING.md`.
- Initial source snapshot: **2026-09-16T22:02:06.810636+08:00**, **101 YAML IDs** (66 verified, 12 unresolved, 23 non_point); other agents are still adding/editing source.
- Available supplied browser artifacts: existing 49 records, selected 8, new 20, candidate leads 16. They are main's public fresh-profile Chrome observations, not this auditor's newly opened Chrome pages.
- Read-only source/QA review; only this Markdown file is owned/written. Compare current YAML rather than stale `sourceLocation` captured when browser queries were made. Extract only named-place `!3d/!4d`, never `@` viewport. Exact candidate links require identity matching and are distinguished from actually opened selected listings.
- Distances are great-circle Haversine using Earth radius 6,371,008.8 m, rounded to nearest metre. A difference alone does not invalidate a documented public visitor anchor.
- Full per-ID coverage/findings follow below; this handoff is **not a publication clearance**.

## Remaining actionable findings and dispositions

| Priority / ID | Finding | Owner action before claiming completion |
|---|---|---|
| P2 `jp-miyakojima-nishi-hennazaki` | Official `24.9095,125.25725` is **211 m** from opened 西平安名崎 `24.9100868,125.2552644`, and **155 m** from candidate 西平安名崎展望台 `24.9086489,125.2584665`. At 80 m neither alternate pin is covered. | [Re-fetched tourism page](https://miyako-island.net/beach_and_spot/beach_spot_024/) supports a visitor cape with parking/toilets, but does not establish the precise pin's stopping surface. Confirm its public land-side approach or explicitly adopt a verified lookout if that is the intended arrival; do **not** blindly move to the cape tip or inflate radius. This is an arrival-precision gap, not proof the official landmark is wrong. |
| P2 `jp-miyakojima-imgya-marine-garden` | Current YAML/new-south audit claims resolved share `T7WfPd4cg4Ctjvdj7` and `24.7247007,125.3583502`. Supplied N and L records show matching named park and 友利605-2 address but **shareUrl:null** and no numeric place link. | Preserve the actual resolved-share browser observation supporting those numbers, or accurately mark the Google numeric crosscheck unavailable. Not a finding that the coordinate is false. The separately listed hilltop 展望台 `24.7232438,125.3578231` is a different target. |
| P2 `jp-miyakojima-miyako-traditional-textile` | Correct centre is explicitly distinguishable by name/address/phone, but E is a **search-results list**, not an opened centre detail page. `existing-3.json` nevertheless labels it `named_listing`; its originalUrl is the list share URL. | Under LOCATION_REVIEW's actual-open definition, open and record the exact adopted centre link, or use an accurately supported method. Keep coordinate `24.7690768,125.3228393`; do not replace with another craft shop or the old approximate address pin. |
| P2 `jp-miyakojima-shiratorisaki` | Current `24.8651896,125.1626357` exactly matches **白鳥崎公園**, but only its E candidate link is in scope. The S detail page is **白鳥崎 西海岸公園**, **732 m** east. `existing-4.json` calls the candidate-only evidence `named_listing`. | Open/record the actual adopted western park listing or accurately classify evidence. Retain current safe-use distinction; consider title 白鳥崎公園（白鳥崎岩礁海岸） to prevent manual name-search confusion. No blanket closure or move to eastern park. |
| Follow-up `jp-miyakojima-nakahara-limestone-cave` | Source claims a resolved share URL absent from N/L snapshots. However E:`hora-cave` contains an exact **仲原鍾乳洞** candidate pin and N/L open the matching cave at 友利1114. | Coordinate independently corroborates at 0 m through the candidate link. Align stored provenance with actual available capture, or preserve the missing share resolution; no coordinate move. |
| Guard `jp-miyakojima-tomori-utaki` | Exact-name 友利御嶽 candidate is `24.4709487,123.8212696`, off Miyako; 友利あま井 is instead a well. | Already unresolved/null navigation. Keep disabled; never promote exact-name hit without island/place identity proof. |
| Guard `jp-miyakojima-miyako-horse` | Opened 宮古馬牧場 `24.9012938,125.2647246` is marked **閉業**, at 狩俣. | Already non_point/null navigation; keep it. This is neither unnamed Irabu ranch nor the municipality's 長間 pasture. |
| Guard `jp-miyakojima-ikema-beach` | Only **カギンミビーチ** in the multi-beach results is marked **臨時休業**. | Generic entry already unresolved. Do not assign closure to all Ikema beaches, or substitute a different beach under this ID. |

### >100 m differences that must not cause blind coordinate replacement

- `jp-miyakojima-ikema-bridge`: **1,027 m** to bridge-body `24.9200526,125.2604759`; existing official mainland viewpoint `24.913723,125.267898` and hint intentionally avoid stopping on the bridge. **Keep**.
- `jp-miyakojima-kurima-bridge`: **833 m** to bridge-body `24.7256881,125.2641684`; official Kurima landward bridgehead `24.721198,125.257565` has the appropriate role. **Keep**.
- `jp-miyakojima-irabu-bridge`: **1,556 m** to bridge-body `24.7962883,125.2410596`, but only **13 m** to actually opened 宮古島口 `24.7950803,125.2564785`. **Keep** official mainland-side `24.794986,125.256406`.
- `jp-miyakojima-sarahama-port`: **467 m** to northern **佐良浜漁港** `24.8421577,125.2125144`, but **2 m** to opened southern **佐良浜港** `24.8382051,125.2140219`. Existing hint explicitly restricts the southern port's public areas. **Keep**; neither pin grants access to working quays.
- `jp-miyakojima-sawada-beach`: **253 m** to Google's broad beach feature `24.8377299,125.1572351`. Current `24.83909607,125.15924072` is the official OCVB destination q; both identify 佐和田1725. [Re-fetched official page](https://www.okinawastory.jp/spot/600006198/) identifies the natural beach and visitor access, not a navigable lagoon centre. **Keep** the documented official visitor-landmark interpretation; no surveyed entrance or guarantee of current open access is asserted.
- `jp-miyakojima-shiratorisaki`: current park is **732 m** from the selected eastern park and **232 m** from closed old **白鳥崎** `24.8631199,125.1629139`. E lists three distinct place IDs; only the old cape is marked 閉業. [Tourism association](https://miyako-island.net/beach_and_spot/beach_spot_010/) describes paths/rest areas from Funasugi to Shiratorisaki, and [municipal heritage page](https://miyakojimabunkazai.jp/bunkazaiinfo537/) places this rocky coast within the West Coast Park area. **Keep current park choice with exact-listing evidence follow-up**, not blanket closure or an eastern-park substitute.
- `jp-miyakojima-kuninaka-sacred-grove`: earlier N candidate 国仲御嶽 `24.8261555,125.1732544` is about **338 m** from earlier official grove anchor `24.825542,125.176538`. Current YAML is already **unresolved with null navigation**. A forest/shrine centre does not establish a publicly permitted approach; **keep disabled**.

Below-threshold but operationally relevant: 17END **93 m**, スサビミャーカ **95 m**, 高腰城跡 **89 m** each exceed an 80 m trigger when measured to the Google feature. This is not proof of coordinate error or reason to enlarge the radius. Keep official provenance and confirm the intended public stopping spot if reliable automatic triggering is required.

## Frozen coverage and evidence vocabulary

- Source ledger snapshot: **2026-09-16T22:05:21.463466+08:00**, still **101 IDs = 71 legacy + 30 new**, unchanged from the 22:02 source snapshot. All IDs at that time appear once in the two ledgers below.
- QA reread immediately after that source snapshot: **E 49, S 8, N 29, L 16 = 102 observation records**. Latest recorded N observation: **2026-09-16T14:05:18.077Z**. This is not 102 distinct current points: selected records and leads overlap; ten lead names have no current source ID.
- These final QA files directly cover **78 current IDs**; earlier N also covered `kuninaka-sacred-grove` before it disappeared from the refreshed aggregate (**79 current IDs observed across both reads**). Its per-ID artifact remains available at `viewer-qa/maps-jp-miyakojima-kuninaka-sacred-grove.json`. The remaining **22** IDs are non_point topics with no supplied browser observation.
- **66 navigation-enabled verified IDs:** **60** have identity-matched numeric Google evidence (**51 D, 9 C**); **6** lack an independently matching numeric place URL in the supplied artifacts. Four have name/address-only corroboration (`harimizu-stone-road`, `head-tax-stone`, `imgya-marine-garden`, `kurima-nagama-beach`); two searches have no matching entity (`isuga-well`, `maiga-sacred-tree`). Official embedded-pin evidence is a separate allowed method; these gaps alone do not prove source coordinates wrong.
- **35 disabled IDs = 12 unresolved + 23 non_point**. All had `location`, `trigger`, `googleMapsUrl` null. All 66 verified coordinates matched their `verifiedLocation`. No source was changed by this reviewer.
- **D** = an actually opened named detail page in main's observations plus numeric `!3d/!4d` from that page/its share resolution. **C** = manually identified exact `placeLinks` candidate with `!3d/!4d`; not automatically the first result and **not** claimed as an opened detail page. The ledger notes the record ID when reused across queries.
- **E** = [maps-existing-results.json](../../../viewer-qa/maps-existing-results.json), **S** = [maps-selected-results.json](../../../viewer-qa/maps-selected-results.json), **N** = [maps-new-results.json](../../../viewer-qa/maps-new-results.json), **L** = [maps-candidate-leads.json](../../../viewer-qa/maps-candidate-leads.json). Match rows by full ID (or the explicit lead/record alias), not array position.
- No Google screenshot, satellite image, Street View frame, travel photo or physical site was visually reviewed. DOM/body/heading/address/URL evidence only. “24 時間営業” is a captured Maps label, not an assurance of legal access, weather safety or trip-date operation.
- Scope intentionally excludes rebuilding, audit sealing, release/publishing, media licensing, code edits and source/audit-JSON edits. This is an independent crosscheck and owner handoff, **not publication clearance**.

## Navigation-enabled ledger — all 66 IDs

Distances compare the frozen YAML location to the explicitly identified Google feature, not browser `sourceLocation` or `@` viewport. “Keep” means no contrary location evidence in this scoped crosscheck, not an independently inspected route or opening guarantee.

| ID / current title | YAML coordinate; anchor | Google evidence / named feature coordinate | Δ m | Disposition |
|---|---|---|---:|---|
| `jp-miyakojima-17end-beach` · 下地島17エンド | 24.84230232, 125.14072418; viewpoint | S-D 17ENDビーチ; 24.8421325, 125.1398185 | 93 | Keep documented official shore viewpoint; not parking (621 m away). 93 m exceeds 80 m trigger: no guarantee at Google's beach pin. |
| `jp-miyakojima-aragusuku-beach` · 新城海岸 | 24.75977, 125.42478; landmark | E-D 新城海岸; 24.7598523, 125.4248602 | 12 | Same named coast; retain official landmark, not a parking/water-entry claim. |
| `jp-miyakojima-awamori-distillery` · 多良川酒造 | 24.7308405, 125.3524826; meeting_point | S-D (株)多良川 本社; 24.7307616, 125.3522427 | 26 | HQ/address 砂川85 matches. Reject Miyako sales office (9.44 km); retain shop check-in restriction. |
| `jp-miyakojima-city-museum` · 宮古島市総合博物館 | 24.7965306, 125.3178511; landmark | E-D 宮古島市総合博物館; 24.7965306, 125.3178511 | 0 | Same museum building. YAML already warns 9/23 regular holiday closure; pin is not admission assurance. |
| `jp-miyakojima-funaha-well` · フナハガー古井 | 24.817664, 125.180929; landmark | N-D フナハガー; 24.8176667, 125.1809167 | 1 | Same well; remain outside, not factory/cave access. |
| `jp-miyakojima-funasugi-banata` · フナウサギバナタ | 24.86148, 125.177959; viewpoint | E-D フナウサギバナタ; 24.861253, 125.1779987 | 26 | Same viewing site; current hint does not promise former bird statue or cliff access. |
| `jp-miyakojima-german-emperor-monument` · 德國皇帝博愛紀念碑 | 24.806258, 125.279706; landmark | N-D ドイツ皇帝博愛記念碑; 24.806258, 125.279706 | 0 | Hirara monument matches; not Ueno German Village. |
| `jp-miyakojima-harimizu-stone-road` · 漲水石疊道 | 24.807217, 125.279913; landmark | N — no matched numeric pin | — | IDENTITY ONLY: named page/address matches; unresolved short URL provides no !3d/!4d. Official q remains separate evidence. |
| `jp-miyakojima-harimizu-utaki` · 漲水御嶽 | 24.807268, 125.27951; landmark | E-D 漲水御嶽; 24.8073672, 125.2796286 | 16 | Same utaki; retain public worship-path boundary, no sacred-grove entry. |
| `jp-miyakojima-head-tax-stone` · 人頭税石 | 24.81279945, 125.28171539; landmark | E — no matched numeric pin | — | IDENTITY ONLY: ぶばかり石 (人頭税石), 荷川取90; no numeric named-place URL in supplied QA. |
| `jp-miyakojima-hennazaki-east` · 東平安名崎 | 24.718962, 125.469101; viewpoint | E-D 東平安名崎; 24.7191788, 125.4684503 | 70 | Same cape; keep official viewpoint, not lighthouse door/parking. |
| `jp-miyakojima-higa-road-park` · 比嘉Road Park海岸展望休憩處 | 24.785332, 125.384118; viewpoint | N-C 比嘉ロードパーク; 24.7849365, 125.3843373 | 49 | Exact 比嘉 link; reject 上比屋ロードパーク. Official stop/roadside viewpoint preserved. |
| `jp-miyakojima-hisamatsu-megalithic-tomb` · 久松巨石墓群（久貝ぶさぎ） | 24.785877, 125.264122; landmark | N-D 久松みゃーか（巨石墓）群の碑; 24.7859332, 125.2639814 | 16 | Google pin names the group monument/碑, not all tombs. Official Kugai tomb anchor remains; no interior access. |
| `jp-miyakojima-hora-spring` · 保良泉 | 24.7301684, 125.4319768; visitor_area | S-D 保良泉ビーチパーク; 24.7301684, 125.4319768 | 0 | Selected beach-park visitor facility matches, not spring source/cave; parking candidate 247 m away is different. |
| `jp-miyakojima-ikeda-stone-bridge` · 池田矼石拱橋 | 24.753347, 125.285709; landmark | N-D 下地町の池田矼; 24.7532346, 125.2854901 | 25 | Same historic bridge; landmark is not a vehicle stopping place. |
| `jp-miyakojima-ikema-bridge` · 池間大橋 | 24.913723, 125.267898; viewpoint | E-D 池間大橋; 24.9200526, 125.2604759 | 1027 | 1,027 m FLAG explained: official mainland bridgehead vs bridge-body pin. Keep land-side anchor. |
| `jp-miyakojima-ikema-toomi` · 池間遠見番所跡 | 24.922257, 125.247986; landmark | N-C 遠見番所; 24.9222801, 125.2479119 | 8 | Matched 平良池間93 historic site, not 島尻/来間 namesakes; second 池間 listing is not selected automatically. |
| `jp-miyakojima-ikema-wetland` · 池間湿地 | 24.9323891, 125.242831; landmark | S-D 池間湿原 展望台; 24.9348056, 125.2424515 | 271 | P1: change centre to selected visitor viewpoint 24.9348056,125.2424515; see priority handoff. |
| `jp-miyakojima-imgya-marine-garden` · 英吉雅海濱公園（インギャーマリンガーデン） | 24.7247007, 125.3583502; visitor_area | N/L — no matched numeric pin | — | P2 EVIDENCE GAP: title/address 友利605-2 match but supplied N/L rows lack claimed resolved share URL. Retrieve that exact observation; do not copy hilltop deck. |
| `jp-miyakojima-irabu-bridge` · 伊良部大橋 | 24.794986, 125.256406; viewpoint | S-D 伊良部大橋宮古島口; 24.7950803, 125.2564785 | 13 | Selected 宮古島口 matches official landward end; ignore 1,556 m bridge-body difference. |
| `jp-miyakojima-isuga-well` · 磯井（イスゥガー） | 24.89758, 125.277269; landmark | N — no matched numeric pin | — | NO MATCH: results are イザガー, 大和井, ムイガー etc. Official 狩俣磯井 anchor not Google-confirmed; reject substitutions. |
| `jp-miyakojima-kamama-ridge-park` · カママ嶺公園 | 24.79746, 125.2767831; landmark | E-D カママ嶺公園; 24.79746, 125.2767831 | 0 | Exact park landmark; hint correctly excludes shisa/entrance. No evidence justifies inventing a gate coordinate. |
| `jp-miyakojima-kanzato-well` · 神里井（神里ガー） | 24.821418, 125.174641; landmark | N-D 神里ガー; 24.8213635, 125.174643 | 6 | Same 神里ガー; retain well-exterior limitation. |
| `jp-miyakojima-kurima-bridge` · 来間大橋 | 24.721198, 125.257565; viewpoint | E-D 来間大橋; 24.7256881, 125.2641684 | 833 | 833 m FLAG explained: official Kurima-side bridgehead vs bridge body; do not navigate to midpoint. |
| `jp-miyakojima-kurima-nagama-beach` · 長間浜 | 24.7261944, 125.2398056; landmark | E — no matched numeric pin | — | IDENTITY ONLY: 長間浜 on 来間, address 484-1 matches; no numeric !3d/!4d in QA. Not a claimed gate. |
| `jp-miyakojima-kurima-viewpoint` · 来間島龍宮城展望台 | 24.72593, 125.25137; viewpoint | E-D 竜宮城展望台; 24.7260129, 125.2516393 | 29 | Same 竜宮城展望台; keep official lookout, not car park. |
| `jp-miyakojima-kurohama-utaki` · 黑濱御嶽 | 24.844423, 125.159253; landmark | N-D 黒浜御嶽; 24.8444844, 125.1586067 | 66 | Same shrine; preserve exterior/public-path-only limitation. |
| `jp-miyakojima-maiga-sacred-tree` · 前井與神木（外側觀看） | 24.765464, 125.346595; landmark | N — no matched numeric pin | — | NO MATCH: 前山/トマイ/飛鳥 groves are different entities. Official 前井 pin not independently Google-confirmed. |
| `jp-miyakojima-makiyama-observatory` · 牧山展望台 | 24.817783, 125.21783; viewpoint | L-D 牧山展望台; 24.8178419, 125.2182529 (record lead-makiyama-viewpoint) | 43 | Named lookout matches; do not substitute it for unresolved ビャクダン山. |
| `jp-miyakojima-marine-park` · 宮古島海中公園 | 24.8788312, 125.2749104; entrance | E-D 宮古島海中公園; 24.8787444, 125.2747111 | 22 | Official reception-route end vs same facility pin (22 m); retain reception entrance purpose, not offshore chamber. |
| `jp-miyakojima-miyako-shrine` · 宮古神社 | 24.807785, 125.28043; landmark | E-D 宮古神社; 24.8077675, 125.280533 | 11 | Same shrine and 西里5-1; not a surveyed gate. |
| `jp-miyakojima-miyako-soba` · 古謝そば屋（宮古そば） | 24.790285, 125.284452; landmark | E-D 古謝そば屋; 24.790285, 125.284452 | 0 | Exact 古謝そば屋/下里1517-1. Already explicitly this shop in HEAD, not a new generic-food substitution. |
| `jp-miyakojima-miyako-traditional-textile` · 宮古上布（宮古島市伝統工芸品センター） | 24.7690768, 125.3228393; landmark | E-C 宮古島市 伝統工芸品センター; 24.7690768, 125.3228393 | 0 | Exact centre name/address/phone candidate, not arbitrary textile shop. HEAD already linked this centre; title now explicit. |
| `jp-miyakojima-muiga-cliff-lookout` · 姆伊嘎斷崖展望處（ムイガー） | 24.7258887, 125.3827058; viewpoint | L-D ムイガー断崖; 24.7258887, 125.3827058 (record lead-muiga-cliff) | 0 | Correct cliff/lookout listing, not ムイガー spring (~95 m) or Imgya lookout; preserve no-cliff-descent hint. |
| `jp-miyakojima-nakahara-limestone-cave` · 仲原鍾乳洞 | 24.7330416, 125.3778424; visitor_area | E-C 仲原鍾乳洞; 24.7330416, 125.3778424 (record jp-miyakojima-hora-cave) | 0 | Exact candidate coordinate plus N/L opened named-page/address confirmation; not 保良泉鍾乳洞. QA lacks source's claimed resolved-share URL. |
| `jp-miyakojima-nakazone-tomb` · 仲宗根豊見親の墓 | 24.80862617, 125.27981567; landmark | E-D 仲宗根豊見親の墓; 24.8086526, 125.2799105 | 10 | Same named tomb; not permission to enter burial chamber. |
| `jp-miyakojima-nishi-hennazaki` · 西平安名崎 | 24.9095, 125.25725; landmark | S-D 西平安名崎; 24.9100868, 125.2552644 | 211 | P2: 211 m to cape, 155 m to separate lookout. Retain official provenance; verify safe stopping/trigger target before claiming accurate arrival. |
| `jp-miyakojima-nishi-tsuga-tomb` · 西ツガ墓 | 24.804758, 125.275332; landmark | N-D 西ツガ墓; 24.80475, 125.2753333 | 1 | Same tomb exterior; no moat/interior access. |
| `jp-miyakojima-nishinaka-sugar-chimney` · 舊西中共同製糖場煙囪 | 24.755491, 125.362717; landmark | N-D 旧西中共同製糖場煙突; 24.7554915, 125.36271 | 1 | Same chimney; stay public roadside, no field/site entry. |
| `jp-miyakojima-nishizato-market` · 宮古島市公設市場 | 24.8039621, 125.2787251; landmark | E-D 宮古島市公設市場; 24.8039621, 125.2787251 | 0 | Exact city public market/下里一番地; corrected title avoids the old 西里-market ambiguity. |
| `jp-miyakojima-obi-iwa` · 下地島帶岩（帯岩） | 24.818952, 125.140738; landmark | N-C 帯石; 24.8189215, 125.1407334 | 3 | Exact 帯石 candidate, not 帯石の海岸; retain land-side viewing restriction. |
| `jp-miyakojima-painagama-beach` · パイナガマビーチ | 24.80275345, 125.27103424; landmark | E-D パイナガマビーチ; 24.8026123, 125.2703656 | 69 | Same beach; do not treat shoreline landmark as parking or swimming entry. |
| `jp-miyakojima-pinza-abu-site` · Pinza-Abu遺跡（洞外解說） | 24.748322, 125.33489; landmark | N-D ピンザアブ遺跡; 24.7485931, 125.3344089 | 57 | Same archaeological site; keep cave-exterior only, not a cave-entry route. |
| `jp-miyakojima-saba-utsuga` · サバウツガー（佐良濱海邊古井） | 24.846921, 125.206351; landmark | N-D サバウツガー; 24.8470632, 125.205828 | 55 | Same historic well; cliff-top stopping/steps distinct from well feature. |
| `jp-miyakojima-sarahama-port` · 佐良浜漁港 | 24.8381863631, 125.2140340536; landmark | S-D 佐良浜港; 24.8382051, 125.2140219 | 2 | Selected southern 佐良浜港 matches (2 m); northern 佐良浜漁港 is 467 m away. Hint resolves title ambiguity. |
| `jp-miyakojima-sawada-beach` · 佐和田の浜 | 24.83909607, 125.15924072; landmark | E-D 佐和田の浜; 24.8377299, 125.1572351 | 253 | 253 m FLAG: official OCVB beach anchor and matching 佐和田1725 vs broad Google beach feature. Keep official visitor landmark; no lagoon-centre move. |
| `jp-miyakojima-sawada-yukui` · 佐和田ユークイ | 24.845655, 125.169365; landmark | N-D 佐和田ユークイ; 24.8455358, 125.1693067 | 15 | Same ritual site; keep external/public-path-only limit. |
| `jp-miyakojima-shimajiri-uganzaki` · 島尻のマングローブ林 | 24.87813888888889, 125.28825; landmark | E-D 島尻のマングローブ林; 24.877956, 125.288553 | 37 | Same mangrove landmark; not kayak meeting/water entry. |
| `jp-miyakojima-shimoji-airport` · 下地島空港 | 24.8291633, 125.149189; landmark | E-D みやこ下地島空港ターミナル; 24.8290343, 125.1495618 | 40 | Same public terminal building; not runway/17END. |
| `jp-miyakojima-shiratorisaki` · 白鳥崎 | 24.8651896, 125.1626357; visitor_area | E-C 白鳥崎公園; 24.8651896, 125.1626357 | 0 | Correct park C link matches exactly; selected eastern park is 732 m away, closed old cape is 232 m away. Retain distinction; consider title 白鳥崎公園. |
| `jp-miyakojima-sumiya-site` · 住屋遺跡 | 24.80607, 125.281163; landmark | N-C 住屋遺跡; 24.8060958, 125.2811226 | 5 | Exact named archaeological site C link, not other tomb/shrine results; keep above-ground/exterior interpretation. |
| `jp-miyakojima-sumurya-myakka` · Sumurya巨石墓（外觀） | 24.720969, 125.247871; landmark | N-C スムリャーミャーカ; 24.7204265, 125.2479443 (record jp-miyakojima-sumiya-site) | 61 | Exact 来間 tomb candidate from N:sumiya-site, confirmed by its own named-page address; no tomb interior. |
| `jp-miyakojima-sunayama-beach` · 砂山ビーチ（砂山海灘） | 24.83953094, 125.28069305; landmark | E-D 砂山ビーチ; 24.8395634, 125.2806924 | 4 | Same beach; restricted rock arch is not a visitor route. |
| `jp-miyakojima-susabi-myahka` · スサビミャーカ巨石墓 | 24.815724, 125.182905; landmark | N-D スサビミャーカ(巨石墓); 24.8162517, 125.18217 | 95 | 95 m near threshold and >80 m trigger. Official tomb vs Google tomb feature: preserve provenance, confirm public approach if trigger reliability required. |
| `jp-miyakojima-takausu-castle` · 高腰城跡 | 24.779078, 125.381972; landmark | N-D 高腰城跡; 24.7797572, 125.3815104 | 89 | 89 m >80 m trigger, though <100 m audit threshold. Landmark, not gate; confirm public stopping point if required. |
| `jp-miyakojima-toguchi-beach` · 渡口の浜 | 24.81194115, 125.18006897; landmark | E-D 渡口の浜; 24.8117373, 125.1806646 | 64 | Same beach; not parking/water-entry pin. |
| `jp-miyakojima-tomori-amaga` · 友利阿瑪井（地面外觀） | 24.726775, 125.354465; landmark | N-D 城辺町の友利のあま井; 24.7271202, 125.3546569 | 43 | Same 城辺友利 well; not same-name 友利御嶽 on another island. |
| `jp-miyakojima-toriki-ike-pools` · 通り池 | 24.824333333333335, 125.13638888888889; landmark | E-D 下地島の通り池; 24.8236648, 125.1361496 | 78 | Same feature, 78 m; no pool-centre route or entry. Public boardwalk access stays explicit. |
| `jp-miyakojima-tropical-botanical-garden` · 宮古島市熱帯植物園 | 24.8000949, 125.3155536; landmark | E-D 宮古島市熱帯植物園; 24.8006932, 125.3152696 | 72 | Same park address, 72 m; address feature is not exact gate. Do not conflate nearby craft village with whole garden. |
| `jp-miyakojima-ueno-german-village` · ドイツ文化村 | 24.7192626, 125.3239909; landmark | E-D うえのドイツ文化村; 24.7190238, 125.3236934 | 40 | Same village/address, 40 m; landmark is not gate or assurance all paid buildings open. |
| `jp-miyakojima-underground-dam-museum` · 宮古島地下水壩資料館 | 24.7392323, 125.3946688; landmark | L-D 宮古島市地下ダム資料館; 24.7392323, 125.3946688 (record lead-underground-dam-museum) | 0 | Exact groundwater-dam museum/福里1645-8; not history museum or general museum. |
| `jp-miyakojima-uruka-tomi` · 砂川遠見番所遺跡 | 24.725666, 125.352241; landmark | N-C 遠見番所; 24.7255441, 125.3520518 | 23 | Matched southern 砂川/城辺 watch platform; reject 島尻, 来間 and 水納 namesakes. |
| `jp-miyakojima-yamato-well` · 大和井（ヤマトガー） | 24.811074, 125.285494; landmark | N-D 大和井; 24.8110072, 125.2854835 | 8 | Same 大和井; no guarantee stairs open or well water usable. |
| `jp-miyakojima-yonaha-maehama` · 与那覇前浜 | 24.7349726, 125.2629745; landmark | E-D 与那覇前浜; 24.7349726, 125.2629745 | 0 | Exact named beach; keep hint distinguishing visitor landmark from parking/entry. |
| `jp-miyakojima-yoshino-coast` · 吉野海岸 | 24.74835396, 125.44252777; landmark | E-D 吉野海岸; 24.748698, 125.442441 | 39 | Same beach; shore guide, not guaranteed safe water-entry point. |
| `jp-miyakojima-yukishio-factory` · 雪塩製塩所 | 24.9022357, 125.2683734; landmark | E-D 雪塩ミュージアム; 24.9022357, 125.2683734 | 0 | Exact museum next to saltworks. Owner post warns typhoon early closure, not permanent 閉業. |

## Disabled-navigation ledger — all 35 IDs

All rows below retain null location/trigger/Google navigation URL; no numerical “pass” is claimed for unobserved generic topics.

| ID | Source status | Browser coverage | Identity / closure disposition |
|---|---|---|---|
| `jp-miyakojima-biyandam-viewpoint` | unresolved | E | No exact identity; unrelated lookout results (including Makiyama) must not replace it. |
| `jp-miyakojima-botanical-bingata` | non_point | none | Generic dyeing workshop theme; no supplied Maps observation, do not attach an arbitrary craft village. |
| `jp-miyakojima-coral-restoration` | non_point | none | Project/activity theme, not a single public arrival point. |
| `jp-miyakojima-hora-cave` | unresolved | E | Search returns 仲原鍾乳洞/保良泉ビーチ; neither establishes this cave identity. |
| `jp-miyakojima-ikema-beach` | unresolved | E | Multiple different beaches. カギンミビーチ is marked 臨時休業; do not equate generic beach with Funakusu/Ohama. |
| `jp-miyakojima-ikema-dugong` | non_point | none | Habitat theme; no single fixed visitor point. |
| `jp-miyakojima-ikema-island` | non_point | none | Island-wide, not a centroid arrival. |
| `jp-miyakojima-irabu-diving` | non_point | none | Boat/diving activity, not an onshore meeting point. |
| `jp-miyakojima-irabu-island` | non_point | none | Island-wide, not a centroid arrival. |
| `jp-miyakojima-irabu-katsuobushi` | non_point | none | Cultural theme; no named workshop established. |
| `jp-miyakojima-irabu-lighthouse` | unresolved | E | Results include 平安名埼/池間島/宮古水納島 lighthouses; wrong islands/identity, no substitution. |
| `jp-miyakojima-irabu-panorama` | unresolved | E | Multiple bridge ends/viewpoints; no unique place identity. |
| `jp-miyakojima-kaijin-no-mori` | unresolved | E | No exact named match; unrelated parks/businesses cannot supply coordinates. |
| `jp-miyakojima-kuninaka-sacred-grove` | unresolved | N earlier snapshot | Earlier N record has 国仲御嶽 24.8261555,125.1732544, ~338 m from prior official grove pin; public approach unresolved. Keep disabled. |
| `jp-miyakojima-kurima-island` | non_point | none | Island-wide, not a centroid arrival. |
| `jp-miyakojima-kurima-sugarcane` | non_point | none | Fields/theme, not public access authorization. |
| `jp-miyakojima-mango-orchard` | non_point | none | Unspecified farm; Utopia/Maipari leads must not silently replace it. |
| `jp-miyakojima-maou-palace-cave` | non_point | none | Underwater dive site, no independent pedestrian arrival. |
| `jp-miyakojima-miyako-beef-ranch` | non_point | none | Unspecified ranch; no substitute business chosen. |
| `jp-miyakojima-miyako-festival` | non_point | none | Event/theme, not a fixed current venue. |
| `jp-miyakojima-miyako-horse` | non_point | E | Google 宮古馬牧場 at 24.9012938,125.2647246 is explicitly 閉業, 狩俣; not municipal 長間 pasture or unnamed Irabu ranch. |
| `jp-miyakojima-nakanoshima-channel` | non_point | none | Dive channel is not 中の島海岸 beach; preserve separate semantics. |
| `jp-miyakojima-ogami-island` | non_point | none | Whole island; no invented port/centre arrival. |
| `jp-miyakojima-sea-kayak-mangrove` | non_point | none | Activity, not the mangrove park or an established meeting point. |
| `jp-miyakojima-sea-turtle-yoshino` | non_point | none | Wildlife/activity theme; not a turtle-guaranteed beach pin. |
| `jp-miyakojima-shimajiri-beach` | unresolved | E | 前浜東岸 not identified; 与那覇前浜 results do not establish it. |
| `jp-miyakojima-shimoji-cave-dive` | non_point | none | Underwater activity distinct from landward 通り池 walk. |
| `jp-miyakojima-shimoji-island` | non_point | none | Whole island; no centroid arrival. |
| `jp-miyakojima-snorkel-rental` | non_point | none | No specific provider/pickup point established. |
| `jp-miyakojima-south-wall` | unresolved | E | Results are dive shops, not the named underwater feature; keep unresolved. |
| `jp-miyakojima-sunagawa-utaki` | unresolved | E | 砂川神社/other utaki do not establish intended shrine; retain unresolved. |
| `jp-miyakojima-sunayama-sunset` | unresolved | E | No exact lookout; 砂山ビーチ and remote sunset spots cannot replace it. |
| `jp-miyakojima-sunset-cruise` | non_point | none | Operator/meeting location unspecified. |
| `jp-miyakojima-tomori-utaki` | unresolved | E | Exact-name candidate 24.4709487,123.8212696 is off Miyako (western Yaeyama/Iriomote area); never adopt. Nearby 友利あま井 is a well, not this utaki. |
| `jp-miyakojima-yabiji-reef` | non_point | none | Offshore reef area; no pedestrian/centroid arrival. |

## Candidate leads without source IDs at the 101-ID snapshot

The following L records were read but **not** silently matched to generic old topics: `lead-shigira-beach`, `lead-waiwai-beach`, `lead-utopia-farm`, `lead-maipari`, `lead-kurima-tako-park`, `lead-nakanoshima-beach`, `lead-irabu-uminoeki`, `lead-atara-market`, `lead-shimanoeki`, `lead-funakusu-beach`. If main adds named source IDs after the frozen snapshot, those IDs need a supplemental crosscheck. Specifically, a beach is not Nakanoshima Channel; a new named farm is not the unspecified mango-orchard theme; a new shop/market is not the existing city public market.

## Owner handoff / completion limits

Main acknowledged the wetland priority and is implementing its viewpoint correction. The ledgers intentionally preserve the pre-fix snapshot so that the original finding remains reproducible. Confirm the actual integrated source change and corresponding audit evidence before release. Also resolve/acknowledge the P2 arrival/evidence findings above; do not label candidate-only or missing-number checks as independently opened numeric listings. Subsequent source additions/edits are not covered merely because another agent completed its batch.

## Final delta supplement — 105 current IDs at 22:12:15 +08:00

Final source reread: **four additions**, plus one changed existing ID (`jp-miyakojima-ikema-wetland`). All four additions below match supplied L observations. Titles, anchor roles, hints, Maps queries and verifiedLocations checked. No additional official page fetch needed: no new coordinate/identity conflict.

**Wetland P1 resolved in source:** title **池間湿原（展望台）**, `anchorType: viewpoint`, `location = verifiedLocation = 24.9348056,125.2424515`, consistent Maps query, 80 m trigger and public-observation/no-wetland-crossing hint. Distance to selected named lookout now **0 m**. Main made the change. Earlier ledger deliberately preserves the pre-fix 271 m finding; sealing/build/release not inspected.

| ID / current title | YAML and matched Google !3d/!4d | Evidence / Δ | Disposition |
|---|---|---|---|
| `jp-miyakojima-irabu-seaside-station` · 伊良部大橋海の駅 | 24.8111392,125.2185239; landmark | L-C `lead-irabu-uminoeki`; **0 m** | Correct **service area**, place ID `0x34f455f648c63a7f:0xb796f810721ab357`, phone 0980-78-3778; operator embedded place ID recorded in YAML corroborates. Same-name **restaurant** is a different listing at `24.8110434,125.2181413`. Hint correctly excludes restaurant/supplier address. **P2:** new-north.json claims `named_listing` but L is a results list; open/record the adopted service-area page or accurately classify official-embedded-pin evidence. Keep correct coordinate. |
| `jp-miyakojima-shigira-beach` · Shigira海灘（シギラビーチ） | 24.7202654,125.3408467; visitor_area | L-D `lead-shigira-beach`; **0 m** | Same beach at 上野新里, not hotel/pool gate. Hint retains public beach approach and potentially paid facilities. No closure marker; no trip-date access guarantee. |
| `jp-miyakojima-shimanoeki-market` · 島の駅みやこ（久貝本店） | 24.7958761,125.2742848; landmark | L-D `lead-shimanoeki`; **0 m** | Same 久貝870-1 branch; new distinct ID, not city public market/airport shop. Owner's typhoon early-closing warning is not permanent closure. |
| `jp-miyakojima-utopia-farm` · Utopia Farm宮古島觀光農園 | 24.738253,125.322026; visitor_area | L-D `lead-utopia-farm`; **0 m** | Same named farm/上野宮国1714-2/operator website and phone. Separate ID, not replacement for generic mango-orchard. Hint requires reception/excludes production areas; weekly-closure caveat present. Google 営業時間外 is not permanent closure. |

**Final coverage: 105/105 source IDs enumerated; 70 verified, 12 unresolved, 23 non_point. 64 verified IDs have matching numeric browser evidence (54 D + 10 C); the same six numeric-evidence gaps remain.** Final supplied aggregate files cover **82** current IDs, or **83** including earlier 国仲 evidence; remaining **22** are correctly disabled generic topics with no browser observations. Six L leads still have no source at this check: `lead-waiwai-beach`, `lead-maipari`, `lead-kurima-tako-park`, `lead-nakanoshima-beach`, `lead-atara-market`, `lead-funakusu-beach`. Later additions require another delta check.

**Release handoff:** no newly identified wrong-island or marked-closed listing remains navigation-enabled in these snapshots; this does not certify public access. Main must acknowledge Nishi-Hennazaki arrival ambiguity and the Google capture/method gaps. Wetland correction was observed, not merely promised. This reviewer wrote only `audits/miyako-trip-2026-09-23/maps-crosscheck.md`.
