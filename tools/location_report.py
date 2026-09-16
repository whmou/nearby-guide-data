"""Print review status and measured correction distances from current sources."""
from collections import Counter, defaultdict
from pathlib import Path
import yaml
from location_contract import distance_m

ROOT = Path(__file__).resolve().parents[1]


def report():
    totals = defaultdict(Counter)
    shifts, unresolved = [], []
    for path in sorted((ROOT / "regions").glob("*/*/points/*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8-sig"))
        p, review = data["point"], data["locationReview"]
        totals[path.parent.parent.name][review["status"]] += 1
        if review["status"] == "verified" and review.get("previousLocation"):
            shifts.append((distance_m(review["previousLocation"], p["location"]), p["id"]))
        elif review["status"] == "unresolved":
            unresolved.append(p["id"])
    lines = ["# 2026-09-16 逐點定位查核", "", "查核採公開來源，不是現場 GPS 測量。verified 包含地標／遊憩區代表 pin，不保證精確入口。", "",
        "| 資料包 | 可定位 | 待查、停用定位 | 非定點主題 |", "|---|---:|---:|---:|"]
    for pack, counts in sorted(totals.items()):
        lines.append(f"| {pack} | {counts['verified']} | {counts['unresolved']} | {counts['non_point']} |")
    lines += ["", f"採用位置與原位置距離超過 200 公尺：{sum(d > 200 for d, _ in shifts)} 筆。未放大觸發半徑掩蓋誤差。", "", "## 最大的定位變更", "", "| ID | 原位置至新錨點距離（公尺） |", "|---|---:|"]
    lines += [f"| {pid} | {distance:.0f} |" for distance, pid in sorted(shifts, reverse=True)[:20]]
    lines += ["", "距離亦可能反映從海域／園區中心改到具名抵達位置，並非全都代表測量誤差。", "", "## 仍待補證", ""]
    lines += [f"- `{pid}`" for pid in unresolved]
    lines += ["", "以上保留文字但不發送 GPS、trigger、Google Maps 導航連結。詳見同目錄逐筆 JSON 與來源 YAML 的 locationReview。", "", "本次不宣稱舊文案、評分與圖片都已查證；已發現的部分方向與安全錯誤另行修正。"]
    return "\n".join(lines)


if __name__ == "__main__":
    print(report())
