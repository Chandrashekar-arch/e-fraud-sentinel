from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from .models import Transaction
from .sample_data import DEFAULT_TRANSACTION, SAMPLE_TRANSACTIONS
from .scoring import compute_risk, evaluate_dataset, money, summarize_transactions


STYLE = """
:root{--bg:#f5f7fa;--surface:#fff;--muted:#637083;--border:#d9e1e8;--ink:#172033;--blue:#0c4a63;--teal:#176b87;--green:#16835d;--amber:#b86f00;--red:#b42318;--plum:#7a4c86;--shadow:0 18px 45px rgba(23,32,51,.08)}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:"Segoe UI",Arial,sans-serif;letter-spacing:0}.shell{width:min(1180px,calc(100% - 32px));margin:0 auto;padding:24px 0 36px}.topbar,.surface,.metric{background:var(--surface);border:1px solid var(--border);border-radius:8px;box-shadow:var(--shadow)}.topbar{display:flex;justify-content:space-between;gap:16px;align-items:center;padding:18px 20px}.eyebrow{margin:0 0 5px;color:var(--teal);font-size:13px;font-weight:800;text-transform:uppercase}.topbar h1{margin:0;font-size:34px;line-height:1.05}.status{display:flex;align-items:center;gap:8px;color:var(--green);font-weight:800}.dot{width:10px;height:10px;border-radius:50%;background:var(--green);box-shadow:0 0 0 4px rgba(22,131,93,.14)}.tabs{display:flex;gap:8px;margin:18px 0;overflow-x:auto}.tabs a,.btn{display:inline-flex;align-items:center;justify-content:center;min-height:40px;padding:0 13px;border:1px solid var(--border);border-radius:8px;background:#fff;color:var(--muted);font-weight:800;text-decoration:none;white-space:nowrap}.tabs a.active,.btn.primary{background:var(--blue);border-color:var(--blue);color:#fff}.main{display:grid;gap:18px}.metrics{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}.metric{min-height:112px;padding:16px}.metric span{color:var(--muted);font-size:13px;font-weight:800;text-transform:uppercase}.metric b{display:block;margin-top:8px;font-size:32px}.metric p,.sub{margin:6px 0 0;color:var(--muted);line-height:1.45}.grid{display:grid;grid-template-columns:minmax(0,1fr) minmax(320px,.72fr);gap:18px}.surface{padding:18px}.surface h2{margin:0 0 8px;font-size:22px}.bar{display:grid;grid-template-columns:95px minmax(0,1fr) 44px;align-items:center;gap:10px;margin:13px 0}.track{height:12px;border-radius:99px;background:#e8edf2;overflow:hidden}.fill{display:block;height:100%;background:var(--teal);border-radius:inherit}.low{background:var(--green)}.watch{background:var(--amber)}.high{background:var(--red)}.critical{background:var(--plum)}.pill{display:inline-flex;align-items:center;min-height:26px;padding:0 9px;border-radius:99px;font-size:12px;font-weight:900}.pill.low{color:#0e5b41;background:#dff4eb}.pill.watch{color:#7a4a00;background:#fff0d4}.pill.high{color:#881a12;background:#ffe1de}.pill.critical{color:#663170;background:#f2e3f5}.queue{display:grid;gap:10px}.queue article{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:12px;padding:12px 0;border-bottom:1px solid var(--border)}.queue article:last-child{border-bottom:0}.queue b{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin-bottom:4px}.muted{color:var(--muted)}.form{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}.field{display:grid;gap:6px}.field span{color:var(--muted);font-size:13px;font-weight:800}.field input,.field select,.search{width:100%;min-height:40px;padding:0 10px;border:1px solid var(--border);border-radius:8px;background:#fff}.actions{display:flex;gap:10px;flex-wrap:wrap;margin-top:16px}.score{display:grid;grid-template-columns:148px minmax(0,1fr);gap:18px;align-items:center;margin-bottom:18px}.ring{--score:0;--color:var(--green);display:grid;place-items:center;width:148px;height:148px;border-radius:50%;background:radial-gradient(circle,#fff 0 56%,transparent 57%),conic-gradient(var(--color) calc(var(--score)*1%),#e8edf2 0)}.ring b{font-size:34px}.factors{list-style:none;margin:0;padding:0}.factors li{padding:11px 0;border-top:1px solid var(--border)}.factor-top{display:flex;justify-content:space-between;gap:10px;font-weight:900}.factor-note{display:block;margin-top:5px;color:var(--muted);font-size:14px;line-height:1.35}.tools{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:12px;align-items:center;margin-bottom:14px}.filters{display:flex;gap:8px;flex-wrap:wrap}.table-wrap{overflow-x:auto;border:1px solid var(--border);border-radius:8px}table{width:100%;min-width:820px;border-collapse:collapse;background:#fff}th,td{padding:11px 12px;border-bottom:1px solid var(--border);text-align:left;white-space:nowrap}th{background:#f9fbfc;color:var(--muted);font-size:13px;text-transform:uppercase}.flow{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}.step{min-height:94px;padding:12px;border:1px solid var(--border);border-radius:8px;background:#f9fbfc}.step b{display:block;margin-bottom:6px}.study-list{line-height:1.55}.matrix{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.cell{min-height:92px;padding:12px;border:1px solid var(--border);border-radius:8px;background:#f9fbfc}.cell b{display:block;font-size:30px}@media(max-width:900px){.metrics,.grid,.form,.flow{grid-template-columns:1fr}.topbar,.score,.tools{display:grid;grid-template-columns:1fr}.ring{justify-self:center}}@media(max-width:620px){.shell{width:calc(100% - 18px);padding-top:10px}.surface,.metric,.topbar{padding:14px}.matrix{grid-template-columns:1fr}.topbar h1{font-size:27px}}
"""


