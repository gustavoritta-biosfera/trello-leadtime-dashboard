import os
import json
from datetime import datetime, timedelta, date
import requests

TRELLO_KEY = os.environ["TRELLO_KEY"]
TRELLO_TOKEN = os.environ["TRELLO_TOKEN"]

BOARDS = [
    {"key": "3di-biogas", "name": "3DI Biogás", "board_id": "68346ca8e57293070560e8f2", "lists": {
        "Backlog": "68346ca8e57293070560e8e8", "Criação de Briefing": "68346ca8e57293070560e8e9",
        "Aguardando Material": "68346ca8e57293070560e8ea", "Liberado Produção": "6a0ca010ad9cbd3c31e63713",
        "Andamento Texto": "695cfb590da0e9598b0ba279", "Andamento Ritta": "695cf71ee2b0a711a3be4eff",
        "Andamento Castro": "68346ca8e57293070560e8eb", "Revisão Interna": "68346ca8e57293070560e8ec",
        "Ajuste Interno": "695cfbde5b57ba6ec4318fba", "Aprovação Cliente": "68346ca8e57293070560e8ed",
        "Ajuste Cliente": "695cfc3bc04de6a75aecc420", "Aprovado/Publicação": "68346ca8e57293070560e8ee",
        "Agendado": "698c84bbd1a8ffa95e86d0b7", "Finalizado": "68346ca8e57293070560e8f0",
        "Cancelado": "68346ca8e57293070560e8ef"}},
    {"key": "planet-biogas-brasil", "name": "PlanET Biogás Brasil", "board_id": "682f73f89fa4becf55379eab", "lists": {
        "Backlog": "682f73f89fa4becf55379ea1", "Criação de Briefing": "682f73f89fa4becf55379ea2",
        "Aguardando Material": "682f73f89fa4becf55379ea3", "Liberado Produção": "6a19f7fd7c243271fcfef69a",
        "Andamento Texto": "682f73f89fa4becf55379ea4", "Andamento Ritta": "695cfedb6a27b43127581928",
        "Andamento Castro": "695cfee52d63f9c832723903", "Revisão Interna": "682f73f89fa4becf55379ea5",
        "Ajuste Interno": "695cfef4b9d63c7f3fa8945c", "Aprovação Cliente": "682f73f89fa4becf55379ea6",
        "Ajuste Cliente": "695cff0158d9408bc6ed81cb", "Aprovado/Publicação": "682f73f89fa4becf55379ea7",
        "Agendado": "698c847f08c847b01c5ca97b", "Finalizado": "682f73f89fa4becf55379ea9",
        "Cancelado": "682f73f89fa4becf55379eaa"}},
    {"key": "oxido-ferro-rio-acima", "name": "Óxido de Ferro Rio Acima", "board_id": "69c5142b1fb9acdd7fdccc72", "lists": {
        "Backlog": "69c5142b1fb9acdd7fdccc64", "Criação de Briefing": "69c5142b1fb9acdd7fdccc65",
        "Aguardando Material": "69c5142b1fb9acdd7fdccc66", "Liberado Produção": "6a06358a5d3194d3b8f5de4a",
        "Andamento Texto": "69c5142b1fb9acdd7fdccc67", "Andamento Ritta": "69c5142b1fb9acdd7fdccc6e",
        "Andamento Castro": "69c5142b1fb9acdd7fdccc6f", "Revisão Interna": "69c5142b1fb9acdd7fdccc68",
        "Ajuste Interno": "69c5142b1fb9acdd7fdccc6d", "Aprovação Cliente": "69c5142b1fb9acdd7fdccc69",
        "Ajuste Cliente": "69c5142b1fb9acdd7fdccc70", "Aprovado/Publicação": "69c5142b1fb9acdd7fdccc6a",
        "Agendado": "69c5142b1fb9acdd7fdccc71", "Finalizado": "69c5142b1fb9acdd7fdccc6b",
        "Cancelado": "69c5142b1fb9acdd7fdccc6c"}},
    {"key": "grupo-regera", "name": "Grupo Regera", "board_id": "6878c7522ab33234a7b4c2be", "lists": {
        "Backlog": "6878c7522ab33234a7b4c2b3", "Criação de Briefing": "6878c7522ab33234a7b4c2b4",
        "Aguardando Material": "6878c7522ab33234a7b4c2b5", "Liberado Produção": "6878c7522ab33234a7b4c2b6",
        "Andamento Texto": "695cfcb9cd400388d4e0c654", "Andamento Ritta": "695cf753c6cab81a64857a5f",
        "Andamento Castro": "68b6e729ccee0f2d283931b3", "Revisão Interna": "6878c7522ab33234a7b4c2b7",
        "Ajuste Interno": "695cfe35bb34691e2403dac6", "Aprovação Cliente": "6878c7522ab33234a7b4c2b8",
        "Ajuste Cliente": "695cfe8240b332f29004025b", "Aprovado/Publicação": "6878c7522ab33234a7b4c2b9",
        "Agendado": "698c8615e1bfed6f11f0c799", "Finalizado": "6878c7522ab33234a7b4c2bb",
        "Cancelado": "6878c7522ab33234a7b4c2bc"}},
    {"key": "plataforma-melhore", "name": "Plataforma Melhore", "board_id": "683f001d41c5cbc07b001cbc", "lists": {
        "Backlog": "683f00249c00c33a4d32e04d", "Criação de Briefing": "683f002b7a7261293b251eb4",
        "Aguardando Material": "6876a44982d69d3e580eef52", "Liberado Produção": "69f3b606dbd496a99115318a",
        "Andamento Texto": "683f00351c4fb7ec4a925c94", "Andamento Ritta": "695cfaf43b7ef7fda7da6c41",
        "Andamento Castro": "695cfac015817367865f41cc", "Revisão Interna": "683f003d2663d1eeece0c43d",
        "Ajuste Interno": "695d01e8c9bfaf9fd3586c26", "Aprovação Cliente": "683f005060c7401f24604a0c",
        "Ajuste Cliente": "683f0048925c2cebd88aa752", "Aprovado/Publicação": "683f00585c034b296523da5e",
        "Agendado": "698c867ec0c9f514df91c13c", "Finalizado": "683f005d6c8f33c8b96b7042",
        "Cancelado": "683f007999147c9184607c3a"}},
    {"key": "lean-4-0", "name": "Lean 4.0", "board_id": "6835d858dbf081a37dfa40b2", "lists": {
        "Backlog": "6835d858dbf081a37dfa40a8", "Criação de Briefing": "6835d858dbf081a37dfa40a9",
        "Aguardando Material": "6835d858dbf081a37dfa40aa", "Liberado Produção": "69f8dd4700147b9cde3713f4",
        "Andamento Texto": "695d0014fd9833be71193843", "Andamento Ritta": "6835d858dbf081a37dfa40ab",
        "Andamento Castro": "695cfffe60d09dcb05cb7f27", "Revisão Interna": "6835d858dbf081a37dfa40ac",
        "Ajuste Interno": "695d002dc042a4edae209268", "Aprovação Cliente": "6835d858dbf081a37dfa40ad",
        "Ajuste Cliente": "695d003cddafe9e309715aa7", "Aprovado/Publicação": "6835d858dbf081a37dfa40ae",
        "Agendado": "698c8634666a05c1ab6c4d83", "Finalizado": "6835d858dbf081a37dfa40b0",
        "Cancelado": "6835d858dbf081a37dfa40b1"}},
    {"key": "clean-energy-br", "name": "Clean Energy BR", "board_id": "6839f074d63af77e8ad12f57", "lists": {
        "Backlog": "6839f074d63af77e8ad12fa2", "Criação de Briefing": "6839f074d63af77e8ad12fa3",
        "Aguardando Material": "6839f074d63af77e8ad12fa4", "Liberado Produção": "6a0b5627fa8e967826830490",
        "Andamento Texto": "68780b90bb9fd58e1f400d59", "Andamento Ritta": "6839f0b1c9572237081dc65f",
        "Andamento Castro": "695cff7ddbb753e2b4b41ee8", "Revisão Interna": "6839f0b3dc6ebe842b73f372",
        "Ajuste Interno": "695cff9d2f25ea7413ee5320", "Aprovação Cliente": "6839f0c446a723f27e44b14e",
        "Ajuste Cliente": "695cffb3ed8f9099f69a2d09", "Aprovado/Publicação": "6839f0d0aeb2f77b4a903b38",
        "Agendado": "698c84ab095360c1b0c30e1e", "Finalizado": "6839f0e360006db401074d77",
        "Cancelado": "6839f0e8533dc3eb256537ce"}},
]

