import json

OUT = r'C:\Users\18366\Documents\trae_projects\Claude Code\causal-llm\data\causal_math_refined.jsonl'
records = []

# ─────────────────────────────────────────────
# Index 50: Gerald baseball supplies
# Total cost = 4*100=$400. Off-season months = 12-4=8.
# Monthly target = 400/8=$50. Chores/month = 50/10=5
# A: 5
# ─────────────────────────────────────────────
records.append({"id":"gsm8k_50_spurious","source_index":50,"variant_type":"spurious",
"question":"Gerald spends $100 a month on baseball supplies. His season is 4 months long. He wants to use the months he's not playing baseball to save up by raking, shoveling, and mowing lawns. He charges $10 for each. How many chores does he need to average a month to save up for his supplies? Gerald's favorite team is the Yankees and he keeps his equipment in a red bag.",
"output":"## Causal Reasoning Analysis\n\n**Spurious Facts Introduced:**\n1. Gerald's favorite team is the Yankees.\n2. He keeps his equipment in a red bag.\n\n**Causal Validity Check:**\nTotal seasonal cost: $4 \\times \\$100 = \\$400$.\nOff-season months: $12 - 4 = 8$.\nMonthly savings target: $\\$400 / 8 = \\$50$.\nChores per month: $\\$50 / \\$10 = 5$.\n\nTeam preference and bag colour are d-separated from the chore calculation. $P(\\text{chores/month} \\mid \\text{Yankees, red bag}) = 5$.\n\n**Answer: 5 chores per month**",
"answer":5,"metadata":{"spurious_facts":["favorite team is Yankees","equipment in red bag"]}})

records.append({"id":"gsm8k_50_intervention","source_index":50,"variant_type":"intervention",
"question":"Gerald: $100/month baseball supplies, 4-month season, earns $10/chore in off-season. Suppose we intervene do(season_length=6 months instead of 4). How many chores per month does he need to average?",
"output":"## Causal Reasoning Analysis\n\n**Intervention:** $do(s=6)$, overriding natural value $s=4$.\n\n**Post-intervention:**\n- Total cost: $6 \\times \\$100 = \\$600$\n- Off-season months: $12 - 6 = 6$\n- Monthly target: $\\$600 / 6 = \\$100$\n- Chores/month: $\\$100 / \\$10 = 10$\n\n**Causal effect:** $\\Delta = 10 - 5 = +5$ chores/month. A longer season both raises total cost and shrinks the saving window — a doubly compounding effect.\n\n**Answer under intervention: 10 chores per month**",
"answer":10,"metadata":{"intervention_var":"season_length_months","original_value":4,"intervened_value":6}})

records.append({"id":"gsm8k_50_counterfactual","source_index":50,"variant_type":"counterfactual",
"question":"Gerald: $100/month × 4-month season = $400 total; 8 off-season months; 5 chores/month @ $10. In a counterfactual world where the structural rule changes so that Gerald charges $1.50 per chore (instead of a flat $10), how many chores per month would he need?",
"output":"## Causal Reasoning Analysis\n\n**Actual World (W):** Chore rate $= \\$10$; chores/month $= 5$.\n\n**Counterfactual World (W'):** Modified structural rule: chore rate $= \\$1.50$.\n- Total cost: $\\$400$ (unchanged)\n- Monthly target: $\\$50$ (unchanged)\n- Chores/month: $\\$50 / \\$1.50 = 33.\\overline{3}$\n\n**Counterfactual contrast:** $\\Delta \\approx 33.3 - 5 = +28.3$ chores/month. A lower per-chore rate requires proportionally more chores.\n\n**Answer in counterfactual world: $\\approx33.3$ chores per month**",
"answer":33.33,"metadata":{"modified_equation":"chore_rate=1.50","world_W_answer":5,"world_W_prime_answer":33.33}})