def pct(value: float) -> str:
    return f"{round(value * 100)}%"


def risk_class(level: str) -> str:
    return level.lower()


def risk_pill(level: str) -> str:
    return f'<span class="pill {risk_class(level)}">{escape(level)}</span>'


def parse_bool(value: str, default: bool = False) -> bool:
    if value.lower() in {"true", "yes", "1", "on"}:
        return True
    if value.lower() in {"false", "no", "0", "off"}:
        return False
    return default


def transaction_from_query(query: dict[str, list[str]]) -> Transaction:
    def get(name: str, default: object) -> str:
        return str(query.get(name, [default])[0])

    return Transaction(
        transaction_id="LIVE-CHECK",
        customer="Live Customer",
        channel=get("channel", DEFAULT_TRANSACTION.channel),
        amount=float(get("amount", DEFAULT_TRANSACTION.amount)),
        hour=max(0, min(23, int(float(get("hour", DEFAULT_TRANSACTION.hour))))),
        country_mismatch=parse_bool(get("country_mismatch", DEFAULT_TRANSACTION.country_mismatch), DEFAULT_TRANSACTION.country_mismatch),
        device_age=max(0, int(float(get("device_age", DEFAULT_TRANSACTION.device_age)))),
        account_age=max(0, int(float(get("account_age", DEFAULT_TRANSACTION.account_age)))),
        failed_logins=max(0, int(float(get("failed_logins", DEFAULT_TRANSACTION.failed_logins)))),
        velocity_24h=max(0, int(float(get("velocity_24h", DEFAULT_TRANSACTION.velocity_24h)))),
        merchant_risk=max(0, min(100, int(float(get("merchant_risk", DEFAULT_TRANSACTION.merchant_risk))))),
        ip_risk=max(0, min(100, int(float(get("ip_risk", DEFAULT_TRANSACTION.ip_risk))))),
        email_age=max(0, int(float(get("email_age", DEFAULT_TRANSACTION.email_age)))),
        shipping_distance=max(0, int(float(get("shipping_distance", DEFAULT_TRANSACTION.shipping_distance)))),
        chargebacks=max(0, int(float(get("chargebacks", DEFAULT_TRANSACTION.chargebacks)))),
        card_country_match=parse_bool(get("card_country_match", DEFAULT_TRANSACTION.card_country_match), DEFAULT_TRANSACTION.card_country_match),
        payment_method=get("payment_method", DEFAULT_TRANSACTION.payment_method),
    )


def layout(title: str, active: str, content: str) -> bytes:
    tabs = [
        ("Dashboard", "/"),
        ("Transaction Check", "/check"),
        ("Case Dataset", "/dataset"),
        ("Model Study", "/study"),
    ]
    nav = "".join(f'<a class="{ "active" if label == active else "" }" href="{href}">{label}</a>' for label, href in tabs)
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <style>{STYLE}</style>
</head>
<body>
  <div class="shell">
    <header class="topbar">
      <div>
        <p class="eyebrow">Python fraud detection project</p>
        <h1>E-Fraud Sentinel</h1>
      </div>
      <div class="status"><span class="dot"></span> Python model active</div>
    </header>
    <nav class="tabs">{nav}</nav>
    <main class="main">{content}</main>
  </div>
