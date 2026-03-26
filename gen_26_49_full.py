import json

OUT = r'C:\Users\18366\Documents\trae_projects\Claude Code\causal-llm\data\causal_math_refined.jsonl'
records = []

# ─────────────────────────────────────────────
# Index 26: Jack seawater salt
# 2L seawater, 20% salt → 0.4L = 400 ml
# A: 400
# ─────────────────────────────────────────────
records.append({"id":"gsm8k_26_spurious","source_index":26,"variant_type":"spurious",
"question":"Jack is stranded on a desert island. He wants some salt to season his fish. He collects 2 liters of seawater in an old bucket. If the water is 20% salt, how many ml of salt will Jack get when all the water evaporates? Jack is wearing a torn blue shirt and the bucket has a small dent in it.",
"output":"## Causal Reasoning Analysis\n\n**Spurious Facts Introduced:**\n1. Jack is wearing a torn blue shirt.\n2. The bucket has a small dent in it.\n\n**Causal Validity Check:**\nSalt volume: $2 \\times 0.20 = 0.4$ litres.\nConverting: $0.4 \\times 1000 = 400$ ml.\n\nClothing and bucket condition are d-separated from salt yield. $P(\\text{salt ml} \\mid \\text{blue shirt, dented bucket}) = P(\\text{salt ml}) = 400$ ml.\n\n**Answer: 400 ml**",
"answer":400,"metadata":{"spurious_facts":["torn blue shirt","dented bucket"]}})

records.append({"id":"gsm8k_26_intervention","source_index":26,"variant_type":"intervention",
"question":"Jack collects 2 liters of seawater that is 20% salt. Suppose we intervene do(salt_concentration=30% instead of 20%). How many ml of salt will Jack get when all the water evaporates?",
"output":"## Causal Reasoning Analysis\n\n**Intervention:** $do(c=0.30)$, overriding natural value $c=0.20$.\n\n**Post-intervention:**\n$$\\text{salt} = 2 \\times 0.30 = 0.6 \\text{ L} = 600 \\text{ ml}$$\n\n**Causal effect:** $\\Delta = 600 - 400 = +200$ ml. Each 1% increase in concentration yields $2 \\times 0.01 \\times 1000 = 20$ ml more salt.\n\n**Answer under intervention: 600 ml**",
"answer":600,"metadata":{"intervention_var":"salt_concentration","original_value":0.20,"intervened_value":0.30}})

records.append({"id":"gsm8k_26_counterfactual","source_index":26,"variant_type":"counterfactual",
"question":"Jack collects 2 liters of seawater (20% salt) and gets 400 ml of salt. In a counterfactual world where the evaporation process only captures 75% of the dissolved salt (the rest crystallises and adheres to the bucket walls), how many ml of salt would Jack actually collect?",
"output":"## Causal Reasoning Analysis\n\n**Actual World (W):** Structural equation: $\\text{salt\\_collected} = V \\times c \\times 1000$. Result: $400$ ml.\n\n**Counterfactual World (W'):** Modified structural equation: $\\text{salt\\_collected} = V \\times c \\times 1000 \\times 0.75$.\n$$= 2 \\times 0.20 \\times 1000 \\times 0.75 = 300 \\text{ ml}$$\n\n**Counterfactual contrast:** $\\Delta = 300 - 400 = -100$ ml. The modified evaporation rule reduces yield by 25%.\n\n**Answer in counterfactual world: 300 ml**",
"answer":300,"metadata":{"modified_equation":"salt_collected = V*c*1000*0.75","world_W_answer":400,"world_W_prime_answer":300}})

records.append({"id":"gsm8k_26_robustness","source_index":26,"variant_type":"robustness",
"question":"Jacques is marooned on a tropical isle and needs seasoning for his catch. He fills a battered tin with two thousand millilitres of ocean brine. The brine is one-fifth salt by volume. Once the liquid fully evaporates, how many millilitres of salt will remain?",
"output":"## Causal Reasoning Analysis\n\n**Parsing non-standard expressions:**\n- 'Jacques' = Jack (name variant)\n- 'Two thousand millilitres' $= 2000$ ml $= 2$ L\n- 'One-fifth salt by volume' $= 20\\%$ salt\n- 'Battered tin' = old bucket\n\n**Computation:**\n$$2000 \\times \\frac{1}{5} = 400 \\text{ ml}$$\n\n**Robustness confirmed:** Name change, ml vs litres, and 'one-fifth' vs '20%' do not alter the causal structure.\n\n**Answer: 400 ml**",
"answer":400,"metadata":{"rephrased_values":{"name":"Jacques","volume":"two thousand millilitres","concentration":"one-fifth"}}})

records.append({"id":"gsm8k_26_mediation","source_index":26,"variant_type":"mediation",
"question":"Jack: 2L seawater, 20% salt → 400 ml salt. Treat 'salt_volume_litres' (M) as mediator between 'seawater_volume_litres' (X) and 'salt_ml' (Y). Decompose NDE, NIE, TE for ΔX=1 litre.",
"output":"## Causal Reasoning Analysis\n\n**Causal DAG:** $X(\\text{seawater L}) \\rightarrow M(\\text{salt L}) \\rightarrow Y(\\text{salt ml})$.\n\n**Structural equations:**\n$$M = 0.20X, \\quad Y = 1000M = 200X$$\n\n**Baseline:** $X=2,\\ M=0.4,\\ Y=400$.\n\n**TE** ($X: 2 \\to 3$): $Y(3) = 200 \\times 3 = 600$; $TE = +200$ ml.\n\n**NDE** (fix $M=0.4$, change $X: 2 \\to 3$): $Y_{NDE} = 1000 \\times 0.4 = 400$; $NDE = 0$.\n\n**NIE:** $NIE = TE - NDE = +200$ ml.\n\n**Interpretation:** The entire effect of seawater volume on salt yield is mediated through salt volume. $NDE = 0$ — no direct path bypasses the mediator.\n\n**Answer: NDE=0, NIE=+200 ml, TE=+200 ml per litre increase in seawater**",
"answer":{"NDE":0,"NIE":200,"TE":200},"metadata":{"mediator":"salt_volume_litres","X":"seawater_volume_litres","Y":"salt_ml","delta_X":1}})

print("[Batch Update] Seeds processed: 2/25 | Total variants saved: 10")

# ─────────────────────────────────────────────
# Index 27: Brennan files
# 800 files, delete 70% → keep 240. Then 400 more, delete 3/5 → keep 160. Total=400
# A: 400
# ─────────────────────────────────────────────
records.append({"id":"gsm8k_27_spurious","source_index":27,"variant_type":"spurious",
"question":"Brennan was researching his school project and had to download files from the internet. After downloading 800 files, he deleted 70% of them because they were not helpful. He downloaded 400 more files but again realized that 3/5 of them were irrelevant. Brennan uses a laptop with a blue case and his project is about ancient Rome. How many valuable files was he left with after deleting the unrelated files he downloaded in the second round?",
"output":"## Causal Reasoning Analysis\n\n**Spurious Facts Introduced:**\n1. Brennan uses a laptop with a blue case.\n2. His project is about ancient Rome.\n\n**Causal Validity Check:**\nRound 1 kept: $(1-0.70) \\times 800 = 240$ files.\nRound 2 kept: $(1-3/5) \\times 400 = 2/5 \\times 400 = 160$ files.\nTotal valuable: $240 + 160 = 400$ files.\n\nLaptop colour and project topic are d-separated from file counts. $P(\\text{total} \\mid \\text{blue laptop, Rome}) = P(\\text{total}) = 400$.\n\n**Answer: 400 files**",
"answer":400,"metadata":{"spurious_facts":["blue laptop case","project about ancient Rome"]}})

records.append({"id":"gsm8k_27_intervention","source_index":27,"variant_type":"intervention",
"question":"Brennan downloads 800 files, deletes 70%, then downloads 400 more and deletes 3/5. Suppose we intervene do(second_round_irrelevant_fraction=1/2 instead of 3/5). How many valuable files does he have?",
"output":"## Causal Reasoning Analysis\n\n**Intervention:** $do(f_2 = 1/2)$, overriding natural value $f_2 = 3/5$.\n\n**Post-intervention:**\n- Round 1 kept: $240$ (unchanged)\n- Round 2 kept: $(1 - 1/2) \\times 400 = 200$ files\n- Total: $240 + 200 = 440$ files\n\n**Causal effect:** $\\Delta = 440 - 400 = +40$ files. Reducing the irrelevant fraction by $1/10$ saves $400 \\times 0.1 = 40$ additional files.\n\n**Answer under intervention: 440 files**",
"answer":440,"metadata":{"intervention_var":"second_round_irrelevant_fraction","original_value":"3/5","intervened_value":"1/2"}})

records.append({"id":"gsm8k_27_counterfactual","source_index":27,"variant_type":"counterfactual",
"question":"Brennan: 800 files delete 70% → 240 kept; 400 files delete 3/5 → 160 kept; total=400. In a counterfactual world where the deletion rule is reversed for round 1 (keep 70% instead of deleting 70%), how many valuable files would he have?",
"output":"## Causal Reasoning Analysis\n\n**Actual World (W):** Round 1 keep-rate $= 30\\%$; Round 2 keep-rate $= 40\\%$; total $= 400$.\n\n**Counterfactual World (W'):** Modified structural equation for round 1: keep-rate $= 70\\%$ (rule inverted).\n- Round 1 kept: $0.70 \\times 800 = 560$ files\n- Round 2 kept: $160$ (unchanged, rule not modified)\n- Total: $560 + 160 = 720$ files\n\n**Counterfactual contrast:** $\\Delta = 720 - 400 = +320$ files. Inverting the round-1 deletion rule more than doubles the valuable file count.\n\n**Answer in counterfactual world: 720 files**",
"answer":720,"metadata":{"modified_equation":"round1_keep_rate=0.70","world_W_answer":400,"world_W_prime_answer":720}})

records.append({"id":"gsm8k_27_robustness","source_index":27,"variant_type":"robustness",
"question":"Brendan was compiling research for a school assignment and retrieved eight hundred documents online. He discarded seven-tenths of them as unhelpful. He then retrieved four hundred more documents but found three-fifths to be irrelevant and removed them. How many useful documents did he retain in total?",
"output":"## Causal Reasoning Analysis\n\n**Parsing non-standard expressions:**\n- 'Brendan' = Brennan (name variant)\n- 'Retrieved' = downloaded; 'documents' = files\n- 'Seven-tenths' $= 70\\%$; 'three-fifths' $= 3/5$\n- 'Eight hundred' $= 800$; 'four hundred' $= 400$\n\n**Computation:**\nRound 1: $800 \\times 0.30 = 240$. Round 2: $400 \\times 0.40 = 160$. Total: $400$.\n\n**Robustness confirmed:** Name variant and word-form numbers do not alter the causal structure.\n\n**Answer: 400 files**",
"answer":400,"metadata":{"rephrased_values":{"name":"Brendan","files":"documents","70pct":"seven-tenths","3/5":"three-fifths"}}})

records.append({"id":"gsm8k_27_mediation","source_index":27,"variant_type":"mediation",
"question":"Brennan: 800 files, delete 70% → 240 kept (round 1). Treat 'round1_kept' (M) as mediator between 'round1_total' (X) and 'total_valuable' (Y). Round 2 contributes fixed 160. Decompose NDE, NIE, TE for ΔX=100.",
"output":"## Causal Reasoning Analysis\n\n**Causal DAG:** $X(\\text{round1 total}) \\rightarrow M(\\text{round1 kept}) \\rightarrow Y(\\text{total valuable})$; round2 kept $= 160$ is fixed.\n\n**Structural equations:**\n$$M = 0.30X, \\quad Y = M + 160 = 0.30X + 160$$\n\n**Baseline:** $X=800,\\ M=240,\\ Y=400$.\n\n**TE** ($X: 800 \\to 900$): $Y(900) = 0.30 \\times 900 + 160 = 430$; $TE = +30$ files.\n\n**NDE** (fix $M=240$, change $X: 800 \\to 900$): $Y_{NDE} = 240 + 160 = 400$; $NDE = 0$.\n\n**NIE:** $NIE = TE - NDE = +30$ files.\n\n**Interpretation:** The entire effect of round-1 download size on total valuable files is mediated through round-1 kept count. $NDE = 0$.\n\n**Answer: NDE=0, NIE=+30, TE=+30 per 100-file increase in round-1 download**",
"answer":{"NDE":0,"NIE":30,"TE":30},"metadata":{"mediator":"round1_kept","X":"round1_total","Y":"total_valuable","delta_X":100}})

print("[Batch Update] Seeds processed: 3/25 | Total variants saved: 15")

# ─────────────────────────────────────────────
# Index 28: 5 houses gnomes
# 4 houses × 3 gnomes = 12; total=20; 5th house = 8
# A: 8
# ─────────────────────────────────────────────
records.append({"id":"gsm8k_28_spurious","source_index":28,"variant_type":"spurious",
"question":"There are 5 houses on a street, and each of the first four houses has 3 gnomes in the garden. If there are a total of 20 gnomes on the street, how many gnomes does the fifth house have? The houses are painted different colours and the street is called Maple Avenue.",
"output":"## Causal Reasoning Analysis\n\n**Spurious Facts Introduced:**\n1. The houses are painted different colours.\n2. The street is called Maple Avenue.\n\n**Causal Validity Check:**\nGnomes in first four houses: $4 \\times 3 = 12$.\nGnomes in fifth house: $20 - 12 = 8$.\n\nHouse colours and street name are d-separated from gnome counts. $P(\\text{5th house gnomes} \\mid \\text{coloured houses, Maple Ave}) = P(\\text{5th house gnomes}) = 8$.\n\n**Answer: 8 gnomes**",
"answer":8,"metadata":{"spurious_facts":["houses painted different colours","street called Maple Avenue"]}})

records.append({"id":"gsm8k_28_intervention","source_index":28,"variant_type":"intervention",
"question":"5 houses on a street; first four each have 3 gnomes; total=20 gnomes. Suppose we intervene do(gnomes_per_first_four=4 instead of 3). How many gnomes does the fifth house have?",
"output":"## Causal Reasoning Analysis\n\n**Intervention:** $do(g=4)$, overriding natural value $g=3$.\n\n**Post-intervention:**\n- Gnomes in first four: $4 \\times 4 = 16$\n- Gnomes in fifth: $20 - 16 = 4$\n\n**Causal effect:** $\\Delta = 4 - 8 = -4$ gnomes. Each additional gnome per house in the first four reduces the fifth house's count by 4.\n\n**Answer under intervention: 4 gnomes**",
"answer":4,"metadata":{"intervention_var":"gnomes_per_first_four","original_value":3,"intervened_value":4}})

records.append({"id":"gsm8k_28_counterfactual","source_index":28,"variant_type":"counterfactual",
"question":"5 houses; first four have 3 gnomes each; total=20; fifth house=8. In a counterfactual world where the total gnome count rule changes to: total = 4 × (gnomes per first-four house) + 2 × (fifth house gnomes), how many gnomes would the fifth house have?",
"output":"## Causal Reasoning Analysis\n\n**Actual World (W):** $\\text{total} = 4g + g_5 = 20$; $g_5 = 8$.\n\n**Counterfactual World (W'):** Modified structural equation: $\\text{total} = 4g + 2g_5$.\n$$20 = 4(3) + 2g_5 = 12 + 2g_5 \\Rightarrow g_5 = 4$$\n\n**Counterfactual contrast:** $\\Delta = 4 - 8 = -4$ gnomes. The new counting rule (double-weighting the fifth house) halves its gnome count.\n\n**Answer in counterfactual world: 4 gnomes**",
"answer":4,"metadata":{"modified_equation":"total = 4*g + 2*g5","world_W_answer":8,"world_W_prime_answer":4}})

records.append({"id":"gsm8k_28_robustness","source_index":28,"variant_type":"robustness",
"question":"On a lane with five dwellings, each of the initial quartet of homes displays three garden ornaments. If the lane has a score of ornaments in total, how many ornaments does the fifth dwelling display?",
"output":"## Causal Reasoning Analysis\n\n**Parsing non-standard expressions:**\n- 'Lane' = street; 'dwellings' = houses\n- 'Initial quartet' = first four\n- 'Garden ornaments' = gnomes\n- 'A score' $= 20$\n\n**Computation:**\n$20 - 4 \\times 3 = 20 - 12 = 8$ ornaments.\n\n**Robustness confirmed:** Archaic number expressions and synonym substitutions do not alter the causal structure.\n\n**Answer: 8 gnomes**",
"answer":8,"metadata":{"rephrased_values":{"street":"lane","houses":"dwellings","gnomes":"garden ornaments","20":"a score"}}})

records.append({"id":"gsm8k_28_mediation","source_index":28,"variant_type":"mediation",
"question":"5 houses; first four each have 3 gnomes; total=20. Treat 'gnomes_in_first_four' (M) as mediator between 'gnomes_per_house' (X) and 'gnomes_in_fifth' (Y). Decompose NDE, NIE, TE for ΔX=1.",
"output":"## Causal Reasoning Analysis\n\n**Causal DAG:** $X(\\text{gnomes/house}) \\rightarrow M(\\text{first-four total}) \\rightarrow Y(\\text{fifth house})$.\n\n**Structural equations:**\n$$M = 4X, \\quad Y = 20 - M = 20 - 4X$$\n\n**Baseline:** $X=3,\\ M=12,\\ Y=8$.\n\n**TE** ($X: 3 \\to 4$): $Y(4) = 20 - 16 = 4$; $TE = -4$.\n\n**NDE** (fix $M=12$, change $X: 3 \\to 4$): $Y_{NDE} = 20 - 12 = 8$; $NDE = 0$.\n\n**NIE:** $NIE = TE - NDE = -4$.\n\n**Interpretation:** The entire effect of per-house gnome count on the fifth house is mediated through the first-four total. $NDE = 0$.\n\n**Answer: NDE=0, NIE=-4, TE=-4 per unit increase in gnomes per house**",
"answer":{"NDE":0,"NIE":-4,"TE":-4},"metadata":{"mediator":"gnomes_in_first_four","X":"gnomes_per_house","Y":"gnomes_in_fifth","delta_X":1}})

print("[Batch Update] Seeds processed: 4/25 | Total variants saved: 20")

