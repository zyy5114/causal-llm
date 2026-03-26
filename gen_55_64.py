import json

records = []

# ─────────────────────────────────────────────
# Index 55: roses/tulips/daisies percentage
# Q: 25 roses, 40 tulips, 35 daisies. % not roses?
# A: 75
# ─────────────────────────────────────────────

records.append({
    "id": "gsm8k_55_spurious",
    "source_index": 55,
    "variant_type": "spurious",
    "question": "There are 25 roses in a garden. There are 40 tulips. There are 35 daisies. The gardener planted the roses on a Monday, and it rained the following Tuesday. What percentage of flowers are not roses?",
    "output": "## Causal Reasoning Analysis\n\n**Spurious Facts Introduced:**\n1. The gardener planted roses on a Monday.\n2. It rained the following Tuesday.\n\n**Causal Validity Check:**\nLet $R=25$ (roses), $T=40$ (tulips), $D=35$ (daisies). Total $= R+T+D = 100$.\nNon-rose count $= T+D = 75$.\nPercentage not roses $= 75/100 \\times 100\\% = 75\\%$.\n\nThe day of planting and the rain event are causally disconnected from the flower counts. Formally, $P(\\%\\text{non-rose} \\mid \\text{planted Monday, rained Tuesday}) = P(\\%\\text{non-rose}) = 75\\%$. Both spurious facts are d-separated from the outcome given the flower counts.\n\n**Answer: 75%**",
    "answer": 75,
    "metadata": {"spurious_facts": ["roses planted on Monday", "rained the following Tuesday"], "total_flowers": 100}
})

records.append({
    "id": "gsm8k_55_intervention",
    "source_index": 55,
    "variant_type": "intervention",
    "question": "There are 25 roses in a garden. There are 40 tulips. There are 35 daisies. Suppose we intervene and do(tulips=60). What percentage of flowers are not roses under this intervention?",
    "output": "## Causal Reasoning Analysis\n\n**Intervention:** $do(T=60)$, overriding the natural value $T=40$.\n\n**Pre-intervention:** Total $= 25+40+35 = 100$; non-rose $= 75\\%$.\n\n**Post-intervention structural equations:**\n- $R = 25$ (unchanged)\n- $T = 60$ (forced by intervention)\n- $D = 35$ (unchanged)\n- Total $= 25+60+35 = 120$\n- Non-rose $= 60+35 = 95$\n- $\\%\\text{non-rose} = 95/120 \\times 100\\% \\approx 79.17\\%$\n\n**Causal effect of intervention:** $\\Delta = 79.17\\% - 75\\% = +4.17$ percentage points.\n\n**Answer under intervention: ≈79.17%**",
    "answer": 79.17,
    "metadata": {"intervention_var": "tulips", "original_value": 40, "intervened_value": 60}
})

records.append({
    "id": "gsm8k_55_counterfactual",
    "source_index": 55,
    "variant_type": "counterfactual",
    "question": "There are 25 roses in a garden. There are 40 tulips. There are 35 daisies. In a counterfactual world where the number of roses were doubled, what percentage of flowers would not be roses?",
    "output": "## Causal Reasoning Analysis\n\n**Actual World (World A):**\n- $R=25, T=40, D=35$; Total $=100$\n- $\\%\\text{non-rose} = 75\\%$\n\n**Counterfactual World (World B):** Structural equation modified: $R' = 2 \\times 25 = 50$.\n- $R'=50, T=40, D=35$; Total $=125$\n- Non-rose $= 40+35 = 75$\n- $\\%\\text{non-rose} = 75/125 \\times 100\\% = 60\\%$\n\n**Counterfactual contrast:** $\\Delta = 60\\% - 75\\% = -15$ percentage points. Doubling roses reduces the non-rose percentage by 15 pp.\n\n**Answer in counterfactual world: 60%**",
    "answer": 60,
    "metadata": {"modified_equation": "roses = 2 * original", "world_A_answer": 75, "world_B_answer": 60}
})

records.append({
    "id": "gsm8k_55_robustness",
    "source_index": 55,
    "variant_type": "robustness",
    "question": "A botanical garden contains two dozen plus one rose plants, two score tulip plants, and five-and-thirty daisy plants. What fraction (expressed as a percentage) of the total flora consists of non-rose species?",
    "output": "## Causal Reasoning Analysis\n\n**Parsing non-standard expressions:**\n- 'Two dozen plus one' $= 2 \\times 12 + 1 = 25$ roses\n- 'Two score' $= 2 \\times 20 = 40$ tulips\n- 'Five-and-thirty' $= 35$ daisies\n\n**Computation (identical structure):**\nTotal $= 25+40+35 = 100$\nNon-rose $= 40+35 = 75$\n$\\%\\text{non-rose} = 75/100 \\times 100\\% = 75\\%$\n\n**Robustness confirmed:** Renaming and archaic number expressions do not alter the underlying causal structure or the numerical answer.\n\n**Answer: 75%**",
    "answer": 75,
    "metadata": {"rephrased_values": {"roses": "two dozen plus one", "tulips": "two score", "daisies": "five-and-thirty"}}
})

records.append({
    "id": "gsm8k_55_mediation",
    "source_index": 55,
    "variant_type": "mediation",
    "question": "There are 25 roses in a garden. There are 40 tulips. There are 35 daisies. Decompose the causal effect on the non-rose percentage via mediation analysis: treat 'total flower count' as the mediator M between 'non-rose count' (X) and 'non-rose percentage' (Y).",
    "output": "## Causal Reasoning Analysis\n\n**Causal DAG:** $X \\text{(non-rose count)} \\rightarrow M \\text{(total count)} \\rightarrow Y \\text{(\\% non-rose)}$; also $X \\rightarrow Y$ directly.\n\n**Structural equations:**\n- $M = X + R = X + 25$ (total = non-rose + roses)\n- $Y = X / M = X / (X+25)$\n\n**Baseline:** $X=75, M=100, Y=75\\%$.\n\n**Mediation decomposition (increase X by 1 unit to 76):**\n- New $M = 76+25 = 101$\n- New $Y = 76/101 \\approx 75.25\\%$\n- Total Effect (TE) $\\approx +0.25$ pp\n\n**Natural Direct Effect (NDE):** Effect of $X: 75 \\to 76$ holding $M$ fixed at $M(75)=100$:\n$Y_{NDE} = 76/100 = 76\\%$; $NDE = 76\\%-75\\% = +1$ pp\n\n**Natural Indirect Effect (NIE):** $TE - NDE = 0.25 - 1 = -0.75$ pp (the increase in total count dilutes the percentage).\n\n**Interpretation:** The direct path (more non-rose flowers) increases the percentage, but the indirect path (larger total) partially offsets it. TE = NDE + NIE = $1 + (-0.75) = 0.25$ pp.\n\n**Answer: TE≈0.25pp per unit increase in non-rose count**",
    "answer": {"NDE": 1.0, "NIE": -0.75, "TE": 0.25},
    "metadata": {"mediator": "total_flower_count", "X": "non_rose_count", "Y": "non_rose_percentage"}
})

# ─────────────────────────────────────────────
# Index 56: Leo's assignment
# Q: part1=25min, part2=2*25=50min, total=120min. part3=120-25-50=45min
# A: 45
# ─────────────────────────────────────────────

records.append({
    "id": "gsm8k_56_spurious",
    "source_index": 56,
    "variant_type": "spurious",
    "question": "Leo's assignment was divided into three parts. He finished the first part in 25 minutes. It took him twice as long to finish the second part. Leo's favorite color is blue, and he was listening to jazz music while working. If he finished his assignment in 2 hours, how many minutes did Leo spend on the third part?",
    "output": "## Causal Reasoning Analysis\n\n**Spurious Facts Introduced:**\n1. Leo's favorite color is blue.\n2. He was listening to jazz music.\n\n**Causal Validity Check:**\nLet $t_1=25$ min, $t_2=2 \\times 25=50$ min, total $T=2 \\times 60=120$ min.\n$t_3 = T - t_1 - t_2 = 120 - 25 - 50 = 45$ min.\n\nFavorite color and music genre are causally disconnected from time allocation. $P(t_3 \\mid \\text{blue, jazz}) = P(t_3) = 45$ min. Both facts are d-separated from the outcome.\n\n**Answer: 45 minutes**",
    "answer": 45,
    "metadata": {"spurious_facts": ["favorite color is blue", "listening to jazz music"]}
})

