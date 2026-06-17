import os
import json
from datetime import datetime, timedelta, date
import requests

TRELLO_KEY = os.environ["TRELLO_KEY"]
TRELLO_TOKEN = os.environ["TRELLO_TOKEN"]
BOARD_ID = "68346ca8e57293070560e8f2"

TODO_LISTS = {"68346ca8e57293070560e8e8", "68346ca8e57293070560e8ea", "68346ca8e57293070560e8e9"}
WIP_LISTS = {"6a0ca010ad9cbd3c31e63713", "695cfb590da0e9598b0ba279", "695cf71ee2b0a711a3be4eff",
             "68346ca8e57293070560e8eb", "68346ca8e57293070560e8ec", "695cfbde5b57ba6ec4318fba",
             "68346ca8e57293070560e8ed", "695cfc3bc04de6a75aecc420", "698c84bbd1a8ffa95e86d0b7"}
DONE_LISTS = {"68346ca8e57293070560e8ee", "68346ca8e57293070560e8f0"}
EXCLUDE_CARD_IDS = {"6a32adc6a82a7a69ed99e338"}

BASE = "https://api.trello.com/1"
BRT_OFFSET = timedelta(hours=-3)


def trello_get(path, **params):
    params["key"] = TRELLO_KEY
    params["token"] = TRELLO_TOKEN
    r = requests.get(BASE + path, params=params, timeout=30)
    r.raise_for_status()
    return r.json()


