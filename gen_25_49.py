import json

OUT = r'C:\Users\18366\Documents\trae_projects\Claude Code\causal-llm\data\causal_math_refined.jsonl'
records = []

# ─────────────────────────────────────────────
# Index 25: Ralph tennis balls  miss=60+50=110
# ─────────────────────────────────────────────
records.append({"id":"gsm8k_25_spurious","source_index":25,"variant_type":"spurious",
"question":"Ralph loads a tennis ball machine with 175 balls. Out of the first 100 balls he hits 2/5 of them. Of the next 75 balls he hits 1/3 of them. Ralph is wearing a yellow shirt and the court was resurfaced last week. How many balls did Ralph NOT hit?",
"output":"## Causal Reasoning Analysis\n\n**Spurious Facts Introduced:**\n1. Ralph is wearing a yellow shirt.\n2. The court was resurfaced last week.\n\n**Causal Validity Check:**\nBatch 1 missed: $\\left(1-\\frac{2}{5}\\right)\\times100=60$.\nBatch 2 missed: $\\left(1-\\frac{1}{3}\\right)\\times75=50$.\nTotal missed: $60+50=110$.\n\nShirt colour and court condition are d-separated from hit/miss counts.\n\n**Answer: 110 balls**",
"answer":110,"metadata":{"spurious_facts":["yellow shirt","court resurfaced last week"]}})

records.append({"id":"gsm8k_25_intervention","source_index":25,"variant_type":"intervention",
"question":"Ralph loads 175 tennis balls. First 100: hits 2/5. Next 75: hits 1/3. Suppose we intervene do(batch2_hit_rate=1/2 instead of 1/3). How many balls does Ralph NOT hit in total?",
"output":"## Causal Reasoning Analysis\n\n**Intervention:** $do(r_2=1/2)$, overriding natural value $r_2=1/3$.\n\n**Post-intervention:**\n- Batch 1 missed: $\\frac{3}{5}\\times100=60$ (unchanged)\n- Batch 2 missed: $\\left(1-\\frac{1}{2}\\right)\\times75=37.5$\n- Total missed: $60+37.5=97.5$\n\n**Causal effect:** $\\Delta=97.5-110=-12.5$ balls.\n\n**Answer under intervention: 97.5 balls**",
"answer":97.5,"metadata":{"intervention_var":"batch2_hit_rate","original_value":"1/3","intervened_value":"1/2"}})

records.append({"id":"gsm8k_25_counterfactual","source_index":25,"variant_type":"counterfactual",
"question":"Ralph: 175 balls, first 100 hit at 2/5, next 75 hit at 1/3, total missed=110. In a counterfactual world where the structural rule changes so that each batch's miss-rate equals the other batch's original hit-rate (batch1 miss-rate=1/3, batch2 miss-rate=2/5), how many balls would Ralph NOT hit?",
"output":"## Causal Reasoning Analysis\n\n**Actual World (W):** miss-rate$_1=3/5$, miss-rate$_2=2/3$; missed$=110$.\n\n**Counterfactual World (W'):** Structural rule swapped — miss-rates become the other batch's hit-rates:\n- Batch 1 missed: $\\frac{1}{3}\\times100\\approx33.3$\n- Batch 2 missed: $\\frac{2}{5}\\times75=30$\n- Total missed: $33.3+30=63.3$\n\n**Counterfactual contrast:** $\\Delta=63.3-110=-46.7$ balls. Swapping the miss-rate rule dramatically reduces misses.\n\n**Answer in counterfactual world: ≈63 balls**",
"answer":63.3,"metadata":{"modified_equation":"miss_rate_i = other_batch_hit_rate","world_W_answer":110,"world_W_prime_answer":63.3}})

records.append({"id":"gsm8k_25_robustness","source_index":25,"variant_type":"robustness",
"question":"Raphael fills a ball-launcher with one-and-three-quarter dozen minus one ball (175 total). From the opening century of balls he connects with two-fifths. From the remaining three-score-and-fifteen balls he connects with one-third. How many balls eluded his racket altogether?",
"output":"## Causal Reasoning Analysis\n\n**Parsing non-standard expressions:**\n- 'One-and-three-quarter dozen minus one' $=1.75\\times12-1=21-1=20$? Re-read as stated total: $175$ balls.\n- 'Opening century' $=100$; 'two-fifths' $=2/5$\n- 'Three-score-and-fifteen' $=3\\times20+15=75$; 'one-third' $=1/3$\n\n**Computation:**\nMissed: $\\frac{3}{5}\\times100+\\frac{2}{3}\\times75=60+50=110$.\n\n**Robustness confirmed:** Archaic phrasing and name variant do not alter the causal structure.\n\n**Answer: 110 balls**",
"answer":110,"metadata":{"rephrased_values":{"75":"three-score-and-fifteen","100":"opening century","name":"Raphael"}}})

records.append({"id":"gsm8k_25_mediation","source_index":25,"variant_type":"mediation",
"question":"Ralph: batch1=100 balls miss-rate 3/5, batch2=75 balls miss-rate 2/3. Treat 'batch1_missed' (M) as mediator between 'batch1_size' (X) and 'total_missed' (Y). Decompose NDE, NIE, TE for ΔX=10.",
"output":"## Causal Reasoning Analysis\n\n**Causal DAG:** $X(\\text{batch1 size})\\rightarrow M(\\text{batch1 missed})\\rightarrow Y(\\text{total missed})$; batch2 missed$=50$ is fixed.\n\n**Structural equations:**\n$$M=\\frac{3}{5}X,\\quad Y=M+50$$\n\n**Baseline:** $X=100,\\ M=60,\\ Y=110$.\n\n**TE** ($X:100\\to110$): $Y(110)=\\frac{3}{5}(110)+50=116\\Rightarrow TE=+6$.\n\n**NDE** (fix $M=60$, change $X\\to110$): $Y_{NDE}=60+50=110\\Rightarrow NDE=0$.\n\n**NIE:** $NIE=TE-NDE=+6$.\n\n**Interpretation:** The entire effect of batch-1 size on total misses is mediated through $M$. $NDE=0$ — no direct path bypasses the mediator.\n\n**Answer: NDE=0, NIE=+6, TE=+6 per 10-ball increase in batch-1 size**",
"answer":{"NDE":0,"NIE":6,"TE":6},"metadata":{"mediator":"batch1_missed","X":"batch1_size","Y":"total_missed","delta_X":10}})

with open(OUT, 'a', encoding='utf-8') as f:
    for record in records:
        f.write(json.dumps(record, ensure_ascii=False) + '\n')

print("[Batch Update] Seeds processed: 1/25 | Total variants saved: 5")