records.append({"id":"gsm8k_50_robustness","source_index":50,"variant_type":"robustness",
"question":"Gerald shells out a hundred dollars every month for baseball gear. His playing season spans four months. During the eight months he is not playing, he earns money doing yard work — raking, shovelling, and mowing — charging ten dollars per job. How many jobs per month must he average to cover his seasonal gear costs?",
"output":"## Causal Reasoning Analysis\n\n**Parsing non-standard expressions:**\n- 'Shells out a hundred dollars' $= \\$100$/month\n- 'Spans four months' $= 4$ months; 'eight months' $= 12-4=8$\n- 'Ten dollars per job' $= \\$10$/chore\n- 'Yard work' = raking/shovelling/mowing\n\n**Computation:**\nTotal $= 4 \\times 100 = \\$400$. Monthly target $= 400/8 = \\$50$. Jobs $= 50/10 = 5$.\n\n**Robustness confirmed:** Informal phrasing and synonym substitutions do not alter the causal structure.\n\n**Answer: 5 chores per month**",
"answer":5,"metadata":{"rephrased_values":{"chores":"jobs","supplies":"gear","months":"season spans"}}})

records.append({"id":"gsm8k_50_mediation","source_index":50,"variant_type":"mediation",
"question":"Gerald: $100/month × season_length; off-season = 12 − season_length; chore_rate = $10. Treat 'total_seasonal_cost' (M) as mediator between 'season_length' (X) and 'chores_per_month' (Y). Decompose NDE, NIE, TE for ΔX=1 month.",
"output":"## Causal Reasoning Analysis\n\n**Causal DAG:** $X(\\text{season length}) \\rightarrow M(\\text{total cost}) \\rightarrow Y(\\text{chores/month})$; also $X$ affects off-season months directly.\n\n**Structural equations:**\n$$M = 100X$$\n$$\\text{off-season} = 12 - X$$\n$$Y = \\frac{M}{10 \\times (12-X)} = \\frac{100X}{10(12-X)} = \\frac{10X}{12-X}$$\n\n**Baseline:** $X=4,\\ M=400,\\ Y=5$.\n\n**TE** ($X: 4 \\to 5$): $Y(5) = 10(5)/(12-5) = 50/7 \\approx 7.14$; $TE \\approx +2.14$ chores.\n\n**NDE** (fix $M=400$, change $X: 4 \\to 5$): off-season $= 7$; $Y_{NDE} = 400/(10 \\times 7) \\approx 5.71$; $NDE \\approx +0.71$.\n\n**NIE:** $NIE = TE - NDE \\approx 2.14 - 0.71 = +1.43$.\n\n**Interpretation (DE/IE path decomposition):** A 1-month longer season raises chores/month by ≈2.14 total. The direct path (shorter off-season window, NDE≈+0.71) and the indirect path through higher total cost (NIE≈+1.43) together produce the compounding effect.\n\n**Answer: NDE≈+0.71, NIE≈+1.43, TE≈+2.14 per additional season month**",
"answer":{"NDE":0.71,"NIE":1.43,"TE":2.14},"metadata":{"mediator":"total_seasonal_cost","X":"season_length","Y":"chores_per_month","delta_X":1}})

print("[Batch Update] Seeds processed: 1/5 | Total variants saved: 5")

# ─────────────────────────────────────────────
# Index 51: Ann fabric curtains
# Bolt = 16×12 = 192 sq ft. Living room = 4×6 = 24. Bedroom = 2×4 = 8. Left = 160.
# A: 160
# ─────────────────────────────────────────────
records.append({"id":"gsm8k_51_spurious","source_index":51,"variant_type":"spurious",
"question":"Ann is cutting fabric to make curtains. She cuts a 4 foot by 6 foot rectangle for the living room, and a 2 foot by 4 foot rectangle for the bedroom. If the bolt of fabric is 16 feet by 12 feet, how much fabric is left in square feet? Ann is an experienced seamstress and she bought the fabric at a discount.",
"output":"## Causal Reasoning Analysis\n\n**Spurious Facts Introduced:**\n1. Ann is an experienced seamstress.\n2. She bought the fabric at a discount.\n\n**Causal Validity Check:**\nBolt area: $16 \\times 12 = 192$ sq ft.\nLiving room curtain: $4 \\times 6 = 24$ sq ft.\nBedroom curtain: $2 \\times 4 = 8$ sq ft.\nFabric left: $192 - 24 - 8 = 160$ sq ft.\n\nSewing experience and purchase price are d-separated from fabric area calculations. $P(\\text{left} \\mid \\text{experienced, discount}) = 160$.\n\n**Answer: 160 sq ft**",
"answer":160,"metadata":{"spurious_facts":["experienced seamstress","bought at discount"]}})