# ─────────────────────────────────────────────
# Index 29: Mrs. Snyder income
# 0.4p = 0.25(p+600) → 0.15p=150 → p=1000
# A: 1000
# ─────────────────────────────────────────────
records.append({"id":"gsm8k_29_spurious","source_index":29,"variant_type":"spurious",
"question":"Mrs. Snyder used to spend 40% of her monthly income on rent and utilities. Her salary was recently increased by $600 so now her rent and utilities only amount to 25% of her monthly income. Mrs. Snyder has two cats and she works in a downtown office tower. How much was her previous monthly income?",
"output":"## Causal Reasoning Analysis\n\n**Spurious Facts Introduced:**\n1. Mrs. Snyder has two cats.\n2. She works in a downtown office tower.\n\n**Causal Validity Check:**\nLet previous income $= p$. Rent is constant:\n$$0.40p = 0.25(p + 600)$$\n$$0.40p = 0.25p + 150 \\Rightarrow 0.15p = 150 \\Rightarrow p = \\$1{,}000$$\n\nPet ownership and workplace are d-separated from income. $P(p \\mid \\text{two cats, downtown}) = P(p) = \\$1{,}000$.\n\n**Answer: $1,000**",
"answer":1000,"metadata":{"spurious_facts":["has two cats","works in downtown office tower"]}})

records.append({"id":"gsm8k_29_intervention","source_index":29,"variant_type":"intervention",
"question":"Mrs. Snyder spent 40% of income on rent. After a $600 raise, rent is now 25% of income. Suppose we intervene do(new_rent_percentage=30% instead of 25%). What was her previous monthly income?",
"output":"## Causal Reasoning Analysis\n\n**Intervention:** $do(r_{new}=0.30)$, overriding natural value $r_{new}=0.25$.\n\n**Post-intervention structural equation:**\n$$0.40p = 0.30(p + 600) = 0.30p + 180$$\n$$0.10p = 180 \\Rightarrow p = \\$1{,}800$$\n\n**Causal effect:** $\\Delta = 1800 - 1000 = +\\$800$. A higher new-rent percentage implies a higher original income was needed for the equation to balance.\n\n**Answer under intervention: $1,800**",
"answer":1800,"metadata":{"intervention_var":"new_rent_percentage","original_value":0.25,"intervened_value":0.30}})

records.append({"id":"gsm8k_29_counterfactual","source_index":29,"variant_type":"counterfactual",
"question":"Mrs. Snyder: 40% of income on rent; $600 raise makes rent 25% of new income; original income=$1,000. In a counterfactual world where the raise was $400 instead of $600, what would her previous monthly income have been?",
"output":"## Causal Reasoning Analysis\n\n**Actual World (W):** Raise $= \\$600$; $p = \\$1{,}000$.\n\n**Counterfactual World (W'):** Modified structural equation: raise $= \\$400$.\n$$0.40p = 0.25(p + 400) = 0.25p + 100$$\n$$0.15p = 100 \\Rightarrow p = \\$666.67$$\n\n**Counterfactual contrast:** $\\Delta = 666.67 - 1000 = -\\$333.33$. A smaller raise implies a lower original income.\n\n**Answer in counterfactual world: $\\approx\\$666.67$**",
"answer":666.67,"metadata":{"modified_equation":"raise=400","world_W_answer":1000,"world_W_prime_answer":666.67}})

records.append({"id":"gsm8k_29_robustness","source_index":29,"variant_type":"robustness",
"question":"Ms. Schneider previously allocated two-fifths of her monthly pay to housing costs. After receiving a six-hundred-dollar raise, housing costs now represent one-quarter of her income. What was her original monthly salary?",
"output":"## Causal Reasoning Analysis\n\n**Parsing non-standard expressions:**\n- 'Ms. Schneider' = Mrs. Snyder (name variant)\n- 'Two-fifths' $= 40\\%$; 'one-quarter' $= 25\\%$\n- 'Housing costs' = rent and utilities\n- 'Six-hundred-dollar raise' $= \\$600$\n\n**Computation:**\n$$0.40p = 0.25(p+600) \\Rightarrow p = \\$1{,}000$$\n\n**Robustness confirmed:** Name change and fractional phrasing do not alter the causal structure.\n\n**Answer: $1,000**",
"answer":1000,"metadata":{"rephrased_values":{"name":"Ms. Schneider","40pct":"two-fifths","25pct":"one-quarter"}}})

records.append({"id":"gsm8k_29_mediation","source_index":29,"variant_type":"mediation",
"question":"Mrs. Snyder: 40% of p on rent; raise=R makes rent=25% of (p+R); p=1000 when R=600. Treat 'new_income' (M) as mediator between 'raise_amount' (X) and 'original_income' (Y). Decompose NDE, NIE, TE for ΔX=60.",
"output":"## Causal Reasoning Analysis\n\n**Causal DAG:** $X(\\text{raise}) \\rightarrow M(\\text{new income}) \\rightarrow Y(\\text{original income})$.\n\n**Structural equations (derived):**\nFrom $0.40Y = 0.25(Y+X)$:\n$$M = Y + X, \\quad Y = \\frac{0.25X}{0.15} = \\frac{5X}{3}$$\n\n**Baseline:** $X=600,\\ M=1600,\\ Y=1000$.\n\n**TE** ($X: 600 \\to 660$): $Y(660) = 5 \\times 660/3 = 1100$; $TE = +100$.\n\n**DE path analysis:** $Y$ depends on $X$ directly (not via $M$), so:\n\n**NDE** (fix $M$ at $M(600)=1600$, change $X: 600 \\to 660$): To hold $M$ fixed at 1600 while $X=660$, $Y=1600-660=940$; $NDE = 940-1000 = -60$.\n\n**NIE:** $NIE = TE - NDE = 100 - (-60) = +160$.\n\n**Interpretation (DE/IE path decomposition):** Raising $X$ by $\\$60$ increases $Y$ by $\\$100$ total (TE). The indirect path through new income accounts for $+\\$160$ (NIE), while the direct constraint effect is $-\\$60$ (NDE). Together: $TE = NDE + NIE = -60 + 160 = +100$. ✓\n\n**Answer: NDE=-$60, NIE=+$160, TE=+$100 per $60 increase in raise**",
"answer":{"NDE":-60,"NIE":160,"TE":100},"metadata":{"mediator":"new_income","X":"raise_amount","Y":"original_income","delta_X":60}})

print("[Batch Update] Seeds processed: 5/25 | Total variants saved: 25")

# ─────────────────────────────────────────────
# Index 30: Pizza pieces
# 4 people, 4 slices each = 16 total. Bill+Dale 50% = 4 eaten. Ann+Cate 75% = 6 eaten. Left=6.
# A: 6
# ─────────────────────────────────────────────
records.append({"id":"gsm8k_30_spurious","source_index":30,"variant_type":"spurious",
"question":"Ann, Bill, Cate, and Dale each buy personal pan pizzas cut into 4 pieces. If Bill and Dale eat 50% of their pizzas and Ann and Cate eat 75% of the pizzas, how many pizza pieces are left uneaten? They are eating at a restaurant with red tablecloths on a Friday evening.",
"output":"## Causal Reasoning Analysis\n\n**Spurious Facts Introduced:**\n1. The restaurant has red tablecloths.\n2. It is a Friday evening.\n\n**Causal Validity Check:**\nTotal pieces: $4 \\times 4 = 16$.\nBill and Dale eat: $2 \\times 4 \\times 0.50 = 4$ pieces.\nAnn and Cate eat: $2 \\times 4 \\times 0.75 = 6$ pieces.\nLeft: $16 - 4 - 6 = 6$ pieces.\n\nTablecloth colour and day of week are d-separated from pizza consumption. $P(\\text{left} \\mid \\text{red tablecloths, Friday}) = 6$.\n\n**Answer: 6 pieces**",
"answer":6,"metadata":{"spurious_facts":["red tablecloths","Friday evening"]}})

records.append({"id":"gsm8k_30_intervention","source_index":30,"variant_type":"intervention",
"question":"Ann, Bill, Cate, and Dale each have a 4-slice pizza. Bill and Dale eat 50%; Ann and Cate eat 75%. Suppose we intervene do(bill_dale_percentage=75% instead of 50%). How many pieces are left uneaten?",
"output":"## Causal Reasoning Analysis\n\n**Intervention:** $do(p_{BD}=0.75)$, overriding natural value $p_{BD}=0.50$.\n\n**Post-intervention:**\n- Total pieces: $16$\n- Bill and Dale eat: $2 \\times 4 \\times 0.75 = 6$\n- Ann and Cate eat: $6$ (unchanged)\n- Left: $16 - 6 - 6 = 4$ pieces\n\n**Causal effect:** $\\Delta = 4 - 6 = -2$ pieces. Raising Bill and Dale's consumption from 50% to 75% removes 2 more pieces.\n\n**Answer under intervention: 4 pieces**",
"answer":4,"metadata":{"intervention_var":"bill_dale_percentage","original_value":0.50,"intervened_value":0.75}})

records.append({"id":"gsm8k_30_counterfactual","source_index":30,"variant_type":"counterfactual",
"question":"Ann, Bill, Cate, Dale: 4 slices each = 16 total; Bill+Dale eat 50%; Ann+Cate eat 75%; left=6. In a counterfactual world where each pizza is cut into 6 slices instead of 4, how many pieces would be left uneaten?",
"output":"## Causal Reasoning Analysis\n\n**Actual World (W):** 4 slices/pizza; 16 total; 6 left.\n\n**Counterfactual World (W'):** Modified structural equation: slices/pizza $= 6$.\n- Total pieces: $4 \\times 6 = 24$\n- Bill and Dale eat: $2 \\times 6 \\times 0.50 = 6$\n- Ann and Cate eat: $2 \\times 6 \\times 0.75 = 9$\n- Left: $24 - 6 - 9 = 9$ pieces\n\n**Counterfactual contrast:** $\\Delta = 9 - 6 = +3$ pieces. Larger slicing granularity increases leftover count proportionally.\n\n**Answer in counterfactual world: 9 pieces**",
"answer":9,"metadata":{"modified_equation":"slices_per_pizza=6","world_W_answer":6,"world_W_prime_answer":9}})

records.append({"id":"gsm8k_30_robustness","source_index":30,"variant_type":"robustness",
"question":"Ann, Bill, Cate, and Dale each purchase a personal-sized pizza divided into four slices. Bill and Dale consume half their respective pizzas; Ann and Cate each eat three-quarters of theirs. How many slices remain uneaten across all four pizzas?",
"output":"## Causal Reasoning Analysis\n\n**Parsing non-standard expressions:**\n- 'Personal-sized pizza divided into four slices' = 4-piece pizza\n- 'Half their respective pizzas' $= 50\\%$\n- 'Three-quarters' $= 75\\%$\n\n**Computation:**\nTotal: $16$. BD eat: $4$. AC eat: $6$. Left: $16 - 10 = 6$.\n\n**Robustness confirmed:** 'Half' and 'three-quarters' as fractions vs percentages do not alter the causal structure.\n\n**Answer: 6 pieces**",
"answer":6,"metadata":{"rephrased_values":{"50pct":"half","75pct":"three-quarters"}}})

records.append({"id":"gsm8k_30_mediation","source_index":30,"variant_type":"mediation",
"question":"Ann/Bill/Cate/Dale: 4 slices each. Bill+Dale eat 50%, Ann+Cate eat 75%. Treat 'pieces_eaten_by_AC' (M) as mediator between 'AC_percentage' (X) and 'pieces_left' (Y). Decompose NDE, NIE, TE for ΔX=0.10.",
"output":"## Causal Reasoning Analysis\n\n**Causal DAG:** $X(\\text{AC fraction}) \\rightarrow M(\\text{AC pieces eaten}) \\rightarrow Y(\\text{pieces left})$; BD eaten $= 4$ is fixed.\n\n**Structural equations:**\n$$M = 2 \\times 4 \\times X = 8X, \\quad Y = 16 - 4 - M = 12 - 8X$$\n\n**Baseline:** $X=0.75,\\ M=6,\\ Y=6$.\n\n**TE** ($X: 0.75 \\to 0.85$): $Y(0.85) = 12 - 8(0.85) = 12 - 6.8 = 5.2$; $TE = -0.8$ pieces.\n\n**NDE** (fix $M=6$, change $X: 0.75 \\to 0.85$): $Y_{NDE} = 12 - 4 - 6 = 2$? Re-derive: $Y = 16 - 4 - M$; with $M$ fixed at $6$: $Y_{NDE} = 16 - 4 - 6 = 6$; $NDE = 0$.\n\n**NIE:** $NIE = TE - NDE = -0.8 - 0 = -0.8$ pieces.\n\n**Interpretation:** The entire effect of Ann and Cate's eating percentage on leftover pieces is mediated through the number of pieces they consume. $NDE = 0$.\n\n**Answer: NDE=0, NIE=-0.8, TE=-0.8 per 10pp increase in AC consumption rate**",
"answer":{"NDE":0,"NIE":-0.8,"TE":-0.8},"metadata":{"mediator":"pieces_eaten_by_AC","X":"AC_percentage","Y":"pieces_left","delta_X":0.10}})

print("[Batch Update] Seeds processed: 6/25 | Total variants saved: 30")

# ─────────────────────────────────────────────
# Index 31: Noah painter
# Last month: 8*60+4*30=480+120=600. This month: 2*600=1200
# A: 1200
# ─────────────────────────────────────────────
records.append({"id":"gsm8k_31_spurious","source_index":31,"variant_type":"spurious",
"question":"Noah is a painter. He paints pictures and sells them at the park. He charges $60 for a large painting and $30 for a small painting. Last month he sold eight large paintings and four small paintings. If he sold twice as much this month, how much is his sales for this month? Noah always wears a paint-splattered apron and he uses only oil paints.",
"output":"## Causal Reasoning Analysis\n\n**Spurious Facts Introduced:**\n1. Noah wears a paint-splattered apron.\n2. He uses only oil paints.\n\n**Causal Validity Check:**\nLast month revenue: $8 \\times \\$60 + 4 \\times \\$30 = \\$480 + \\$120 = \\$600$.\nThis month: $2 \\times \\$600 = \\$1{,}200$.\n\nApron and paint type are d-separated from sales figures. $P(\\text{revenue} \\mid \\text{apron, oil paint}) = \\$1{,}200$.\n\n**Answer: $1,200**",
"answer":1200,"metadata":{"spurious_facts":["paint-splattered apron","uses only oil paints"]}})

records.append({"id":"gsm8k_31_intervention","source_index":31,"variant_type":"intervention",
"question":"Noah: large painting=$60, small=$30; sold 8 large+4 small last month. This month sold twice as much. Suppose we intervene do(large_painting_price=$80 instead of $60). What are this month's sales?",
"output":"## Causal Reasoning Analysis\n\n**Intervention:** $do(p_L = \\$80)$, overriding natural value $p_L = \\$60$.\n\n**Post-intervention:**\n- Last month: $8 \\times \\$80 + 4 \\times \\$30 = \\$640 + \\$120 = \\$760$\n- This month: $2 \\times \\$760 = \\$1{,}520$\n\n**Causal effect:** $\\Delta = 1520 - 1200 = +\\$320$. Each \\$1 increase in large-painting price raises this month's revenue by $2 \\times 8 = \\$16$.\n\n**Answer under intervention: $1,520**",
"answer":1520,"metadata":{"intervention_var":"large_painting_price","original_value":60,"intervened_value":80}})

records.append({"id":"gsm8k_31_counterfactual","source_index":31,"variant_type":"counterfactual",
"question":"Noah: 8 large @ $60 + 4 small @ $30 = $600 last month; this month = $1,200. In a counterfactual world where 'sold twice as much this month' means he sold three times as many paintings (not twice the revenue), what would his sales be?",
"output":"## Causal Reasoning Analysis\n\n**Actual World (W):** 'Twice as much' $\\equiv$ 2× revenue $= \\$1{,}200$.\n\n**Counterfactual World (W'):** Modified structural rule: 'twice as much' $\\equiv$ 3× quantity sold (not 2× revenue).\n- Large sold: $3 \\times 8 = 24$; Small sold: $3 \\times 4 = 12$\n- Revenue: $24 \\times \\$60 + 12 \\times \\$30 = \\$1{,}440 + \\$360 = \\$1{,}800$\n\n**Counterfactual contrast:** $\\Delta = 1800 - 1200 = +\\$600$. Reinterpreting 'twice as much' as triple quantity yields 50% more revenue.\n\n**Answer in counterfactual world: $1,800**",
"answer":1800,"metadata":{"modified_equation":"this_month = 3*last_month_quantity","world_W_answer":1200,"world_W_prime_answer":1800}})

records.append({"id":"gsm8k_31_robustness","source_index":31,"variant_type":"robustness",
"question":"Noel is an artist who hawks his work at the local park. He prices large canvases at three-score dollars and small ones at half that. Last month he shifted eight large and four small canvases. This month his turnover doubled. What were his earnings this month?",
"output":"## Causal Reasoning Analysis\n\n**Parsing non-standard expressions:**\n- 'Noel' = Noah (name variant); 'canvases' = paintings\n- 'Three-score dollars' $= 3 \\times 20 = \\$60$\n- 'Half that' $= \\$30$; 'shifted' = sold; 'turnover doubled' = sales ×2\n\n**Computation:**\nLast month: $8 \\times 60 + 4 \\times 30 = \\$600$. This month: $2 \\times 600 = \\$1{,}200$.\n\n**Robustness confirmed:** Archaic expressions do not alter the causal structure.\n\n**Answer: $1,200**",
"answer":1200,"metadata":{"rephrased_values":{"name":"Noel","$60":"three-score dollars","paintings":"canvases"}}})

records.append({"id":"gsm8k_31_mediation","source_index":31,"variant_type":"mediation",
"question":"Noah: 8 large @ $60, 4 small @ $30 last month. Treat 'last_month_revenue' (M) as mediator between 'large_painting_price' (X) and 'this_month_revenue' (Y). Decompose NDE, NIE, TE for ΔX=$10.",
"output":"## Causal Reasoning Analysis\n\n**Causal DAG:** $X(\\text{large price}) \\rightarrow M(\\text{last month revenue}) \\rightarrow Y(\\text{this month revenue})$.\n\n**Structural equations:**\n$$M = 8X + 4 \\times 30 = 8X + 120, \\quad Y = 2M = 16X + 240$$\n\n**Baseline:** $X=60,\\ M=600,\\ Y=1200$.\n\n**TE** ($X: 60 \\to 70$): $Y(70) = 16(70) + 240 = 1360$; $TE = +\\$160$.\n\n**NDE** (fix $M=600$, change $X: 60 \\to 70$): $Y_{NDE} = 2 \\times 600 = 1200$; $NDE = 0$.\n\n**NIE:** $NIE = TE - NDE = +\\$160$.\n\n**Interpretation:** The entire effect of large-painting price on this month's revenue is mediated through last month's revenue. $NDE = 0$.\n\n**Answer: NDE=0, NIE=+$160, TE=+$160 per $10 increase in large painting price**",
"answer":{"NDE":0,"NIE":160,"TE":160},"metadata":{"mediator":"last_month_revenue","X":"large_painting_price","Y":"this_month_revenue","delta_X":10}})