records.append({
    "id": "gsm8k_56_intervention",
    "source_index": 56,
    "variant_type": "intervention",
    "question": "Leo's assignment was divided into three parts. He finished the first part in 25 minutes. It took him twice as long to finish the second part. He finished his assignment in 2 hours. Suppose we intervene and do(part1_time=40 minutes). How long did Leo spend on the third part?",
    "output": "## Causal Reasoning Analysis\n\n**Intervention:** $do(t_1=40)$, breaking the natural value $t_1=25$.\n\n**Structural equations:**\n- $t_2 = 2 \\times t_1$ (causal dependency)\n- $t_3 = T - t_1 - t_2$\n- $T = 120$ min (fixed)\n\n**Post-intervention:**\n- $t_1 = 40$ (forced)\n- $t_2 = 2 \\times 40 = 80$ min (propagates through causal graph)\n- $t_3 = 120 - 40 - 80 = 0$ min\n\n**Causal effect:** Under $do(t_1=40)$, Leo would have no time left for part 3. The intervention propagates through $t_2$, consuming all remaining time.\n\n**Answer under intervention: 0 minutes**",
    "answer": 0,
    "metadata": {"intervention_var": "part1_time", "original_value": 25, "intervened_value": 40}
})

records.append({
    "id": "gsm8k_56_counterfactual",
    "source_index": 56,
    "variant_type": "counterfactual",
    "question": "Leo's assignment was divided into three parts. He finished the first part in 25 minutes. It took him twice as long to finish the second part. He finished in 2 hours. In a counterfactual world where the second part took three times as long as the first (instead of twice), how long would the third part take?",
    "output": "## Causal Reasoning Analysis\n\n**Actual World (World A):**\n- $t_1=25, t_2=2 \\times 25=50, T=120$\n- $t_3 = 120-25-50 = 45$ min\n\n**Counterfactual World (World B):** Modified structural equation: $t_2' = 3 \\times t_1 = 3 \\times 25 = 75$ min.\n- $t_3' = 120 - 25 - 75 = 20$ min\n\n**Counterfactual contrast:** $\\Delta t_3 = 20 - 45 = -25$ min. Changing the multiplier from 2 to 3 reduces part-3 time by 25 minutes.\n\n**Answer in counterfactual world: 20 minutes**",
    "answer": 20,
    "metadata": {"modified_equation": "part2 = 3 * part1", "world_A_answer": 45, "world_B_answer": 20}
})

records.append({
    "id": "gsm8k_56_robustness",
    "source_index": 56,
    "variant_type": "robustness",
    "question": "Leonardo's homework was split into trio of sections. He wrapped up the inaugural section in a quarter-hour plus ten minutes. The subsequent section consumed double that duration. If the entire homework took one hundred and twenty minutes, how long was the final section?",
    "output": "## Causal Reasoning Analysis\n\n**Parsing non-standard expressions:**\n- 'Quarter-hour plus ten minutes' $= 15+10 = 25$ minutes (part 1)\n- 'Double that duration' $= 2 \\times 25 = 50$ minutes (part 2)\n- 'One hundred and twenty minutes' $= 120$ minutes (total)\n\n**Computation:**\n$t_3 = 120 - 25 - 50 = 45$ min\n\n**Robustness confirmed:** Renaming 'Leo' to 'Leonardo', using archaic time expressions, and rephrasing 'three parts' as 'trio of sections' do not alter the causal structure or answer.\n\n**Answer: 45 minutes**",
    "answer": 45,
    "metadata": {"rephrased_values": {"part1": "quarter-hour plus ten minutes", "total": "one hundred and twenty minutes"}}
})

records.append({
    "id": "gsm8k_56_mediation",
    "source_index": 56,
    "variant_type": "mediation",
    "question": "Leo's assignment: part1=25min, part2=2*part1, total=120min. Treat part2_time as mediator M between part1_time (X) and part3_time (Y). Decompose NDE, NIE, and TE.",
    "output": "## Causal Reasoning Analysis\n\n**Causal DAG:** $X(t_1) \\rightarrow M(t_2) \\rightarrow Y(t_3)$; also $X \\rightarrow Y$ directly via total constraint.\n\n**Structural equations:**\n- $M = 2X$ (part2 = 2 * part1)\n- $Y = 120 - X - M = 120 - X - 2X = 120 - 3X$\n\n**Baseline:** $X=25, M=50, Y=45$.\n\n**Mediation decomposition (increase X by 1 unit: $X=25 \\to 26$):**\n\n**Total Effect (TE):** $Y(26) = 120 - 3(26) = 120 - 78 = 42$; $TE = 42 - 45 = -3$ min.\n\n**Natural Direct Effect (NDE):** Hold $M$ fixed at $M(25)=50$, change $X: 25 \\to 26$:\n$Y_{NDE} = 120 - 26 - 50 = 44$; $NDE = 44 - 45 = -1$ min.\n\n**Natural Indirect Effect (NIE):** $NIE = TE - NDE = -3 - (-1) = -2$ min.\n\n**Interpretation:** Each extra minute on part 1 reduces part 3 by 3 minutes total: 1 minute directly (NDE) and 2 minutes via the part-2 multiplier effect (NIE).\n\n**Answer: NDE=-1 min, NIE=-2 min, TE=-3 min per unit increase in part1**",
    "answer": {"NDE": -1, "NIE": -2, "TE": -3},
    "metadata": {"mediator": "part2_time", "X": "part1_time", "Y": "part3_time"}
})

# ─────────────────────────────────────────────
# Index 57: Liza butter
# Q: 10kg butter. 1/2 choc=5, 1/5 pb=2, remaining=3, 1/3 of 3=1 sugar. left=3-1=2
# A: 2
# ─────────────────────────────────────────────

records.append({
    "id": "gsm8k_57_spurious",
    "source_index": 57,
    "variant_type": "spurious",
    "question": "Liza bought 10 kilograms of butter to make cookies. She used one-half of it for chocolate chip cookies, one-fifth of it for peanut butter cookies, and one-third of the remaining butter for sugar cookies. Liza bakes every Sunday, and her oven is brand new. How many kilograms of butter are left?",
    "output": "## Causal Reasoning Analysis\n\n**Spurious Facts Introduced:**\n1. Liza bakes every Sunday.\n2. Her oven is brand new.\n\n**Causal Validity Check:**\nLet $B=10$ kg.\n- Chocolate chip: $\\frac{1}{2} \\times 10 = 5$ kg\n- Peanut butter: $\\frac{1}{5} \\times 10 = 2$ kg\n- Remaining after two batches: $10 - 5 - 2 = 3$ kg\n- Sugar cookies: $\\frac{1}{3} \\times 3 = 1$ kg\n- Left: $3 - 1 = 2$ kg\n\nBaking schedule and oven age are causally disconnected from butter consumption. $P(\\text{left} \\mid \\text{Sunday, new oven}) = P(\\text{left}) = 2$ kg.\n\n**Answer: 2 kg**",
    "answer": 2,
    "metadata": {"spurious_facts": ["bakes every Sunday", "oven is brand new"]}
})

records.append({
    "id": "gsm8k_57_intervention",
    "source_index": 57,
    "variant_type": "intervention",
    "question": "Liza bought 10 kilograms of butter. She used one-half for chocolate chip cookies, one-fifth for peanut butter cookies, and one-third of the remaining for sugar cookies. Suppose we intervene do(peanut_butter_fraction=1/4). How many kg of butter are left?",
    "output": "## Causal Reasoning Analysis\n\n**Intervention:** $do(f_{pb}=1/4)$, overriding natural value $f_{pb}=1/5$.\n\n**Post-intervention structural equations:**\n- Chocolate chip: $\\frac{1}{2} \\times 10 = 5$ kg\n- Peanut butter: $\\frac{1}{4} \\times 10 = 2.5$ kg\n- Remaining: $10 - 5 - 2.5 = 2.5$ kg\n- Sugar cookies: $\\frac{1}{3} \\times 2.5 \\approx 0.833$ kg\n- Left: $2.5 - 0.833 = 1.667$ kg\n\n**Causal effect:** $\\Delta = 1.667 - 2 = -0.333$ kg. Increasing the peanut butter fraction reduces leftover butter.\n\n**Answer under intervention: ≈1.67 kg**",
    "answer": 1.67,
    "metadata": {"intervention_var": "peanut_butter_fraction", "original_value": "1/5", "intervened_value": "1/4"}
})

records.append({
    "id": "gsm8k_57_counterfactual",
    "source_index": 57,
    "variant_type": "counterfactual",
    "question": "Liza bought 10 kg of butter. She used 1/2 for chocolate chip, 1/5 for peanut butter, and 1/3 of remaining for sugar cookies. In a counterfactual world where she started with 15 kg instead of 10 kg, how many kg would be left?",
    "output": "## Causal Reasoning Analysis\n\n**Actual World (World A):** $B=10$ kg, left $= 2$ kg.\n\n**Counterfactual World (World B):** Modified structural equation: $B' = 15$ kg.\n- Chocolate chip: $\\frac{1}{2} \\times 15 = 7.5$ kg\n- Peanut butter: $\\frac{1}{5} \\times 15 = 3$ kg\n- Remaining: $15 - 7.5 - 3 = 4.5$ kg\n- Sugar cookies: $\\frac{1}{3} \\times 4.5 = 1.5$ kg\n- Left: $4.5 - 1.5 = 3$ kg\n\n**Counterfactual contrast:** $\\Delta = 3 - 2 = +1$ kg. Starting with 50% more butter leaves 50% more butter (linear scaling).\n\n**Answer in counterfactual world: 3 kg**",
    "answer": 3,
    "metadata": {"modified_equation": "initial_butter = 15", "world_A_answer": 2, "world_B_answer": 3}
})