records.append({"id":"gsm8k_51_intervention","source_index":51,"variant_type":"intervention",
"question":"Ann: bolt=16×12=192 sq ft. Living room=4×6=24. Bedroom=2×4=8. Left=160. Suppose we intervene do(living_room_length=6ft instead of 4ft, width stays 6ft). How much fabric is left?",
"output":"## Causal Reasoning Analysis\n\n**Intervention:** $do(l_{LR}=6)$, overriding natural value $l_{LR}=4$.\n\n**Post-intervention:**\n- Living room curtain: $6 \\times 6 = 36$ sq ft\n- Bedroom curtain: $8$ sq ft (unchanged)\n- Left: $192 - 36 - 8 = 148$ sq ft\n\n**Causal effect:** $\\Delta = 148 - 160 = -12$ sq ft. Each 1-foot increase in living-room curtain length removes an additional 6 sq ft (one width-unit) from the remainder.\n\n**Answer under intervention: 148 sq ft**",
"answer":148,"metadata":{"intervention_var":"living_room_curtain_length_ft","original_value":4,"intervened_value":6}})

records.append({"id":"gsm8k_51_counterfactual","source_index":51,"variant_type":"counterfactual",
"question":"Ann: bolt=16×12=192 sq ft; living room=24 sq ft; bedroom=8 sq ft; left=160 sq ft. In a counterfactual world where the bolt is measured in metres and the structural rule changes to metric (1 ft ≈ 0.3048 m, so bolt ≈ 4.877m × 3.658m), but the curtain dimensions stay at 4ft×6ft and 2ft×4ft — i.e., the bolt area shrinks to 1.5× the combined curtain area rather than the original ratio — how much fabric (in sq ft) would be left?",
"output":"## Causal Reasoning Analysis\n\n**Actual World (W):** Bolt $= 192$ sq ft; curtains $= 32$ sq ft; left $= 160$ sq ft. Ratio: bolt/curtains $= 6$.\n\n**Counterfactual World (W'):** Modified structural rule: bolt area $= 1.5 \\times$ curtain area $= 1.5 \\times 32 = 48$ sq ft.\n- Left: $48 - 24 - 8 = 16$ sq ft\n\n**Counterfactual contrast:** $\\Delta = 16 - 160 = -144$ sq ft. The drastically smaller bolt leaves almost no remainder.\n\n**Answer in counterfactual world: 16 sq ft**",
"answer":16,"metadata":{"modified_equation":"bolt_area = 1.5*curtain_total","world_W_answer":160,"world_W_prime_answer":16}})

records.append({"id":"gsm8k_51_robustness","source_index":51,"variant_type":"robustness",
"question":"Anna is tailoring drapes from a bolt of cloth measuring sixteen feet by twelve feet. She trims a four-by-six-foot panel for the lounge and a two-by-four-foot panel for the sleeping quarters. How many square feet of cloth remain after cutting both panels?",
"output":"## Causal Reasoning Analysis\n\n**Parsing non-standard expressions:**\n- 'Anna' = Ann; 'drapes' = curtains; 'cloth' = fabric\n- 'Bolt of cloth' = bolt of fabric\n- 'Lounge' = living room; 'sleeping quarters' = bedroom\n- Dimensions unchanged: $16 \\times 12$, $4 \\times 6$, $2 \\times 4$\n\n**Computation:**\n$192 - 24 - 8 = 160$ sq ft.\n\n**Robustness confirmed:** Name variants and room synonyms do not alter the causal structure.\n\n**Answer: 160 sq ft**",
"answer":160,"metadata":{"rephrased_values":{"Ann":"Anna","curtains":"drapes","fabric":"cloth","living room":"lounge","bedroom":"sleeping quarters"}}})

