import os
import json
import bisect
import calendar
from datetime import datetime, timedelta, date
from collections import defaultdict
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

    {"key": "smarty", "name": "Smarty", "board_id": "6a39972b6afe4853707ad1ba", "lists": {
        "Backlog": "6a39972b6afe4853707ad1ab", "Criação de Briefing": "6a39972b6afe4853707ad1ac",
        "Aguardando Material": "6a39972b6afe4853707ad1ad", "Liberado Produção": "6a39972b6afe4853707ad1b9",
        "Andamento Texto": "6a39972b6afe4853707ad1ae", "Andamento Ritta": "6a39972b6afe4853707ad1b5",
        "Andamento Castro": "6a39972b6afe4853707ad1b6", "Revisão Interna": "6a39972b6afe4853707ad1af",
        "Ajuste Interno": "6a39972b6afe4853707ad1b4", "Aprovação Cliente": "6a39972b6afe4853707ad1b0",
        "Ajuste Cliente": "6a39972b6afe4853707ad1b7", "Aprovado/Publicação": "6a39972b6afe4853707ad1b1",
        "Agendado": "6a39972b6afe4853707ad1b8", "Finalizado": "6a39972b6afe4853707ad1b2",
        "Cancelado": "6a39972b6afe4853707ad1b3"}},
]

REVISAO_NAMES = {"Revisão Interna", "Ajuste Interno"}
CLIENTE_NAMES = {"Aprovação Cliente", "Ajuste Cliente"}
EXIT_NAMES = {"Aprovado/Publicação", "Agendado", "Finalizado"}

MACRO_ORDER = ["Backlog", "Produção", "Aprovação", "Agendado", "Finalizado"]
MACRO_STAGE_NAMES = {
    "Backlog": ["Backlog", "Criação de Briefing", "Aguardando Material"],
    "Produção": ["Liberado Produção", "Andamento Texto", "Andamento Ritta", "Andamento Castro"],
    "Aprovação": ["Revisão Interna", "Ajuste Interno", "Aprovação Cliente", "Ajuste Cliente"],
    "Agendado": ["Agendado"],
    "Finalizado": ["Aprovado/Publicação", "Finalizado"],
}

PERIOD_DEFS = [
    ("1m", "Último mês", 1),
    ("3m", "Últimos 3 meses", 3),
    ("6m", "Últimos 6 meses", 6),
    ("9m", "Últimos 9 meses", 9),
    ("12m", "Últimos 12 meses", 12),
]

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
        params = {"filter": "createCard,updateCard:idList", "limit": "1000", "fields": "data,date,type"}
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