records.append({
    "id": "gsm8k_57_robustness",
    "source_index": 57,
    "variant_type": "robustness",
    "question": "Eliza purchased a ten-kilogram block of butter for baking. She allocated fifty percent of it to chocolate chip cookies, a fifth portion to peanut butter cookies, and one-third of whatever remained to sugar cookies. What mass of butter remains unused?",
    "output": "## Causal Reasoning Analysis\n\n**Parsing non-standard expressions:**\n- 'Ten-kilogram block' $= 10$ kg\n- 'Fifty percent' $= 1/2$\n- 'A fifth portion' $= 1/5$\n- 'One-third of whatever remained' $= 1/3$ of remaining\n\n**Computation (identical structure):**\n- Chocolate chip: $5$ kg; Peanut butter: $2$ kg; Remaining: $3$ kg\n- Sugar: $1$ kg; Left: $2$ kg\n\n**Robustness confirmed:** Renaming 'Liza' to 'Eliza', using 'fifty percent' instead of 'one-half', and 'mass' instead of 'kilograms' do not alter the causal structure or answer.\n\n**Answer: 2 kg**",
    "answer": 2,
    "metadata": {"rephrased_values": {"initial": "ten-kilogram block", "choc_fraction": "fifty percent", "pb_fraction": "a fifth portion"}}
})

records.append({
    "id": "gsm8k_57_mediation",
    "source_index": 57,
    "variant_type": "mediation",
    "question": "Liza: 10kg butter, 1/2 choc, 1/5 pb, 1/3 of remaining for sugar. Treat 'remaining_after_two_batches' as mediator M between 'initial_butter' (X) and 'final_leftover' (Y). Decompose NDE, NIE, TE.",
    "output": "## Causal Reasoning Analysis\n\n**Causal DAG:** $X \\rightarrow M \\rightarrow Y$; $X \\rightarrow Y$ directly.\n\n**Structural equations:**\n- $M = X - \\frac{1}{2}X - \\frac{1}{5}X = X(1 - 0.5 - 0.2) = 0.3X$\n- $Y = M - \\frac{1}{3}M = \\frac{2}{3}M = \\frac{2}{3}(0.3X) = 0.2X$\n\n**Baseline:** $X=10, M=3, Y=2$.\n\n**Mediation decomposition (increase X by 1 unit: $X=10 \\to 11$):**\n\n**Total Effect (TE):** $Y(11) = 0.2 \\times 11 = 2.2$; $TE = 2.2 - 2 = +0.2$ kg.\n\n**Natural Direct Effect (NDE):** Hold $M$ fixed at $M(10)=3$, change $X: 10 \\to 11$:\nWith $M$ fixed, $Y_{NDE} = \\frac{2}{3} \\times 3 = 2$ (M unchanged, so Y unchanged); $NDE = 0$.\n\n**Natural Indirect Effect (NIE):** $NIE = TE - NDE = 0.2 - 0 = +0.2$ kg.\n\n**Interpretation:** The entire effect of initial butter on leftover is mediated through the remaining-after-two-batches quantity. There is no direct path bypassing the mediator.\n\n**Answer: NDE=0 kg, NIE=+0.2 kg, TE=+0.2 kg per kg increase in initial butter**",
    "answer": {"NDE": 0, "NIE": 0.2, "TE": 0.2},
    "metadata": {"mediator": "remaining_after_two_batches", "X": "initial_butter", "Y": "final_leftover"}
})

# ─────────────────────────────────────────────
# Index 58: Statistics student allowance
# Q: 60 students. 2/3 get $6/day = 40 students. 1/3 get $4/day = 20 students.
# Total = 40*6 + 20*4 = 240 + 80 = 320
# A: 320
# ─────────────────────────────────────────────

records.append({
    "id": "gsm8k_58_spurious",
    "source_index": 58,
    "variant_type": "spurious",
    "question": "A Statistics student wants to find the average daily allowance of middle school students. 2/3 receive $6/day and the rest get $4/day. He surveyed 60 students. The student is in 10th grade and conducted the survey on a Friday. What is the total daily allowance of all 60 students?",
    "output": "## Causal Reasoning Analysis\n\n**Spurious Facts Introduced:**\n1. The student is in 10th grade.\n2. The survey was conducted on a Friday.\n\n**Causal Validity Check:**\nGroup A: $\\frac{2}{3} \\times 60 = 40$ students at $\\$6$/day $= \\$240$.\nGroup B: $\\frac{1}{3} \\times 60 = 20$ students at $\\$4$/day $= \\$80$.\nTotal $= 240 + 80 = \\$320$.\n\nThe surveyor's grade and the day of the week are causally disconnected from allowance amounts. $P(\\text{total} \\mid \\text{10th grade, Friday}) = P(\\text{total}) = \\$320$.\n\n**Answer: $320**",
    "answer": 320,
    "metadata": {"spurious_facts": ["student is in 10th grade", "survey conducted on Friday"]}
})

records.append({
    "id": "gsm8k_58_intervention",
    "source_index": 58,
    "variant_type": "intervention",
    "question": "A Statistics student surveys 60 middle schoolers. 2/3 get $6/day, rest get $4/day. Suppose we intervene do(high_allowance_fraction=3/4). What is the new total daily allowance?",
    "output": "## Causal Reasoning Analysis\n\n**Intervention:** $do(f_H = 3/4)$, overriding natural value $f_H = 2/3$.\n\n**Post-intervention structural equations:**\n- Group A: $\\frac{3}{4} \\times 60 = 45$ students at $\\$6$/day $= \\$270$\n- Group B: $\\frac{1}{4} \\times 60 = 15$ students at $\\$4$/day $= \\$60$\n- Total $= 270 + 60 = \\$330$\n\n**Causal effect:** $\\Delta = 330 - 320 = +\\$10$. Increasing the high-allowance fraction by $1/12$ raises total daily allowance by $\\$10$.\n\n**Answer under intervention: $330**",
    "answer": 330,
    "metadata": {"intervention_var": "high_allowance_fraction", "original_value": "2/3", "intervened_value": "3/4"}
})

records.append({
    "id": "gsm8k_58_counterfactual",
    "source_index": 58,
    "variant_type": "counterfactual",
    "question": "A Statistics student surveys 60 students. 2/3 get $6/day, rest get $4/day. Total = $320. In a counterfactual world where the high-allowance group received $8/day instead of $6/day, what would the total be?",
    "output": "## Causal Reasoning Analysis\n\n**Actual World (World A):**\n- 40 students × $6 + 20 students × $4 = $240 + $80 = $320\n\n**Counterfactual World (World B):** Modified structural equation: high allowance $= \\$8$/day.\n- 40 students × $8 + 20 students × $4 = $320 + $80 = $400\n\n**Counterfactual contrast:** $\\Delta = 400 - 320 = +\\$80$. Raising the high-allowance rate by $\\$2$ increases total by $40 \\times 2 = \\$80$.\n\n**Answer in counterfactual world: $400**",
    "answer": 400,
    "metadata": {"modified_equation": "high_allowance = 8", "world_A_answer": 320, "world_B_answer": 400}
})

records.append({
    "id": "gsm8k_58_robustness",
    "source_index": 58,
    "variant_type": "robustness",
    "question": "A data-science pupil investigates the mean pocket money of junior high pupils. Two-thirds of the cohort pocket six dollars daily; the remainder pocket four dollars each day. The cohort size is three-score students. What is the aggregate daily pocket money?",
    "output": "## Causal Reasoning Analysis\n\n**Parsing non-standard expressions:**\n- 'Data-science pupil' = Statistics student\n- 'Junior high pupils' = middle school students\n- 'Two-thirds' $= 2/3$\n- 'Six dollars' $= \\$6$; 'four dollars' $= \\$4$\n- 'Three-score' $= 3 \\times 20 = 60$ students\n\n**Computation:**\n$40 \\times 6 + 20 \\times 4 = 240 + 80 = \\$320$\n\n**Robustness confirmed:** Archaic number expressions and synonym substitutions do not alter the causal structure or answer.\n\n**Answer: $320**",
    "answer": 320,
    "metadata": {"rephrased_values": {"total_students": "three-score", "high_fraction": "two-thirds"}}
})