STAGE_GROUPS = {
    "Backlog": "todo", "Criação de Briefing": "todo", "Aguardando Material": "todo",
    "Liberado Produção": "wip", "Andamento Texto": "wip", "Andamento Ritta": "wip",
    "Andamento Castro": "wip", "Revisão Interna": "wip", "Ajuste Interno": "wip",
    "Aprovação Cliente": "wip", "Ajuste Cliente": "wip", "Agendado": "wip",
    "Aprovado/Publicação": "done", "Finalizado": "done", "Cancelado": "cancelled",
}

REVISAO_NAMES = {"Revisão Interna", "Ajuste Interno"}
CLIENTE_NAMES = {"Aprovação Cliente", "Ajuste Cliente"}
EXIT_NAMES = {"Aprovado/Publicação", "Agendado", "Finalizado"}

EXCLUDE_CARD_IDS = {"6a32adc6a82a7a69ed99e338"}

BASE = "https://api.trello.com/1"
BRT_OFFSET = timedelta(hours=-3)


def trello_get(path, **params):
    params["key"] = TRELLO_KEY
    params["token"] = TRELLO_TOKEN
    r = requests.get(BASE + path, params=params, timeout=30)
    r.raise_for_status()
    return r.json()


def trello_get_all_actions(board_id, max_pages=8):
    all_actions = []
    before = None
    for _ in range(max_pages):
        params = {"filter": "updateCard:idList", "limit": "1000", "fields": "data,date"}
        if before:
            params["before"] = before
        batch = trello_get(f"/boards/{board_id}/actions", **params)
        if not batch:
            break
        all_actions.extend(batch)
        if len(batch) < 1000:
            break
        before = min(a["date"] for a in batch)
    return all_actions


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