def to_brt(iso_str):
    dt = datetime.strptime(iso_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    return dt + BRT_OFFSET


def created_date_brt(card_id):
    ts = int(card_id[:8], 16)
    return datetime.utcfromtimestamp(ts) + BRT_OFFSET


def business_days_between(start_date, end_date):
    if start_date >= end_date:
        return 0
    days, cur = 0, start_date
    while cur < end_date:
        if cur.weekday() < 5:
            days += 1
        cur += timedelta(days=1)
    return days


def median(values):
    s = sorted(values)
    n = len(s)
    if n == 0:
        return 0
    mid = n // 2
    return s[mid] if n % 2 == 1 else (s[mid - 1] + s[mid]) / 2


def quantile(sorted_vals, q):
    n = len(sorted_vals)
    if n == 0:
        return 0
    if n == 1:
        return sorted_vals[0]
    pos = q * (n - 1)
    lo = int(pos)
    hi = min(lo + 1, n - 1)
    frac = pos - lo
    return sorted_vals[lo] + (sorted_vals[hi] - sorted_vals[lo]) * frac


def iqr_upper_fence(sorted_vals):
    if len(sorted_vals) < 4:
        return float("inf")
    q1, q3 = quantile(sorted_vals, 0.25), quantile(sorted_vals, 0.75)
    return q3 + 1.5 * (q3 - q1)


def fmt_pt(n):
    return f"{n:.1f}".replace(".", ",")


def build_dataset():
    today = date.today()
    period_start = date(today.year, 1, 1)
    since_iso = f"{period_start.isoformat()}T00:00:00.000Z"
    before_iso = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")

    cards = trello_get(f"/boards/{BOARD_ID}/cards", filter="open", fields="id,name,idList,closed")
    actions = trello_get(f"/boards/{BOARD_ID}/actions", filter="updateCard:idList",
                          since=since_iso, before=before_iso, limit=1000, fields="data,date")

    by_card = {}
    for a in actions:
        cid = a["data"]["card"]["id"]
        if cid in EXCLUDE_CARD_IDS:
            continue
        dt = to_brt(a["date"])
        if cid not in by_card or dt > by_card[cid]["dt"]:
            by_card[cid] = {"dt": dt, "name": a["data"]["card"]["name"],
                             "listAfter_id": a["data"]["listAfter"]["id"]}

    completed = []
    for cid, info in by_card.items():
        if info["listAfter_id"] in DONE_LISTS:
            created = created_date_brt(cid)
            comp_dt = info["dt"]
            completed.append({
                "id": cid, "name": info["name"],
                "created": created.date().isoformat(),
                "completed": comp_dt.date().isoformat(),
                "calendar_days": (comp_dt.date() - created.date()).days,
                "business_days": business_days_between(created.date(), comp_dt.date()),
            })
    completed.sort(key=lambda c: c["completed"])

    afazer = []
    for c in cards:
        if c["id"] in EXCLUDE_CARD_IDS:
            continue
        if c["idList"] in TODO_LISTS:
            created = created_date_brt(c["id"]).date()
            afazer.append({
                "id": c["id"], "name": c["name"], "created": created.isoformat(),
                "business_days_waiting": business_days_between(created, today),
                "calendar_days_waiting": (today - created).days,
            })
    afazer.sort(key=lambda c: -c["business_days_waiting"])

    wip_count = sum(1 for c in cards if c["idList"] in WIP_LISTS)
    done_total = sum(1 for c in cards if c["idList"] in DONE_LISTS)

    bd_vals = sorted(c["business_days"] for c in completed)
    cd_vals = sorted(c["calendar_days"] for c in completed)
    n = len(completed)

    median_bd = median(bd_vals)
    median_cd = median(cd_vals)
    avg_bd = round(sum(bd_vals) / n, 1) if n else 0
    bd_min, bd_max = (min(bd_vals), max(bd_vals)) if n else (0, 0)

    fence_bd = iqr_upper_fence(bd_vals)
    fence_cd = iqr_upper_fence(cd_vals)
    outliers = [c for c in completed if c["business_days"] > fence_bd]
    rest = [c for c in completed if c not in outliers]
    avg_wo_outliers = round(sum(c["business_days"] for c in rest) / len(rest), 1) if rest else avg_bd

    if outliers:
        plural = len(outliers) > 1
        note = (
            f"Cartões ordenados do menor para o maior lead time. A linha vertical marca a mediana. "
            f"{len(outliers)} {'cartões' if plural else 'cartão'} "
            f"{'destacados' if plural else 'destacado'} em vermelho "
            f"{'estão' if plural else 'está'} fora da curva; "
            f"sem {'eles' if plural else 'ele'}, a média do período cai de {fmt_pt(avg_bd)} "
            f"para cerca de {fmt_pt(avg_wo_outliers)} dias úteis."
        )
    else:
        note = "Cartões ordenados do menor para o maior lead time. A linha vertical marca a mediana."

    return {
        "generated_at": datetime.utcnow().isoformat(),
        "period_start": period_start.isoformat(),
        "period_end": today.isoformat(),
        "completed": completed,
        "afazer": afazer,
        "stats": {
            "count": n, "median_bd": median_bd, "median_cd": median_cd,
            "avg_bd": avg_bd, "bd_min": bd_min, "bd_max": bd_max,
            "fence_bd": fence_bd if fence_bd != float("inf") else 999999,
            "fence_cd": fence_cd if fence_cd != float("inf") else 999999,
            "todo_count": len(afazer), "wip_count": wip_count, "done_total": done_total,
        },
        "note": note,
    }


def render_html(d):
    s = d["stats"]
    tpl = open("template.html", encoding="utf-8").read()
    repl = {
        "__PERIOD_START__": datetime.fromisoformat(d["period_start"]).strftime("%d %b %Y").lower(),
        "__PERIOD_END__": datetime.fromisoformat(d["period_end"]).strftime("%d %b %Y").lower(),
        "__GENERATED_AT__": (datetime.utcnow() + BRT_OFFSET).strftime("%d/%m/%Y %H:%M"),
        "__TODO_COUNT__": str(s["todo_count"]),
        "__WIP_COUNT__": str(s["wip_count"]),
        "__DONE_PERIOD_COUNT__": str(s["count"]),
        "__DONE_TOTAL_COUNT__": str(s["done_total"]),
        "__STAT_COUNT__": str(s["count"]),
        "__STAT_MEDIAN__": str(s["median_bd"]),
        "__STAT_AVG__": fmt_pt(s["avg_bd"]),
        "__STAT_MINMAX__": f"{s['bd_min']}–{s['bd_max']}",
        "__SECTION_NOTE__": d["note"],
        "__COMPLETED_JSON__": json.dumps(d["completed"], ensure_ascii=False),
        "__AFAZER_JSON__": json.dumps(d["afazer"], ensure_ascii=False),
        "__MEDIAN_VALUES_JSON__": json.dumps({"business_days": s["median_bd"], "calendar_days": s["median_cd"]}),
        "__OUTLIER_THRESHOLDS_JSON__": json.dumps({"business_days": s["fence_bd"], "calendar_days": s["fence_cd"]}),
    }
    for k, v in repl.items():
        tpl = tpl.replace(k, v)
    return tpl


if __name__ == "__main__":
    dataset = build_dataset()
    html = render_html(dataset)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print(f"OK: {dataset['stats']['count']} cartoes concluidos, mediana {dataset['stats']['median_bd']} dias uteis")