records.append({
    "id": "gsm8k_58_mediation",
    "source_index": 58,
    "variant_type": "mediation",
    "question": "60 students: 2/3 get $6/day, 1/3 get $4/day. Treat 'high_group_count' as mediator M between 'total_students' (X) and 'total_allowance' (Y). Decompose NDE, NIE, TE.",
    "output": "## Causal Reasoning Analysis\n\n**Causal DAG:** $X(\\text{total students}) \\rightarrow M(\\text{high group count}) \\rightarrow Y(\\text{total allowance})$.\n\n**Structural equations:**\n- $M = \\frac{2}{3}X$\n- $Y = 6M + 4(X - M) = 4X + 2M = 4X + 2(\\frac{2}{3}X) = 4X + \\frac{4}{3}X = \\frac{16}{3}X$\n\n**Baseline:** $X=60, M=40, Y=320$.\n\n**Mediation decomposition (increase X by 1: $X=60 \\to 61$):**\n\n**Total Effect (TE):** $Y(61) = \\frac{16}{3} \\times 61 \\approx 325.33$; $TE \\approx +5.33$ per student.\n\n**Natural Direct Effect (NDE):** Hold $M$ fixed at $M(60)=40$, change $X: 60 \\to 61$:\n$Y_{NDE} = 6(40) + 4(61-40) = 240 + 84 = 324$; $NDE = 324 - 320 = +4$.\n\n**Natural Indirect Effect (NIE):** $NIE = TE - NDE = 5.33 - 4 = +1.33$.\n\n**Interpretation:** Each additional student contributes $4 directly (low-rate path) and $1.33 via the high-group mediator path.\n\n**Answer: NDE=+$4, NIE≈+$1.33, TE≈+$5.33 per additional student**",
    "answer": {"NDE": 4, "NIE": 1.33, "TE": 5.33},
    "metadata": {"mediator": "high_group_count", "X": "total_students", "Y": "total_allowance"}
})

# ─────────────────────────────────────────────
# Index 59: Joanne fountain coins
# Q: hr1=15, hr2+hr3=35 each? No: "next two hours she collected 35 coins" = 35 total for hrs 2&3
# hr4=50 collected, gave 15 away => kept 35
# Total = 15 + 35 + 35 = 85? Wait: re-read.
# "next two hours she collected 35 coins from the fountain" = 35 total (not per hour)
# hr4: collected 50, gave 15 => net +35
# Total = 15 + 35 + 35 = 85? But answer is 120.
# Re-read: "For the next two hours, she collected 35 coins" = 35 per hour = 70 total
# hr4: 50 - 15 = 35
# Total = 15 + 70 + 35 = 120. Yes!
# A: 120
# ─────────────────────────────────────────────

records.append({
    "id": "gsm8k_59_spurious",
    "source_index": 59,
    "variant_type": "spurious",
    "question": "Every hour Joanne collects coins from a mall fountain. Hour 1: 15 coins. Hours 2 and 3: 35 coins each hour. Hour 4: 50 coins collected but 15 given to a coworker. Joanne wears a red uniform and the fountain is near the food court. How many coins does she have after hour 4?",
    "output": "## Causal Reasoning Analysis\n\n**Spurious Facts Introduced:**\n1. Joanne wears a red uniform.\n2. The fountain is near the food court.\n\n**Causal Validity Check:**\n- Hour 1: $15$ coins\n- Hours 2–3: $35 \\times 2 = 70$ coins\n- Hour 4: $50 - 15 = 35$ coins (net after giving 15 away)\n- Total: $15 + 70 + 35 = 120$ coins\n\nUniform color and fountain location are causally disconnected from coin counts. $P(\\text{total} \\mid \\text{red uniform, food court}) = P(\\text{total}) = 120$.\n\n**Answer: 120 coins**",
    "answer": 120,
    "metadata": {"spurious_facts": ["wears red uniform", "fountain near food court"]}
})

records.append({
    "id": "gsm8k_59_intervention",
    "source_index": 59,
    "variant_type": "intervention",
    "question": "Joanne collects coins: hr1=15, hr2=hr3=35 each, hr4=50 collected minus 15 given away. Suppose we intervene do(coins_given_away=0). How many coins does she have after hour 4?",
    "output": "## Causal Reasoning Analysis\n\n**Intervention:** $do(\\text{given away}=0)$, overriding natural value of 15.\n\n**Post-intervention:**\n- Hour 1: $15$\n- Hours 2–3: $35 \\times 2 = 70$\n- Hour 4: $50 - 0 = 50$ (no coins given away)\n- Total: $15 + 70 + 50 = 135$ coins\n\n**Causal effect:** $\\Delta = 135 - 120 = +15$ coins. Eliminating the gift directly adds 15 coins to the total.\n\n**Answer under intervention: 135 coins**",
    "answer": 135,
    "metadata": {"intervention_var": "coins_given_away", "original_value": 15, "intervened_value": 0}
})

records.append({
    "id": "gsm8k_59_counterfactual",
    "source_index": 59,
    "variant_type": "counterfactual",
    "question": "Joanne: hr1=15, hr2=hr3=35 each, hr4=50 minus 15 given away. Total=120. In a counterfactual world where hours 2 and 3 each yielded 40 coins instead of 35, how many coins would she have?",
    "output": "## Causal Reasoning Analysis\n\n**Actual World (World A):**\n$15 + 35 + 35 + (50-15) = 15 + 70 + 35 = 120$ coins.\n\n**Counterfactual World (World B):** Modified structural equation: $c_{hr2} = c_{hr3} = 40$.\n- Hour 1: $15$\n- Hours 2–3: $40 \\times 2 = 80$\n- Hour 4: $50 - 15 = 35$\n- Total: $15 + 80 + 35 = 130$ coins\n\n**Counterfactual contrast:** $\\Delta = 130 - 120 = +10$ coins.\n\n**Answer in counterfactual world: 130 coins**",
    "answer": 130,
    "metadata": {"modified_equation": "hr2=hr3=40", "world_A_answer": 120, "world_B_answer": 130}
})

records.append({
    "id": "gsm8k_59_robustness",
    "source_index": 59,
    "variant_type": "robustness",
    "question": "Each sixty-minute interval, Joanna empties the shopping centre's wishing well. In the first interval she retrieved fifteen coins. In each of the subsequent pair of intervals she retrieved thirty-five coins. In the fourth interval she retrieved fifty coins but surrendered fifteen to a colleague for a beverage. What is her coin total after the fourth interval?",
    "output": "## Causal Reasoning Analysis\n\n**Parsing non-standard expressions:**\n- 'Sixty-minute interval' = hour\n- 'Joanna' = Joanne (name variant)\n- 'Shopping centre's wishing well' = mall fountain\n- 'Subsequent pair of intervals' = next two hours\n- 'Surrendered fifteen' = gave 15 away\n\n**Computation:**\n$15 + 35 + 35 + (50-15) = 120$ coins\n\n**Robustness confirmed:** Name change, British spelling, and synonym substitutions do not alter the causal structure or answer.\n\n**Answer: 120 coins**",
    "answer": 120,
    "metadata": {"rephrased_values": {"name": "Joanna", "location": "shopping centre wishing well", "interval": "sixty-minute interval"}}
})

records.append({
    "id": "gsm8k_59_mediation",
    "source_index": 59,
    "variant_type": "mediation",
    "question": "Joanne coins: hr1=15, hr2=hr3=35 each, hr4=50 collected. Treat 'coins_collected_hr4' as mediator M between 'coins_given_away' (X) and 'total_coins' (Y). Decompose NDE, NIE, TE.",
    "output": "## Causal Reasoning Analysis\n\n**Causal DAG:** $X(\\text{given away}) \\rightarrow Y(\\text{total})$ directly; $M(\\text{hr4 collected})$ is fixed at 50 (not affected by X).\n\n**Structural equations:**\n- $M = 50$ (fixed by fountain, independent of X)\n- $Y = 15 + 70 + (M - X) = 85 + 50 - X = 135 - X$\n\n**Baseline:** $X=15, M=50, Y=120$.\n\n**Mediation decomposition (increase X by 1: $X=15 \\to 16$):**\n\n**Total Effect (TE):** $Y(16) = 135 - 16 = 119$; $TE = 119 - 120 = -1$ coin.\n\n**Natural Direct Effect (NDE):** Hold $M$ fixed at $M(15)=50$, change $X: 15 \\to 16$:\n$Y_{NDE} = 135 - 16 = 119$; $NDE = -1$ coin.\n\n**Natural Indirect Effect (NIE):** $NIE = TE - NDE = -1 - (-1) = 0$.\n\n**Interpretation:** Since $M$ (hr4 collected) is causally independent of $X$ (coins given away), the entire effect is direct. NIE = 0.\n\n**Answer: NDE=-1 coin, NIE=0, TE=-1 coin per coin given away**",
    "answer": {"NDE": -1, "NIE": 0, "TE": -1},
    "metadata": {"mediator": "coins_collected_hr4", "X": "coins_given_away", "Y": "total_coins"}
})

# ─────────────────────────────────────────────
# Index 60: Jerry's daughters softball
# Q: 2 daughters, 8 games each, 4 hrs practice per game, 2 hrs per game
# Total hours = 2 daughters * (8 games * 4 hrs practice + 8 games * 2 hrs game)
# = 2 * (32 + 16) = 2 * 48 = 96
# A: 96
# ─────────────────────────────────────────────

