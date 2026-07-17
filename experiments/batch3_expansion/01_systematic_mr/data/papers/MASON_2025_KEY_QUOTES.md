# Mason et al. 2025 — Key Quotable Passages

**Full citation:** Mason, Zuber, Hemani, Burgess et al. (2025). "Mendelian randomization in a multi-ancestry world: reflections and practical advice." arXiv:2510.17554v1.

**Authors include:** Alice Mason, Verena Zuber, Gibran Hemani, Stephen Burgess, plus 14 others from Bristol, Cambridge, Karolinska, UCL, Imperial.

**Paper type:** Review/guidance paper. 15 pages, 90 references, 2 figures, 1 table.

---

## Abstract (p2)

> "We conclude that differences in MR estimates by ancestry group should be interpreted cautiously, with consideration of how the identified differences may arise due to social and cultural factors. Corroborating evidence of a biological mechanism altering the causal pathway is needed to support a conclusion of differing causal pathways between ancestry groups."

**Use in Discussion:** This is the headline quote. Our Q-test detects heterogeneity in MR estimates, but Mason et al. independently argue that statistical heterogeneity alone does not prove biological effect modification. Our composite-hypothesis framing is consistent with their conclusion.

---

## Genetic architecture (p8)

> "We expect differences in causal impacts of exposures due to underlying differences in biology between ancestry groups to be unusual."

And from the same section:

> "Humans are 99.9% genetically identical with only 0.1% of our DNA base pairs differing from person to person. If we divide people into ancestry groups, more of the variation is found within an ancestry group than between them - estimates suggest only 5-23% of the variance is between ancestry groups."

**Use in Introduction/Discussion:** Supports the prior expectation that most MR estimates should be transportable. Non-transportability (significant Q) is the exception requiring explanation, not the rule.

---

## Six sources of heterogeneity (Table 1, pp5-6)

Mason et al. enumerate six pathways that can cause apparent heterogeneity in cross-ancestry MR estimates:

1. **LD and allele frequency differences** — Same causal variant, different instrument strength
2. **Heterogeneity in genetic effects on exposure** — Same variant, different beta on exposure
3. **Differences in distribution of exposure** — Threshold/nonlinear effects interact with population-level exposure distributions
4. **Differences in distribution and effects of confounders** — FADS/PUFA diet interaction, CHRNA5/smoking heaviness
5. **Differences in causal effect of exposure on outcome** — The ONE pathway that reflects real biology (e.g., ADH1B rs671 acetaldehyde → oesophageal cancer)
6. **Differences in definition of outcome** — Schistosomiasis prevalence, diagnostic bias

**Use in Methods/Discussion:** Our Cochran's Q test cannot distinguish pathway 5 (real biology) from pathways 1-4 and 6 (artifacts). This is precisely the composite-hypothesis problem. Cite Table 1 directly.

---

## Confounders and environment (p7)

> "Ethnicity is associated with strong disparities in many health outcomes. This is often for social and environmental reasons rather than genetic differences."

> "Certain traits (which may represent risk factors and/or confounders) vary in their distribution between populations. For example, alcohol consumption and smoking behaviour vary substantially across populations."

**Use in Discussion:** When we observe Q > chi-squared threshold, the heterogeneity could reflect confounding differences, not causal effect modification.

---

## Interpretation of results (p14)

> "Researchers should be cautious in using MR alone to justify claiming a difference in causal effects between populations. Evidence should be triangulated with lab-based studies, observational data, and randomized controlled trials."

> "Consideration should be given to potential confounding by environment, behaviour, or deprivation before attributing differences to ancestry."

> "Poorly worded labels and titles may cause confusion for clinicians and policy makers. There is a temptation to conflate ethnicity and ancestry labels, risking application of results to individuals who are outside the population under analysis."

**Use in Discussion:** Independent authority supporting our caution that Q-significance is necessary but not sufficient evidence for biological non-transportability.

---

## Conclusion (pp14-15)

> "Researchers looking at differences in MR estimates by ancestry group should carefully consider what evidence they have of a plausible biological mechanism altering the causal pathway. They should remain alert to the possibility that any identified differences in estimates may arise due to social and cultural factors rather than differences in biological mechanisms."

> "Evidence beyond MR is essential before concluding that causal effects vary between ancestry populations."

**Use in Discussion:** Closing citation. Our framework provides the statistical detection (Q-test) that Mason et al. say is necessary, while their review provides the interpretive caution we apply.

---

## Specific examples relevant to our pairs

### BMI instruments (p7, pathway 4)
> "Variants in FADS genes influence the metabolism of PUFA (polyunsaturated fatty acids). These variants are associated with lower weight in Greenland populations who have high-PUFA diets, but not European populations who have low-PUFA diets, with evidence of an interaction between diet and genetics. Hence MR estimates using these variants as instruments for BMI on an outcome are likely to be heterogeneous for populations with different diets."

**Relevant to:** BMI_CAD_MR (non-transport), BMI_T2D_MR (non-transport), BMI_depression_MR (non-transport), BMI_breast_cancer_MR (transport)

### Alcohol metabolism (p6, pathway 5)
> "The impact of alcohol on oesophageal squamous cell cancer risk is higher among people with variant rs671, which is common in East Asians, and uncommon in Europeans. This increase in impact on oesophageal cancer is not through increased alcohol consumption, but through changing how alcohol is metabolized. The variant causes acetaldehyde accumulation, magnifying the effect of alcohol per unit on the oesophagus."

**Relevant to:** alcohol_CAD_MR — rs671/ADH1B acetaldehyde pathway is the textbook example of genuine biological non-transportability. Our alcohol pair uses consistent ADH1B instruments from MVP, so the rs671 mechanism does NOT apply (ADH1B ≠ ALDH2). The null homogeneity we observe is expected.

### Smoking proxy (p7)
> "Variants in CHRNA5 are associated with alcohol intake and smoking heaviness. If associations are evaluated in a non-smoking or low-smoking population, the impact on smoking might not be detected."

**Relevant to:** smoking_schizophrenia_MR — Smoking prevalence differs between EUR and EAS populations, which could contribute to the very wide CI in Su 2022's EAS estimate.

### Folate threshold effect (p7, pathway 3)
> "Genetic predictors of folate are associated with disease outcomes in populations with low folate diets but not in high folate ones; thus MR analyses of impact of folate changes in high folate populations are unlikely to find evidence of effects even when MR analyses in low folate population do find effects."

**Relevant to:** General principle — threshold effects can produce apparent non-transportability even when the underlying biology is identical.

---

## How to cite in our paper

**Discussion paragraph (draft):**
Mason et al. (2025) enumerate six pathways through which cross-ancestry MR estimates may diverge, only one of which reflects genuine differences in causal biology. The remaining five — LD structure, instrument heterogeneity, exposure distribution effects, confounding differences, and outcome definition — are methodological artifacts that produce statistically significant Q without any underlying biological effect modification. Our framework intentionally treats Q-significance as a composite hypothesis: the test detects heterogeneity but cannot attribute it. This aligns with Mason et al.'s conclusion that "corroborating evidence of a biological mechanism altering the causal pathway is needed to support a conclusion of differing causal pathways between ancestry groups."