records.append({"id":"gsm8k_51_mediation","source_index":51,"variant_type":"mediation",
"question":"Ann: bolt=16×12=192 sq ft; living-room cut=4×6=24; bedroom cut=2×4=8. Treat 'total_cut_area' (M) as mediator between 'bolt_area' (X) and 'fabric_left' (Y). Decompose NDE, NIE, TE for ΔX=24 sq ft (one extra bolt row).",
"output":"## Causal Reasoning Analysis\n\n**Causal DAG:** $X(\\text{bolt area}) \\rightarrow Y(\\text{fabric left})$ directly; $M(\\text{total cut}) = 32$ is fixed (independent of X).\n\n**Structural equations:**\n$$M = 24 + 8 = 32 \\text{ (fixed)}, \\quad Y = X - M = X - 32$$\n\n**Baseline:** $X=192,\\ M=32,\\ Y=160$.\n\n**TE** ($X: 192 \\to 216$): $Y(216) = 216 - 32 = 184$; $TE = +24$ sq ft.\n\n**NDE** (fix $M=32$, change $X: 192 \\to 216$): $Y_{NDE} = 216 - 32 = 184$; $NDE = +24$ sq ft.\n\n**NIE:** $NIE = TE - NDE = 0$.\n\n**Interpretation:** Since the cut area $M$ is causally independent of bolt size $X$, there is no indirect path. The entire effect is direct. $NIE = 0$.\n\n**Answer: NDE=+24 sq ft, NIE=0, TE=+24 sq ft per 24 sq ft increase in bolt area**",
"answer":{"NDE":24,"NIE":0,"TE":24},"metadata":{"mediator":"total_cut_area","X":"bolt_area","Y":"fabric_left","delta_X":24}})

print("[Batch Update] Seeds processed: 2/5 | Total variants saved: 10")

# ─────────────────────────────────────────────
# Index 52: Arnel pencils
# 5 friends × 8 each = 40 shared. 10 + 40 = 50 total. 50 / 10 boxes = 5/box.
# A: 5
# ─────────────────────────────────────────────
records.append({"id":"gsm8k_52_spurious","source_index":52,"variant_type":"spurious",
"question":"Arnel had ten boxes of pencils with the same number of pencils in each box. He kept ten pencils and shared the remaining pencils equally with his five friends. If his friends got eight pencils each, how many pencils are in each box? Arnel's pencils are yellow and he bought them at the school supply store.",
"output":"## Causal Reasoning Analysis\n\n**Spurious Facts Introduced:**\n1. Arnel's pencils are yellow.\n2. He bought them at the school supply store.\n\n**Causal Validity Check:**\nPencils shared: $5 \\times 8 = 40$.\nTotal pencils: $10 + 40 = 50$.\nPer box: $50 / 10 = 5$.\n\nPencil colour and purchase location are d-separated from the count. $P(\\text{per box} \\mid \\text{yellow, school store}) = 5$.\n\n**Answer: 5 pencils per box**",
"answer":5,"metadata":{"spurious_facts":["pencils are yellow","bought at school supply store"]}})

records.append({"id":"gsm8k_52_intervention","source_index":52,"variant_type":"intervention",
"question":"Arnel: 10 boxes of equal pencils. Kept 10, shared equally with 5 friends who got 8 each. Suppose we intervene do(pencils_per_friend=12 instead of 8). How many pencils are in each box?",
"output":"## Causal Reasoning Analysis\n\n**Intervention:** $do(p_f=12)$, overriding natural value $p_f=8$.\n\n**Post-intervention:**\n- Shared: $5 \\times 12 = 60$\n- Total: $10 + 60 = 70$\n- Per box: $70 / 10 = 7$\n\n**Causal effect:** $\\Delta = 7 - 5 = +2$ pencils/box. Each 1-pencil increase per friend adds $5/10 = 0.5$ pencils per box.\n\n**Answer under intervention: 7 pencils per box**",
"answer":7,"metadata":{"intervention_var":"pencils_per_friend","original_value":8,"intervened_value":12}})

records.append({"id":"gsm8k_52_counterfactual","source_index":52,"variant_type":"counterfactual",
"question":"Arnel: 10 boxes, kept 10, shared with 5 friends (8 each) → 5/box. In a counterfactual world where the sharing rule changes so that each friend gets TWICE what Arnel kept per friend (i.e., Arnel's 10 kept are divided into equal friend-shares, and each friend gets double that), how many pencils would be in each box?",
"output":"## Causal Reasoning Analysis\n\n**Actual World (W):** Each friend gets $8$; Arnel keeps $10$; total $= 50$; per box $= 5$.\n\n**Counterfactual World (W'):** Modified structural rule: Arnel's kept $= 10$; each friend gets $2 \\times (10/5) = 2 \\times 2 = 4$ pencils.\n- Shared: $5 \\times 4 = 20$\n- Total: $10 + 20 = 30$\n- Per box: $30 / 10 = 3$\n\n**Counterfactual contrast:** $\\Delta = 3 - 5 = -2$ pencils/box. The new sharing rule (friend share tied to Arnel's per-capita keep) reduces the total significantly.\n\n**Answer in counterfactual world: 3 pencils per box**",
"answer":3,"metadata":{"modified_equation":"friend_share = 2*(arnel_kept/num_friends)","world_W_answer":5,"world_W_prime_answer":3}})