</body>
</html>"""
    return html.encode("utf-8")


def dashboard_page() -> bytes:
    summary = summarize_transactions(SAMPLE_TRANSACTIONS)
    scored = sorted(((transaction, compute_risk(transaction)) for transaction in SAMPLE_TRANSACTIONS), key=lambda item: item[1].score, reverse=True)
    max_bucket = max(summary["buckets"].values()) or 1
    channel_exposure: dict[str, int] = {}
    for transaction, result in scored:
        if result.score >= 55:
            channel_exposure[transaction.channel] = channel_exposure.get(transaction.channel, 0) + 1
    max_channel = max(channel_exposure.values()) if channel_exposure else 1

    bucket_bars = "".join(
        f"""<div class="bar"><b class="muted">{level}</b><span class="track"><span class="fill {risk_class(level)}" style="width:{count / max_bucket * 100:.0f}%"></span></span><b>{count}</b></div>"""
        for level, count in summary["buckets"].items()
    )
    channel_bars = "".join(
        f"""<div class="bar"><b class="muted">{escape(channel)}</b><span class="track"><span class="fill" style="width:{count / max_channel * 100:.0f}%"></span></span><b>{count}</b></div>"""
        for channel, count in sorted(channel_exposure.items(), key=lambda item: item[1], reverse=True)
    )
    queue = "".join(
        f"""<article><div><b>{transaction.transaction_id} {risk_pill(result.level)} <span class="pill">{result.score}</span></b><span class="muted">{escape(transaction.customer)} | {escape(transaction.channel)} | {money(transaction.amount)} | {escape(result.action)}</span></div><a class="btn" href="/check?sample={transaction.transaction_id}">Open</a></article>"""
        for transaction, result in scored[:6]
    )

    content = f"""
<section class="metrics">
  <article class="metric"><span>Transactions</span><b>{summary["total"]}</b><p>Sample review window</p></article>
  <article class="metric"><span>High Risk</span><b>{summary["high_risk"]}</b><p>{summary["critical"]} critical blocks</p></article>
  <article class="metric"><span>Average Score</span><b>{summary["average_score"]}</b><p>0 to 100 risk scale</p></article>
  <article class="metric"><span>Auto Approval</span><b>{pct(summary["auto_approval_rate"])}</b><p>Low-risk cases</p></article>
</section>
<section class="grid">
  <article class="surface"><h2>Risk Distribution</h2><p class="sub">Transactions scored by the Python risk engine.</p>{bucket_bars}</article>
  <article class="surface"><h2>Channel Exposure</h2><p class="sub">High-risk counts by transaction channel.</p>{channel_bars}</article>
</section>
<section class="surface"><h2>Review Queue</h2><p class="sub">Highest-priority transactions ranked by score.</p><div class="queue">{queue}</div></section>
"""
    return layout("E-Fraud Sentinel Dashboard", "Dashboard", content)


def input_field(name: str, label: str, value: object, field_type: str = "number", minimum: int | None = 0, maximum: int | None = None) -> str:
    min_attr = "" if minimum is None else f' min="{minimum}"'
    max_attr = "" if maximum is None else f' max="{maximum}"'
    return f'<label class="field"><span>{label}</span><input name="{name}" type="{field_type}" value="{escape(str(value))}"{min_attr}{max_attr}></label>'


def select_field(name: str, label: str, value: object, options: list[tuple[str, str]]) -> str:
    opts = "".join(f'<option value="{escape(raw)}" {"selected" if str(value) == raw else ""}>{escape(text)}</option>' for raw, text in options)
    return f'<label class="field"><span>{label}</span><select name="{name}">{opts}</select></label>'


def checker_page(query: dict[str, list[str]]) -> bytes:
    sample_id = query.get("sample", [""])[0]
    sample = next((transaction for transaction in SAMPLE_TRANSACTIONS if transaction.transaction_id == sample_id), None)
    transaction = sample or (transaction_from_query(query) if query else DEFAULT_TRANSACTION)
    result = compute_risk(transaction)
    color = {"Critical": "var(--plum)", "High": "var(--red)", "Watch": "var(--amber)", "Low": "var(--green)"}[result.level]

    fields = "".join(
        [
            input_field("amount", "Amount", transaction.amount),
            input_field("hour", "Hour", transaction.hour, maximum=23),
            select_field("payment_method", "Payment Method", transaction.payment_method, [("Card", "Card"), ("Wallet", "Wallet"), ("Bank", "Bank"), ("Crypto", "Crypto")]),
            select_field("channel", "Channel", transaction.channel, [(item, item) for item in ["Checkout", "Wallet", "Transfer", "Marketplace", "Bill Pay", "Recharge", "Subscription"]]),
            input_field("device_age", "Device Age Days", transaction.device_age),
            input_field("account_age", "Account Age Days", transaction.account_age),
            input_field("email_age", "Email Age Days", transaction.email_age),
            input_field("failed_logins", "Failed Logins", transaction.failed_logins),
            input_field("velocity_24h", "24h Velocity", transaction.velocity_24h),
            input_field("merchant_risk", "Merchant Risk", transaction.merchant_risk, maximum=100),
            input_field("ip_risk", "IP Risk", transaction.ip_risk, maximum=100),
            input_field("shipping_distance", "Shipping Distance KM", transaction.shipping_distance),
            input_field("chargebacks", "Chargebacks", transaction.chargebacks),
            select_field("country_mismatch", "Country Mismatch", str(transaction.country_mismatch).lower(), [("true", "Yes"), ("false", "No")]),
            select_field("card_country_match", "Card Country Match", str(transaction.card_country_match).lower(), [("true", "Yes"), ("false", "No")]),
        ]
    )
    factors = "".join(
        f"""<li><div class="factor-top"><span>{escape(factor.name)}</span><span>{factor.points:+d}</span></div><span class="factor-note">{escape(factor.detail)}</span></li>"""
        for factor in result.factors[:9]
    )

    content = f"""