print("[Batch Update] Seeds processed: 7/25 | Total variants saved: 35")

# ─────────────────────────────────────────────
# Index 32: Car tunnel ring
# Total=23m; turn1→5m; turn2→8m; turn4→0m (exits immediately)
# turn3 = 23-5-8-0 = 10m
# A: 10
# ─────────────────────────────────────────────
records.append({"id":"gsm8k_32_spurious","source_index":32,"variant_type":"spurious",
"question":"A car is driving through a tunnel with many turns. After a while, the car must travel through a ring that requires a total of 4 right-hand turns. After the 1st turn, it travels 5 meters. After the 2nd turn, it travels 8 meters. After the 3rd turn, it travels a little further and at the 4th turn, it immediately exits the tunnel. If the car has driven a total of 23 meters around the ring, how far did it have to travel after the 3rd turn? The car is painted red and the tunnel was built in 1952.",
"output":"## Causal Reasoning Analysis\n\n**Spurious Facts Introduced:**\n1. The car is painted red.\n2. The tunnel was built in 1952.\n\n**Causal Validity Check:**\nKnown segments: $d_1=5$m, $d_2=8$m, $d_4=0$m (exits immediately).\n$$d_3 = 23 - 5 - 8 - 0 = 10 \\text{ m}$$\n\nCar colour and tunnel construction year are d-separated from distance. $P(d_3 \\mid \\text{red car, 1952}) = 10$ m.\n\n**Answer: 10 meters**",
"answer":10,"metadata":{"spurious_facts":["car painted red","tunnel built in 1952"]}})

records.append({"id":"gsm8k_32_intervention","source_index":32,"variant_type":"intervention",
"question":"Car tunnel ring: 4 turns, total=23m; turn1→5m, turn2→8m, turn4→0m. Suppose we intervene do(distance_after_turn2=12m instead of 8m). How far did the car travel after turn 3?",
"output":"## Causal Reasoning Analysis\n\n**Intervention:** $do(d_2=12)$, overriding natural value $d_2=8$.\n\n**Post-intervention:**\n$$d_3 = 23 - 5 - 12 - 0 = 6 \\text{ m}$$\n\n**Causal effect:** $\\Delta = 6 - 10 = -4$ m. Each additional metre after turn 2 reduces the turn-3 segment by exactly 1 m.\n\n**Answer under intervention: 6 meters**",
"answer":6,"metadata":{"intervention_var":"distance_after_turn2","original_value":8,"intervened_value":12}})

records.append({"id":"gsm8k_32_counterfactual","source_index":32,"variant_type":"counterfactual",
"question":"Car ring: 4 turns, 23m total; turn1=5m, turn2=8m, turn4=0m; turn3=10m. In a counterfactual world where the car travels 3 meters after the 4th turn before exiting (instead of immediately), how far would it have traveled after the 3rd turn?",
"output":"## Causal Reasoning Analysis\n\n**Actual World (W):** $d_4=0$m; $d_3=10$m.\n\n**Counterfactual World (W'):** Modified structural equation: $d_4 = 3$m (car travels 3m after turn 4 before exiting).\n$$d_3 = 23 - 5 - 8 - 3 = 7 \\text{ m}$$\n\n**Counterfactual contrast:** $\\Delta = 7 - 10 = -3$ m. Adding a post-exit-turn distance reduces the turn-3 segment proportionally.\n\n**Answer in counterfactual world: 7 meters**",
"answer":7,"metadata":{"modified_equation":"d4=3","world_W_answer":10,"world_W_prime_answer":7}})

records.append({"id":"gsm8k_32_robustness","source_index":32,"variant_type":"robustness",
"question":"A vehicle navigates a circular section of a subterranean passage requiring four right-hand turns. After the first turn it covers five metres; after the second, eight metres; after the fourth, it exits without travelling further. If the circular section spans twenty-three metres in total, how far did the vehicle travel between the third and fourth turns?",
"output":"## Causal Reasoning Analysis\n\n**Parsing non-standard expressions:**\n- 'Vehicle' = car; 'subterranean passage' = tunnel\n- 'Circular section' = ring; 'covers' = travels\n- 'Five metres', 'eight metres', 'twenty-three metres' = 5m, 8m, 23m\n\n**Computation:**\n$d_3 = 23 - 5 - 8 - 0 = 10$ m.\n\n**Robustness confirmed:** Synonym substitutions do not alter the causal structure.\n\n**Answer: 10 meters**",
"answer":10,"metadata":{"rephrased_values":{"car":"vehicle","tunnel":"subterranean passage","ring":"circular section"}}})

records.append({"id":"gsm8k_32_mediation","source_index":32,"variant_type":"mediation",
"question":"Car ring: total=23m, d1=5m, d2=8m, d4=0m. Treat 'distance_turns_1_and_2' (M) as mediator between 'total_ring_distance' (X) and 'distance_after_turn3' (Y). Decompose NDE, NIE, TE for ΔX=5m.",
"output":"## Causal Reasoning Analysis\n\n**Causal DAG:** $X(\\text{total distance}) \\rightarrow Y(\\text{turn-3 distance})$ directly; $M = d_1 + d_2 = 13$ is fixed (independent of X).\n\n**Structural equations:**\n$$M = 5 + 8 = 13 \\text{ (fixed)}, \\quad Y = X - M - 0 = X - 13$$\n\n**Baseline:** $X=23,\\ M=13,\\ Y=10$.\n\n**TE** ($X: 23 \\to 28$): $Y(28) = 28 - 13 = 15$; $TE = +5$ m.\n\n**NDE** (fix $M=13$, change $X: 23 \\to 28$): $Y_{NDE} = 28 - 13 = 15$; $NDE = +5$ m.\n\n**NIE:** $NIE = TE - NDE = 0$.\n\n**Interpretation:** Since $M$ is fixed (turns 1 and 2 distances do not depend on total ring distance), there is no indirect path. The entire effect is direct. $NIE = 0$.\n\n**Answer: NDE=+5m, NIE=0, TE=+5m per 5m increase in total ring distance**",
"answer":{"NDE":5,"NIE":0,"TE":5},"metadata":{"mediator":"distance_turns_1_and_2","X":"total_ring_distance","Y":"distance_after_turn3","delta_X":5}})

print("[Batch Update] Seeds processed: 8/25 | Total variants saved: 40")

# ─────────────────────────────────────────────
# Index 33: Kimber pizza
# 10 cups water + 16 cups flour + 1/2*16=8 tsp salt = 34
# A: 34
# ─────────────────────────────────────────────
records.append({"id":"gsm8k_33_spurious","source_index":33,"variant_type":"spurious",
"question":"To make pizza, together with other ingredients, Kimber needs 10 cups of water, 16 cups of flour, and 1/2 times as many teaspoons of salt as the number of cups of flour. Calculate the combined total number of cups of water, flour, and teaspoons of salt that she needs to make the pizza. Kimber is making pizza for a family dinner and she uses a wood-fired oven.",
"output":"## Causal Reasoning Analysis\n\n**Spurious Facts Introduced:**\n1. Kimber is making pizza for a family dinner.\n2. She uses a wood-fired oven.\n\n**Causal Validity Check:**\n- Water: $10$ cups\n- Flour: $16$ cups\n- Salt: $\\frac{1}{2} \\times 16 = 8$ teaspoons\n- Total: $10 + 16 + 8 = 34$\n\nOccasion and oven type are d-separated from ingredient quantities. $P(\\text{total} \\mid \\text{family dinner, wood-fired oven}) = 34$.\n\n**Answer: 34**",
"answer":34,"metadata":{"spurious_facts":["family dinner","wood-fired oven"]}})

records.append({"id":"gsm8k_33_intervention","source_index":33,"variant_type":"intervention",
"question":"Kimber pizza: 10 cups water, 16 cups flour, salt = 1/2 × flour cups. Suppose we intervene do(salt_ratio=2/3 instead of 1/2). What is the combined total?",
"output":"## Causal Reasoning Analysis\n\n**Intervention:** $do(r_s = 2/3)$, overriding natural value $r_s = 1/2$.\n\n**Post-intervention:**\n- Water: $10$; Flour: $16$\n- Salt: $\\frac{2}{3} \\times 16 = \\frac{32}{3} \\approx 10.67$ tsp\n- Total: $10 + 16 + 10.67 \\approx 36.67$\n\n**Causal effect:** $\\Delta \\approx 36.67 - 34 = +2.67$. Each $+1/6$ increase in salt ratio adds $16/6 \\approx 2.67$ units to the total.\n\n**Answer under intervention: ≈36.67**",
"answer":36.67,"metadata":{"intervention_var":"salt_ratio","original_value":"1/2","intervened_value":"2/3"}})

records.append({"id":"gsm8k_33_counterfactual","source_index":33,"variant_type":"counterfactual",
"question":"Kimber: 10 water, 16 flour, 8 salt tsp, total=34. In a counterfactual world where salt is measured in cups (not teaspoons) and the rule changes to: salt_cups = 1/4 × flour_cups, what would the combined total be?",
"output":"## Causal Reasoning Analysis\n\n**Actual World (W):** Salt unit = teaspoons; $s = \\frac{1}{2} \\times 16 = 8$ tsp; total $= 34$.\n\n**Counterfactual World (W'):** Modified structural rule: salt unit = cups; $s' = \\frac{1}{4} \\times 16 = 4$ cups.\n- Total: $10 + 16 + 4 = 30$\n\n**Counterfactual contrast:** $\\Delta = 30 - 34 = -4$. Changing both the unit and the ratio reduces the total by 4.\n\n**Answer in counterfactual world: 30**",
"answer":30,"metadata":{"modified_equation":"salt_cups = flour/4","world_W_answer":34,"world_W_prime_answer":30}})

records.append({"id":"gsm8k_33_robustness","source_index":33,"variant_type":"robustness",
"question":"To prepare her pizza, Kimberley requires ten cups of water, sixteen cups of flour, and half as many teaspoons of salt as there are cups of flour. What is the aggregate of cups of water, cups of flour, and teaspoons of salt required?",
"output":"## Causal Reasoning Analysis\n\n**Parsing non-standard expressions:**\n- 'Kimberley' = Kimber (name variant)\n- 'Ten cups', 'sixteen cups' = 10 and 16\n- 'Half as many teaspoons of salt as cups of flour' $= \\frac{1}{2} \\times 16 = 8$ tsp\n- 'Aggregate' = combined total\n\n**Computation:** $10 + 16 + 8 = 34$.\n\n**Robustness confirmed:** Name variant and synonym substitutions do not alter the causal structure.\n\n**Answer: 34**",
"answer":34,"metadata":{"rephrased_values":{"name":"Kimberley","combined total":"aggregate"}}})

records.append({"id":"gsm8k_33_mediation","source_index":33,"variant_type":"mediation",
"question":"Kimber pizza: 10 water, 16 flour, salt = 1/2 × flour. Treat 'salt_amount' (M) as mediator between 'flour_amount' (X) and 'total_ingredients' (Y). Decompose NDE, NIE, TE for ΔX=4.",
"output":"## Causal Reasoning Analysis\n\n**Causal DAG:** $X(\\text{flour}) \\rightarrow M(\\text{salt}) \\rightarrow Y(\\text{total})$; also $X \\rightarrow Y$ directly.\n\n**Structural equations:**\n$$M = \\frac{1}{2}X, \\quad Y = 10 + X + M = 10 + X + \\frac{X}{2} = 10 + \\frac{3X}{2}$$\n\n**Baseline:** $X=16,\\ M=8,\\ Y=34$.\n\n**TE** ($X: 16 \\to 20$): $Y(20) = 10 + 30 = 40$; $TE = +6$.\n\n**NDE** (fix $M=8$, change $X: 16 \\to 20$): $Y_{NDE} = 10 + 20 + 8 = 38$; $NDE = +4$.\n\n**NIE:** $NIE = TE - NDE = +2$.\n\n**Interpretation:** Each 4-cup increase in flour adds 4 directly (NDE — flour itself) and 2 indirectly via the salt mediator (NIE — extra salt from higher flour). TE = NDE + NIE = $4 + 2 = 6$. ✓\n\n**Answer: NDE=+4, NIE=+2, TE=+6 per 4-cup increase in flour**",
"answer":{"NDE":4,"NIE":2,"TE":6},"metadata":{"mediator":"salt_amount","X":"flour_amount","Y":"total_ingredients","delta_X":4}})

print("[Batch Update] Seeds processed: 9/25 | Total variants saved: 45")

# ─────────────────────────────────────────────
# Index 34: Mr. Sam money
# Ken=$1750, Tony=2*1750=$3500, Total=$5250
# A: 5250
# ─────────────────────────────────────────────
records.append({"id":"gsm8k_34_spurious","source_index":34,"variant_type":"spurious",
"question":"Mr. Sam shared a certain amount of money between his two sons, Ken and Tony. If Ken got $1750, and Tony got twice as much as Ken, how much was the money shared? Mr. Sam is a retired teacher and he shared the money on his birthday.",
"output":"## Causal Reasoning Analysis\n\n**Spurious Facts Introduced:**\n1. Mr. Sam is a retired teacher.\n2. He shared the money on his birthday.\n\n**Causal Validity Check:**\n$\\text{Tony} = 2 \\times \\$1{,}750 = \\$3{,}500$.\n$\\text{Total} = \\$1{,}750 + \\$3{,}500 = \\$5{,}250$.\n\nOccupation and occasion are d-separated from the shared amount. $P(\\text{total} \\mid \\text{retired teacher, birthday}) = \\$5{,}250$.\n\n**Answer: $5,250**",
"answer":5250,"metadata":{"spurious_facts":["retired teacher","shared on birthday"]}})

records.append({"id":"gsm8k_34_intervention","source_index":34,"variant_type":"intervention",
"question":"Mr. Sam: Ken=$1750, Tony=2×Ken. Suppose we intervene do(tony_multiplier=3 instead of 2). How much was the total money shared?",
"output":"## Causal Reasoning Analysis\n\n**Intervention:** $do(k=3)$, overriding natural value $k=2$.\n\n**Post-intervention:**\n- Tony: $3 \\times \\$1{,}750 = \\$5{,}250$\n- Total: $\\$1{,}750 + \\$5{,}250 = \\$7{,}000$\n\n**Causal effect:** $\\Delta = 7000 - 5250 = +\\$1{,}750$. Each unit increase in the multiplier adds $\\$1{,}750$ to the total.\n\n**Answer under intervention: $7,000**",
"answer":7000,"metadata":{"intervention_var":"tony_multiplier","original_value":2,"intervened_value":3}})

records.append({"id":"gsm8k_34_counterfactual","source_index":34,"variant_type":"counterfactual",
"question":"Mr. Sam: Ken=$1750, Tony=2*Ken=$3500, total=$5250. In a counterfactual world where Tony gets twice Ken's share AND Ken gets $500 more than in the actual world, what would the total shared amount be?",
"output":"## Causal Reasoning Analysis\n\n**Actual World (W):** Ken $= \\$1{,}750$; Tony $= \\$3{,}500$; Total $= \\$5{,}250$.\n\n**Counterfactual World (W'):** Modified structural equation: Ken' $= \\$1{,}750 + \\$500 = \\$2{,}250$; Tony' $= 2 \\times \\$2{,}250 = \\$4{,}500$.\n- Total' $= \\$2{,}250 + \\$4{,}500 = \\$6{,}750$\n\n**Counterfactual contrast:** $\\Delta = 6750 - 5250 = +\\$1{,}500$. The \\$500 increase to Ken propagates through the multiplier, adding $3 \\times \\$500 = \\$1{,}500$ to the total.\n\n**Answer in counterfactual world: $6,750**",
"answer":6750,"metadata":{"modified_equation":"ken=2250, tony=2*ken","world_W_answer":5250,"world_W_prime_answer":6750}})

records.append({"id":"gsm8k_34_robustness","source_index":34,"variant_type":"robustness",
"question":"Mr. Samuel divided a sum of money between his two sons, Kenneth and Anthony. Kenneth received one thousand seven hundred and fifty dollars. Anthony received double what Kenneth got. What was the total sum divided?",
"output":"## Causal Reasoning Analysis\n\n**Parsing non-standard expressions:**\n- 'Mr. Samuel' = Mr. Sam; 'Kenneth' = Ken; 'Anthony' = Tony\n- 'One thousand seven hundred and fifty' $= \\$1{,}750$\n- 'Double' $= 2\\times$\n\n**Computation:**\nTony $= 2 \\times 1750 = \\$3{,}500$. Total $= 1750 + 3500 = \\$5{,}250$.\n\n**Robustness confirmed:** Name variants and word-form numbers do not alter the causal structure.\n\n**Answer: $5,250**",
"answer":5250,"metadata":{"rephrased_values":{"Ken":"Kenneth","Tony":"Anthony","$1750":"one thousand seven hundred and fifty dollars"}}})

records.append({"id":"gsm8k_34_mediation","source_index":34,"variant_type":"mediation",
"question":"Mr. Sam: Ken=$1750, Tony=2*Ken. Treat 'tony_amount' (M) as mediator between 'ken_amount' (X) and 'total_shared' (Y). Decompose NDE, NIE, TE for ΔX=$100.",
"output":"## Causal Reasoning Analysis\n\n**Causal DAG:** $X(\\text{Ken}) \\rightarrow M(\\text{Tony}) \\rightarrow Y(\\text{total})$; also $X \\rightarrow Y$ directly.\n\n**Structural equations:**\n$$M = 2X, \\quad Y = X + M = 3X$$\n\n**Baseline:** $X=1750,\\ M=3500,\\ Y=5250$.\n\n**TE** ($X: 1750 \\to 1850$): $Y(1850) = 3 \\times 1850 = 5550$; $TE = +\\$300$.\n\n**NDE** (fix $M=3500$, change $X: 1750 \\to 1850$): $Y_{NDE} = 1850 + 3500 = 5350$; $NDE = +\\$100$.\n\n**NIE:** $NIE = TE - NDE = +\\$200$.\n\n**Interpretation (DE/IE):** A \\$100 increase in Ken's share contributes \\$100 directly (NDE — Ken's own addition to total) and \\$200 indirectly via Tony's share (NIE — multiplier propagation). TE $= 100 + 200 = \\$300$. ✓\n\n**Answer: NDE=+$100, NIE=+$200, TE=+$300 per $100 increase in Ken's share**",
"answer":{"NDE":100,"NIE":200,"TE":300},"metadata":{"mediator":"tony_amount","X":"ken_amount","Y":"total_shared","delta_X":100}})