def months_ago(d, n):
    month = d.month - n
    year = d.year + (month - 1) // 12
    month = (month - 1) % 12 + 1
    day = min(d.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


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


def extract_list(d, key):
    if d is None:
        return []
    if isinstance(d, list):
        return d
    if isinstance(d, dict):
        return d.get(key, d.get("data", []))
    return []


def build_lead_time_all(board, actions, current_cards):
    name_to_id = board["lists"]
    DONE_LISTS = {name_to_id["Aprovado/Publicação"], name_to_id["Agendado"], name_to_id["Finalizado"]}
    TODO_LISTS = {name_to_id["Backlog"], name_to_id["Criação de Briefing"], name_to_id["Aguardando Material"], name_to_id["Liberado Produção"]}

    creates_first = {}
    by_card = {}
    for a in actions:
        d = a.get("data", {})
        card = d.get("card")
        if not card or card["id"] in EXCLUDE_CARD_IDS:
            continue
        cid = card["id"]
        if a.get("type") == "createCard" and d.get("list"):
            t = to_brt(a["date"])
            if cid not in creates_first or t < creates_first[cid]:
                creates_first[cid] = t
        elif a.get("type") == "updateCard" and d.get("listAfter"):
            t = to_brt(a["date"])
            if cid not in by_card or t > by_card[cid]["dt"]:
                by_card[cid] = {"dt": t, "name": card.get("name", ""), "listAfter_id": d["listAfter"]["id"]}

    def creation_dt(cid):
        return creates_first.get(cid) or created_date_brt(cid)

    completed_all = []
    for cid, info in by_card.items():
        if info["listAfter_id"] in DONE_LISTS:
            created = creation_dt(cid)
            comp_dt = info["dt"]
            completed_all.append({
                "id": cid, "name": info["name"],
                "created": created.date().isoformat(), "completed": comp_dt.date().isoformat(),
                "calendar_days": (comp_dt.date() - created.date()).days,
                "business_days": business_days_between(created.date(), comp_dt.date()),
            })

    afazer = []
    today = date.today()
    for c in current_cards:
        if c["id"] in EXCLUDE_CARD_IDS:
            continue
        if c["idList"] in TODO_LISTS:
            created = creation_dt(c["id"]).date()
            afazer.append({
                "id": c["id"], "name": c["name"], "created": created.isoformat(),
                "business_days_waiting": business_days_between(created, today),
                "calendar_days_waiting": (today - created).days,
            })
    afazer.sort(key=lambda c: -c["business_days_waiting"])
    return completed_all, afazer


def lead_time_stats_for_period(completed_all, period_start, period_end):
    completed = [c for c in completed_all if period_start <= date.fromisoformat(c["completed"]) <= period_end]
    completed.sort(key=lambda c: c["completed"])
    bd_vals = sorted(c["business_days"] for c in completed)
    cd_vals = sorted(c["calendar_days"] for c in completed)
    n = len(completed)
    median_bd, median_cd = median(bd_vals), median(cd_vals)
    avg_bd = round(sum(bd_vals) / n, 1) if n else 0
    bd_min, bd_max = (min(bd_vals), max(bd_vals)) if n else (0, 0)
    fence_bd, fence_cd = iqr_upper_fence(bd_vals), iqr_upper_fence(cd_vals)
    outliers = [c for c in completed if c["business_days"] > fence_bd]
    rest = [c for c in completed if c not in outliers]
    avg_wo = round(sum(c["business_days"] for c in rest) / len(rest), 1) if rest else avg_bd
    if outliers:
        plural = len(outliers) > 1
        note = (
            f"Cartões ordenados do menor para o maior lead time. A linha vertical marca a mediana. "
            f"{len(outliers)} {'cartões' if plural else 'cartão'} "
            f"{'destacados' if plural else 'destacado'} em vermelho "
            f"{'estão' if plural else 'está'} fora da curva; "
            f"sem {'eles' if plural else 'ele'}, a média do período cai de {fmt_days(avg_bd)} "
            f"para cerca de {fmt_days(avg_wo)} dias úteis."
        )
    else:
        note = "Cartões ordenados do menor para o maior lead time. A linha vertical marca a mediana."
    return {
        "completed": completed,
        "stats": {
            "count": n, "median_bd": median_bd, "median_bd_display": fmt_days(median_bd),
            "median_cd": median_cd, "avg_bd": avg_bd, "avg_bd_display": fmt_days(avg_bd),
            "bd_min": bd_min, "bd_max": bd_max,
            "fence_bd": fence_bd if fence_bd != float("inf") else 999999,
            "fence_cd": fence_cd if fence_cd != float("inf") else 999999,
        },
        "note": note,
    }


def build_approval_all(board, actions):
    name_to_id = board["lists"]
    id_to_name = {v: k for k, v in name_to_id.items()}
    REVISAO_IDS = {name_to_id[n] for n in REVISAO_NAMES}
    CLIENTE_IDS = {name_to_id[n] for n in CLIENTE_NAMES}
    APPROVAL_IDS = REVISAO_IDS | CLIENTE_IDS
    EXIT_IDS = {name_to_id[n] for n in EXIT_NAMES}

    by_card = defaultdict(list)
    for a in actions:
        d = a.get("data", {})
        if a.get("type") != "updateCard":
            continue
        before, after, card = d.get("listBefore"), d.get("listAfter"), d.get("card")
        if not before or not after or not card or card["id"] in EXCLUDE_CARD_IDS:
            continue
        by_card[card["id"]].append({"t": to_brt(a["date"]), "before": before["id"], "after": after["id"], "name": card.get("name", "")})

    completed_all, waiting = [], []
    for cid, moves in by_card.items():
        moves.sort(key=lambda m: m["t"])
        in_block_since = None
        pend_start = pend_list = None
        segments = []
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
                    rev_bd = cli_bd = rev_cd = cli_cd = 0
                    for ss, se, sl in segments:
                        sd, ed = ss.date(), se.date()
                        bd, cd = business_days_between(sd, ed), (ed - sd).days
                        if sl in REVISAO_IDS:
                            rev_bd += bd; rev_cd += cd
                        else:
                            cli_bd += bd; cli_cd += cd
                    sd, ed = in_block_since.date(), t.date()
                    completed_all.append({
                        "name": card_name, "started": sd.isoformat(), "finished": ed.isoformat(),
                        "exit_stage": id_to_name.get(a, "?"),
                        "rev_bd": rev_bd, "cli_bd": cli_bd, "total_bd": business_days_between(sd, ed),
                        "rev_cd": rev_cd, "cli_cd": cli_cd, "total_cd": (ed - sd).days,
                    })
                in_block_since, segments = None, []
            elif b in APPROVAL_IDS and a not in APPROVAL_IDS and a not in EXIT_IDS:
                in_block_since, segments = None, []
        if in_block_since is not None:
            segs_open = list(segments) + [(pend_start, None, pend_list)]
            rev_bd = cli_bd = rev_cd = cli_cd = 0
            today = date.today()
            for ss, se, sl in segs_open:
                sd = ss.date()
                ed = se.date() if se else today
                bd, cd = business_days_between(sd, ed), (ed - sd).days
                if sl in REVISAO_IDS:
                    rev_bd += bd; rev_cd += cd
                else:
                    cli_bd += bd; cli_cd += cd
            sd = in_block_since.date()
            waiting.append({
                "name": card_name, "since": sd.isoformat(),
                "rev_bd": rev_bd, "cli_bd": cli_bd, "total_bd": business_days_between(sd, today),
                "rev_cd": rev_cd, "cli_cd": cli_cd, "total_cd": (today - sd).days,
            })
    waiting.sort(key=lambda c: -c["total_bd"])
    return completed_all, waiting


def approval_stats_for_period(completed_all, period_start, period_end):
    completed = [c for c in completed_all if period_start <= date.fromisoformat(c["finished"]) <= period_end]
    completed.sort(key=lambda c: c["finished"])
    bd_vals = sorted(c["total_bd"] for c in completed)
    rev_vals = sorted(c["rev_bd"] for c in completed)
    cli_vals = sorted(c["cli_bd"] for c in completed)
    n = len(completed)
    fence_bd = iqr_upper_fence(bd_vals)
    return {
        "completed": completed,
        "stats": {
            "count": n,
            "median_total_bd": median(bd_vals), "median_total_bd_display": fmt_days(median(bd_vals)),
            "median_rev_bd": median(rev_vals), "median_rev_bd_display": fmt_days(median(rev_vals)),
            "median_cli_bd": median(cli_vals), "median_cli_bd_display": fmt_days(median(cli_vals)),
            "fence_bd": fence_bd if fence_bd != float("inf") else 999999,
        },
    }


def build_card_reached_dates(board, actions, current_cards):
    name_to_id = board["lists"]
    macro_of_list = {}
    for macro, names_ in MACRO_STAGE_NAMES.items():
        for n in names_:
            macro_of_list[name_to_id[n]] = macro
    cancelado_id = name_to_id["Cancelado"]

    current_list_by_card = {c["id"]: c["idList"] for c in current_cards}
    eligible_ids = {cid for cid, lid in current_list_by_card.items() if lid != cancelado_id and cid not in EXCLUDE_CARD_IDS}

    creates = defaultdict(list)
    moves = defaultdict(list)
    card_names = {}
    for a in actions:
        d = a.get("data", {})
        card = d.get("card")
        if not card or card["id"] in EXCLUDE_CARD_IDS:
            continue
        cid = card["id"]
        card_names[cid] = card.get("name", card_names.get(cid, ""))
        if a.get("type") == "createCard" and d.get("list"):
            creates[cid].append((to_brt(a["date"]), d["list"]["id"]))
        elif a.get("type") == "updateCard" and d.get("listAfter"):
            moves[cid].append((to_brt(a["date"]), d["listAfter"]["id"]))

    reached = {}
    for cid in eligible_ids:
        timeline = []
        if creates.get(cid):
            t0, l0 = min(creates[cid], key=lambda x: x[0])
            timeline.append((t0, l0))
        mv = sorted(moves.get(cid, []), key=lambda x: x[0])
        timeline.extend(mv)
        if not timeline:
            timeline = [(created_date_brt(cid), current_list_by_card[cid])]
        elif not creates.get(cid):
            t0 = created_date_brt(cid)
            l0 = mv[0][1] if mv else current_list_by_card[cid]
            timeline.insert(0, (t0, l0))

        direct = {}
        for t, lid in timeline:
            macro = macro_of_list.get(lid)
            if macro and macro not in direct:
                direct[macro] = t

        r = {}
        carry = None
        for macro in reversed(MACRO_ORDER):
            cand = direct.get(macro)
            if cand is not None and (carry is None or cand < carry):
                carry = cand
            if carry is not None:
                r[macro] = carry
        reached[cid] = {"name": card_names.get(cid, ""), "reached": r}
    return reached


def build_cfd_series(reached, period_start, period_end):
    # Abordagem por coorte: o CFD acompanha apenas os cartoes cuja chegada ao
    # Backlog (criacao) caiu dentro do periodo selecionado, e mostra o caminho
    # desses cartoes especificos pelas etapas. Isso faz os valores serem
    # proprios do periodo, em vez de um total acumulado desde sempre do board.
    cohort = {
        cid: v for cid, v in reached.items()
        if "Backlog" in v["reached"] and period_start <= v["reached"]["Backlog"].date() <= period_end
    }
    sorted_dates = {}
    for macro in MACRO_ORDER:
        ds = sorted(v["reached"][macro].date() for v in cohort.values() if macro in v["reached"])
        sorted_dates[macro] = ds
    n_days = (period_end - period_start).days + 1
    dates = [(period_start + timedelta(days=i)).isoformat() for i in range(n_days)]
    series = {}
    for macro in MACRO_ORDER:
        ds = sorted_dates[macro]
        series[macro] = [bisect.bisect_right(ds, period_start + timedelta(days=i)) for i in range(n_days)]
    return {"dates": dates, "series": series, "cohort_size": len(cohort)}


def build_dataset(board):
    today = date.today()
    board_id = board["board_id"]
    name_to_id = board["lists"]

    cards = trello_get(f"/boards/{board_id}/cards", filter="open", fields="id,name,idList,closed")
    actions = trello_get_all_actions(board_id)

    TODO_LISTS = {name_to_id["Backlog"], name_to_id["Criação de Briefing"], name_to_id["Aguardando Material"], name_to_id["Liberado Produção"]}
    WIP_NAMES = ["Andamento Texto", "Andamento Ritta", "Andamento Castro",
                 "Revisão Interna", "Ajuste Interno", "Aprovação Cliente", "Ajuste Cliente"]
    WIP_LISTS = {name_to_id[n] for n in WIP_NAMES}
    DONE_LISTS = {name_to_id["Aprovado/Publicação"], name_to_id["Agendado"], name_to_id["Finalizado"]}

    wip_count = sum(1 for c in cards if c["idList"] in WIP_LISTS)
    done_total = sum(1 for c in cards if c["idList"] in DONE_LISTS)

    lt_completed_all, afazer = build_lead_time_all(board, actions, cards)
    ap_completed_all, ap_waiting = build_approval_all(board, actions)
    reached = build_card_reached_dates(board, actions, cards)

    periods = {}
    for key, label, n_months in PERIOD_DEFS:
        period_start = months_ago(today, n_months)
        lt = lead_time_stats_for_period(lt_completed_all, period_start, today)
        ap = approval_stats_for_period(ap_completed_all, period_start, today)
        cfd = build_cfd_series(reached, period_start, today)
        periods[key] = {
            "label": label,
            "period_start": period_start.isoformat(), "period_end": today.isoformat(),
            "lead_time": lt, "approval": ap, "cfd": cfd,
        }

    return {
        "name": board["name"],
        "flow": {
            "todo_count": len(afazer), "wip_count": wip_count, "done_total": done_total,
            "wip_stage_count": len(WIP_LISTS),
        },
        "afazer": afazer,
        "approval_waiting": ap_waiting,
        "periods": periods,
    }


def render_html(all_data, board_order, generated_at_str):
    tpl = open("template.html", encoding="utf-8").read()
    all_data_json = json.dumps(all_data, ensure_ascii=False).replace("</script", "<\\/script")
    board_order_json = json.dumps(board_order, ensure_ascii=False)
    options_html = "".join(
        f'<option value="{k}">{all_data[k]["name"]}</option>' for k in board_order
    )
    period_options_html = "".join(
        f'<option value="{key}"{" selected" if key=="12m" else ""}>{label}</option>' for key, label, _ in PERIOD_DEFS
    )
    repl = {
        "__GENERATED_AT__": generated_at_str,
        "__ALL_BOARDS_JSON__": all_data_json,
        "__BOARD_ORDER_JSON__": board_order_json,
        "__BOARD_OPTIONS_HTML__": options_html,
        "__PERIOD_OPTIONS_HTML__": period_options_html,
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
        d = all_data[k]
        p12 = d["periods"]["12m"]
        print(f"OK [{d['name']}]: lead_time(12m)={p12['lead_time']['stats']['count']} "
              f"aprovacao(12m)={p12['approval']['stats']['count']} "
              f"cfd_dias={len(p12['cfd']['dates'])}")