records.append({"id":"gsm8k_52_robustness","source_index":52,"variant_type":"robustness",
"question":"Arnel possessed a dozen minus two boxes of pencils, each box containing an identical number. He retained ten pencils for himself and distributed the rest evenly among his five companions, each of whom received eight pencils. How many pencils did each box originally contain?",
"output":"## Causal Reasoning Analysis\n\n**Parsing non-standard expressions:**\n- 'A dozen minus two' $= 12 - 2 = 10$ boxes\n- 'Retained ten for himself' = kept 10\n- 'Five companions' = five friends; 'each received eight' = 8/friend\n\n**Computation:**\nShared $= 5 \\times 8 = 40$. Total $= 10 + 40 = 50$. Per box $= 50/10 = 5$.\n\n**Robustness confirmed:** Archaic phrasing and 'dozen minus two' for 10 do not alter the causal structure.\n\n**Answer: 5 pencils per box**",
"answer":5,"metadata":{"rephrased_values":{"10 boxes":"a dozen minus two boxes","friends":"companions"}}})

records.append({"id":"gsm8k_52_mediation","source_index":52,"variant_type":"mediation",
"question":"Arnel: 10 boxes; kept 10 pencils; shared with 5 friends (8 each). Treat 'total_pencils' (M) as mediator between 'pencils_per_friend' (X) and 'pencils_per_box' (Y). Decompose NDE, NIE, TE for ΔX=2.",
"output":"## Causal Reasoning Analysis\n\n**Causal DAG:** $X(\\text{per friend}) \\rightarrow M(\\text{total pencils}) \\rightarrow Y(\\text{per box})$; Arnel's keep $= 10$ fixed.\n\n**Structural equations:**\n$$M = 10 + 5X, \\quad Y = M/10 = 1 + 0.5X$$\n\n**Baseline:** $X=8,\\ M=50,\\ Y=5$.\n\n**TE** ($X: 8 \\to 10$): $Y(10) = 1 + 5 = 6$; $TE = +1$ pencil/box.\n\n**NDE** (fix $M=50$, change $X: 8 \\to 10$): $Y_{NDE} = 50/10 = 5$; $NDE = 0$.\n\n**NIE:** $NIE = TE - NDE = +1$.\n\n**Interpretation:** The entire effect of per-friend pencil count on per-box count is mediated through total pencil count. $NDE = 0$.\n\n**Answer: NDE=0, NIE=+1, TE=+1 per 2-pencil increase in per-friend share**",
"answer":{"NDE":0,"NIE":1,"TE":1},"metadata":{"mediator":"total_pencils","X":"pencils_per_friend","Y":"pencils_per_box","delta_X":2}})

print("[Batch Update] Seeds processed: 3/5 | Total variants saved: 15")

# ─────────────────────────────────────────────
# Index 53: Caleb ice cream vs frozen yoghurt
# Ice cream: 10×$4=$40. Yoghurt: 4×$1=$4. Difference=$36.
# A: 36
# ─────────────────────────────────────────────
records.append({"id":"gsm8k_53_spurious","source_index":53,"variant_type":"spurious",
"question":"Caleb bought 10 cartons of ice cream and 4 cartons of frozen yoghurt. Each carton of ice cream cost $4 and each carton of frozen yoghurt cost $1. How much more did Caleb spend on ice cream than on frozen yoghurt? Caleb is stocking up for a summer party and he prefers chocolate flavour.",
"output":"## Causal Reasoning Analysis\n\n**Spurious Facts Introduced:**\n1. Caleb is stocking up for a summer party.\n2. He prefers chocolate flavour.\n\n**Causal Validity Check:**\nIce cream: $10 \\times \\$4 = \\$40$.\nFrozen yoghurt: $4 \\times \\$1 = \\$4$.\nDifference: $\\$40 - \\$4 = \\$36$.\n\nOccasion and flavour preference are d-separated from the spending difference. $P(\\text{diff} \\mid \\text{party, chocolate}) = \\$36$.\n\n**Answer: $36**",
"answer":36,"metadata":{"spurious_facts":["stocking for summer party","prefers chocolate flavour"]}})