print("[Batch Update] Seeds processed: 10/25 | Total variants saved: 50")

# ─────────────────────────────────────────────
# Index 35: Mr. Sanchez students
# 40% below B → 60% B and above. 60*0.6=36
# A: 36
# ─────────────────────────────────────────────
records.append({"id":"gsm8k_35_spurious","source_index":35,"variant_type":"spurious",
"question":"Mr. Sanchez found out that 40% of his Grade 5 students got a final grade below B. How many of his students got a final grade of B and above if he has 60 students in Grade 5? Mr. Sanchez teaches at Lincoln Elementary and he gives extra credit assignments.",
"output":"## Causal Reasoning Analysis\n\n**Spurious Facts Introduced:**\n1. Mr. Sanchez teaches at Lincoln Elementary.\n2. He gives extra credit assignments.\n\n**Causal Validity Check:**\nB-and-above rate: $100\\% - 40\\% = 60\\%$.\nCount: $60 \\times 0.60 = 36$ students.\n\nSchool name and extra credit practices are d-separated from grade distribution. $P(\\text{B+} \\mid \\text{Lincoln Elem., extra credit}) = 36$.\n\n**Answer: 36 students**",
"answer":36,"metadata":{"spurious_facts":["teaches at Lincoln Elementary","gives extra credit"]}})

records.append({"id":"gsm8k_35_intervention","source_index":35,"variant_type":"intervention",
"question":"Mr. Sanchez: 40% below B, 60 students. Suppose we intervene do(below_B_percentage=50% instead of 40%). How many students got B and above?",
"output":"## Causal Reasoning Analysis\n\n**Intervention:** $do(p_{<B}=0.50)$, overriding natural value $p_{<B}=0.40$.\n\n**Post-intervention:**\n- B-and-above rate: $1 - 0.50 = 50\\%$\n- Count: $60 \\times 0.50 = 30$ students\n\n**Causal effect:** $\\Delta = 30 - 36 = -6$ students. Each 10pp increase in the below-B rate reduces B-and-above count by 6.\n\n**Answer under intervention: 30 students**",
"answer":30,"metadata":{"intervention_var":"below_B_percentage","original_value":0.40,"intervened_value":0.50}})

records.append({"id":"gsm8k_35_counterfactual","source_index":35,"variant_type":"counterfactual",
"question":"Mr. Sanchez: 40% below B, 60 students, 36 got B+. In a counterfactual world where his class size is 80 students (instead of 60) with the same grade distribution, how many would get B and above?",
"output":"## Causal Reasoning Analysis\n\n**Actual World (W):** $n=60$; B+ count $= 36$.\n\n**Counterfactual World (W'):** Modified structural equation: $n' = 80$; grade distribution unchanged ($60\\%$ B+).\n$$\\text{B+ count} = 80 \\times 0.60 = 48$$\n\n**Counterfactual contrast:** $\\Delta = 48 - 36 = +12$ students.\n\n**Answer in counterfactual world: 48 students**",
"answer":48,"metadata":{"modified_equation":"class_size=80","world_W_answer":36,"world_W_prime_answer":48}})

records.append({"id":"gsm8k_35_robustness","source_index":35,"variant_type":"robustness",
"question":"Professor Sanchez discovered that two-fifths of his fifth-grade cohort received a final mark below B. If his cohort numbers sixty pupils, how many achieved a B or higher?",
"output":"## Causal Reasoning Analysis\n\n**Parsing non-standard expressions:**\n- 'Professor Sanchez' = Mr. Sanchez\n- 'Two-fifths' $= 40\\%$\n- 'Cohort numbers sixty' = 60 students\n- 'Final mark below B' = grade below B\n\n**Computation:**\n$(1 - 2/5) \\times 60 = 3/5 \\times 60 = 36$ students.\n\n**Robustness confirmed:** 'Professor' vs 'Mr.', 'two-fifths' vs '40%', and 'cohort' vs 'class' do not alter the causal structure.\n\n**Answer: 36 students**",
"answer":36,"metadata":{"rephrased_values":{"40pct":"two-fifths","students":"pupils","class":"cohort"}}})

records.append({"id":"gsm8k_35_mediation","source_index":35,"variant_type":"mediation",
"question":"Mr. Sanchez: 60 students, 40% below B → 36 got B+. Treat 'below_B_count' (M) as mediator between 'total_students' (X) and 'B_plus_count' (Y). Decompose NDE, NIE, TE for ΔX=10.",
"output":"## Causal Reasoning Analysis\n\n**Causal DAG:** $X(\\text{total}) \\rightarrow M(\\text{below-B count}) \\rightarrow Y(\\text{B+ count})$.\n\n**Structural equations:**\n$$M = 0.40X, \\quad Y = X - M = 0.60X$$\n\n**Baseline:** $X=60,\\ M=24,\\ Y=36$.\n\n**TE** ($X: 60 \\to 70$): $Y(70) = 0.60 \\times 70 = 42$; $TE = +6$.\n\n**NDE** (fix $M=24$, change $X: 60 \\to 70$): $Y_{NDE} = 70 - 24 = 46$; $NDE = +10$.\n\n**NIE:** $NIE = TE - NDE = -4$.\n\n**Interpretation:** Adding 10 students raises B+ count by 10 directly (NDE — more students), but via the mediator (M also rises by 4), it pulls 4 students into the below-B group (NIE $= -4$). Net TE $= 10 - 4 = +6$. ✓\n\n**Answer: NDE=+10, NIE=-4, TE=+6 per 10-student increase in class size**",
"answer":{"NDE":10,"NIE":-4,"TE":6},"metadata":{"mediator":"below_B_count","X":"total_students","Y":"B_plus_count","delta_X":10}})

print("[Batch Update] Seeds processed: 11/25 | Total variants saved: 55")

# ─────────────────────────────────────────────
# Index 36: Lisa Jack Tommy
# Total=$60; Lisa=30; Tommy=15; Lisa-Tommy=15
# A: 15
# ─────────────────────────────────────────────
records.append({"id":"gsm8k_36_spurious","source_index":36,"variant_type":"spurious",
"question":"Lisa, Jack, and Tommy earned $60 from washing cars all week. However, half of the $60 was earned by Lisa. Tommy earned half of what Lisa earned. How much more money did Lisa earn than Tommy? They washed cars on a Saturday morning and used eco-friendly soap.",
"output":"## Causal Reasoning Analysis\n\n**Spurious Facts Introduced:**\n1. They washed cars on a Saturday morning.\n2. They used eco-friendly soap.\n\n**Causal Validity Check:**\nLisa $= \\$60 / 2 = \\$30$.\nTommy $= \\$30 / 2 = \\$15$.\nDifference $= \\$30 - \\$15 = \\$15$.\n\nDay of week and soap type are d-separated from earnings. $P(\\text{diff} \\mid \\text{Saturday, eco soap}) = \\$15$.\n\n**Answer: $15**",
"answer":15,"metadata":{"spurious_facts":["Saturday morning","eco-friendly soap"]}})

records.append({"id":"gsm8k_36_intervention","source_index":36,"variant_type":"intervention",
"question":"Lisa/Jack/Tommy earn $60. Lisa=half the total. Tommy=half of Lisa. Suppose we intervene do(tommy_fraction=1/3 of Lisa instead of 1/2). How much more did Lisa earn than Tommy?",
"output":"## Causal Reasoning Analysis\n\n**Intervention:** $do(f_T = 1/3)$, overriding natural value $f_T = 1/2$.\n\n**Post-intervention:**\n- Lisa $= \\$30$ (unchanged)\n- Tommy $= \\$30 / 3 = \\$10$\n- Difference $= \\$30 - \\$10 = \\$20$\n\n**Causal effect:** $\\Delta = 20 - 15 = +\\$5$. Reducing Tommy's fraction increases Lisa's advantage.\n\n**Answer under intervention: $20**",
"answer":20,"metadata":{"intervention_var":"tommy_fraction_of_lisa","original_value":"1/2","intervened_value":"1/3"}})

records.append({"id":"gsm8k_36_counterfactual","source_index":36,"variant_type":"counterfactual",
"question":"Lisa/Jack/Tommy earn $60; Lisa=1/2 total=$30; Tommy=1/2 of Lisa=$15; diff=$15. In a counterfactual world where the rule changes so that Tommy earns half of what JACK earns (instead of half of Lisa), how much more does Lisa earn than Tommy?",
"output":"## Causal Reasoning Analysis\n\n**Actual World (W):** Tommy $= \\frac{1}{2} \\times$ Lisa $= \\$15$; Jack $= 60 - 30 - 15 = \\$15$.\n\n**Counterfactual World (W'):** Modified structural rule: Tommy $= \\frac{1}{2} \\times$ Jack.\nLet Tommy $= t$, Jack $= j$, Lisa $= 30$ (unchanged):\n$$t = j/2, \\quad 30 + j + t = 60 \\Rightarrow j + j/2 = 30 \\Rightarrow 3j/2 = 30 \\Rightarrow j = 20, \\ t = 10$$\nDifference $= 30 - 10 = \\$20$.\n\n**Counterfactual contrast:** $\\Delta = 20 - 15 = +\\$5$. Switching Tommy's reference from Lisa to Jack increases Lisa's advantage.\n\n**Answer in counterfactual world: $20**",
"answer":20,"metadata":{"modified_equation":"tommy = jack/2","world_W_answer":15,"world_W_prime_answer":20}})

records.append({"id":"gsm8k_36_robustness","source_index":36,"variant_type":"robustness",
"question":"Liza, Jake, and Tim pooled sixty dollars from a weekend car-wash. Liza took half the pot. Tim pocketed half of what Liza received. By how many dollars did Liza's take exceed Tim's?",
"output":"## Causal Reasoning Analysis\n\n**Parsing non-standard expressions:**\n- 'Liza/Jake/Tim' = Lisa/Jack/Tommy (name variants)\n- 'Pooled sixty dollars' = earned $60 total\n- 'Half the pot' $= \\$30$; 'pocketed half' $= \\$15$\n\n**Computation:**\nLiza $= \\$30$. Tim $= \\$15$. Difference $= \\$15$.\n\n**Robustness confirmed:** Name changes and synonym substitutions do not alter the causal structure.\n\n**Answer: $15**",
"answer":15,"metadata":{"rephrased_values":{"Lisa":"Liza","Jack":"Jake","Tommy":"Tim"}}})

records.append({"id":"gsm8k_36_mediation","source_index":36,"variant_type":"mediation",
"question":"Lisa/Tommy/Jack earn $60. Lisa=X (half of 60). Tommy = X/2. Treat 'lisa_earnings' (M) as mediator between 'total_earnings' (X) and 'lisa_tommy_difference' (Y). Decompose NDE, NIE, TE for ΔX=$10.",
"output":"## Causal Reasoning Analysis\n\n**Causal DAG:** $X(\\text{total}) \\rightarrow M(\\text{Lisa earnings}) \\rightarrow Y(\\text{Lisa−Tommy diff})$.\n\n**Structural equations:**\n$$M = \\frac{X}{2}, \\quad Y = M - \\frac{M}{2} = \\frac{M}{2} = \\frac{X}{4}$$\n\n**Baseline:** $X=60,\\ M=30,\\ Y=15$.\n\n**TE** ($X: 60 \\to 70$): $Y(70) = 70/4 = 17.5$; $TE = +\\$2.50$.\n\n**NDE** (fix $M=30$, change $X: 60 \\to 70$): $Y_{NDE} = 30 - 30/2 = 15$ (M fixed, so Y unchanged); $NDE = 0$.\n\n**NIE:** $NIE = TE - NDE = +\\$2.50$.\n\n**Interpretation:** The entire effect of total earnings on the Lisa–Tommy gap is mediated through Lisa's earnings. $NDE = 0$.\n\n**Answer: NDE=0, NIE=+$2.50, TE=+$2.50 per $10 increase in total earnings**",
"answer":{"NDE":0,"NIE":2.5,"TE":2.5},"metadata":{"mediator":"lisa_earnings","X":"total_earnings","Y":"lisa_tommy_difference","delta_X":10}})

print("[Batch Update] Seeds processed: 12/25 | Total variants saved: 60")

# ─────────────────────────────────────────────
# Index 37: Five friends fast food
# 5*3+4*1.2+5*0.5+2.7=15+4.8+2.5+2.7=25; per person=25/5=5
# A: 5
# ─────────────────────────────────────────────
records.append({"id":"gsm8k_37_spurious","source_index":37,"variant_type":"spurious",
"question":"Five friends eat at a fast-food chain and order the following: 5 pieces of hamburger that cost $3 each; 4 sets of French fries that cost $1.20; 5 cups of soda that cost $0.5 each; and 1 platter of spaghetti that cost $2.7. How much will each of them pay if they will split the bill equally? They are celebrating a birthday and the restaurant has a drive-through.",
"output":"## Causal Reasoning Analysis\n\n**Spurious Facts Introduced:**\n1. They are celebrating a birthday.\n2. The restaurant has a drive-through.\n\n**Causal Validity Check:**\n- Hamburgers: $5 \\times \\$3 = \\$15$\n- Fries: $4 \\times \\$1.20 = \\$4.80$\n- Sodas: $5 \\times \\$0.50 = \\$2.50$\n- Spaghetti: $\\$2.70$\n- Total: $\\$15 + \\$4.80 + \\$2.50 + \\$2.70 = \\$25$\n- Per person: $\\$25 / 5 = \\$5$\n\nOccasion and restaurant features are d-separated from the bill. $P(\\text{per person} \\mid \\text{birthday, drive-through}) = \\$5$.\n\n**Answer: $5**",
"answer":5,"metadata":{"spurious_facts":["celebrating birthday","restaurant has drive-through"]}})

records.append({"id":"gsm8k_37_intervention","source_index":37,"variant_type":"intervention",
"question":"Five friends: 5 burgers@$3, 4 fries@$1.20, 5 sodas@$0.50, 1 spaghetti@$2.70; split equally. Suppose we intervene do(hamburger_price=$4 instead of $3). How much does each person pay?",
"output":"## Causal Reasoning Analysis\n\n**Intervention:** $do(p_H = \\$4)$, overriding natural value $p_H = \\$3$.\n\n**Post-intervention:**\n- Hamburgers: $5 \\times \\$4 = \\$20$\n- Rest: $\\$4.80 + \\$2.50 + \\$2.70 = \\$10$ (unchanged)\n- Total: $\\$20 + \\$10 = \\$30$\n- Per person: $\\$30 / 5 = \\$6$\n\n**Causal effect:** $\\Delta = 6 - 5 = +\\$1$. Each \\$1 increase in burger price raises per-person cost by $5/5 = \\$1$.\n\n**Answer under intervention: $6**",
"answer":6,"metadata":{"intervention_var":"hamburger_price","original_value":3,"intervened_value":4}})

records.append({"id":"gsm8k_37_counterfactual","source_index":37,"variant_type":"counterfactual",
"question":"Five friends: total bill $25, split equally=$5. In a counterfactual world where one friend leaves (only 4 split the bill) but the order stays the same, how much does each person pay?",
"output":"## Causal Reasoning Analysis\n\n**Actual World (W):** 5 people; per-person cost $= \\$5$.\n\n**Counterfactual World (W'):** Modified structural rule: number of people $= 4$ (one leaves; bill unchanged).\n$$\\text{Per person} = \\frac{\\$25}{4} = \\$6.25$$\n\n**Counterfactual contrast:** $\\Delta = 6.25 - 5 = +\\$1.25$. Fewer people increases each person's share.\n\n**Answer in counterfactual world: $6.25**",
"answer":6.25,"metadata":{"modified_equation":"num_people=4","world_W_answer":5,"world_W_prime_answer":6.25}})

records.append({"id":"gsm8k_37_robustness","source_index":37,"variant_type":"robustness",
"question":"Five companions dine at a fast-food establishment. They order five burgers at three dollars apiece, four servings of fries at one dollar twenty each, five beverages at fifty cents each, and a single pasta dish priced at two dollars seventy. Dividing the bill equally, what does each companion owe?",
"output":"## Causal Reasoning Analysis\n\n**Parsing non-standard expressions:**\n- 'Companions' = friends; 'establishment' = restaurant\n- 'Three dollars apiece' $= \\$3$ each; 'one dollar twenty' $= \\$1.20$\n- 'Fifty cents' $= \\$0.50$; 'pasta dish' = spaghetti\n- 'Two dollars seventy' $= \\$2.70$\n\n**Computation:**\nTotal $= 15 + 4.80 + 2.50 + 2.70 = \\$25$. Per person $= \\$5$.\n\n**Robustness confirmed:** Synonym substitutions and currency phrasing do not alter the causal structure.\n\n**Answer: $5**",
"answer":5,"metadata":{"rephrased_values":{"friends":"companions","hamburgers":"burgers","spaghetti":"pasta dish","$0.50":"fifty cents"}}})

records.append({"id":"gsm8k_37_mediation","source_index":37,"variant_type":"mediation",
"question":"Five friends: burgers 5×$3, fries 4×$1.20, sodas 5×$0.50, spaghetti $2.70; split equally. Treat 'total_bill' (M) as mediator between 'hamburger_price' (X) and 'per_person_cost' (Y). Decompose NDE, NIE, TE for ΔX=$1.",
"output":"## Causal Reasoning Analysis\n\n**Causal DAG:** $X(\\text{burger price}) \\rightarrow M(\\text{total bill}) \\rightarrow Y(\\text{per-person cost})$.\n\n**Structural equations:**\n$$M = 5X + 4(1.20) + 5(0.50) + 2.70 = 5X + 10, \\quad Y = M/5 = X + 2$$\n\n**Baseline:** $X=3,\\ M=25,\\ Y=5$.\n\n**TE** ($X: 3 \\to 4$): $Y(4) = 4 + 2 = 6$; $TE = +\\$1$.\n\n**NDE** (fix $M=25$, change $X: 3 \\to 4$): $Y_{NDE} = 25/5 = 5$ (M fixed); $NDE = 0$.\n\n**NIE:** $NIE = TE - NDE = +\\$1$.\n\n**Interpretation:** The entire per-person cost increase from a higher burger price flows through the total bill mediator. $NDE = 0$.\n\n**Answer: NDE=0, NIE=+$1, TE=+$1 per $1 increase in burger price**",
"answer":{"NDE":0,"NIE":1,"TE":1},"metadata":{"mediator":"total_bill","X":"hamburger_price","Y":"per_person_cost","delta_X":1}})