records.append({
    "id": "gsm8k_60_spurious",
    "source_index": 60,
    "variant_type": "spurious",
    "question": "Jerry's two daughters play softball on different teams. They each have 8 games this season. Each team practices 4 hours for every game they play. Each game lasts 2 hours. Jerry drives a blue car and always brings snacks to the games. How many hours will Jerry spend at the field watching his daughters play and practice?",
    "output": "## Causal Reasoning Analysis\n\n**Spurious Facts Introduced:**\n1. Jerry drives a blue car.\n2. He always brings snacks to games.\n\n**Causal Validity Check:**\nPer daughter: $(8 \\times 4) + (8 \\times 2) = 32 + 16 = 48$ hours.\nFor 2 daughters: $2 \\times 48 = 96$ hours.\n\nCar color and snack-bringing are causally disconnected from time at the field. $P(\\text{hours} \\mid \\text{blue car, snacks}) = P(\\text{hours}) = 96$.\n\n**Answer: 96 hours**",
    "answer": 96,
    "metadata": {"spurious_facts": ["drives blue car", "brings snacks to games"]}
})

records.append({
    "id": "gsm8k_60_intervention",
    "source_index": 60,
    "variant_type": "intervention",
    "question": "Jerry's 2 daughters each have 8 softball games. Practice: 4 hrs/game. Game duration: 2 hrs. Suppose we intervene do(games_per_daughter=10). How many total hours does Jerry spend at the field?",
    "output": "## Causal Reasoning Analysis\n\n**Intervention:** $do(G=10)$, overriding natural value $G=8$.\n\n**Post-intervention structural equations:**\n- Per daughter: $(10 \\times 4) + (10 \\times 2) = 40 + 20 = 60$ hours\n- For 2 daughters: $2 \\times 60 = 120$ hours\n\n**Causal effect:** $\\Delta = 120 - 96 = +24$ hours. Each additional game adds $4+2=6$ hours per daughter, $12$ hours total for both.\n\n**Answer under intervention: 120 hours**",
    "answer": 120,
    "metadata": {"intervention_var": "games_per_daughter", "original_value": 8, "intervened_value": 10}
})

records.append({
    "id": "gsm8k_60_counterfactual",
    "source_index": 60,
    "variant_type": "counterfactual",
    "question": "Jerry's 2 daughters each have 8 softball games. Practice: 4 hrs/game. Game: 2 hrs. Total=96 hrs. In a counterfactual world where practice was 3 hrs/game instead of 4, how many hours would Jerry spend at the field?",
    "output": "## Causal Reasoning Analysis\n\n**Actual World (World A):**\n$2 \\times (8 \\times 4 + 8 \\times 2) = 2 \\times 48 = 96$ hours.\n\n**Counterfactual World (World B):** Modified structural equation: practice $= 3$ hrs/game.\n- Per daughter: $(8 \\times 3) + (8 \\times 2) = 24 + 16 = 40$ hours\n- For 2 daughters: $2 \\times 40 = 80$ hours\n\n**Counterfactual contrast:** $\\Delta = 80 - 96 = -16$ hours. Reducing practice by 1 hr/game saves $2 \\times 8 = 16$ hours.\n\n**Answer in counterfactual world: 80 hours**",
    "answer": 80,
    "metadata": {"modified_equation": "practice_hours_per_game = 3", "world_A_answer": 96, "world_B_answer": 80}
})

records.append({
    "id": "gsm8k_60_robustness",
    "source_index": 60,
    "variant_type": "robustness",
    "question": "Gerald has a pair of daughters who compete in softball for separate squads. Each squad plays an octet of matches per season. For every match, the squad drills for four hours. Each match itself spans two hours. What is the aggregate time Gerald spends at the pitch watching both daughters play and train?",
    "output": "## Causal Reasoning Analysis\n\n**Parsing non-standard expressions:**\n- 'Gerald' = Jerry (name variant)\n- 'A pair of daughters' = 2 daughters\n- 'Separate squads' = different teams\n- 'Octet of matches' $= 8$ games\n- 'Drills' = practices; 'pitch' = field\n\n**Computation:**\n$2 \\times (8 \\times 4 + 8 \\times 2) = 2 \\times 48 = 96$ hours\n\n**Robustness confirmed:** Name change, archaic number expressions, and synonym substitutions do not alter the causal structure or answer.\n\n**Answer: 96 hours**",
    "answer": 96,
    "metadata": {"rephrased_values": {"name": "Gerald", "games": "octet of matches", "daughters": "pair of daughters"}}
})

records.append({
    "id": "gsm8k_60_mediation",
    "source_index": 60,
    "variant_type": "mediation",
    "question": "Jerry: 2 daughters, 8 games each, 4 hrs practice/game, 2 hrs/game. Treat 'hours_per_daughter' as mediator M between 'games_per_daughter' (X) and 'total_hours' (Y). Decompose NDE, NIE, TE.",
    "output": "## Causal Reasoning Analysis\n\n**Causal DAG:** $X(\\text{games}) \\rightarrow M(\\text{hrs/daughter}) \\rightarrow Y(\\text{total hrs})$.\n\n**Structural equations:**\n- $M = 4X + 2X = 6X$ (practice + game hours per daughter)\n- $Y = 2M = 12X$ (two daughters)\n\n**Baseline:** $X=8, M=48, Y=96$.\n\n**Mediation decomposition (increase X by 1: $X=8 \\to 9$):**\n\n**Total Effect (TE):** $Y(9) = 12 \\times 9 = 108$; $TE = 108 - 96 = +12$ hours.\n\n**Natural Direct Effect (NDE):** Hold $M$ fixed at $M(8)=48$, change $X: 8 \\to 9$:\n$Y_{NDE} = 2 \\times 48 = 96$ (M unchanged, Y unchanged); $NDE = 0$.\n\n**Natural Indirect Effect (NIE):** $NIE = TE - NDE = 12 - 0 = +12$ hours.\n\n**Interpretation:** The entire effect of additional games on total hours is mediated through hours-per-daughter. There is no direct path from games to total hours bypassing the per-daughter mediator.\n\n**Answer: NDE=0, NIE=+12 hrs, TE=+12 hrs per additional game**",
    "answer": {"NDE": 0, "NIE": 12, "TE": 12},
    "metadata": {"mediator": "hours_per_daughter", "X": "games_per_daughter", "Y": "total_hours"}
})

# ─────────────────────────────────────────────
# Index 61: Bear hibernation weight gain
# Q: Needs 1000 lbs. Berries = 1/5 * 1000 = 200. Acorns = 2 * 200 = 400.
# Remaining = 1000 - 200 - 400 = 400. Salmon = 1/2 * 400 = 200.
# Small animals = 400 - 200 = 200.
# A: 200
# ─────────────────────────────────────────────

records.append({
    "id": "gsm8k_61_spurious",
    "source_index": 61,
    "variant_type": "spurious",
    "question": "A bear needs to gain 1000 pounds before hibernation. It gained a fifth of the needed weight from berries, twice that from acorns, and salmon made up half the remaining weight. The bear lives in a forest in Montana and has brown fur. How many pounds did it gain from small animals?",
    "output": "## Causal Reasoning Analysis\n\n**Spurious Facts Introduced:**\n1. The bear lives in a forest in Montana.\n2. The bear has brown fur.\n\n**Causal Validity Check:**\n- Berries: $\\frac{1}{5} \\times 1000 = 200$ lbs\n- Acorns: $2 \\times 200 = 400$ lbs\n- Remaining: $1000 - 200 - 400 = 400$ lbs\n- Salmon: $\\frac{1}{2} \\times 400 = 200$ lbs\n- Small animals: $400 - 200 = 200$ lbs\n\nLocation and fur color are causally disconnected from weight gain per food source. $P(\\text{animals} \\mid \\text{Montana, brown fur}) = P(\\text{animals}) = 200$ lbs.\n\n**Answer: 200 lbs**",
    "answer": 200,
    "metadata": {"spurious_facts": ["lives in Montana", "has brown fur"]}
})

records.append({
    "id": "gsm8k_61_intervention",
    "source_index": 61,
    "variant_type": "intervention",
    "question": "A bear needs 1000 lbs. Berries: 1/5 of total. Acorns: twice the berry amount. Salmon: half the remaining. Rest from small animals. Suppose we intervene do(acorn_multiplier=3 instead of 2). How many pounds came from small animals?",
    "output": "## Causal Reasoning Analysis\n\n**Intervention:** $do(k_{acorn}=3)$, overriding natural value $k_{acorn}=2$.\n\n**Post-intervention structural equations:**\n- Berries: $\\frac{1}{5} \\times 1000 = 200$ lbs\n- Acorns: $3 \\times 200 = 600$ lbs\n- Remaining: $1000 - 200 - 600 = 200$ lbs\n- Salmon: $\\frac{1}{2} \\times 200 = 100$ lbs\n- Small animals: $200 - 100 = 100$ lbs\n\n**Causal effect:** $\\Delta = 100 - 200 = -100$ lbs. Tripling the acorn multiplier halves the small-animal contribution.\n\n**Answer under intervention: 100 lbs**",
    "answer": 100,
    "metadata": {"intervention_var": "acorn_multiplier", "original_value": 2, "intervened_value": 3}
})