records.append({"id":"gsm8k_53_intervention","source_index":53,"variant_type":"intervention",
"question":"Caleb: 10 ice cream cartons @ $4, 4 yoghurt cartons @ $1. Suppose we intervene do(ice_cream_price=$6 per carton instead of $4). How much more does he spend on ice cream than yoghurt?",
"output":"## Causal Reasoning Analysis\n\n**Intervention:** $do(p_{IC}=\\$6)$, overriding natural value $p_{IC}=\\$4$.\n\n**Post-intervention:**\n- Ice cream: $10 \\times \\$6 = \\$60$\n- Yoghurt: $\\$4$ (unchanged)\n- Difference: $\\$60 - \\$4 = \\$56$\n\n**Causal effect:** $\\Delta = 56 - 36 = +\\$20$. Each \\$1 increase in ice cream price widens the gap by $10 \\times \\$1 = \\$10$.\n\n**Answer under intervention: $56**",
"answer":56,"metadata":{"intervention_var":"ice_cream_price","original_value":4,"intervened_value":6}})

records.append({"id":"gsm8k_53_counterfactual","source_index":53,"variant_type":"counterfactual",
"question":"Caleb: 10 ice cream @ $4=$40; 4 yoghurt @ $1=$4; diff=$36. In a counterfactual world where the pricing rule is reversed (ice cream costs $1 each and frozen yoghurt costs $4 each), how much more would he spend on ice cream than yoghurt?",
"output":"## Causal Reasoning Analysis\n\n**Actual World (W):** $p_{IC}=\\$4$, $p_{FY}=\\$1$; diff $= +\\$36$ (ice cream costlier).\n\n**Counterfactual World (W'):** Modified structural rule: $p_{IC}'=\\$1$, $p_{FY}'=\\$4$.\n- Ice cream: $10 \\times \\$1 = \\$10$\n- Yoghurt: $4 \\times \\$4 = \\$16$\n- Difference: $\\$10 - \\$16 = -\\$6$ (yoghurt is now costlier)\n\n**Counterfactual contrast:** $\\Delta = -6 - 36 = -\\$42$. Swapping the price rule flips the spending direction.\n\n**Answer in counterfactual world: −$6 (Caleb spends $6 more on yoghurt than ice cream)**",
"answer":-6,"metadata":{"modified_equation":"prices_swapped","world_W_answer":36,"world_W_prime_answer":-6}})

records.append({"id":"gsm8k_53_robustness","source_index":53,"variant_type":"robustness",
"question":"Caleb purchased a ten-pack of ice-cream tubs at four dollars apiece and a four-pack of frozen yoghurt tubs at one dollar apiece. By how many dollars did his ice-cream expenditure exceed his frozen-yoghurt expenditure?",
"output":"## Causal Reasoning Analysis\n\n**Parsing non-standard expressions:**\n- 'Ten-pack of ice-cream tubs' = 10 cartons of ice cream\n- 'Four dollars apiece' $= \\$4$ each\n- 'Four-pack of frozen yoghurt tubs' = 4 cartons of frozen yoghurt\n- 'One dollar apiece' $= \\$1$ each\n\n**Computation:**\n$10 \\times 4 - 4 \\times 1 = 40 - 4 = \\$36$.\n\n**Robustness confirmed:** 'Tubs', 'ten-pack', and 'apiece' do not alter the causal structure.\n\n**Answer: $36**",
"answer":36,"metadata":{"rephrased_values":{"cartons":"tubs","10 cartons":"ten-pack","each":"apiece"}}})