print("[Batch Update] Seeds processed: 13/25 | Total variants saved: 65")

# ─────────────────────────────────────────────
# Index 38: Artemis tea
# Ratio: 1oz tea / 8oz water. 12 people × 6oz = 72oz water. Tea = 72/8 = 9oz
# A: 9
# ─────────────────────────────────────────────
records.append({"id":"gsm8k_38_spurious","source_index":38,"variant_type":"spurious",
"question":"Artemis is making tea for a party. She knows her mom drinks an 8-ounce cup of tea and uses one ounce of tea. She will use this same ratio for the party. The party has 12 people there and each of them wants a 6-ounce cup of tea. How many ounces of tea does she need? Artemis is hosting a garden party and she uses loose-leaf tea.",
"output":"## Causal Reasoning Analysis\n\n**Spurious Facts Introduced:**\n1. Artemis is hosting a garden party.\n2. She uses loose-leaf tea.\n\n**Causal Validity Check:**\nRatio: $1$ oz tea per $8$ oz water.\nTotal water needed: $12 \\times 6 = 72$ oz.\nTea needed: $72 / 8 = 9$ oz.\n\nEvent type and tea variety are d-separated from the required amount. $P(\\text{tea oz} \\mid \\text{garden party, loose-leaf}) = 9$.\n\n**Answer: 9 ounces**",
"answer":9,"metadata":{"spurious_facts":["garden party","loose-leaf tea"]}})

records.append({"id":"gsm8k_38_intervention","source_index":38,"variant_type":"intervention",
"question":"Artemis: 1oz tea per 8oz water. 12 people, 6oz cups. Suppose we intervene do(cup_size=8oz instead of 6oz). How many ounces of tea does she need?",
"output":"## Causal Reasoning Analysis\n\n**Intervention:** $do(c=8)$ oz, overriding natural value $c=6$.\n\n**Post-intervention:**\n- Total water: $12 \\times 8 = 96$ oz\n- Tea needed: $96 / 8 = 12$ oz\n\n**Causal effect:** $\\Delta = 12 - 9 = +3$ oz. Each 2-oz increase in cup size adds $12 \\times 2/8 = 3$ oz of tea.\n\n**Answer under intervention: 12 ounces**",
"answer":12,"metadata":{"intervention_var":"cup_size_oz","original_value":6,"intervened_value":8}})

records.append({"id":"gsm8k_38_counterfactual","source_index":38,"variant_type":"counterfactual",
"question":"Artemis: ratio 1oz tea/8oz water; 12 people, 6oz cups; needs 9oz tea. In a counterfactual world where the tea-to-water ratio changes to 1oz tea per 6oz water (stronger brew), how many ounces of tea would she need?",
"output":"## Causal Reasoning Analysis\n\n**Actual World (W):** Ratio $= 1:8$; tea $= 9$ oz.\n\n**Counterfactual World (W'):** Modified structural equation: ratio $= 1:6$ (stronger brew).\n- Total water: $72$ oz (unchanged)\n- Tea: $72 / 6 = 12$ oz\n\n**Counterfactual contrast:** $\\Delta = 12 - 9 = +3$ oz. A stronger brew ratio requires 33% more tea.\n\n**Answer in counterfactual world: 12 ounces**",
"answer":12,"metadata":{"modified_equation":"ratio=1oz_tea_per_6oz_water","world_W_answer":9,"world_W_prime_answer":12}})

records.append({"id":"gsm8k_38_robustness","source_index":38,"variant_type":"robustness",
"question":"Artemis is brewing tea for a gathering of a dozen guests, each wanting a six-fluid-ounce cup. Her recipe uses one ounce of tea leaves for every eight ounces of hot water. How many ounces of tea leaves does she require?",
"output":"## Causal Reasoning Analysis\n\n**Parsing non-standard expressions:**\n- 'A dozen guests' $= 12$ people\n- 'Six-fluid-ounce cup' $= 6$ oz\n- 'One ounce per eight ounces' $= 1:8$ ratio\n- 'Tea leaves' = tea (same ingredient)\n\n**Computation:**\nTotal water: $12 \\times 6 = 72$ oz. Tea: $72/8 = 9$ oz.\n\n**Robustness confirmed:** 'Dozen', 'fluid-ounce', and 'tea leaves' do not alter the causal structure.\n\n**Answer: 9 ounces**",
"answer":9,"metadata":{"rephrased_values":{"12":"a dozen","guests":"people","tea":"tea leaves"}}})

records.append({"id":"gsm8k_38_mediation","source_index":38,"variant_type":"mediation",
"question":"Artemis tea: ratio 1oz/8oz, 12 people, 6oz cups. Treat 'total_water_oz' (M) as mediator between 'number_of_guests' (X) and 'tea_oz_needed' (Y). Decompose NDE, NIE, TE for ΔX=4 guests.",
"output":"## Causal Reasoning Analysis\n\n**Causal DAG:** $X(\\text{guests}) \\rightarrow M(\\text{total water}) \\rightarrow Y(\\text{tea needed})$.\n\n**Structural equations:**\n$$M = 6X, \\quad Y = M/8 = 6X/8 = 0.75X$$\n\n**Baseline:** $X=12,\\ M=72,\\ Y=9$.\n\n**TE** ($X: 12 \\to 16$): $Y(16) = 0.75 \\times 16 = 12$; $TE = +3$ oz.\n\n**NDE** (fix $M=72$, change $X: 12 \\to 16$): $Y_{NDE} = 72/8 = 9$ (M fixed); $NDE = 0$.\n\n**NIE:** $NIE = TE - NDE = +3$ oz.\n\n**Interpretation:** The entire effect of additional guests on tea needed is mediated through total water volume. $NDE = 0$.\n\n**Answer: NDE=0, NIE=+3oz, TE=+3oz per 4 additional guests**",
"answer":{"NDE":0,"NIE":3,"TE":3},"metadata":{"mediator":"total_water_oz","X":"number_of_guests","Y":"tea_oz_needed","delta_X":4}})

print("[Batch Update] Seeds processed: 14/25 | Total variants saved: 70")

# ─────────────────────────────────────────────
# Index 39: Anna trick-or-treating
# Anna: 14/house × 60 houses = 840. Billy: 11/house × 75 houses = 825. Diff=15
# A: 15
# ─────────────────────────────────────────────
records.append({"id":"gsm8k_39_spurious","source_index":39,"variant_type":"spurious",
"question":"Anna goes trick-or-treating in a subdivision where she gets 14 pieces of candy per house. Her brother Billy goes trick-or-treating in a neighboring subdivision where he gets 11 pieces of candy per house. If the first subdivision has 60 houses and the second subdivision has 75 houses, how many more pieces of candy does Anna get? It is Halloween night and Anna is dressed as a witch.",
"output":"## Causal Reasoning Analysis\n\n**Spurious Facts Introduced:**\n1. It is Halloween night.\n2. Anna is dressed as a witch.\n\n**Causal Validity Check:**\nAnna: $14 \\times 60 = 840$ pieces.\nBilly: $11 \\times 75 = 825$ pieces.\nDifference: $840 - 825 = 15$ pieces.\n\nDate and costume are d-separated from candy counts. $P(\\text{diff} \\mid \\text{Halloween, witch}) = 15$.\n\n**Answer: 15 pieces**",
"answer":15,"metadata":{"spurious_facts":["Halloween night","Anna dressed as witch"]}})

records.append({"id":"gsm8k_39_intervention","source_index":39,"variant_type":"intervention",
"question":"Anna: 14/house, 60 houses=840. Billy: 11/house, 75 houses=825. Diff=15. Suppose we intervene do(anna_houses=70 instead of 60). How many more pieces does Anna get than Billy?",
"output":"## Causal Reasoning Analysis\n\n**Intervention:** $do(H_A=70)$, overriding natural value $H_A=60$.\n\n**Post-intervention:**\n- Anna: $14 \\times 70 = 980$\n- Billy: $825$ (unchanged)\n- Difference: $980 - 825 = 155$\n\n**Causal effect:** $\\Delta_{\\text{diff}} = 155 - 15 = +140$ pieces. Each additional house Anna visits adds 14 pieces to her advantage.\n\n**Answer under intervention: 155 pieces**",
"answer":155,"metadata":{"intervention_var":"anna_houses","original_value":60,"intervened_value":70}})

records.append({"id":"gsm8k_39_counterfactual","source_index":39,"variant_type":"counterfactual",
"question":"Anna: 14/house×60=840. Billy: 11/house×75=825. Anna wins by 15. In a counterfactual world where Anna's subdivision has an answer-rate of 1.5 per house (she gets 1.5× the normal candy at each house, so effectively 21 pieces/house), how many more pieces does she get than Billy?",
"output":"## Causal Reasoning Analysis\n\n**Actual World (W):** Anna $= 840$; Billy $= 825$; diff $= 15$.\n\n**Counterfactual World (W'):** Modified structural rule: Anna's candy rate $= 1.5 \\times 14 = 21$ pieces/house.\n- Anna: $21 \\times 60 = 1260$\n- Billy: $825$ (unchanged)\n- Difference: $1260 - 825 = 435$\n\n**Counterfactual contrast:** $\\Delta = 435 - 15 = +420$ pieces. A 50% rate boost multiplies Anna's advantage dramatically.\n\n**Answer in counterfactual world: 435 pieces**",
"answer":435,"metadata":{"modified_equation":"anna_rate=21_pieces_per_house","world_W_answer":15,"world_W_prime_answer":435}})

records.append({"id":"gsm8k_39_robustness","source_index":39,"variant_type":"robustness",
"question":"On All Hallows' Eve, Anna visits sixty dwellings in her neighbourhood, collecting fourteen sweets per home. Her sibling Billy visits three-score-and-fifteen dwellings in the adjacent neighbourhood, obtaining eleven sweets per abode. By how many sweets does Anna's haul exceed Billy's?",
"output":"## Causal Reasoning Analysis\n\n**Parsing non-standard expressions:**\n- 'All Hallows' Eve' = Halloween; 'sweets' = candy\n- 'Sixty dwellings' $= 60$ houses\n- 'Fourteen sweets per home' $= 14$/house\n- 'Three-score-and-fifteen' $= 3 \\times 20 + 15 = 75$ houses\n- 'Sibling' = brother; 'abode' = house\n\n**Computation:**\nAnna: $14 \\times 60 = 840$. Billy: $11 \\times 75 = 825$. Diff: $15$.\n\n**Robustness confirmed:** Archaic expressions do not alter the causal structure.\n\n**Answer: 15 pieces**",
"answer":15,"metadata":{"rephrased_values":{"60":"sixty","75":"three-score-and-fifteen","candy":"sweets"}}})

records.append({"id":"gsm8k_39_mediation","source_index":39,"variant_type":"mediation",
"question":"Anna: 14/house×60 houses. Billy: 11/house×75=825. Treat 'anna_total' (M) as mediator between 'anna_houses' (X) and 'candy_difference' (Y). Decompose NDE, NIE, TE for ΔX=1 house.",
"output":"## Causal Reasoning Analysis\n\n**Causal DAG:** $X(\\text{Anna houses}) \\rightarrow M(\\text{Anna total}) \\rightarrow Y(\\text{Anna−Billy diff})$; Billy total $= 825$ is fixed.\n\n**Structural equations:**\n$$M = 14X, \\quad Y = M - 825 = 14X - 825$$\n\n**Baseline:** $X=60,\\ M=840,\\ Y=15$.\n\n**TE** ($X: 60 \\to 61$): $Y(61) = 14(61) - 825 = 854 - 825 = 29$; $TE = +14$ pieces.\n\n**NDE** (fix $M=840$, change $X: 60 \\to 61$): $Y_{NDE} = 840 - 825 = 15$; $NDE = 0$.\n\n**NIE:** $NIE = TE - NDE = +14$ pieces.\n\n**Interpretation:** The entire effect of one more house visited on the candy advantage is mediated through Anna's total. $NDE = 0$.\n\n**Answer: NDE=0, NIE=+14, TE=+14 per additional house**",
"answer":{"NDE":0,"NIE":14,"TE":14},"metadata":{"mediator":"anna_total","X":"anna_houses","Y":"candy_difference","delta_X":1}})

print("[Batch Update] Seeds processed: 15/25 | Total variants saved: 75")

# ─────────────────────────────────────────────
# Index 40: Concert tickets
# 12 tickets. First 10 @ $40 = $400. Next 2 get 5% off: $38 each = $76. Total=$476
# A: 476
# ─────────────────────────────────────────────
records.append({"id":"gsm8k_40_spurious","source_index":40,"variant_type":"spurious",
"question":"A concert ticket costs $40. Mr. Benson bought 12 tickets and received a 5% discount for every ticket bought that exceeds 10. How much did Mr. Benson pay in all? The concert is for a rock band and Mr. Benson is buying tickets for his family.",
"output":"## Causal Reasoning Analysis\n\n**Spurious Facts Introduced:**\n1. The concert is for a rock band.\n2. Mr. Benson is buying tickets for his family.\n\n**Causal Validity Check:**\n- Excess tickets: $12 - 10 = 2$\n- Discounted price: $\\$40 \\times (1 - 0.05) = \\$38$\n- First 10 tickets: $10 \\times \\$40 = \\$400$\n- Last 2 tickets: $2 \\times \\$38 = \\$76$\n- Total: $\\$400 + \\$76 = \\$476$\n\nGenre and buyer's purpose are d-separated from ticket cost. $P(\\text{total} \\mid \\text{rock, family}) = \\$476$.\n\n**Answer: $476**",
"answer":476,"metadata":{"spurious_facts":["rock band concert","buying for family"]}})

records.append({"id":"gsm8k_40_intervention","source_index":40,"variant_type":"intervention",
"question":"Concert ticket=$40; 12 bought; 5% discount on tickets exceeding 10. Suppose we intervene do(discount_percentage=10% instead of 5%). How much does Mr. Benson pay?",
"output":"## Causal Reasoning Analysis\n\n**Intervention:** $do(d=0.10)$, overriding natural value $d=0.05$.\n\n**Post-intervention:**\n- Discounted price: $\\$40 \\times 0.90 = \\$36$\n- First 10: $\\$400$ (unchanged)\n- Last 2: $2 \\times \\$36 = \\$72$\n- Total: $\\$400 + \\$72 = \\$472$\n\n**Causal effect:** $\\Delta = 472 - 476 = -\\$4$. Each 1pp increase in discount rate saves $2 \\times \\$0.40 = \\$0.80$. For 5pp: $-\\$4$. ✓\n\n**Answer under intervention: $472**",
"answer":472,"metadata":{"intervention_var":"discount_percentage","original_value":0.05,"intervened_value":0.10}})

records.append({"id":"gsm8k_40_counterfactual","source_index":40,"variant_type":"counterfactual",
"question":"Concert: $40/ticket, 12 bought, 5% discount for tickets beyond 10. Total=$476. In a counterfactual world where the discount threshold is 8 tickets (instead of 10), how much would Mr. Benson pay?",
"output":"## Causal Reasoning Analysis\n\n**Actual World (W):** Threshold $= 10$; 2 discounted tickets; total $= \\$476$.\n\n**Counterfactual World (W'):** Modified structural rule: threshold $= 8$.\n- Excess tickets: $12 - 8 = 4$\n- Discounted price: $\\$38$ each (5% off \\$40)\n- First 8 tickets: $8 \\times \\$40 = \\$320$\n- Last 4 tickets: $4 \\times \\$38 = \\$152$\n- Total: $\\$320 + \\$152 = \\$472$\n\n**Counterfactual contrast:** $\\Delta = 472 - 476 = -\\$4$. A lower threshold means more discounted tickets, reducing total cost.\n\n**Answer in counterfactual world: $472**",
"answer":472,"metadata":{"modified_equation":"discount_threshold=8","world_W_answer":476,"world_W_prime_answer":472}})

records.append({"id":"gsm8k_40_robustness","source_index":40,"variant_type":"robustness",
"question":"A concert ticket is priced at two-score dollars. Mr. Benson purchased a dozen tickets and received a five-percent reduction on each ticket beyond the tenth. What was his total expenditure?",
"output":"## Causal Reasoning Analysis\n\n**Parsing non-standard expressions:**\n- 'Two-score dollars' $= 2 \\times 20 = \\$40$\n- 'A dozen tickets' $= 12$\n- 'Five-percent reduction' $= 5\\%$ discount\n- 'Each ticket beyond the tenth' = tickets 11 and 12\n\n**Computation:**\n$10 \\times 40 + 2 \\times 38 = 400 + 76 = \\$476$.\n\n**Robustness confirmed:** Archaic number expressions do not alter the causal structure.\n\n**Answer: $476**",
"answer":476,"metadata":{"rephrased_values":{"$40":"two-score dollars","12":"a dozen","discount":"reduction"}}})

records.append({"id":"gsm8k_40_mediation","source_index":40,"variant_type":"mediation",
"question":"Concert: $40/ticket, 12 tickets, 5% off for >10. Treat 'discounted_tickets_cost' (M) as mediator between 'discount_rate' (X) and 'total_cost' (Y). Decompose NDE, NIE, TE for ΔX=0.05.",
"output":"## Causal Reasoning Analysis\n\n**Causal DAG:** $X(\\text{discount rate}) \\rightarrow M(\\text{discounted 2-ticket cost}) \\rightarrow Y(\\text{total cost})$; first-10 cost $= \\$400$ fixed.\n\n**Structural equations:**\n$$M = 2 \\times 40 \\times (1-X) = 80(1-X), \\quad Y = 400 + M = 480 - 80X$$\n\n**Baseline:** $X=0.05,\\ M=76,\\ Y=476$.\n\n**TE** ($X: 0.05 \\to 0.10$): $Y(0.10) = 480 - 8 = 472$; $TE = -\\$4$.\n\n**NDE** (fix $M=76$, change $X: 0.05 \\to 0.10$): $Y_{NDE} = 400 + 76 = 476$; $NDE = 0$.\n\n**NIE:** $NIE = TE - NDE = -\\$4$.\n\n**Interpretation:** The entire cost reduction from a higher discount rate is mediated through the discounted-ticket cost. $NDE = 0$.\n\n**Answer: NDE=0, NIE=-$4, TE=-$4 per 5pp increase in discount rate**",
"answer":{"NDE":0,"NIE":-4,"TE":-4},"metadata":{"mediator":"discounted_tickets_cost","X":"discount_rate","Y":"total_cost","delta_X":0.05}})

print("[Batch Update] Seeds processed: 16/25 | Total variants saved: 80")