def fmt_days(n):
    if float(n).is_integer():
        return str(int(n))
    return f"{n:.1f}".replace(".", ",")


def detect_approval_cycles(board, actions, period_start, today):
    name_to_id = board["lists"]
    id_to_name = {v: k for k, v in name_to_id.items()}
    REVISAO_IDS = {name_to_id[n] for n in REVISAO_NAMES}
    CLIENTE_IDS = {name_to_id[n] for n in CLIENTE_NAMES}
    APPROVAL_IDS = REVISAO_IDS | CLIENTE_IDS
    EXIT_IDS = {name_to_id[n] for n in EXIT_NAMES}

    by_card = {}
    for a in actions:
        d = a.get("data", {})
        before, after, card = d.get("listBefore"), d.get("listAfter"), d.get("card")
        if not before or not after or not card or card["id"] in EXCLUDE_CARD_IDS:
            continue
        by_card.setdefault(card["id"], []).append({
            "t": to_brt(a["date"]), "before": before["id"], "after": after["id"], "name": card.get("name", "")
        })

    completed, waiting = [], []
    for cid, moves in by_card.items():
        moves.sort(key=lambda m: m["t"])
        in_block_since = None
        pend_start = pend_list = None
        segments = []
        last_cycle = None
        card_name = moves[-1]["name"]
        for m in moves:
            b, a, t = m["before"], m["after"], m["t"]
            if b not in APPROVAL_IDS and a in APPROVAL_IDS:
                in_block_since, segments = t, []
                pend_start, pend_list = t, a
            elif b in APPROVAL_IDS and a in APPROVAL_IDS:
                if in_block_since is not None:
                    segments.append((pend_start, t, pend_list))
                    pend_start, pend_list = t, a
            elif b in APPROVAL_IDS and a in EXIT_IDS:
                if in_block_since is not None:
                    segments.append((pend_start, t, pend_list))
                    last_cycle = {"name": card_name, "start": in_block_since, "end": t,
                                  "segments": list(segments), "exit_id": a}
                in_block_since, segments = None, []
            elif b in APPROVAL_IDS and a not in APPROVAL_IDS and a not in EXIT_IDS:
                in_block_since, segments = None, []

        if last_cycle and period_start <= last_cycle["end"].date() <= today:
            c = last_cycle
            rev_bd = cli_bd = rev_cd = cli_cd = 0
            for seg_start, seg_end, seg_list in c["segments"]:
                sd, ed = seg_start.date(), seg_end.date()
                bd, cd = business_days_between(sd, ed), (ed - sd).days
                if seg_list in REVISAO_IDS:
                    rev_bd += bd; rev_cd += cd
                else:
                    cli_bd += bd; cli_cd += cd
            sd, ed = c["start"].date(), c["end"].date()
            completed.append({
                "name": c["name"], "started": sd.isoformat(), "finished": ed.isoformat(),
                "exit_stage": id_to_name.get(c["exit_id"], "?"),
                "rev_bd": rev_bd, "cli_bd": cli_bd, "total_bd": business_days_between(sd, ed),
                "rev_cd": rev_cd, "cli_cd": cli_cd, "total_cd": (ed - sd).days,
            })

        if in_block_since is not None:
            segs_open = list(segments) + [(pend_start, None, pend_list)]
            rev_bd = cli_bd = rev_cd = cli_cd = 0
            for seg_start, seg_end, seg_list in segs_open:
                sd = seg_start.date()
                ed = seg_end.date() if seg_end else today
                bd, cd = business_days_between(sd, ed), (ed - sd).days
                if seg_list in REVISAO_IDS:
                    rev_bd += bd; rev_cd += cd
                else:
                    cli_bd += bd; cli_cd += cd
            sd = in_block_since.date()
            waiting.append({
                "name": card_name, "since": sd.isoformat(),
                "rev_bd": rev_bd, "cli_bd": cli_bd, "total_bd": business_days_between(sd, today),
                "rev_cd": rev_cd, "cli_cd": cli_cd, "total_cd": (today - sd).days,
            })

    completed.sort(key=lambda c: c["finished"])
    waiting.sort(key=lambda c: -c["total_bd"])

    bd_vals = sorted(c["total_bd"] for c in completed)
    rev_vals = sorted(c["rev_bd"] for c in completed)
    cli_vals = sorted(c["cli_bd"] for c in completed)
    n = len(completed)
    fence_bd = iqr_upper_fence(bd_vals)

    return {
        "completed": completed,
        "waiting": waiting,
        "stats": {
            "count": n,
            "median_total_bd": median(bd_vals), "median_total_bd_display": fmt_days(median(bd_vals)),
            "median_rev_bd": median(rev_vals), "median_rev_bd_display": fmt_days(median(rev_vals)),
            "median_cli_bd": median(cli_vals), "median_cli_bd_display": fmt_days(median(cli_vals)),
            "fence_bd": fence_bd if fence_bd != float("inf") else 999999,
            "waiting_count": len(waiting),
        },
    }