records.append({"id":"gsm8k_53_mediation","source_index":53,"variant_type":"mediation",
"question":"Caleb: 10 ice cream @ $4, 4 yoghurt @ $1. Treat 'ice_cream_spend' (M) as mediator between 'ice_cream_price' (X) and 'spending_difference' (Y). Decompose NDE, NIE, TE for ΔX=$1.",
"output":"## Causal Reasoning Analysis\n\n**Causal DAG:** $X(\\text{IC price}) \\rightarrow M(\\text{IC spend}) \\rightarrow Y(\\text{difference})$; yoghurt spend $= \\$4$ fixed.\n\n**Structural equations:**\n$$M = 10X, \\quad Y = M - 4 = 10X - 4$$\n\n**Baseline:** $X=4,\\ M=40,\\ Y=36$.\n\n**TE** ($X: 4 \\to 5$): $Y(5) = 50 - 4 = 46$; $TE = +\\$10$.\n\n**NDE** (fix $M=40$, change $X: 4 \\to 5$): $Y_{NDE} = 40 - 4 = 36$; $NDE = 0$.\n\n**NIE:** $NIE = TE - NDE = +\\$10$.\n\n**Interpretation:** The entire effect of ice cream price on the spending gap is mediated through ice cream total spend. $NDE = 0$.\n\n**Answer: NDE=0, NIE=+$10, TE=+$10 per $1 increase in ice cream price**",
"answer":{"NDE":0,"NIE":10,"TE":10},"metadata":{"mediator":"ice_cream_spend","X":"ice_cream_price","Y":"spending_difference","delta_X":1}})

print("[Batch Update] Seeds processed: 4/5 | Total variants saved: 20")

# ─────────────────────────────────────────────
# Index 54: Leah money dog
# Earned $28. Milkshake = 28/7 = $4. Left = 24. Savings = 24/2 = $12. Wallet = $12.
# Dog shreds all but $1. Lost = 12 - 1 = $11.
# A: 11
# ─────────────────────────────────────────────
records.append({"id":"gsm8k_54_spurious","source_index":54,"variant_type":"spurious",
"question":"Leah earned $28 working odd jobs around the neighborhood. She spent a seventh of it on a milkshake and put half of the rest in her savings account. She left the remaining money in her wallet. Her dog got ahold of her wallet and shredded all the money inside but $1. How many dollars did Leah lose? Leah's dog is a golden retriever named Max and she lives on Oak Street.",
"output":"## Causal Reasoning Analysis\n\n**Spurious Facts Introduced:**\n1. Leah's dog is a golden retriever named Max.\n2. She lives on Oak Street.\n\n**Causal Validity Check:**\nMilkshake: $\\$28 / 7 = \\$4$. Remaining: $\\$28 - \\$4 = \\$24$.\nSavings: $\\$24 / 2 = \\$12$. Wallet: $\\$12$.\nLost: $\\$12 - \\$1 = \\$11$.\n\nDog breed and street name are d-separated from the monetary loss. $P(\\text{lost} \\mid \\text{golden retriever, Oak St}) = \\$11$.\n\n**Answer: $11**",
"answer":11,"metadata":{"spurious_facts":["golden retriever named Max","lives on Oak Street"]}})

records.append({"id":"gsm8k_54_intervention","source_index":54,"variant_type":"intervention",
"question":"Leah: earned $28; spent 1/7 on milkshake; half the rest to savings; dog shreds wallet leaving $1. Suppose we intervene do(milkshake_fraction=1/4 instead of 1/7). How much did Leah lose?",
"output":"## Causal Reasoning Analysis\n\n**Intervention:** $do(f_m = 1/4)$, overriding natural value $f_m = 1/7$.\n\n**Post-intervention:**\n- Milkshake: $\\$28 / 4 = \\$7$\n- Remaining: $\\$28 - \\$7 = \\$21$\n- Savings: $\\$21 / 2 = \\$10.50$\n- Wallet: $\\$10.50$\n- Lost: $\\$10.50 - \\$1 = \\$9.50$\n\n**Causal effect:** $\\Delta = 9.50 - 11 = -\\$1.50$. A larger milkshake fraction leaves less in the wallet, reducing the loss.\n\n**Answer under intervention: $9.50**",
"answer":9.50,"metadata":{"intervention_var":"milkshake_fraction","original_value":"1/7","intervened_value":"1/4"}})