# ─────────────────────────────────────────────
# Index 41: Rachel Sara shoes
# Sara: shoes=$50, dress=$200. Rachel: 2× each. Rachel=100+400=$500
# A: 500
# ─────────────────────────────────────────────
records.append({"id":"gsm8k_41_spurious","source_index":41,"variant_type":"spurious",
"question":"Rachel and Sara want to attend a beauty and modeling contest. They both want to buy new pairs of shoes and dresses. Sara buys a pair of shoes which costs $50 and a dress which costs $200. How much should Rachel budget if she wants to spend twice as much as what Sara spent on the pair of shoes and dress? They are shopping at a mall and the contest is next weekend.",
"output":"## Causal Reasoning Analysis\n\n**Spurious Facts Introduced:**\n1. They are shopping at a mall.\n2. The contest is next weekend.\n\n**Causal Validity Check:**\n- Rachel's shoes: $2 \\times \\$50 = \\$100$\n- Rachel's dress: $2 \\times \\$200 = \\$400$\n- Total budget: $\\$100 + \\$400 = \\$500$\n\nShopping location and contest timing are d-separated from budget. $P(\\text{budget} \\mid \\text{mall, next weekend}) = \\$500$.\n\n**Answer: $500**",
"answer":500,"metadata":{"spurious_facts":["shopping at mall","contest next weekend"]}})

records.append({"id":"gsm8k_41_intervention","source_index":41,"variant_type":"intervention",
"question":"Sara: shoes=$50, dress=$200. Rachel spends twice as much as Sara on each item. Suppose we intervene do(rachel_multiplier=3 instead of 2). What is Rachel's total budget?",
"output":"## Causal Reasoning Analysis\n\n**Intervention:** $do(k=3)$, overriding natural value $k=2$.\n\n**Post-intervention:**\n- Shoes: $3 \\times \\$50 = \\$150$\n- Dress: $3 \\times \\$200 = \\$600$\n- Total: $\\$150 + \\$600 = \\$750$\n\n**Causal effect:** $\\Delta = 750 - 500 = +\\$250$. Each unit increase in multiplier adds $\\$50 + \\$200 = \\$250$ to Rachel's budget.\n\n**Answer under intervention: $750**",
"answer":750,"metadata":{"intervention_var":"rachel_multiplier","original_value":2,"intervened_value":3}})

records.append({"id":"gsm8k_41_counterfactual","source_index":41,"variant_type":"counterfactual",
"question":"Sara: shoes=$50, dress=$200. Rachel: 2× each item=$500. In a counterfactual world where Rachel spends twice as much on shoes but 1.5 times as much on the dress (instead of twice each), what would her budget be?",
"output":"## Causal Reasoning Analysis\n\n**Actual World (W):** Rachel $= 2 \\times 50 + 2 \\times 200 = \\$500$.\n\n**Counterfactual World (W'):** Modified structural rule:\n- Shoes: $2 \\times \\$50 = \\$100$ (unchanged)\n- Dress: $1.5 \\times \\$200 = \\$300$\n- Total: $\\$100 + \\$300 = \\$400$\n\n**Counterfactual contrast:** $\\Delta = 400 - 500 = -\\$100$. A lower dress multiplier reduces Rachel's budget by \\$100.\n\n**Answer in counterfactual world: $400**",
"answer":400,"metadata":{"modified_equation":"shoes×2, dress×1.5","world_W_answer":500,"world_W_prime_answer":400}})

records.append({"id":"gsm8k_41_robustness","source_index":41,"variant_type":"robustness",
"question":"Rachel and Sara are preparing for a modelling pageant. Sara purchased footwear for fifty dollars and an outfit for two hundred dollars. Rachel wishes to spend double what Sara paid for each item separately. What is the total sum Rachel must set aside?",
"output":"## Causal Reasoning Analysis\n\n**Parsing non-standard expressions:**\n- 'Footwear' = shoes; 'outfit' = dress\n- 'Fifty dollars' $= \\$50$; 'two hundred dollars' $= \\$200$\n- 'Double what Sara paid for each item separately' $= 2\\times$ each\n\n**Computation:**\nRachel $= 2 \\times 50 + 2 \\times 200 = 100 + 400 = \\$500$.\n\n**Robustness confirmed:** Synonym substitutions do not alter the causal structure.\n\n**Answer: $500**",
"answer":500,"metadata":{"rephrased_values":{"shoes":"footwear","dress":"outfit","$50":"fifty dollars"}}})

records.append({"id":"gsm8k_41_mediation","source_index":41,"variant_type":"mediation",
"question":"Sara: shoes=$50, dress=$200. Rachel: 2× each. Treat 'rachel_shoes_budget' (M) as mediator between 'sara_shoes_price' (X) and 'rachel_total_budget' (Y). Decompose NDE, NIE, TE for ΔX=$10.",
"output":"## Causal Reasoning Analysis\n\n**Causal DAG:** $X(\\text{Sara shoes price}) \\rightarrow M(\\text{Rachel shoes}) \\rightarrow Y(\\text{Rachel total})$; Rachel dress $= 2 \\times 200 = \\$400$ fixed.\n\n**Structural equations:**\n$$M = 2X, \\quad Y = M + 400 = 2X + 400$$\n\n**Baseline:** $X=50,\\ M=100,\\ Y=500$.\n\n**TE** ($X: 50 \\to 60$): $Y(60) = 2(60) + 400 = 520$; $TE = +\\$20$.\n\n**NDE** (fix $M=100$, change $X: 50 \\to 60$): $Y_{NDE} = 100 + 400 = 500$; $NDE = 0$.\n\n**NIE:** $NIE = TE - NDE = +\\$20$.\n\n**Interpretation:** The entire effect of Sara's shoe price on Rachel's total budget is mediated through Rachel's shoe budget. $NDE = 0$.\n\n**Answer: NDE=0, NIE=+$20, TE=+$20 per $10 increase in Sara's shoe price**",
"answer":{"NDE":0,"NIE":20,"TE":20},"metadata":{"mediator":"rachel_shoes_budget","X":"sara_shoes_price","Y":"rachel_total_budget","delta_X":10}})

print("[Batch Update] Seeds processed: 17/25 | Total variants saved: 85")

# ─────────────────────────────────────────────
# Index 42: Monkeys bananas
# Type-A: 6 piles × 9 hands × 14 bananas = 756
# Type-B: 4 piles × 12 hands × 9 bananas = 432
# Total = 1188. Per monkey = 1188/12 = 99
# A: 99
# ─────────────────────────────────────────────
records.append({"id":"gsm8k_42_spurious","source_index":42,"variant_type":"spurious",
"question":"A family of 12 monkeys collected 10 piles of bananas. 6 piles had 9 hands, with each hand having 14 bananas, while the remaining piles had 12 hands, with each hand having 9 bananas. How many bananas would each monkey get if they divide the bananas equally amongst themselves? The monkeys live in a tropical rainforest and it is the dry season.",
"output":"## Causal Reasoning Analysis\n\n**Spurious Facts Introduced:**\n1. The monkeys live in a tropical rainforest.\n2. It is the dry season.\n\n**Causal Validity Check:**\n- Type-A piles: $6 \\times 9 \\times 14 = 756$ bananas\n- Type-B piles: $(10-6) \\times 12 \\times 9 = 4 \\times 108 = 432$ bananas\n- Total: $756 + 432 = 1{,}188$\n- Per monkey: $1{,}188 / 12 = 99$\n\nHabitat and season are d-separated from banana counts. $P(\\text{per monkey} \\mid \\text{rainforest, dry season}) = 99$.\n\n**Answer: 99 bananas**",
"answer":99,"metadata":{"spurious_facts":["tropical rainforest","dry season"]}})

records.append({"id":"gsm8k_42_intervention","source_index":42,"variant_type":"intervention",
"question":"12 monkeys, 10 piles: 6 piles (9 hands×14 bananas), 4 piles (12 hands×9 bananas). Suppose we intervene do(bananas_per_hand_typeA=12 instead of 14). How many bananas per monkey?",
"output":"## Causal Reasoning Analysis\n\n**Intervention:** $do(b_A=12)$, overriding natural value $b_A=14$.\n\n**Post-intervention:**\n- Type-A: $6 \\times 9 \\times 12 = 648$\n- Type-B: $432$ (unchanged)\n- Total: $648 + 432 = 1{,}080$\n- Per monkey: $1{,}080 / 12 = 90$\n\n**Causal effect:** $\\Delta = 90 - 99 = -9$ bananas/monkey. Each 1-banana reduction per hand in Type-A reduces the share by $6 \\times 9 / 12 = 4.5$.\n\n**Answer under intervention: 90 bananas per monkey**",
"answer":90,"metadata":{"intervention_var":"bananas_per_hand_typeA","original_value":14,"intervened_value":12}})

records.append({"id":"gsm8k_42_counterfactual","source_index":42,"variant_type":"counterfactual",
"question":"12 monkeys; Type-A: 6×9×14=756; Type-B: 4×12×9=432; total=1188; per monkey=99. In a counterfactual world where Type-B piles also have 9 hands per pile (instead of 12), how many bananas per monkey?",
"output":"## Causal Reasoning Analysis\n\n**Actual World (W):** Type-B hands/pile $= 12$; per monkey $= 99$.\n\n**Counterfactual World (W'):** Modified structural rule: Type-B hands/pile $= 9$.\n- Type-A: $756$ (unchanged)\n- Type-B: $4 \\times 9 \\times 9 = 324$\n- Total: $756 + 324 = 1{,}080$\n- Per monkey: $1{,}080 / 12 = 90$\n\n**Counterfactual contrast:** $\\Delta = 90 - 99 = -9$ bananas/monkey. Reducing Type-B hands from 12 to 9 removes $4 \\times 3 \\times 9 = 108$ bananas.\n\n**Answer in counterfactual world: 90 bananas per monkey**",
"answer":90,"metadata":{"modified_equation":"typeB_hands_per_pile=9","world_W_answer":99,"world_W_prime_answer":90}})

records.append({"id":"gsm8k_42_robustness","source_index":42,"variant_type":"robustness",
"question":"A troop of a dozen simians gathered ten clusters of bananas. Half a dozen clusters each comprised nine bunches of fourteen bananas apiece. The remaining clusters each comprised a dozen bunches of nine bananas apiece. If the bananas are divided equally among all simians, how many does each receive?",
"output":"## Causal Reasoning Analysis\n\n**Parsing non-standard expressions:**\n- 'Dozen simians' $= 12$ monkeys\n- 'Half a dozen clusters' $= 6$ piles; 'nine bunches' = 9 hands\n- 'Fourteen bananas apiece' $= 14$/hand\n- 'A dozen bunches' $= 12$ hands; 'nine bananas apiece' $= 9$/hand\n\n**Computation:**\nType-A: $6 \\times 9 \\times 14 = 756$. Type-B: $4 \\times 12 \\times 9 = 432$. Total: $1{,}188$. Per monkey: $99$.\n\n**Robustness confirmed:** Archaic expressions do not alter the causal structure.\n\n**Answer: 99 bananas**",
"answer":99,"metadata":{"rephrased_values":{"monkeys":"simians","piles":"clusters","hands":"bunches","12":"a dozen","6":"half a dozen"}}})

records.append({"id":"gsm8k_42_mediation","source_index":42,"variant_type":"mediation",
"question":"12 monkeys; Type-A: 6 piles, 9 hands, 14 bananas/hand; Type-B: 4 piles, 12 hands, 9 bananas/hand. Treat 'typeA_total' (M) as mediator between 'typeA_piles' (X) and 'per_monkey' (Y). Decompose NDE, NIE, TE for ΔX=1.",
"output":"## Causal Reasoning Analysis\n\n**Causal DAG:** $X(\\text{Type-A piles}) \\rightarrow M(\\text{Type-A bananas}) \\rightarrow Y(\\text{per monkey})$; Type-B total $= 432$ fixed.\n\n**Structural equations:**\n$$M = X \\times 9 \\times 14 = 126X, \\quad Y = (M + 432)/12 = 10.5X + 36$$\n\n**Baseline:** $X=6,\\ M=756,\\ Y=99$.\n\n**TE** ($X: 6 \\to 7$): $Y(7) = 10.5(7) + 36 = 73.5 + 36 = 109.5$; $TE = +10.5$.\n\n**NDE** (fix $M=756$, change $X: 6 \\to 7$): $Y_{NDE} = (756+432)/12 = 99$; $NDE = 0$.\n\n**NIE:** $NIE = TE - NDE = +10.5$.\n\n**Interpretation:** The entire effect of adding one more Type-A pile on per-monkey share is mediated through total Type-A banana count. $NDE = 0$.\n\n**Answer: NDE=0, NIE=+10.5, TE=+10.5 per additional Type-A pile**",
"answer":{"NDE":0,"NIE":10.5,"TE":10.5},"metadata":{"mediator":"typeA_total","X":"typeA_piles","Y":"per_monkey","delta_X":1}})

print("[Batch Update] Seeds processed: 18/25 | Total variants saved: 90")

# ─────────────────────────────────────────────
# Index 43: Earthquake buildings
# EQ1=4, EQ2=8, EQ3=16, EQ4=32. Total=60
# A: 60
# ─────────────────────────────────────────────
records.append({"id":"gsm8k_43_spurious","source_index":43,"variant_type":"spurious",
"question":"An earthquake caused four buildings to collapse. Experts predicted that each following earthquake would have double the number of collapsing buildings as the previous one, since each one would make the foundations less stable. After three more earthquakes, how many buildings had collapsed including those from the first earthquake? The earthquakes occurred in a coastal city and seismologists were monitoring them.",
"output":"## Causal Reasoning Analysis\n\n**Spurious Facts Introduced:**\n1. The earthquakes occurred in a coastal city.\n2. Seismologists were monitoring them.\n\n**Causal Validity Check:**\n$EQ_1=4,\\ EQ_2=8,\\ EQ_3=16,\\ EQ_4=32$.\nTotal: $4+8+16+32=60$.\n\nGeographic location and monitoring personnel are d-separated from building collapse counts. $P(\\text{total} \\mid \\text{coastal, seismologists}) = 60$.\n\n**Answer: 60 buildings**",
"answer":60,"metadata":{"spurious_facts":["coastal city","seismologists monitoring"]}})

records.append({"id":"gsm8k_43_intervention","source_index":43,"variant_type":"intervention",
"question":"Earthquake sequence: EQ1=4 collapses; each next EQ doubles. 4 earthquakes total. Suppose we intervene do(initial_collapses=6 instead of 4). How many buildings collapse in total?",
"output":"## Causal Reasoning Analysis\n\n**Intervention:** $do(EQ_1=6)$, overriding natural value $EQ_1=4$.\n\n**Post-intervention (doubling chain propagates):**\n- $EQ_1=6,\\ EQ_2=12,\\ EQ_3=24,\\ EQ_4=48$\n- Total: $6+12+24+48=90$\n\n**Causal effect:** $\\Delta = 90 - 60 = +30$ buildings. Each unit increase in $EQ_1$ scales the entire geometric series by $+15$ (sum factor $= 1+2+4+8=15$).\n\n**Answer under intervention: 90 buildings**",
"answer":90,"metadata":{"intervention_var":"initial_collapses","original_value":4,"intervened_value":6}})

records.append({"id":"gsm8k_43_counterfactual","source_index":43,"variant_type":"counterfactual",
"question":"Earthquake: EQ1=4, each doubles, 4 EQs, total=60. In a counterfactual world where each earthquake causes 1.5× the previous collapses (instead of 2×), how many total buildings would collapse?",
"output":"## Causal Reasoning Analysis\n\n**Actual World (W):** Doubling rule; total $= 60$.\n\n**Counterfactual World (W'):** Modified structural rule: multiplier $= 1.5$.\n- $EQ_1=4,\\ EQ_2=4\\times1.5=6,\\ EQ_3=6\\times1.5=9,\\ EQ_4=9\\times1.5=13.5$\n- Total: $4+6+9+13.5=32.5$\n\n**Counterfactual contrast:** $\\Delta = 32.5 - 60 = -27.5$ buildings. Slower growth cuts total damage nearly in half.\n\n**Answer in counterfactual world: 32.5 buildings**",
"answer":32.5,"metadata":{"modified_equation":"multiplier=1.5","world_W_answer":60,"world_W_prime_answer":32.5}})

records.append({"id":"gsm8k_43_robustness","source_index":43,"variant_type":"robustness",
"question":"A seismic event caused a quartet of structures to collapse. Experts forecast that each subsequent tremor would topple double the number of buildings as the previous one. After three more tremors, what is the cumulative count of collapsed structures, including those from the initial event?",
"output":"## Causal Reasoning Analysis\n\n**Parsing non-standard expressions:**\n- 'Seismic event' = earthquake; 'structures' = buildings\n- 'A quartet' $= 4$; 'subsequent tremor' = following earthquake\n- 'Cumulative count' = total\n\n**Computation:**\n$4 + 8 + 16 + 32 = 60$.\n\n**Robustness confirmed:** Synonym substitutions and archaic grouping expressions do not alter the causal structure.\n\n**Answer: 60 buildings**",
"answer":60,"metadata":{"rephrased_values":{"earthquake":"seismic event","buildings":"structures","4":"a quartet"}}})

records.append({"id":"gsm8k_43_mediation","source_index":43,"variant_type":"mediation",
"question":"Earthquake: EQ1=4; each next doubles. 4 EQs total. Treat 'EQ2_collapses' (M) as mediator between 'EQ1_collapses' (X) and 'total_collapses' (Y). Decompose NDE, NIE, TE for ΔX=1.",
"output":"## Causal Reasoning Analysis\n\n**Causal DAG:** $X(EQ_1) \\rightarrow M(EQ_2) \\rightarrow Y(\\text{total})$; $EQ_3=2M$, $EQ_4=4M$.\n\n**Structural equations:**\n$$M = 2X, \\quad Y = X + M + 2M + 4M = X + 7M = X + 14X = 15X$$\n\n**Baseline:** $X=4,\\ M=8,\\ Y=60$.\n\n**TE** ($X: 4 \\to 5$): $Y(5) = 15 \\times 5 = 75$; $TE = +15$.\n\n**NDE** (fix $M=8$, change $X: 4 \\to 5$): $Y_{NDE} = 5 + 7(8) = 5 + 56 = 61$; $NDE = +1$.\n\n**NIE:** $NIE = TE - NDE = +14$.\n\n**Interpretation (DE/IE path decomposition):** The direct effect is 1 (one extra EQ1 collapse, path $X \\to Y$). The indirect effect is 14 (via the doubling chain $X \\to M \\to EQ_3 \\to EQ_4 \\to Y$, contributing $2+4+8=14$). TE $= 1 + 14 = 15$. ✓\n\n**Answer: NDE=+1, NIE=+14, TE=+15 per unit increase in EQ1 collapses**",
"answer":{"NDE":1,"NIE":14,"TE":15},"metadata":{"mediator":"EQ2_collapses","X":"EQ1_collapses","Y":"total_collapses","delta_X":1}})

