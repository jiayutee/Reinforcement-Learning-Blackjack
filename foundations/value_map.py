"""Turn a Foundations Monte Carlo JSON export into an offline learning view."""

import argparse
import json
import math
from pathlib import Path


RULES = "foundations-v1: replacement draws, S17, no natural bonus, hit/stand"


def validate_report(report):
    """Reject incompatible data instead of presenting it under the wrong rules."""
    if not isinstance(report, dict) or report.get("schema_version") != 1 or report.get("rules") != RULES:
        raise ValueError("Expected a Foundations v1 Monte Carlo export.")
    if report.get("estimator") != "first-visit Monte Carlo state-value prediction" or report.get("gamma") != 1.0:
        raise ValueError("Expected undiscounted first-visit state values.")
    if report.get("observation_fields") != ["player_total", "dealer_upcard", "usable_ace"]:
        raise ValueError("Unexpected observation schema.")
    policy = report.get("policy", {})
    if not isinstance(policy, dict) or policy.get("name") != "threshold" or policy.get("learned") is not False:
        raise ValueError("Expected a fixed threshold policy.")
    if type(policy.get("hit_below")) is not int or not 4 <= policy["hit_below"] <= 21:
        raise ValueError("Invalid policy threshold.")
    episodes = report.get("episodes")
    if type(episodes) is not int or episodes < 1:
        raise ValueError("Invalid episode count.")
    outcomes = [report.get(key) for key in ("wins", "losses", "pushes")]
    if any(type(n) is not int or n < 0 for n in outcomes) or sum(outcomes) != episodes:
        raise ValueError("Outcome counts do not match episode count.")
    mean = report.get("mean_return")
    if type(mean) not in (int, float) or not math.isfinite(mean) or not math.isclose(mean, (outcomes[0] - outcomes[1]) / episodes, abs_tol=1e-12):
        raise ValueError("Mean return does not match outcomes.")
    rows = report.get("states")
    if not isinstance(rows, list):
        raise ValueError("Expected a state list.")
    seen = set()
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError("Invalid state row.")
        state = row.get("observation")
        if not isinstance(state, list) or len(state) != 3:
            raise ValueError("Invalid state observation.")
        total, upcard, ace = state
        if type(total) is not int or not 4 <= total <= 21 or type(upcard) is not int or not 1 <= upcard <= 10 or type(ace) is not bool:
            raise ValueError("Invalid state observation.")
        if tuple(state) in seen:
            raise ValueError("Duplicate state observation.")
        seen.add(tuple(state))
        visits, value = row.get("visits"), row.get("value")
        if type(visits) is not int or not 1 <= visits <= episodes:
            raise ValueError("Invalid visit count.")
        if type(value) not in (int, float) or not math.isfinite(value) or not -1 <= value <= 1:
            raise ValueError("Invalid state value.")


def render_report(report):
    validate_report(report)
    # JSON lives in a nonexecuting script block. Escaping '<' prevents a metadata
    # string containing '</script>' from closing that element.
    payload = json.dumps(report, allow_nan=False).replace("<", "\\u003c")
    return TEMPLATE.replace("__REPORT_JSON__", payload)