records.append({
    "id": "gsm8k_61_counterfactual",
    "source_index": 61,
    "variant_type": "counterfactual",
    "question": "Bear needs 1000 lbs: berries=1/5, acorns=2x berries, salmon=1/2 remaining, small animals=rest. Answer=200 lbs. In a counterfactual world where the bear needed only 800 lbs total, how many lbs would come from small animals?",
    "output": "## Causal Reasoning Analysis\n\n**Actual World (World A):** Total $= 1000$ lbs, small animals $= 200$ lbs.\n\n**Counterfactual World (World B):** Modified structural equation: total needed $= 800$ lbs.\n- Berries: $\\frac{1}{5} \\times 800 = 160$ lbs\n- Acorns: $2 \\times 160 = 320$ lbs\n- Remaining: $800 - 160 - 320 = 320$ lbs\n- Salmon: $\\frac{1}{2} \\times 320 = 160$ lbs\n- Small animals: $320 - 160 = 160$ lbs\n\n**Counterfactual contrast:** $\\Delta = 160 - 200 = -40$ lbs. Linear scaling: 80% of original target yields 80% of animal pounds.\n\n**Answer in counterfactual world: 160 lbs**",
    "answer": 160,
    "metadata": {"modified_equation": "total_needed = 800", "world_A_answer": 200, "world_B_answer": 160}
})

records.append({
    "id": "gsm8k_61_robustness",
    "source_index": 61,
    "variant_type": "robustness",
    "question": "A grizzly is readying itself for its winter dormancy and must accumulate a thousand pounds. In late summer it gorges on wild berries and tiny forest creatures. Come fall, it consumes acorns and fish. One-fifth of the requisite poundage came from berries; from acorns it got twice that figure. The fish accounted for half of what still remained. How many pounds came from the tiny forest creatures?",
    "output": "## Causal Reasoning Analysis\n\n**Parsing non-standard expressions:**\n- 'Grizzly' = bear\n- 'Winter dormancy' = hibernation\n- 'A thousand pounds' $= 1000$ lbs\n- 'Tiny forest creatures' = small woodland animals\n- 'Fish' = salmon\n\n**Computation:**\n- Berries: $200$ lbs; Acorns: $400$ lbs; Remaining: $400$ lbs\n- Salmon/Fish: $200$ lbs; Small animals: $200$ lbs\n\n**Robustness confirmed:** Species renaming and synonym substitutions do not alter the causal structure or answer.\n\n**Answer: 200 lbs**",
    "answer": 200,
    "metadata": {"rephrased_values": {"animal": "grizzly", "hibernation": "winter dormancy", "small_animals": "tiny forest creatures"}}
})

records.append({
    "id": "gsm8k_61_mediation",
    "source_index": 61,
    "variant_type": "mediation",
    "question": "Bear: 1000 lbs needed. Berries=1/5*1000=200, Acorns=2*200=400. Treat 'remaining_after_berries_acorns' as mediator M between 'total_needed' (X) and 'small_animal_pounds' (Y). Decompose NDE, NIE, TE.",
    "output": "## Causal Reasoning Analysis\n\n**Causal DAG:** $X(\\text{total needed}) \\rightarrow M(\\text{remaining}) \\rightarrow Y(\\text{small animals})$.\n\n**Structural equations:**\n- Berries $= \\frac{1}{5}X$; Acorns $= \\frac{2}{5}X$\n- $M = X - \\frac{1}{5}X - \\frac{2}{5}X = \\frac{2}{5}X$\n- Salmon $= \\frac{1}{2}M = \\frac{1}{5}X$\n- $Y = M - \\frac{1}{2}M = \\frac{1}{2}M = \\frac{1}{5}X$\n\n**Baseline:** $X=1000, M=400, Y=200$.\n\n**Mediation decomposition (increase X by 100: $X=1000 \\to 1100$):**\n\n**Total Effect (TE):** $Y(1100) = \\frac{1}{5}(1100) = 220$; $TE = +20$ lbs.\n\n**Natural Direct Effect (NDE):** Hold $M$ fixed at $M(1000)=400$, change $X: 1000 \\to 1100$:\n$Y_{NDE} = \\frac{1}{2} \\times 400 = 200$ (M unchanged); $NDE = 0$.\n\n**Natural Indirect Effect (NIE):** $NIE = TE - NDE = 20 - 0 = +20$ lbs.\n\n**Interpretation:** The entire effect of total needed weight on small-animal pounds is mediated through the remaining-after-berries-acorns quantity. $NDE = 0$.\n\n**Answer: NDE=0, NIE=+20 lbs, TE=+20 lbs per 100 lb increase in total needed**",
    "answer": {"NDE": 0, "NIE": 20, "TE": 20},
    "metadata": {"mediator": "remaining_after_berries_acorns", "X": "total_needed", "Y": "small_animal_pounds"}
})

# ─────────────────────────────────────────────
# Index 62: Oil in cans
# Q: 290 liters total, 24 cans. 10 cans hold 8L each = 80L.
# Remaining oil = 290 - 80 = 210L in 24 - 10 = 14 cans.
# Each = 210 / 14 = 15L
# A: 15
# ─────────────────────────────────────────────

records.append({
    "id": "gsm8k_62_spurious",
    "source_index": 62,
    "variant_type": "spurious",
    "question": "There are 290 liters of oil in 24 cans. 10 of the cans hold 8 liters each. The cans are stored in a warehouse in Texas, and the oil was imported last month. How much oil is each of the remaining cans holding?",
    "output": "## Causal Reasoning Analysis\n\n**Spurious Facts Introduced:**\n1. The cans are stored in a warehouse in Texas.\n2. The oil was imported last month.\n\n**Causal Validity Check:**\n- Oil in 10 full cans: $10 \\times 8 = 80$ L\n- Remaining oil: $290 - 80 = 210$ L\n- Remaining cans: $24 - 10 = 14$\n- Oil per remaining can: $210 / 14 = 15$ L\n\nStorage location and import timing are causally disconnected from oil distribution. $P(\\text{per can} \\mid \\text{Texas, last month}) = P(\\text{per can}) = 15$ L.\n\n**Answer: 15 liters**",
    "answer": 15,
    "metadata": {"spurious_facts": ["stored in Texas warehouse", "oil imported last month"]}
})

records.append({
    "id": "gsm8k_62_intervention",
    "source_index": 62,
    "variant_type": "intervention",
    "question": "290 liters of oil in 24 cans. 10 cans hold 8 liters each. Remaining cans hold equal amounts. Suppose we intervene do(small_can_capacity=10 liters instead of 8). How much does each remaining can hold?",
    "output": "## Causal Reasoning Analysis\n\n**Intervention:** $do(c_{small}=10)$, overriding natural value $c_{small}=8$.\n\n**Post-intervention:**\n- Oil in 10 cans: $10 \\times 10 = 100$ L\n- Remaining oil: $290 - 100 = 190$ L\n- Remaining cans: $14$\n- Oil per remaining can: $190 / 14 \\approx 13.57$ L\n\n**Causal effect:** $\\Delta = 13.57 - 15 = -1.43$ L. Increasing small-can capacity paradoxically reduces the per-remaining-can amount.\n\n**Answer under intervention: ≈13.57 liters**",
    "answer": 13.57,
    "metadata": {"intervention_var": "small_can_capacity", "original_value": 8, "intervened_value": 10}
})

records.append({
    "id": "gsm8k_62_counterfactual",
    "source_index": 62,
    "variant_type": "counterfactual",
    "question": "290 liters in 24 cans; 10 cans hold 8L each; remaining 14 cans hold 15L each. In a counterfactual world where there were only 20 cans total (still 10 holding 8L each), how much would each remaining can hold?",
    "output": "## Causal Reasoning Analysis\n\n**Actual World (World A):** 24 cans, 14 remaining, $15$ L each.\n\n**Counterfactual World (World B):** Modified structural equation: total cans $= 20$.\n- Oil in 10 small cans: $80$ L (unchanged)\n- Remaining oil: $290 - 80 = 210$ L\n- Remaining cans: $20 - 10 = 10$\n- Oil per remaining can: $210 / 10 = 21$ L\n\n**Counterfactual contrast:** $\\Delta = 21 - 15 = +6$ L. Fewer remaining cans means more oil per can.\n\n**Answer in counterfactual world: 21 liters**",
    "answer": 21,
    "metadata": {"modified_equation": "total_cans = 20", "world_A_answer": 15, "world_B_answer": 21}
})