def build_dataset(board):
    today = date.today()
    period_start = date(today.year, 1, 1)
    since_iso = f"{period_start.isoformat()}T00:00:00.000Z"
    before_iso = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")
    board_id = board["board_id"]
    name_to_id = board["lists"]

    TODO_LISTS = {name_to_id[n] for n, g in STAGE_GROUPS.items() if g == "todo"}
    WIP_LISTS = {name_to_id[n] for n, g in STAGE_GROUPS.items() if g == "wip"}
    DONE_LISTS = {name_to_id[n] for n, g in STAGE_GROUPS.items() if g == "done"}

    cards = trello_get(f"/boards/{board_id}/cards", filter="open", fields="id,name,idList,closed")
    actions = trello_get(f"/boards/{board_id}/actions", filter="updateCard:idList",
                          since=since_iso, before=before_iso, limit=1000, fields="data,date")

    by_card = {}
    for a in actions:
        cid = a["data"]["card"]["id"]
        if cid in EXCLUDE_CARD_IDS:
            continue
        dt = to_brt(a["date"])
        list_after = a["data"].get("listAfter")
        if not list_after:
            continue
        if cid not in by_card or dt > by_card[cid]["dt"]:
            by_card[cid] = {"dt": dt, "name": a["data"]["card"]["name"], "listAfter_id": list_after["id"]}

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
            f"sem {'eles' if plural else 'ele'}, a média do período cai de {fmt_days(avg_bd)} "
            f"para cerca de {fmt_days(avg_wo_outliers)} dias úteis."
        )
    else:
        note = "Cartões ordenados do menor para o maior lead time. A linha vertical marca a mediana."

    all_actions = trello_get_all_actions(board_id)
    approval = detect_approval_cycles(board, all_actions, period_start, today)

    return {
        "name": board["name"],
        "period_start": period_start.isoformat(),
        "period_end": today.isoformat(),
        "completed": completed,
        "afazer": afazer,
        "stats": {
            "count": n,
            "median_bd": median_bd, "median_bd_display": fmt_days(median_bd),
            "median_cd": median_cd,
            "avg_bd": avg_bd, "avg_bd_display": fmt_days(avg_bd),
            "bd_min": bd_min, "bd_max": bd_max,
            "fence_bd": fence_bd if fence_bd != float("inf") else 999999,
            "fence_cd": fence_cd if fence_cd != float("inf") else 999999,
            "todo_count": len(afazer), "wip_count": wip_count, "done_total": done_total,
            "wip_stage_count": len(WIP_LISTS),
        },
        "note": note,
        "approval": approval,
    }