print("[Batch Update] Seeds processed: 19/25 | Total variants saved: 95")

# ─────────────────────────────────────────────
# Index 44: James university budget
# $1000. Food=30%=$300. Accom=15%=$150. Entertainment=25%=$250. Coursework=1000-700=$300
# A: 300
# ─────────────────────────────────────────────
records.append({"id":"gsm8k_44_spurious","source_index":44,"variant_type":"spurious",
"question":"James is a first-year student at a University in Chicago. He has a budget of $1000 per semester. He spends 30% of his money on food, 15% on accommodation, 25% on entertainment, and the rest on coursework materials. How much money does he spend on coursework materials? James is studying computer science and lives in a dormitory.",
"output":"## Causal Reasoning Analysis\n\n**Spurious Facts Introduced:**\n1. James is studying computer science.\n2. He lives in a dormitory.\n\n**Causal Validity Check:**\n- Food: $0.30 \\times \\$1{,}000 = \\$300$\n- Accommodation: $0.15 \\times \\$1{,}000 = \\$150$\n- Entertainment: $0.25 \\times \\$1{,}000 = \\$250$\n- Coursework: $\\$1{,}000 - \\$300 - \\$150 - \\$250 = \\$300$\n\nMajor and housing type are d-separated from spending allocation. $P(\\text{coursework} \\mid \\text{CS, dorm}) = \\$300$.\n\n**Answer: $300**",
"answer":300,"metadata":{"spurious_facts":["studying computer science","lives in dormitory"]}})

records.append({"id":"gsm8k_44_intervention","source_index":44,"variant_type":"intervention",
"question":"James: $1000 budget; food=30%, accommodation=15%, entertainment=25%, rest=coursework. Suppose we intervene do(entertainment_percentage=35% instead of 25%). How much does he spend on coursework materials?",
"output":"## Causal Reasoning Analysis\n\n**Intervention:** $do(p_E=0.35)$, overriding natural value $p_E=0.25$.\n\n**Post-intervention:**\n- Food: $\\$300$; Accommodation: $\\$150$; Entertainment: $0.35 \\times 1000 = \\$350$\n- Coursework: $\\$1{,}000 - \\$300 - \\$150 - \\$350 = \\$200$\n\n**Causal effect:** $\\Delta = 200 - 300 = -\\$100$. Each 10pp increase in entertainment spend reduces coursework budget by \\$100.\n\n**Answer under intervention: $200**",
"answer":200,"metadata":{"intervention_var":"entertainment_percentage","original_value":0.25,"intervened_value":0.35}})

records.append({"id":"gsm8k_44_counterfactual","source_index":44,"variant_type":"counterfactual",
"question":"James: $1000; food=30%, accom=15%, entertainment=25%, coursework=$300. In a counterfactual world where accommodation is a fixed $200 (not percentage-based), how much would he spend on coursework?",
"output":"## Causal Reasoning Analysis\n\n**Actual World (W):** Accommodation $= 15\\% \\times \\$1000 = \\$150$; coursework $= \\$300$.\n\n**Counterfactual World (W'):** Modified structural rule: accommodation $= \\$200$ (fixed, not percentage).\n- Fixed costs: food $= \\$300$; accom $= \\$200$; entertainment $= \\$250$\n- Coursework: $\\$1{,}000 - \\$300 - \\$200 - \\$250 = \\$250$\n\n**Counterfactual contrast:** $\\Delta = 250 - 300 = -\\$50$. Fixed accommodation at \\$200 instead of \\$150 reduces coursework budget by \\$50.\n\n**Answer in counterfactual world: $250**",
"answer":250,"metadata":{"modified_equation":"accommodation=200_fixed","world_W_answer":300,"world_W_prime_answer":250}})

records.append({"id":"gsm8k_44_robustness","source_index":44,"variant_type":"robustness",
"question":"James, a freshman at a Chicago university, has one thousand dollars per semester. He allocates thirty percent to food, fifteen percent to housing, one-quarter to leisure activities, and the remainder to academic supplies. How much does he allocate to academic supplies?",
"output":"## Causal Reasoning Analysis\n\n**Parsing non-standard expressions:**\n- 'One thousand dollars' $= \\$1{,}000$\n- 'Thirty percent' $= 30\\%$; 'fifteen percent' $= 15\\%$\n- 'One-quarter' $= 25\\%$\n- 'Leisure activities' = entertainment; 'academic supplies' = coursework materials\n\n**Computation:**\nCoursework $= 1000 \\times (1 - 0.30 - 0.15 - 0.25) = 1000 \\times 0.30 = \\$300$.\n\n**Robustness confirmed:** 'One-quarter' and synonym substitutions do not alter the causal structure.\n\n**Answer: $300**",
"answer":300,"metadata":{"rephrased_values":{"entertainment":"leisure activities","coursework":"academic supplies","25pct":"one-quarter"}}})

records.append({"id":"gsm8k_44_mediation","source_index":44,"variant_type":"mediation",
"question":"James: $1000 budget; food=30%, accom=15%, entertainment=25%. Treat 'non_coursework_spending' (M) as mediator between 'total_budget' (X) and 'coursework_spending' (Y). Decompose NDE, NIE, TE for ΔX=$100.",
"output":"## Causal Reasoning Analysis\n\n**Causal DAG:** $X(\\text{total budget}) \\rightarrow M(\\text{non-coursework}) \\rightarrow Y(\\text{coursework})$.\n\n**Structural equations:**\n$$M = (0.30 + 0.15 + 0.25)X = 0.70X, \\quad Y = X - M = 0.30X$$\n\n**Baseline:** $X=1000,\\ M=700,\\ Y=300$.\n\n**TE** ($X: 1000 \\to 1100$): $Y(1100) = 0.30 \\times 1100 = 330$; $TE = +\\$30$.\n\n**NDE** (fix $M=700$, change $X: 1000 \\to 1100$): $Y_{NDE} = 1100 - 700 = 400$; $NDE = +\\$100$.\n\n**NIE:** $NIE = TE - NDE = -\\$70$.\n\n**Interpretation (DE/IE path decomposition):** A \\$100 budget increase directly adds \\$100 to coursework (NDE), but the 70% non-coursework allocation absorbs \\$70 via the mediator (NIE $= -\\$70$). Net TE $= +\\$30$. ✓\n\n**Answer: NDE=+$100, NIE=-$70, TE=+$30 per $100 increase in total budget**",
"answer":{"NDE":100,"NIE":-70,"TE":30},"metadata":{"mediator":"non_coursework_spending","X":"total_budget","Y":"coursework_spending","delta_X":100}})

print("[Batch Update] Seeds processed: 20/25 | Total variants saved: 100")

# ─────────────────────────────────────────────
# Index 45: Ava piñata
# Piñata=$13. Reese's=4×$9=$36. Snickers=3×$5=$15. Skittles=5×$7=$35. Total=$99
# A: 99
# ─────────────────────────────────────────────
records.append({"id":"gsm8k_45_spurious","source_index":45,"variant_type":"spurious",
"question":"It's Ava's birthday party. Her parents bought a unicorn piñata for $13 and filled it with all of her favorite treats. They bought 4 bags of Reese's for $9 per bag, 3 bags of Snickers for $5 per bag, and 5 bags of Skittles for $7 per bag. How much did the unicorn piñata and the treats cost altogether? Ava is turning 7 and the party is in the backyard.",
"output":"## Causal Reasoning Analysis\n\n**Spurious Facts Introduced:**\n1. Ava is turning 7.\n2. The party is in the backyard.\n\n**Causal Validity Check:**\n- Piñata: $\\$13$\n- Reese's: $4 \\times \\$9 = \\$36$\n- Snickers: $3 \\times \\$5 = \\$15$\n- Skittles: $5 \\times \\$7 = \\$35$\n- Total: $\\$13 + \\$36 + \\$15 + \\$35 = \\$99$\n\nAge and venue are d-separated from costs. $P(\\text{total} \\mid \\text{age 7, backyard}) = \\$99$.\n\n**Answer: $99**",
"answer":99,"metadata":{"spurious_facts":["turning 7","party in backyard"]}})

records.append({"id":"gsm8k_45_intervention","source_index":45,"variant_type":"intervention",
"question":"Ava's party: piñata=$13, 4 Reese's@$9, 3 Snickers@$5, 5 Skittles@$7. Suppose we intervene do(reeses_bags=6 instead of 4). What is the total cost?",
"output":"## Causal Reasoning Analysis\n\n**Intervention:** $do(n_R=6)$, overriding natural value $n_R=4$.\n\n**Post-intervention:**\n- Reese's: $6 \\times \\$9 = \\$54$\n- Rest: $\\$13 + \\$15 + \\$35 = \\$63$ (unchanged)\n- Total: $\\$54 + \\$63 = \\$117$\n\n**Causal effect:** $\\Delta = 117 - 99 = +\\$18$. Each additional Reese's bag adds \\$9 to the total.\n\n**Answer under intervention: $117**",
"answer":117,"metadata":{"intervention_var":"reeses_bags","original_value":4,"intervened_value":6}})

records.append({"id":"gsm8k_45_counterfactual","source_index":45,"variant_type":"counterfactual",
"question":"Ava's party: piñata=$13, Reese's=$36, Snickers=$15, Skittles=$35, total=$99. In a counterfactual world where the piñata costs twice as much as the most expensive candy category, what would the total be?",
"output":"## Causal Reasoning Analysis\n\n**Actual World (W):** Piñata $= \\$13$; most expensive candy $=$ Reese's $= \\$36$; total $= \\$99$.\n\n**Counterfactual World (W'):** Modified structural rule: piñata $= 2 \\times \\max(\\$36, \\$15, \\$35) = 2 \\times \\$36 = \\$72$.\n- Candy total: $\\$36 + \\$15 + \\$35 = \\$86$ (unchanged)\n- Grand total: $\\$72 + \\$86 = \\$158$\n\n**Counterfactual contrast:** $\\Delta = 158 - 99 = +\\$59$. The piñata price rule change adds \\$59.\n\n**Answer in counterfactual world: $158**",
"answer":158,"metadata":{"modified_equation":"pinata = 2*max_candy_category","world_W_answer":99,"world_W_prime_answer":158}})

records.append({"id":"gsm8k_45_robustness","source_index":45,"variant_type":"robustness",
"question":"For Ava's birthday celebration, her parents purchased a unicorn piñata for thirteen dollars and filled it with sweets: four bags of Reese's at nine dollars per bag, three bags of Snickers at five dollars per bag, and five bags of Skittles at seven dollars per bag. What was the combined expenditure on the piñata and all the sweets?",
"output":"## Causal Reasoning Analysis\n\n**Parsing non-standard expressions:**\n- 'Thirteen dollars' $= \\$13$\n- 'Nine dollars per bag' $= \\$9$/bag, etc.\n- 'Combined expenditure' = total cost\n\n**Computation:**\n$13 + 4(9) + 3(5) + 5(7) = 13 + 36 + 15 + 35 = \\$99$.\n\n**Robustness confirmed:** Formal language and explicit dollar words do not alter the causal structure.\n\n**Answer: $99**",
"answer":99,"metadata":{"rephrased_values":{"$13":"thirteen dollars","total":"combined expenditure"}}})

records.append({"id":"gsm8k_45_mediation","source_index":45,"variant_type":"mediation",
"question":"Ava's party: piñata=$13, 4 Reese's@$9, 3 Snickers@$5, 5 Skittles@$7. Treat 'candy_total' (M) as mediator between 'reeses_price_per_bag' (X) and 'grand_total' (Y). Decompose NDE, NIE, TE for ΔX=$1.",
"output":"## Causal Reasoning Analysis\n\n**Causal DAG:** $X(\\text{Reese's price/bag}) \\rightarrow M(\\text{candy total}) \\rightarrow Y(\\text{grand total})$; piñata $= \\$13$ fixed.\n\n**Structural equations:**\n$$M = 4X + 3(5) + 5(7) = 4X + 50, \\quad Y = 13 + M = 4X + 63$$\n\n**Baseline:** $X=9,\\ M=86,\\ Y=99$.\n\n**TE** ($X: 9 \\to 10$): $Y(10) = 4(10) + 63 = 103$; $TE = +\\$4$.\n\n**NDE** (fix $M=86$, change $X: 9 \\to 10$): $Y_{NDE} = 13 + 86 = 99$; $NDE = 0$.\n\n**NIE:** $NIE = TE - NDE = +\\$4$.\n\n**Interpretation:** The entire effect of Reese's price on grand total is mediated through candy total. $NDE = 0$ (piñata cost is unaffected by candy price).\n\n**Answer: NDE=0, NIE=+$4, TE=+$4 per $1 increase in Reese's price per bag**",
"answer":{"NDE":0,"NIE":4,"TE":4},"metadata":{"mediator":"candy_total","X":"reeses_price_per_bag","Y":"grand_total","delta_X":1}})

print("[Batch Update] Seeds processed: 21/25 | Total variants saved: 105")

# ─────────────────────────────────────────────
# Index 46: Carolyn piano violin
# Piano=20/day; violin=3×20=60/day; total/day=80; per week=80×6=480; per month=480×4=1920
# A: 1920
# ─────────────────────────────────────────────
records.append({"id":"gsm8k_46_spurious","source_index":46,"variant_type":"spurious",
"question":"Carolyn practices the piano for 20 minutes a day and the violin for three times as long. If she practices six days a week, how many minutes does she spend practicing in a month with four weeks? Carolyn is preparing for a recital and she practices in the morning.",
"output":"## Causal Reasoning Analysis\n\n**Spurious Facts Introduced:**\n1. Carolyn is preparing for a recital.\n2. She practices in the morning.\n\n**Causal Validity Check:**\n- Violin: $3 \\times 20 = 60$ min/day\n- Daily total: $20 + 60 = 80$ min/day\n- Weekly: $80 \\times 6 = 480$ min/week\n- Monthly: $480 \\times 4 = 1{,}920$ min\n\nRecital preparation and practice timing are d-separated from duration calculations. $P(\\text{monthly} \\mid \\text{recital, morning}) = 1{,}920$.\n\n**Answer: 1,920 minutes**",
"answer":1920,"metadata":{"spurious_facts":["preparing for recital","practices in morning"]}})

records.append({"id":"gsm8k_46_intervention","source_index":46,"variant_type":"intervention",
"question":"Carolyn: piano=20min/day, violin=3×piano, 6 days/week, 4 weeks/month. Suppose we intervene do(violin_multiplier=4 instead of 3). How many minutes does she practice per month?",
"output":"## Causal Reasoning Analysis\n\n**Intervention:** $do(k=4)$, overriding natural value $k=3$.\n\n**Post-intervention:**\n- Violin: $4 \\times 20 = 80$ min/day\n- Daily total: $20 + 80 = 100$ min\n- Weekly: $100 \\times 6 = 600$ min\n- Monthly: $600 \\times 4 = 2{,}400$ min\n\n**Causal effect:** $\\Delta = 2400 - 1920 = +480$ min/month. Each unit increase in violin multiplier adds $20 \\times 6 \\times 4 = 480$ minutes per month.\n\n**Answer under intervention: 2,400 minutes**",
"answer":2400,"metadata":{"intervention_var":"violin_multiplier","original_value":3,"intervened_value":4}})

records.append({"id":"gsm8k_46_counterfactual","source_index":46,"variant_type":"counterfactual",
"question":"Carolyn: piano=20/day, violin=3×piano, 6 days/week, 4 weeks/month=1920. In a counterfactual world where she practices 7 days a week (not 6), how many minutes per month?",
"output":"## Causal Reasoning Analysis\n\n**Actual World (W):** 6 days/week; monthly $= 1{,}920$ min.\n\n**Counterfactual World (W'):** Modified structural rule: practice days $= 7$/week.\n- Daily total: $80$ min (unchanged)\n- Weekly: $80 \\times 7 = 560$ min\n- Monthly: $560 \\times 4 = 2{,}240$ min\n\n**Counterfactual contrast:** $\\Delta = 2240 - 1920 = +320$ min. Adding one rest-day to the practice schedule gains one extra day per week.\n\n**Answer in counterfactual world: 2,240 minutes**",
"answer":2240,"metadata":{"modified_equation":"practice_days_per_week=7","world_W_answer":1920,"world_W_prime_answer":2240}})

records.append({"id":"gsm8k_46_robustness","source_index":46,"variant_type":"robustness",
"question":"Carolyn devotes twenty minutes daily to the piano and thrice that duration to the violin. She rehearses six days each week. In a four-week month, what is the aggregate practice time in minutes?",
"output":"## Causal Reasoning Analysis\n\n**Parsing non-standard expressions:**\n- 'Twenty minutes daily' $= 20$ min/day\n- 'Thrice that duration' $= 3 \\times 20 = 60$ min\n- 'Six days each week' = 6 days\n- 'Aggregate practice time' = total minutes\n\n**Computation:**\n$(20+60) \\times 6 \\times 4 = 80 \\times 24 = 1{,}920$ min.\n\n**Robustness confirmed:** 'Thrice', 'aggregate', and formal phrasing do not alter the causal structure.\n\n**Answer: 1,920 minutes**",
"answer":1920,"metadata":{"rephrased_values":{"3×":"thrice","total":"aggregate","practices":"rehearses"}}})

records.append({"id":"gsm8k_46_mediation","source_index":46,"variant_type":"mediation",
"question":"Carolyn: piano=20/day, violin=3×piano, 6 days/week, 4 weeks/month. Treat 'daily_practice_minutes' (M) as mediator between 'piano_minutes' (X) and 'monthly_total' (Y). Decompose NDE, NIE, TE for ΔX=5.",
"output":"## Causal Reasoning Analysis\n\n**Causal DAG:** $X(\\text{piano min/day}) \\rightarrow M(\\text{daily total}) \\rightarrow Y(\\text{monthly total})$.\n\n**Structural equations:**\n$$M = X + 3X = 4X, \\quad Y = M \\times 6 \\times 4 = 24M = 96X$$\n\n**Baseline:** $X=20,\\ M=80,\\ Y=1920$.\n\n**TE** ($X: 20 \\to 25$): $Y(25) = 96 \\times 25 = 2400$; $TE = +480$ min.\n\n**NDE** (fix $M=80$, change $X: 20 \\to 25$): $Y_{NDE} = 80 \\times 24 = 1920$; $NDE = 0$.\n\n**NIE:** $NIE = TE - NDE = +480$ min.\n\n**Interpretation:** The entire effect of piano practice time on monthly total is mediated through daily practice total. $NDE = 0$.\n\n**Answer: NDE=0, NIE=+480, TE=+480 per 5-minute increase in daily piano time**",
"answer":{"NDE":0,"NIE":480,"TE":480},"metadata":{"mediator":"daily_practice_minutes","X":"piano_minutes","Y":"monthly_total","delta_X":5}})