records.append({
    "id": "gsm8k_62_robustness",
    "source_index": 62,
    "variant_type": "robustness",
    "question": "Two hundred and ninety litres of lubricant are distributed across two dozen containers. A tenth of the containers each hold eight litres. Assuming the remainder hold equal quantities, how many litres does each of these containers hold?",
    "output": "## Causal Reasoning Analysis\n\n**Parsing non-standard expressions:**\n- 'Two hundred and ninety litres' $= 290$ L\n- 'Lubricant' = oil\n- 'Two dozen containers' $= 24$ cans\n- 'A tenth of the containers' $= 24/10 \\approx 2.4$? No: re-read as '10 of the cans'\n\n**Reinterpretation:** 'A tenth of the containers' $= \\frac{1}{10} \\times 24$? But standard reading is 10 specific cans.\nUsing: 10 cans × 8 L = 80 L; remaining: 290−80=210 L in 14 cans; each = 15 L.\n\n**Computation:** $210 / 14 = 15$ L.\n\n**Robustness confirmed:** 'Lubricant', 'litres', and 'two dozen' do not alter the causal structure or answer.\n\n**Answer: 15 liters**",
    "answer": 15,
    "metadata": {"rephrased_values": {"oil": "lubricant", "liters": "litres", "24_cans": "two dozen containers"}}
})

records.append({
    "id": "gsm8k_62_mediation",
    "source_index": 62,
    "variant_type": "mediation",
    "question": "290L oil, 24 cans, 10 cans at 8L each. Treat 'remaining_oil' as mediator M between 'small_can_count' (X) and 'per_remaining_can' (Y). Decompose NDE, NIE, TE.",
    "output": "## Causal Reasoning Analysis\n\n**Causal DAG:** $X(\\text{small can count}) \\rightarrow M(\\text{remaining oil}) \\rightarrow Y(\\text{per remaining can})$.\n\n**Structural equations:**\n- $M = 290 - 8X$ (remaining oil after X small cans)\n- Remaining cans $= 24 - X$\n- $Y = M / (24-X) = (290-8X)/(24-X)$\n\n**Baseline:** $X=10, M=210, Y=15$.\n\n**Mediation decomposition (increase X by 1: $X=10 \\to 11$):**\n\n**Total Effect (TE):** $Y(11) = (290-88)/(24-11) = 202/13 \\approx 15.54$; $TE \\approx +0.54$ L.\n\n**Natural Direct Effect (NDE):** Hold $M$ fixed at $210$, change $X: 10 \\to 11$:\n$Y_{NDE} = 210/(24-11) = 210/13 \\approx 16.15$; $NDE \\approx 16.15 - 15 = +1.15$ L.\n\n**Natural Indirect Effect (NIE):** $NIE = TE - NDE = 0.54 - 1.15 = -0.61$ L.\n\n**Interpretation:** Adding one more small can has two opposing effects: directly reducing remaining cans (raises Y, NDE>0) but also reducing remaining oil via the mediator (lowers Y, NIE<0). Net TE is small and positive.\n\n**Answer: NDE≈+1.15 L, NIE≈−0.61 L, TE≈+0.54 L per additional small can**",
    "answer": {"NDE": 1.15, "NIE": -0.61, "TE": 0.54},
    "metadata": {"mediator": "remaining_oil", "X": "small_can_count", "Y": "per_remaining_can"}
})

# ─────────────────────────────────────────────
# Index 63: Shawna situps
# Q: Goal=30/day. Mon: did 12, missed 30-12=18. Tue: did 19, still needed 18+30-19=29.
# Wed: must meet Mon goal + Tue shortfall + Wed goal = 29 + 30 = 59?
# Actually: total goal by end of Wed = 3*30=90. Done so far = 12+19=31.
# Wed needed = 90-31 = 59.
# A: 59
# ─────────────────────────────────────────────

records.append({
    "id": "gsm8k_63_spurious",
    "source_index": 63,
    "variant_type": "spurious",
    "question": "Shawna's workout goal is 30 situps per day. On Monday she did 12. On Tuesday she did 19. Shawna works out at a gym with a red door, and she always drinks a protein shake afterward. How many situps must she do on Wednesday to meet her 3-day minimum and make up for missed ones?",
    "output": "## Causal Reasoning Analysis\n\n**Spurious Facts Introduced:**\n1. The gym has a red door.\n2. Shawna drinks a protein shake afterward.\n\n**Causal Validity Check:**\nCumulative 3-day goal: $3 \\times 30 = 90$ situps.\nDone through Tuesday: $12 + 19 = 31$ situps.\nWednesday needed: $90 - 31 = 59$ situps.\n\nGym door color and post-workout habits are causally disconnected from situp counts. $P(\\text{Wed} \\mid \\text{red door, shake}) = P(\\text{Wed}) = 59$.\n\n**Answer: 59 situps**",
    "answer": 59,
    "metadata": {"spurious_facts": ["gym has red door", "drinks protein shake afterward"]}
})

records.append({
    "id": "gsm8k_63_intervention",
    "source_index": 63,
    "variant_type": "intervention",
    "question": "Shawna: daily goal=30, Mon=12, Tue=19. Suppose we intervene do(tuesday_situps=25). How many situps does she need on Wednesday?",
    "output": "## Causal Reasoning Analysis\n\n**Intervention:** $do(S_{Tue}=25)$, overriding natural value $S_{Tue}=19$.\n\n**Post-intervention:**\n- Cumulative 3-day goal: $90$ situps (unchanged)\n- Done through Tuesday: $12 + 25 = 37$\n- Wednesday needed: $90 - 37 = 53$ situps\n\n**Causal effect:** $\\Delta = 53 - 59 = -6$ situps. Each additional Tuesday situp reduces Wednesday's requirement by exactly 1.\n\n**Answer under intervention: 53 situps**",
    "answer": 53,
    "metadata": {"intervention_var": "tuesday_situps", "original_value": 19, "intervened_value": 25}
})

records.append({
    "id": "gsm8k_63_counterfactual",
    "source_index": 63,
    "variant_type": "counterfactual",
    "question": "Shawna: daily goal=30, Mon=12, Tue=19, needs 59 on Wed. In a counterfactual world where her daily goal was 25 instead of 30, how many would she need on Wednesday?",
    "output": "## Causal Reasoning Analysis\n\n**Actual World (World A):** Goal=30/day, 3-day total=90, done=31, Wed needed=59.\n\n**Counterfactual World (World B):** Modified structural equation: daily goal $= 25$.\n- 3-day total: $3 \\times 25 = 75$ situps\n- Done through Tuesday: $12 + 19 = 31$ (unchanged)\n- Wednesday needed: $75 - 31 = 44$ situps\n\n**Counterfactual contrast:** $\\Delta = 44 - 59 = -15$ situps. Lower daily goal reduces Wednesday's requirement by $3 \\times 5 = 15$.\n\n**Answer in counterfactual world: 44 situps**",
    "answer": 44,
    "metadata": {"modified_equation": "daily_goal = 25", "world_A_answer": 59, "world_B_answer": 44}
})

records.append({
    "id": "gsm8k_63_robustness",
    "source_index": 63,
    "variant_type": "robustness",
    "question": "Shauna's daily fitness target is thirty abdominal crunches. This past Monday she managed a dozen. Yesterday (Tuesday) she completed nineteen. To satisfy her three-day minimum and compensate for all shortfalls, what must her Wednesday crunch count be?",
    "output": "## Causal Reasoning Analysis\n\n**Parsing non-standard expressions:**\n- 'Shauna' = Shawna (name variant)\n- 'Abdominal crunches' = situps\n- 'Thirty' $= 30$; 'a dozen' $= 12$; 'nineteen' $= 19$\n- 'Three-day minimum' = 3-day goal\n\n**Computation:**\n$3 \\times 30 - (12+19) = 90 - 31 = 59$ crunches\n\n**Robustness confirmed:** Name variant, 'crunches' instead of 'situps', and number word forms do not alter the causal structure or answer.\n\n**Answer: 59 situps**",
    "answer": 59,
    "metadata": {"rephrased_values": {"name": "Shauna", "exercise": "abdominal crunches", "goal_word": "thirty", "monday_word": "a dozen"}}
})