TEMPLATE = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Blackjack · Value lab</title>
<style>
:root{color-scheme:dark;--bg:#0b1719;--panel:#142629;--ink:#edf6ef;--muted:#a9bebb;--accent:#a7e0bb}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 system-ui,sans-serif}
main{max-width:1100px;margin:auto;padding:36px 24px 64px}.eyebrow{text-transform:uppercase;letter-spacing:.18em;font-size:12px;color:var(--accent)}
h1{font:500 clamp(32px,5vw,54px)/1.1 Georgia,serif;margin:12px 0 18px}h2{font-size:20px;margin:0 0 10px}p{margin:10px 0}.muted,small{color:var(--muted)}
.intro{max-width:720px}.stats{display:flex;flex-wrap:wrap;gap:12px;margin:28px 0}.stat{background:var(--panel);border:1px solid #294044;border-radius:12px;padding:14px 20px;flex:1;min-width:160px}.stat strong{display:block;font-size:24px}
.controls{display:flex;gap:18px;flex-wrap:wrap;align-items:end;margin:20px 0}label{display:block;font-size:14px}select,input{display:block;background:#1c3438;color:var(--ink);border:1px solid #688481;border-radius:6px;padding:10px;margin-top:6px;font:inherit}input{width:140px}
button{font:inherit}button:focus-visible,select:focus-visible,input:focus-visible,summary:focus-visible{outline:3px solid #ffe093;outline-offset:2px}
.grid-wrap{overflow:auto;border:1px solid #345054;border-radius:10px}table{border-collapse:collapse;width:100%;min-width:740px;font-size:14px}caption{text-align:left;padding:14px;background:var(--panel);font-weight:600}
th{padding:9px;text-align:center;color:var(--muted);background:#142629;font-weight:500}th[scope=row]{min-width:55px}td{padding:3px;border:1px solid #21383b}
.cell{display:block;width:100%;min-width:58px;min-height:56px;border:1px solid transparent;border-radius:5px;cursor:pointer;color:var(--ink);padding:5px;background:#192e32;font-variant-numeric:tabular-nums}
.cell small{display:block;font-size:10px;color:inherit}.cell[aria-pressed=true]{border:2px solid #fff2bc}.cell.unseen{color:#a2b5b3}.cell.filtered{border:1px dashed #809593;background:#182b2e}
.legend{display:flex;flex-wrap:wrap;gap:16px;font-size:13px;margin:12px 0 20px}.legend span::before{content:'';display:inline-block;width:12px;height:12px;border-radius:3px;margin-right:6px;background:var(--swatch)}
.inspector{background:var(--panel);border:1px solid #345054;border-radius:12px;padding:22px;margin-top:20px}.inspector strong{color:var(--accent)}details{margin-top:22px}summary{cursor:pointer}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:12px;color:var(--muted)}
footer{margin-top:28px;font-size:13px;color:var(--muted)}@media(max-width:600px){main{padding:24px 14px}.stat{min-width:130px;padding:12px}.stats{gap:8px}h1{font-size:36px}}
</style>
</head>
<body><main>
<header><div class="eyebrow">Blackjack / learning lab preview</div><h1>What is a position worth?</h1>
<p class="intro">These estimates learn from completed hands. The player still follows one fixed rule. Explore the evidence before we teach it to choose better actions.</p></header>
<noscript>This interactive report needs JavaScript. The original JSON export contains all estimates and visit counts.</noscript>
<div class="stats"><div class="stat"><span>Completed hands</span><strong id="episodes"></strong></div><div class="stat"><span>Sample mean return</span><strong id="mean"></strong><small>units per hand, not win rate</small></div><div class="stat"><span>Fixed policy</span><strong id="policy"></strong></div></div>
<section aria-labelledby="map-heading"><h2 id="map-heading">Explore the value map</h2><p class="muted">Rows show your total; columns show the dealer's visible card. A means ace. Values are expected-return estimates, not hit/stand recommendations.</p>
<div class="controls"><label>Hand type<select id="hand"><option value="hard">Hard · no usable ace</option><option value="soft">Soft · usable ace</option></select></label>
<label>Minimum visits<input id="minimum" type="number" min="1" step="1" value="1"></label></div>
<p id="coverage" class="muted" aria-live="polite"></p>
<div class="legend"><span style="--swatch:#633e54">Negative return</span><span style="--swatch:#214c41">Positive return</span><span style="--swatch:#192e32">Unknown or filtered · see text</span></div>
<div class="grid-wrap" tabindex="0" aria-label="Scrollable value table"><table><caption id="caption"></caption><thead><tr><th scope="col">You / dealer</th></tr></thead><tbody id="grid"></tbody></table></div>
<aside class="inspector" aria-live="polite" aria-atomic="true"><h2 id="selection-title">Choose a position</h2><p id="selection-value">Select any table cell to inspect its estimate and the evidence behind it.</p><p id="selection-policy" class="muted"></p></aside>
<p class="muted">A blank estimate means unknown or below your visit filter, never a proven value of zero. Some blank cells represent impossible hands. More visits do not guarantee accuracy; this filter is not a confidence interval.</p>
</section>
<details><summary>Rules and experiment details</summary><pre id="metadata"></pre></details>
<footer>Replacement draws · dealer stands on soft 17 · no natural bonus · hit/stand only.<br>This local report is a preview of the learning lab. It is not the published blackjack game.</footer>
</main>
<script id="report" type="application/json">__REPORT_JSON__</script>
<script>
'use strict';
const report = JSON.parse(document.getElementById('report').textContent);
const byId = id => document.getElementById(id);
const rows = new Map(report.states.map(row => [row.observation.join(','), row]));
const signed = value => (value >= 0 ? '+' : '') + value.toFixed(3);
let selected = null;
byId('episodes').textContent = report.episodes.toLocaleString();
byId('mean').textContent = signed(report.mean_return);
byId('policy').textContent = 'Hit below ' + report.policy.hit_below;
byId('metadata').textContent = JSON.stringify({rules:report.rules,policy:report.policy,seed:report.seed,gamma:report.gamma,source:report.source || 'Not supplied'},null,2);
for(let dealer=1;dealer<=10;dealer++){const th=document.createElement('th');th.scope='col';th.textContent=dealer===1?'A':dealer;document.querySelector('thead tr').appendChild(th);}
function minimum(){return Math.max(1, Math.floor(Number(byId('minimum').value) || 1));}
function inspect(total,dealer,soft){
 selected=[total,dealer,soft];
 const row=rows.get(selected.join(',')), threshold=minimum();
 byId('selection-title').textContent=(soft?'Soft ':'Hard ')+total+' against '+(dealer===1?'ace':dealer);
 byId('selection-value').textContent=!row?'Unknown: no observed decisions at this position. This does not mean its value is zero.':row.visits<threshold?'Estimate hidden by the minimum-visit filter. Observed '+row.visits+' first visits; required '+threshold+'.':'Estimated return '+signed(row.value)+' units from '+row.visits+' first visits. This is an average outcome, not a win probability.';
 byId('selection-policy').textContent='The current fixed policy would '+(total<report.policy.hit_below?'hit':'stand')+'. That action comes from its threshold, not from this estimate.';
 document.querySelectorAll('.cell').forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.state===selected.join(','))));
}
function render(){
 const soft=byId('hand').value==='soft', min=minimum();
 byId('minimum').value=min;
 byId('caption').textContent=(soft?'Soft hands (ace counts as 11)':'Hard hands (no ace counts as 11)')+' · values in units';
 byId('grid').replaceChildren();let visible=0,observed=0;
 for(let total=21;total>=4;total--){
  const tr=document.createElement('tr'), label=document.createElement('th');label.scope='row';label.textContent=total;tr.appendChild(label);
  for(let dealer=1;dealer<=10;dealer++){
   const state=[total,dealer,soft],row=rows.get(state.join(',')),td=document.createElement('td'),button=document.createElement('button');button.type='button';button.className='cell';button.dataset.state=state.join(',');button.setAttribute('aria-pressed','false');
   let valueText='—',evidence='unknown';
   if(row){observed++;if(row.visits>=min){visible++;valueText=signed(row.value);evidence='N='+row.visits;button.style.backgroundColor=row.value<0?'hsl(325 24% '+(18+Math.abs(row.value)*16)+'%)':'hsl(155 34% '+(15+row.value*12)+'%)';}else{button.classList.add('filtered');evidence='N='+row.visits+' · hidden';}}else{button.classList.add('unseen');}
   const value=document.createElement('span'),count=document.createElement('small');value.textContent=valueText;count.textContent=evidence;button.append(value,count);
   button.setAttribute('aria-label',(soft?'Soft ':'Hard ')+total+' against '+dealer+': '+(valueText==='—'?evidence:'value '+valueText+', '+evidence));
   button.addEventListener('click',()=>inspect(total,dealer,soft));td.appendChild(button);tr.appendChild(td);
  }byId('grid').appendChild(tr);
 }
 byId('coverage').textContent=visible+' estimates shown · '+observed+' positions observed · at least '+min+' first visits per shown estimate.';
 if(selected){inspect(selected[0],selected[1],soft);}
}
byId('hand').addEventListener('change',render);byId('minimum').addEventListener('change',render);render();
</script></body></html>
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="JSON written by foundations.monte_carlo")
    parser.add_argument("--output", type=Path, required=True, help="Standalone HTML report")
    args = parser.parse_args()
    if args.input.resolve() == args.output.resolve():
        parser.error("Input and output must be different files.")
    try:
        html = render_report(json.loads(args.input.read_text()))
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(html, encoding="utf-8")
    except (OSError, ValueError, TypeError) as error:
        parser.error(str(error))
    print(f"Open in a browser: {args.output.resolve()}")


if __name__ == "__main__":
    main()