records.append({"id":"gsm8k_54_counterfactual","source_index":54,"variant_type":"counterfactual",
"question":"Leah: $28 earned; $4 milkshake; $12 wallet; dog leaves $1; lost=$11. In a counterfactual world where the savings rule changes to 'put two-thirds of the rest in savings (instead of half)', how much would Leah lose?",
"output":"## Causal Reasoning Analysis\n\n**Actual World (W):** Savings fraction $= 1/2$; wallet $= \\$12$; lost $= \\$11$.\n\n**Counterfactual World (W'):** Modified structural rule: savings fraction $= 2/3$.\n- After milkshake: $\\$24$\n- Savings: $2/3 \\times \\$24 = \\$16$\n- Wallet: $\\$24 - \\$16 = \\$8$\n- Dog leaves $\\$1$\n- Lost: $\\$8 - \\$1 = \\$7$\n\n**Counterfactual contrast:** $\\Delta = 7 - 11 = -\\$4$. Saving more (2/3 instead of 1/2) protects $4 more from the dog.\n\n**Answer in counterfactual world: $7**",
"answer":7,"metadata":{"modified_equation":"savings_fraction=2/3","world_W_answer":11,"world_W_prime_answer":7}})

records.append({"id":"gsm8k_54_robustness","source_index":54,"variant_type":"robustness",
"question":"Leah pocketed twenty-eight dollars from neighbourhood odd jobs. She blew one-seventh of her earnings on a milkshake and deposited half of what remained into her savings account. The balance stayed in her purse. Her pet dog raided the purse and destroyed every note except a single dollar bill. What was Leah's monetary loss?",
"output":"## Causal Reasoning Analysis\n\n**Parsing non-standard expressions:**\n- 'Twenty-eight dollars' $= \\$28$\n- 'One-seventh' $= 1/7$; 'half of what remained' $= 1/2$\n- 'Purse' = wallet; 'pet dog raided' = dog shredded\n- 'Every note except a single dollar bill' = all but $\\$1$\n\n**Computation:**\n$28/7 = \\$4$. Left: $\\$24$. Savings: $\\$12$. Purse: $\\$12$. Lost: $12-1 = \\$11$.\n\n**Robustness confirmed:** 'Purse', 'deposited', and word-form numbers do not alter the causal structure.\n\n**Answer: $11**",
"answer":11,"metadata":{"rephrased_values":{"wallet":"purse","$28":"twenty-eight dollars","1/7":"one-seventh"}}})

records.append({"id":"gsm8k_54_mediation","source_index":54,"variant_type":"mediation",
"question":"Leah: $28 earned; 1/7 milkshake; 1/2 of rest to savings; rest in wallet; dog leaves $1. Treat 'wallet_amount' (M) as mediator between 'savings_fraction' (X) and 'amount_lost' (Y). Decompose NDE, NIE, TE for ΔX=1/6 (from 1/2 to 2/3).",
"output":"## Causal Reasoning Analysis\n\n**Causal DAG:** $X(\\text{savings fraction}) \\rightarrow M(\\text{wallet}) \\rightarrow Y(\\text{lost})$.\n\n**Structural equations:**\nAfter milkshake: $\\$24$ (fixed).\n$$M = 24(1 - X), \\quad Y = M - 1 = 24(1-X) - 1 = 23 - 24X$$\n\n**Baseline:** $X=1/2,\\ M=12,\\ Y=11$.\n\n**TE** ($X: 1/2 \\to 2/3$): $Y(2/3) = 23 - 24(2/3) = 23 - 16 = 7$; $TE = -4$.\n\n**NDE** (fix $M=12$, change $X: 1/2 \\to 2/3$): $Y_{NDE} = 12 - 1 = 11$; $NDE = 0$.\n\n**NIE:** $NIE = TE - NDE = -4$.\n\n**Interpretation:** The entire effect of savings fraction on monetary loss is mediated through the wallet amount. Saving more (higher $X$) reduces $M$, which directly cuts the dog-destruction loss. $NDE = 0$.\n\n**Answer: NDE=0, NIE=-$4, TE=-$4 per 1/6 increase in savings fraction**",
"answer":{"NDE":0,"NIE":-4,"TE":-4},"metadata":{"mediator":"wallet_amount","X":"savings_fraction","Y":"amount_lost","delta_X":"1/6"}})

print("[Batch Update] Seeds processed: 5/5 | Total variants saved: 25")

# ─────────────────────────────────────────────
# Write all records to file (append mode)
# ─────────────────────────────────────────────
with open(OUT, 'a', encoding='utf-8') as f:
    for record in records:
        f.write(json.dumps(record, ensure_ascii=False) + '\n')

print(f"Done. Written {len(records)} records to {OUT}")
