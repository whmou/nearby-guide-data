# 座標審核與發布規則

Schema、ZIP、SHA-256 通過不代表景點位置正確。2026-09 實測發現的公里級錯誤需要逐點查證，而不是增大觸發半徑掩蓋。

- 使用官方景點頁面的座標、Google Maps 地標 pin/query 或地理資料。保存來源 URL、實際提取座標的方式、查核日期與抵達位置說明。
- 地圖 URL 的 `@lat,lng` 通常只是視窗中心；行政區範圍、同名搜尋第一筆、區域代表照片 EXIF、模型記憶均不能充當定位證據。
- 區分入口、公共觀景位置、景點本體、集合點、海中活動區。島嶼中心、潛點、浮潛活動或泛稱美食不能假造「抵達點」。
- `landmark` 可使用具名實體景物的可靠圖釘，不假稱入口；`visitor_area` 僅限有明確官方導航點與陸側到訪佐證的具名遊憩區，不是幾何中心。定位提示必須說明實際用途與限制。`area` 區域中心不能通過定位審核。
- `locationReview.status: verified` 僅表示座標核對，不代表文案、照片、開放時間皆已審核。它必須保存 `verifiedLocation`，座標變更後需重新核對。
- 無法確認者標為 `unresolved`；沒有單一固定位置者標為 `non_point`。保留原座標於審核紀錄，但不向 App 發送 GPS/trigger/Google Maps 連結，文字導覽仍可手動開啟。
- Google Maps query 和 App location 必須同源；不得更新其中一個卻漏掉另一個。
- 不推測精確座標，不虛構照片/授權，不以 placeholder 通過檢查。來源不足就記錄缺口。
- 每次發布都從本次 source 重新建置、檢查產物中的全部景點，使用固定 Release tag，下載核對 hash 後才更新 catalog。

`audits/location-2026-09-16/*.json` 保存各批調查結果；來源 YAML 的 `locationReview` 為最終採用的結論。自動測試能防止已審核座標與 URL 不一致，不能取代實地測量。

## 宮古島旅行版的第二層審核

`audits/index.json` 依序列出調查批次，同一批不得重複認領景點；新批次可取代舊結論，舊紀錄不刪除。
`miyako-trip-2026-09-23` 同時保留 Google Maps 驗證方式與故事逐項來源。
`named_listing` 是實際開啟具名 Google 地標；`official_embedded_pin` 是官方具名頁面所附的 Google 圖釘；
`unavailable` 必須說明缺口。自行拼出的座標連結、不具名的地圖中心，以及搜尋第一筆都不能冒充地標驗證。

新資料包以 `reviewBatch` 啟用嚴格的逐筆檢查。完成事實核對後才執行
`python tools/seal_review.py --region jp/miyako-jima`，保存完整來源及調查紀錄兩份 SHA-256 審核快照。
其後改座標、故事、來源或媒體都會使建置失敗，必須重新審核，不可只重算 hash 當作驗證。
`mediaPolicy: referenced-only` 使撤下的錯配照片也不再進入新版 ZIP；舊來源檔案留在版本歷史中，不拿別處照片補空。
新增景點暫無可靠授權圖片時明確保留空 media，而非虛構照片、授權或把區域示意照當現場照。

官方座標也可能是自然地標中心，不一定適合現場觸發。若公共展望台、岸邊入口與整體地標相距超過觸發範圍，
必須再確認實際到訪位置或暫停定位，不可只用一句「不是入口」掩蓋已知抵達差異。
Google 候選連結經人工選定後，仍須真正開啟該具名頁才能記成 `named_listing`；搜尋清單與實際開啟證據分開留存。