<section class="grid">
  <article class="surface">
    <h2>Transaction Check</h2>
    <p class="sub">Enter a payment attempt and let the Python scoring model calculate fraud risk.</p>
    <form method="get" action="/check">
      <div class="form">{fields}</div>
      <div class="actions"><button class="btn primary" type="submit">Analyze</button><a class="btn" href="/check?sample=TXN-1007">Load Risky Sample</a><a class="btn" href="/check?sample=TXN-1001">Load Safe Sample</a></div>
    </form>
  </article>
  <article class="surface">
    <div class="score"><div class="ring" style="--score:{result.score};--color:{color}"><b>{result.score}</b></div><div>{risk_pill(result.level)}<h2>{escape(result.action)}</h2><p class="sub">{escape(result.narrative)}</p></div></div>
    <h2>Evidence</h2>
    <ul class="factors">{factors}</ul>
  </article>
</section>
"""
    return layout("Transaction Check", "Transaction Check", content)


def dataset_page(query: dict[str, list[str]]) -> bytes:
    filter_value = query.get("filter", ["all"])[0].lower()
    search = query.get("search", [""])[0].strip().lower()
    rows = []
    for transaction in SAMPLE_TRANSACTIONS:
        result = compute_risk(transaction)
        haystack = " ".join([transaction.transaction_id, transaction.customer, transaction.channel, transaction.payment_method, transaction.label]).lower()
        if filter_value != "all" and result.level.lower() != filter_value:
            continue
        if search and search not in haystack:
            continue
        rows.append((transaction, result))

    filter_buttons = "".join(
        f'<a class="btn {"primary" if filter_value == item else ""}" href="/dataset?filter={item}&search={escape(search)}">{item.title()}</a>'
        for item in ["all", "low", "watch", "high", "critical"]
    )
    table_rows = "".join(
        f"""<tr><td>{transaction.transaction_id}</td><td>{escape(transaction.customer)}</td><td><b>{money(transaction.amount)}</b></td><td>{escape(transaction.channel)}</td><td>{result.score}</td><td>{risk_pill(result.level)}</td><td>{escape(transaction.label)}</td><td><a class="btn" href="/check?sample={transaction.transaction_id}">Open</a></td></tr>"""
        for transaction, result in rows
    )

    content = f"""
<section class="surface">
  <h2>Case Dataset</h2>
  <p class="sub">Synthetic digital payment cases for project demonstration.</p>
  <form class="tools" method="get" action="/dataset">
    <input type="hidden" name="filter" value="{escape(filter_value)}">
    <input class="search" name="search" type="search" value="{escape(search)}" placeholder="Search cases">
    <button class="btn primary" type="submit">Search</button>
  </form>
  <div class="filters">{filter_buttons}</div>
  <br>
  <div class="table-wrap"><table><thead><tr><th>ID</th><th>Customer</th><th>Amount</th><th>Channel</th><th>Score</th><th>Risk</th><th>Label</th><th>Action</th></tr></thead><tbody>{table_rows}</tbody></table></div>