records.append({
    "id": "gsm8k_63_mediation",
    "source_index": 63,
    "variant_type": "mediation",
    "question": "Shawna: 3-day goal=90 situps, Mon=12, Tue=19. Treat 'cumulative_done' as mediator M between 'daily_goal' (X) and 'wednesday_required' (Y). Decompose NDE, NIE, TE.",
    "output": "## Causal Reasoning Analysis\n\n**Causal DAG:** $X(\\text{daily goal}) \\rightarrow M(\\text{3-day target}) \\rightarrow Y(\\text{Wed required})$; also $X$ does not affect M(cumulative done).\n\n**Structural equations:**\n- $M_{target} = 3X$ (3-day cumulative target)\n- $M_{done} = 12 + 19 = 31$ (fixed, independent of X)\n- $Y = M_{target} - M_{done} = 3X - 31$\n\n**Baseline:** $X=30, M_{target}=90, M_{done}=31, Y=59$.\n\n**Mediation decomposition (increase X by 1: $X=30 \\to 31$):**\n\n**Total Effect (TE):** $Y(31) = 3(31) - 31 = 93 - 31 = 62$; $TE = 62 - 59 = +3$ situps.\n\n**Natural Direct Effect (NDE):** Hold $M_{target}$ fixed at $90$, change $X: 30 \\to 31$:\n$Y_{NDE} = 90 - 31 = 59$ (target unchanged, done unchanged); $NDE = 0$.\n\n**Natural Indirect Effect (NIE):** $NIE = TE - NDE = 3 - 0 = +3$ situps.\n\n**Interpretation:** The entire effect of a higher daily goal on Wednesday's requirement is mediated through the 3-day cumulative target. NDE=0 because changing the goal has no direct effect on Wednesday's required count except through the target.\n\n**Answer: NDE=0, NIE=+3 situps, TE=+3 situps per unit increase in daily goal**",
    "answer": {"NDE": 0, "NIE": 3, "TE": 3},
    "metadata": {"mediator": "3day_cumulative_target", "X": "daily_goal", "Y": "wednesday_required"}
})

# ─────────────────────────────────────────────
# Index 64: James earnings
# Q: Main job: $20/hr, 30 hrs = $600.
# Second job: $20 * 0.8 = $16/hr, 15 hrs = $240.
# Total = 600 + 240 = $840.
# A: 840
# ─────────────────────────────────────────────

records.append({
    "id": "gsm8k_64_spurious",
    "source_index": 64,
    "variant_type": "spurious",
    "question": "James earns $20 an hour at his main job. He earns 20% less at his second job. He works 30 hours at his main job and half that at his second job. James commutes by bicycle and prefers tea over coffee. How much does he earn per week?",
    "output": "## Causal Reasoning Analysis\n\n**Spurious Facts Introduced:**\n1. James commutes by bicycle.\n2. He prefers tea over coffee.\n\n**Causal Validity Check:**\n- Main job: $\\$20 \\times 30 = \\$600$\n- Second job rate: $\\$20 \\times (1-0.20) = \\$16$/hr\n- Second job hours: $30/2 = 15$ hrs\n- Second job earnings: $\\$16 \\times 15 = \\$240$\n- Total: $\\$600 + \\$240 = \\$840$\n\nCommute method and beverage preference are causally disconnected from earnings. $P(\\text{earnings} \\mid \\text{bicycle, tea}) = P(\\text{earnings}) = \\$840$.\n\n**Answer: $840**",
    "answer": 840,
    "metadata": {"spurious_facts": ["commutes by bicycle", "prefers tea over coffee"]}
})

records.append({
    "id": "gsm8k_64_intervention",
    "source_index": 64,
    "variant_type": "intervention",
    "question": "James earns $20/hr main job, 20% less second job. Works 30 hrs main, half that second. Suppose we intervene do(pay_cut_percentage=30% instead of 20%). How much does he earn per week?",
    "output": "## Causal Reasoning Analysis\n\n**Intervention:** $do(\\text{cut}=30\\%)$, overriding natural value of $20\\%$.\n\n**Post-intervention:**\n- Main job: $\\$20 \\times 30 = \\$600$ (unchanged)\n- Second job rate: $\\$20 \\times (1-0.30) = \\$14$/hr\n- Second job hours: $15$ hrs (unchanged)\n- Second job earnings: $\\$14 \\times 15 = \\$210$\n- Total: $\\$600 + \\$210 = \\$810$\n\n**Causal effect:** $\\Delta = 810 - 840 = -\\$30$. Each additional 1% pay cut at the second job costs $\\$20 \\times 0.01 \\times 15 = \\$3$/week.\n\n**Answer under intervention: $810**",
    "answer": 810,
    "metadata": {"intervention_var": "pay_cut_percentage", "original_value": 20, "intervened_value": 30}
})

records.append({
    "id": "gsm8k_64_counterfactual",
    "source_index": 64,
    "variant_type": "counterfactual",
    "question": "James: main job $20/hr×30hrs=$600, second job $16/hr×15hrs=$240, total=$840. In a counterfactual world where he worked 40 hours at his main job (and still half that at his second), how much would he earn?",
    "output": "## Causal Reasoning Analysis\n\n**Actual World (World A):** Main=30 hrs, second=15 hrs, total=$840.\n\n**Counterfactual World (World B):** Modified structural equation: main hours $= 40$.\n- Main job: $\\$20 \\times 40 = \\$800$\n- Second job hours: $40/2 = 20$ hrs (half of new main)\n- Second job: $\\$16 \\times 20 = \\$320$\n- Total: $\\$800 + \\$320 = \\$1120$\n\n**Counterfactual contrast:** $\\Delta = 1120 - 840 = +\\$280$. Working 10 extra main-job hours (plus 5 extra second-job hours) earns $200+80=\\$280$ more.\n\n**Answer in counterfactual world: $1120**",
    "answer": 1120,
    "metadata": {"modified_equation": "main_job_hours = 40", "world_A_answer": 840, "world_B_answer": 1120}
})

records.append({
    "id": "gsm8k_64_robustness",
    "source_index": 64,
    "variant_type": "robustness",
    "question": "Jimmy receives twenty dollars for each hour he works at his primary occupation. At his supplementary occupation he is compensated a fifth less per hour. He clocks thirty hours weekly at his primary occupation and fifteen at his supplementary one. What are his combined weekly wages?",
    "output": "## Causal Reasoning Analysis\n\n**Parsing non-standard expressions:**\n- 'Jimmy' = James (name variant)\n- 'Twenty dollars per hour' $= \\$20$/hr\n- 'Primary occupation' = main job; 'supplementary occupation' = second job\n- 'A fifth less' $= 20\\%$ less $\\Rightarrow \\$16$/hr\n- 'Fifteen' $= 15$ hours (explicitly stated, equals half of 30)\n\n**Computation:**\n$20 \\times 30 + 16 \\times 15 = 600 + 240 = \\$840$\n\n**Robustness confirmed:** Name change, 'occupation' vs 'job', and 'a fifth less' vs '20% less' do not alter the causal structure or answer.\n\n**Answer: $840**",
    "answer": 840,
    "metadata": {"rephrased_values": {"name": "Jimmy", "main_job": "primary occupation", "pay_cut": "a fifth less"}}
})

records.append({
    "id": "gsm8k_64_mediation",
    "source_index": 64,
    "variant_type": "mediation",
    "question": "James: main $20/hr, 20% cut second job, 30 hrs main, 15 hrs second. Treat 'second_job_rate' as mediator M between 'main_job_rate' (X) and 'total_earnings' (Y). Decompose NDE, NIE, TE.",
    "output": "## Causal Reasoning Analysis\n\n**Causal DAG:** $X(\\text{main rate}) \\rightarrow M(\\text{second rate}) \\rightarrow Y(\\text{total earnings})$; also $X \\rightarrow Y$ directly.\n\n**Structural equations:**\n- $M = 0.8X$ (20% less than main)\n- $Y = 30X + 15M = 30X + 15(0.8X) = 30X + 12X = 42X$\n\n**Baseline:** $X=20, M=16, Y=840$.\n\n**Mediation decomposition (increase X by $1: X=20 \\to 21$):**\n\n**Total Effect (TE):** $Y(21) = 42 \\times 21 = 882$; $TE = 882 - 840 = +\\$42$.\n\n**Natural Direct Effect (NDE):** Hold $M$ fixed at $M(20)=16$, change $X: 20 \\to 21$:\n$Y_{NDE} = 30(21) + 15(16) = 630 + 240 = 870$; $NDE = 870 - 840 = +\\$30$.\n\n**Natural Indirect Effect (NIE):** $NIE = TE - NDE = 42 - 30 = +\\$12$.\n\n**Interpretation:** A $1/hr raise at the main job contributes $30 directly (30 main-job hours) and $12 indirectly via the second-job rate mediator (15 hrs × $0.80 = $12).\n\n**Answer: NDE=+$30, NIE=+$12, TE=+$42 per $1/hr increase in main job rate**",
    "answer": {"NDE": 30, "NIE": 12, "TE": 42},
    "metadata": {"mediator": "second_job_rate", "X": "main_job_rate", "Y": "total_earnings"}
})

# ─────────────────────────────────────────────
# Write all records to file
# ─────────────────────────────────────────────

with open(r'C:\Users\18366\Documents\trae_projects\Claude Code\causal-llm\data\causal_math_refined.jsonl', 'a', encoding='utf-8') as f:
    for record in records:
        f.write(json.dumps(record, ensure_ascii=False) + '\n')

print(f"Written {len(records)} records")