print("[Batch Update] Seeds processed: 22/25 | Total variants saved: 110")

# ─────────────────────────────────────────────
# Index 47: File download
# First 60MB at 5MB/s = 12s. Remaining 30MB at 10MB/s = 3s. Total = 15s
# A: 15
# ─────────────────────────────────────────────
records.append({"id":"gsm8k_47_spurious","source_index":47,"variant_type":"spurious",
"question":"The file, 90 megabytes in size, downloads at the rate of 5 megabytes per second for its first 60 megabytes, and then 10 megabytes per second thereafter. How long, in seconds, does it take to download entirely? The file is a video game update and the server is located in Japan.",
"output":"## Causal Reasoning Analysis\n\n**Spurious Facts Introduced:**\n1. The file is a video game update.\n2. The server is located in Japan.\n\n**Causal Validity Check:**\n- Phase 1: $60 \\text{ MB} / 5 \\text{ MB/s} = 12$ s\n- Remaining: $90 - 60 = 30$ MB\n- Phase 2: $30 \\text{ MB} / 10 \\text{ MB/s} = 3$ s\n- Total: $12 + 3 = 15$ s\n\nFile type and server location are d-separated from download time. $P(\\text{time} \\mid \\text{game update, Japan}) = 15$ s.\n\n**Answer: 15 seconds**",
"answer":15,"metadata":{"spurious_facts":["video game update","server in Japan"]}})

records.append({"id":"gsm8k_47_intervention","source_index":47,"variant_type":"intervention",
"question":"90MB file: first 60MB at 5MB/s, remaining at 10MB/s. Suppose we intervene do(phase1_speed=7.5MB/s instead of 5MB/s). How long does the download take?",
"output":"## Causal Reasoning Analysis\n\n**Intervention:** $do(s_1 = 7.5)$ MB/s, overriding natural value $s_1 = 5$ MB/s.\n\n**Post-intervention:**\n- Phase 1: $60 / 7.5 = 8$ s\n- Phase 2: $30 / 10 = 3$ s (unchanged)\n- Total: $8 + 3 = 11$ s\n\n**Causal effect:** $\\Delta = 11 - 15 = -4$ s. Increasing phase-1 speed by 1.5× saves 4 seconds.\n\n**Answer under intervention: 11 seconds**",
"answer":11,"metadata":{"intervention_var":"phase1_speed_MBps","original_value":5,"intervened_value":7.5}})

records.append({"id":"gsm8k_47_counterfactual","source_index":47,"variant_type":"counterfactual",
"question":"90MB file: 60MB at 5MB/s=12s, 30MB at 10MB/s=3s, total=15s. In a counterfactual world where the speed-threshold is 45MB (not 60MB), so the first 45MB download at 5MB/s and the rest at 10MB/s, how long would the download take?",
"output":"## Causal Reasoning Analysis\n\n**Actual World (W):** Threshold $= 60$ MB; total $= 15$ s.\n\n**Counterfactual World (W'):** Modified structural rule: threshold $= 45$ MB.\n- Phase 1: $45 / 5 = 9$ s\n- Remaining: $90 - 45 = 45$ MB\n- Phase 2: $45 / 10 = 4.5$ s\n- Total: $9 + 4.5 = 13.5$ s\n\n**Counterfactual contrast:** $\\Delta = 13.5 - 15 = -1.5$ s. Moving 15 MB from the slower phase to the faster phase saves 1.5 s.\n\n**Answer in counterfactual world: 13.5 seconds**",
"answer":13.5,"metadata":{"modified_equation":"speed_threshold=45MB","world_W_answer":15,"world_W_prime_answer":13.5}})

records.append({"id":"gsm8k_47_robustness","source_index":47,"variant_type":"robustness",
"question":"A ninety-megabyte archive transfers at five megabytes per second for its initial sixty megabytes, then accelerates to ten megabytes per second for the remainder. How many seconds does the complete transfer require?",
"output":"## Causal Reasoning Analysis\n\n**Parsing non-standard expressions:**\n- 'Ninety-megabyte archive' = 90 MB file\n- 'Five megabytes per second' $= 5$ MB/s\n- 'Initial sixty megabytes' = first 60 MB\n- 'Accelerates to ten megabytes per second' $= 10$ MB/s\n- 'Complete transfer' = full download\n\n**Computation:**\n$60/5 + 30/10 = 12 + 3 = 15$ s.\n\n**Robustness confirmed:** 'Archive/transfer' vs 'file/download' and formal phrasing do not alter the causal structure.\n\n**Answer: 15 seconds**",
"answer":15,"metadata":{"rephrased_values":{"file":"archive","download":"transfer","90MB":"ninety-megabyte"}}})

records.append({"id":"gsm8k_47_mediation","source_index":47,"variant_type":"mediation",
"question":"90MB file: 60MB at 5MB/s, 30MB at 10MB/s. Treat 'phase1_time' (M) as mediator between 'phase1_speed' (X) and 'total_time' (Y). Decompose NDE, NIE, TE for ΔX=1 MB/s.",
"output":"## Causal Reasoning Analysis\n\n**Causal DAG:** $X(\\text{phase-1 speed}) \\rightarrow M(\\text{phase-1 time}) \\rightarrow Y(\\text{total time})$; phase-2 time $= 3$ s is fixed.\n\n**Structural equations:**\n$$M = 60/X, \\quad Y = M + 3 = 60/X + 3$$\n\n**Baseline:** $X=5,\\ M=12,\\ Y=15$.\n\n**TE** ($X: 5 \\to 6$): $Y(6) = 60/6 + 3 = 10 + 3 = 13$; $TE = -2$ s.\n\n**NDE** (fix $M=12$, change $X: 5 \\to 6$): $Y_{NDE} = 12 + 3 = 15$; $NDE = 0$.\n\n**NIE:** $NIE = TE - NDE = -2$ s.\n\n**Interpretation:** The entire effect of phase-1 speed on total download time is mediated through phase-1 time. $NDE = 0$.\n\n**Answer: NDE=0, NIE=-2s, TE=-2s per 1 MB/s increase in phase-1 speed**",
"answer":{"NDE":0,"NIE":-2,"TE":-2},"metadata":{"mediator":"phase1_time","X":"phase1_speed","Y":"total_time","delta_X":1}})

print("[Batch Update] Seeds processed: 23/25 | Total variants saved: 115")

# ─────────────────────────────────────────────
# Index 48: Sam Carlos Mina pi digits
# Mina=24; Carlos=24/6=4; Sam=4+6=10
# A: 10
# ─────────────────────────────────────────────
records.append({"id":"gsm8k_48_spurious","source_index":48,"variant_type":"spurious",
"question":"Sam memorized six more digits of pi than Carlos memorized. Mina memorized six times as many digits of pi as Carlos memorized. If Mina memorized 24 digits of pi, how many digits did Sam memorize? They are all members of the school math club and the competition is next Friday.",
"output":"## Causal Reasoning Analysis\n\n**Spurious Facts Introduced:**\n1. They are all members of the school math club.\n2. The competition is next Friday.\n\n**Causal Validity Check:**\nCarlos $= 24 / 6 = 4$ digits.\nSam $= 4 + 6 = 10$ digits.\n\nClub membership and competition date are d-separated from memorized digit counts. $P(\\text{Sam} \\mid \\text{math club, Friday}) = 10$.\n\n**Answer: 10 digits**",
"answer":10,"metadata":{"spurious_facts":["school math club","competition next Friday"]}})

records.append({"id":"gsm8k_48_intervention","source_index":48,"variant_type":"intervention",
"question":"Sam=Carlos+6. Mina=6×Carlos=24. Suppose we intervene do(mina_digits=36 instead of 24). How many digits did Sam memorize?",
"output":"## Causal Reasoning Analysis\n\n**Intervention:** $do(M=36)$, overriding natural value $M=24$.\n\n**Post-intervention:**\n- Carlos $= 36 / 6 = 6$ digits\n- Sam $= 6 + 6 = 12$ digits\n\n**Causal effect:** $\\Delta = 12 - 10 = +2$ digits. Each 6-digit increase in Mina's count adds 1 to Carlos (1/6) and 1 to Sam.\n\n**Answer under intervention: 12 digits**",
"answer":12,"metadata":{"intervention_var":"mina_digits","original_value":24,"intervened_value":36}})

records.append({"id":"gsm8k_48_counterfactual","source_index":48,"variant_type":"counterfactual",
"question":"Sam=Carlos+6; Mina=6×Carlos=24; Carlos=4; Sam=10. In a counterfactual world where the rule changes so that Mina memorized 4 times as many digits as Carlos (instead of 6 times), how many digits would Sam have memorized?",
"output":"## Causal Reasoning Analysis\n\n**Actual World (W):** Mina $= 6 \\times$ Carlos; Sam $= 10$.\n\n**Counterfactual World (W'):** Modified structural rule: Mina $= 4 \\times$ Carlos.\n$$24 = 4 \\times \\text{Carlos} \\Rightarrow \\text{Carlos} = 6$$\n$$\\text{Sam} = 6 + 6 = 12 \\text{ digits}$$\n\n**Counterfactual contrast:** $\\Delta = 12 - 10 = +2$ digits. Halving the Mina-to-Carlos multiplier doubles Carlos's count, adding 2 to Sam's.\n\n**Answer in counterfactual world: 12 digits**",
"answer":12,"metadata":{"modified_equation":"mina = 4*carlos","world_W_answer":10,"world_W_prime_answer":12}})

records.append({"id":"gsm8k_48_robustness","source_index":48,"variant_type":"robustness",
"question":"Samantha memorised half-a-dozen more digits of pi than Carlo. Mina committed six times as many digits to memory as Carlo. If Mina memorised twenty-four digits, how many digits of pi did Samantha memorise?",
"output":"## Causal Reasoning Analysis\n\n**Parsing non-standard expressions:**\n- 'Samantha' = Sam; 'Carlo' = Carlos (name variants)\n- 'Half-a-dozen more' $= 6$ more\n- 'Twenty-four' $= 24$\n- 'Committed to memory' = memorized\n\n**Computation:**\nCarlo $= 24/6 = 4$. Samantha $= 4 + 6 = 10$.\n\n**Robustness confirmed:** Name variants and archaic number expressions do not alter the causal structure.\n\n**Answer: 10 digits**",
"answer":10,"metadata":{"rephrased_values":{"Sam":"Samantha","Carlos":"Carlo","6":"half-a-dozen","24":"twenty-four"}}})

records.append({"id":"gsm8k_48_mediation","source_index":48,"variant_type":"mediation",
"question":"Sam=Carlos+6; Mina=6×Carlos=24 → Carlos=4 → Sam=10. Treat 'carlos_digits' (M) as mediator between 'mina_digits' (X) and 'sam_digits' (Y). Decompose NDE, NIE, TE for ΔX=6.",
"output":"## Causal Reasoning Analysis\n\n**Causal DAG:** $X(\\text{Mina}) \\rightarrow M(\\text{Carlos}) \\rightarrow Y(\\text{Sam})$.\n\n**Structural equations:**\n$$M = X/6, \\quad Y = M + 6 = X/6 + 6$$\n\n**Baseline:** $X=24,\\ M=4,\\ Y=10$.\n\n**TE** ($X: 24 \\to 30$): $Y(30) = 30/6 + 6 = 5 + 6 = 11$; $TE = +1$ digit.\n\n**NDE** (fix $M=4$, change $X: 24 \\to 30$): $Y_{NDE} = 4 + 6 = 10$; $NDE = 0$.\n\n**NIE:** $NIE = TE - NDE = +1$ digit.\n\n**Interpretation:** The entire effect of Mina's digit count on Sam's count is mediated through Carlos's count. $NDE = 0$ (Sam's +6 over Carlos is a fixed offset, unaffected by Mina directly).\n\n**Answer: NDE=0, NIE=+1, TE=+1 per 6-digit increase in Mina's count**",
"answer":{"NDE":0,"NIE":1,"TE":1},"metadata":{"mediator":"carlos_digits","X":"mina_digits","Y":"sam_digits","delta_X":6}})

print("[Batch Update] Seeds processed: 24/25 | Total variants saved: 120")

# ─────────────────────────────────────────────
# Index 49: Alan Ben Laurie shells
# Laurie=36; Ben=36/3=12; Alan=12*4=48
# A: 48
# ─────────────────────────────────────────────
records.append({"id":"gsm8k_49_spurious","source_index":49,"variant_type":"spurious",
"question":"On a school trip to the seashore, Alan and his friends collected shells. Alan collected four times as many shells as Ben did. Ben got a late start and only collected a third of what Laurie did. If Laurie collected 36 shells how many did Alan collect? The class trip was on a Tuesday and the weather was sunny.",
"output":"## Causal Reasoning Analysis\n\n**Spurious Facts Introduced:**\n1. The class trip was on a Tuesday.\n2. The weather was sunny.\n\n**Causal Validity Check:**\nBen $= 36 / 3 = 12$ shells.\nAlan $= 4 \\times 12 = 48$ shells.\n\nDay of week and weather are d-separated from shell counts. $P(\\text{Alan} \\mid \\text{Tuesday, sunny}) = 48$.\n\n**Answer: 48 shells**",
"answer":48,"metadata":{"spurious_facts":["class trip on Tuesday","sunny weather"]}})

records.append({"id":"gsm8k_49_intervention","source_index":49,"variant_type":"intervention",
"question":"Alan=4×Ben; Ben=Laurie/3; Laurie=36. Suppose we intervene do(laurie_shells=54 instead of 36). How many shells did Alan collect?",
"output":"## Causal Reasoning Analysis\n\n**Intervention:** $do(L=54)$, overriding natural value $L=36$.\n\n**Post-intervention (causal chain propagates):**\n- Ben $= 54 / 3 = 18$\n- Alan $= 4 \\times 18 = 72$\n\n**Causal effect:** $\\Delta = 72 - 48 = +24$ shells. Each 1-shell increase in Laurie's count adds $4/3 \\approx 1.33$ shells to Alan's total.\n\n**Answer under intervention: 72 shells**",
"answer":72,"metadata":{"intervention_var":"laurie_shells","original_value":36,"intervened_value":54}})

records.append({"id":"gsm8k_49_counterfactual","source_index":49,"variant_type":"counterfactual",
"question":"Laurie=36; Ben=1/3*Laurie=12; Alan=4*Ben=48. In a counterfactual world where Ben collected half of what Laurie did (instead of one-third), how many shells would Alan have collected?",
"output":"## Causal Reasoning Analysis\n\n**Actual World (W):** Ben's fraction of Laurie $= 1/3$; Alan $= 48$.\n\n**Counterfactual World (W'):** Modified structural rule: Ben $= 1/2 \\times$ Laurie.\n$$\\text{Ben}' = 36/2 = 18, \\quad \\text{Alan}' = 4 \\times 18 = 72$$\n\n**Counterfactual contrast:** $\\Delta = 72 - 48 = +24$ shells. Changing Ben's fraction from $1/3$ to $1/2$ (a 50% increase in Ben's share) doubles the gap through Alan's $4\\times$ multiplier.\n\n**Answer in counterfactual world: 72 shells**",
"answer":72,"metadata":{"modified_equation":"ben = laurie/2","world_W_answer":48,"world_W_prime_answer":72}})

records.append({"id":"gsm8k_49_robustness","source_index":49,"variant_type":"robustness",
"question":"During a coastal excursion, Alan and two companions gathered seashells. Alan amassed four times the number collected by Ben. Ben, having started late, gathered only one-third of Laurie's haul. Laurie collected three dozen shells. How many shells did Alan collect?",
"output":"## Causal Reasoning Analysis\n\n**Parsing non-standard expressions:**\n- 'Coastal excursion' = school trip to seashore\n- 'Amassed four times' $= 4\\times$\n- 'One-third of Laurie's haul' $= 1/3 \\times$ Laurie\n- 'Three dozen shells' $= 3 \\times 12 = 36$\n\n**Computation:**\nBen $= 36/3 = 12$. Alan $= 4 \\times 12 = 48$.\n\n**Robustness confirmed:** 'Excursion', 'amassed', and 'three dozen' do not alter the causal structure.\n\n**Answer: 48 shells**",
"answer":48,"metadata":{"rephrased_values":{"trip":"coastal excursion","collected":"amassed","36":"three dozen"}}})

records.append({"id":"gsm8k_49_mediation","source_index":49,"variant_type":"mediation",
"question":"Laurie=36; Ben=Laurie/3; Alan=4×Ben. Treat 'ben_shells' (M) as mediator between 'laurie_shells' (X) and 'alan_shells' (Y). Decompose NDE, NIE, TE for ΔX=3.",
"output":"## Causal Reasoning Analysis\n\n**Causal DAG:** $X(\\text{Laurie}) \\rightarrow M(\\text{Ben}) \\rightarrow Y(\\text{Alan})$.\n\n**Structural equations:**\n$$M = X/3, \\quad Y = 4M = 4X/3$$\n\n**Baseline:** $X=36,\\ M=12,\\ Y=48$.\n\n**TE** ($X: 36 \\to 39$): $Y(39) = 4 \\times 39/3 = 52$; $TE = +4$ shells.\n\n**NDE** (fix $M=12$, change $X: 36 \\to 39$): $Y_{NDE} = 4 \\times 12 = 48$; $NDE = 0$.\n\n**NIE:** $NIE = TE - NDE = +4$ shells.\n\n**Interpretation:** The entire effect of Laurie's shell count on Alan's count is fully mediated through Ben's count. $NDE = 0$ — there is no direct path from Laurie to Alan bypassing Ben.\n\n**Answer: NDE=0, NIE=+4, TE=+4 per 3-shell increase in Laurie's count**",
"answer":{"NDE":0,"NIE":4,"TE":4},"metadata":{"mediator":"ben_shells","X":"laurie_shells","Y":"alan_shells","delta_X":3}})

print("[Batch Update] Seeds processed: 25/25 | Total variants saved: 125")

# ─────────────────────────────────────────────
# Write all records to file (append mode)
# ─────────────────────────────────────────────
with open(OUT, 'a', encoding='utf-8') as f:
    for record in records:
        f.write(json.dumps(record, ensure_ascii=False) + '\n')

print(f"Done. Written {len(records)} records to {OUT}")