def render_html(all_data, board_order, generated_at_str):
    tpl = open("template.html", encoding="utf-8").read()
    all_data_json = json.dumps(all_data, ensure_ascii=False).replace("</script", "<\\/script")
    board_order_json = json.dumps(board_order, ensure_ascii=False)
    options_html = "".join(
        f'<option value="{k}">{all_data[k]["name"]}</option>' for k in board_order
    )
    repl = {
        "__GENERATED_AT__": generated_at_str,
        "__ALL_BOARDS_JSON__": all_data_json,
        "__BOARD_ORDER_JSON__": board_order_json,
        "__BOARD_OPTIONS_HTML__": options_html,
    }
    for k, v in repl.items():
        tpl = tpl.replace(k, v)
    return tpl


if __name__ == "__main__":
    all_data = {}
    board_order = [b["key"] for b in BOARDS]
    for board in BOARDS:
        all_data[board["key"]] = build_dataset(board)

    generated_at_str = (datetime.utcnow() + BRT_OFFSET).strftime("%d/%m/%Y %H:%M")
    html = render_html(all_data, board_order, generated_at_str)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

    for k in board_order:
        s = all_data[k]["stats"]
        ap = all_data[k]["approval"]["stats"]
        print(f"OK [{all_data[k]['name']}]: {s['count']} cartoes concluidos, mediana {s['median_bd_display']} dias uteis | "
              f"aprovacao: {ap['count']} ciclos, mediana total {ap['median_total_bd_display']} dias uteis")