</section>
"""
    return layout("Case Dataset", "Case Dataset", content)


def study_page() -> bytes:
    metrics = evaluate_dataset(SAMPLE_TRANSACTIONS)
    content = f"""
<section class="grid">
  <article class="surface">
    <h2>Detection Architecture</h2>
    <p class="sub">A transparent Python risk engine designed for academic demonstration and auditability.</p>
    <div class="flow">
      <div class="step"><b>1. Capture</b><span class="muted">Payment, account, device, location, and behavior signals.</span></div>
      <div class="step"><b>2. Validate</b><span class="muted">Normalize numbers, ranges, and categorical inputs.</span></div>
      <div class="step"><b>3. Score</b><span class="muted">Apply fraud indicators and stabilizing trust signals.</span></div>
      <div class="step"><b>4. Decide</b><span class="muted">Approve, step up, review, or block.</span></div>
    </div>
    <ul class="study-list">
      <li><b>Objective:</b> detect high-risk online transactions before settlement.</li>
      <li><b>Core features:</b> amount, velocity, device age, account age, failed logins, country mismatch, IP risk, merchant risk, email age, shipping distance, chargebacks, and payment method.</li>
      <li><b>Thresholds:</b> Low 0-34, Watch 35-54, High 55-74, Critical 75-100.</li>
      <li><b>Explainability:</b> every score shows the strongest evidence for investigator review.</li>
    </ul>
  </article>
  <article class="surface">
    <h2>Sample Evaluation</h2>
    <p class="sub">The included labels are synthetic and used for project study.</p>
    <div class="matrix">
      <div class="cell"><b>{metrics["true_positive"]}</b><span class="muted">True fraud alerts</span></div>
      <div class="cell"><b>{metrics["false_positive"]}</b><span class="muted">False alerts</span></div>
      <div class="cell"><b>{metrics["false_negative"]}</b><span class="muted">Missed fraud cases</span></div>
      <div class="cell"><b>{metrics["true_negative"]}</b><span class="muted">Correct approvals</span></div>
    </div>
    <ul class="study-list">
      <li><b>Accuracy:</b> {pct(float(metrics["accuracy"]))}</li>
      <li><b>Precision:</b> {pct(float(metrics["precision"]))}</li>
      <li><b>Recall:</b> {pct(float(metrics["recall"]))}</li>
      <li><b>Future upgrade:</b> train logistic regression, random forest, or gradient boosting on real labeled data.</li>
    </ul>
  </article>
</section>
"""
    return layout("Model Study", "Model Study", content)


class FraudRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)

        if parsed.path == "/api/score":
            self.write_json(self.api_score(query))
            return
        if parsed.path == "/check":
            self.write_html(checker_page(query))
            return
        if parsed.path == "/dataset":
            self.write_html(dataset_page(query))
            return
        if parsed.path == "/study":
            self.write_html(study_page())
            return
        if parsed.path in {"/", "/dashboard"}:
            self.write_html(dashboard_page())
            return

        self.send_error(404, "Page not found")

    def api_score(self, query: dict[str, list[str]]) -> dict[str, object]:
        transaction = transaction_from_query(query) if query else DEFAULT_TRANSACTION
        result = compute_risk(transaction)
        return {
            "transaction": asdict(transaction),
            "risk": {
                "score": result.score,
                "level": result.level,
                "action": result.action,
                "narrative": result.narrative,
                "factors": [asdict(factor) for factor in result.factors],
            },
        }

    def write_html(self, content: bytes) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def write_json(self, payload: dict[str, object]) -> None:
        content = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, format: str, *args: object) -> None:
        return


def run_server(host: str = "127.0.0.1", port: int = 8000) -> None:
    server = ThreadingHTTPServer((host, port), FraudRequestHandler)
    print("E-Fraud Sentinel is running.")
    print(f"Open this URL in your browser: http://{host}:{port}")
    print("Press Ctrl+C to stop the server.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the E-Fraud Sentinel Python web app.")
    parser.add_argument("--host", default="127.0.0.1", help="Host address. Default: 127.0.0.1")
    parser.add_argument("--port", type=int, default=8000, help="Port number. Default: 8000")
    args = parser.parse_args()
    run_server(args.host, args.port)
