#!/usr/bin/env python3
"""Generate the workshop's synthetic data packs.

Three therapeutic areas, 32 artefacts each. Generated rather than hand-written
so that the *content* is reviewable in one place, the structure stays consistent
across areas, and regenerating after an edit is one command.

    python3 workshop/data/generate.py

Everything here is invented: fictional company, fictional products, fictional
experts, fictional institutions. Real disease science and real published trial
names may be referenced because those are public literature — no real named
individual's views or interaction history appears anywhere.

Every emitted file carries a SYNTHETIC DATA banner in its first lines, which
scripts/validate_skills.py enforces.

Deliberately seeded into each field-observation set, because the safety scan
finding them is the point of Mission 2:
  - at least two adverse events, one of them serious (hospitalisation)
  - one product quality complaint
  - one special situation (pregnancy exposure)
  - one off-label use with an outcome
  - one possible lack of therapeutic effect
"""

from __future__ import annotations

import csv
import random
import zlib
from pathlib import Path

from synthetic_expansion import render_artifacts

HERE = Path(__file__).resolve().parent

BANNER = """<!-- SYNTHETIC DATA — WORKSHOP USE ONLY
     Fictional company, products, experts and institutions. Written to behave
     like real material. Not for any purpose other than training. -->
"""

CSV_BANNER = (
    "# SYNTHETIC DATA - WORKSHOP USE ONLY. Fictional company, products, experts\n"
    "# and institutions. Contains deliberately seeded adverse events, a product\n"
    "# quality complaint and an off-label use. Not real data.\n"
)

SETTINGS = ["Academic", "Academic", "Academic", "Community", "Community", "Regional centre"]
COUNTRIES = ["US", "US", "US", "DE", "FR", "UK", "ES", "IT", "JP"]

# --------------------------------------------------------------------------
# Therapeutic area content. This is the part worth reading in a review.
# --------------------------------------------------------------------------

TAS: dict[str, dict] = {
    "oncology-mm": {
        "label": "Oncology — relapsed/refractory multiple myeloma",
        "company": "Nordvant Biopharma",
        "product": "NORVANTIB",
        "generic": "norvantimab",
        "code": "NVB-2201",
        "moa": "BCMA×CD3 bispecific T-cell engager, subcutaneous, weekly after step-up dosing",
        "indication": (
            "adult patients with relapsed or refractory multiple myeloma who have "
            "received at least four prior lines of therapy, including a proteasome "
            "inhibitor, an immunomodulatory agent and an anti-CD38 antibody"
        ),
        "pivotal": "NVB-201",
        "pivotal_design": "single-arm, open-label, phase 1/2",
        "pivotal_n": 168,
        "key_results": [
            ("Overall response rate", "62.5% (95% CI 54.8–69.8)", "primary endpoint"),
            ("Very good partial response or better", "58.3%", "secondary"),
            ("Median duration of response", "18.1 months (95% CI 14.2–NE)", "secondary, immature"),
            ("Median progression-free survival", "11.4 months (95% CI 8.9–15.2)", "secondary"),
            ("Median follow-up", "16.8 months", ""),
        ],
        "safety": [
            ("Cytokine release syndrome", "71.4%", "grade ≥3: 0.6%"),
            ("Neutropenia", "68.5%", "grade ≥3: 61.3%"),
            ("Anaemia", "50.6%", "grade ≥3: 36.3%"),
            ("Infections", "74.4%", "grade ≥3: 43.5%"),
            ("ICANS", "12.5%", "grade ≥3: 0.6%"),
            ("Discontinuation due to adverse events", "4.8%", ""),
        ],
        "competitors": [
            ("VELTRAXA (competitor A)", "BCMA×CD3 bispecific", "approved 5L+, single-arm ORR 61%"),
            ("TARRICEL (competitor B)", "GPRC5D×CD3 bispecific", "approved 4L+, single-arm ORR 71%"),
            ("CELVARIS (competitor C)", "BCMA CAR-T", "approved 4L+, ORR 88%, manufacturing slot-limited"),
        ],
        "gaps": [
            "No randomised comparison against current standard of care in any line",
            "Sequencing after prior BCMA-directed therapy — no prospective data",
            "Optimal duration of therapy and whether response-adapted discontinuation is safe",
            "Efficacy and tolerability in patients with renal impairment (CrCl <30)",
            "Real-world infection rates outside trial-mandated prophylaxis",
            "No data in patients with extramedullary disease beyond n=21 subgroup",
        ],
        "kols": [
            {
                "name": "Dr Adaeze Okafor",
                "role": "Director, Myeloma Programme",
                "inst": "Fictional Cancer Centre, Springfield",
                "focus": "MRD-guided therapy de-escalation; treatment burden",
                "stance": "difficult",
                "notes": (
                    "Publicly sceptical. At the last regional meeting she said bispecifics "
                    "are being adopted 'on response rates alone, with no idea what to do "
                    "at 18 months'. Her last four papers concern discontinuation and "
                    "treatment burden rather than efficacy. She is not anti-class — she "
                    "runs two bispecific trials — she objects to the evidence being used "
                    "to answer questions it was not designed for."
                ),
                "pubs": [
                    "MRD-guided discontinuation in sustained responders: a prospective cohort (2025)",
                    "Treatment burden in relapsed myeloma: patient-reported outcomes (2024)",
                    "Infection prophylaxis practice variation across 14 centres (2024)",
                    "Rethinking duration of therapy in the bispecific era — editorial (2023)",
                ],
            },
            {
                "name": "Prof Henrik Lindqvist",
                "role": "Chair, Haematology",
                "inst": "Institute of Fictional Medicine, Uppsala",
                "focus": "Cytogenetic risk stratification; early-line combinations",
                "stance": "engaged",
                "notes": (
                    "Long-standing collaborator. Interested in whether high-risk "
                    "cytogenetics predicts durability. Has asked twice for the "
                    "cytogenetic subgroup breakdown and has not received it."
                ),
                "pubs": [
                    "Cytogenetic risk and outcomes with T-cell redirecting therapy (2025)",
                    "Early-line combination strategies in high-risk myeloma (2024)",
                ],
            },
            {
                "name": "Dr Marisol Vega",
                "role": "Consultant Haematologist, community network lead",
                "inst": "Riverbend Regional Health (fictional)",
                "focus": "Delivering bispecifics outside academic centres",
                "stance": "practical",
                "notes": (
                    "Represents the community perspective, which the KOL set otherwise "
                    "lacks entirely. Her question is not whether it works but whether it "
                    "can be given safely without an inpatient step-up bed."
                ),
                "pubs": [
                    "Outpatient step-up dosing: a feasibility analysis in community practice (2025)",
                ],
            },
        ],
        "observations": [
            "Asked directly what happens at 18 months if a patient is still responding. Said the answer 'we continue' is not evidence-based.",
            "Wants the cytogenetic subgroup breakdown. Has asked before. Frustrated it has not come.",
            "Says his centre now does step-up dosing as outpatient with a 24h observation window; no CRS escalations so far in 11 patients.",
            "Two of her patients discontinued because of recurrent infections, not disease progression.",
            "Thinks the infection rate in the label understates what he sees, because trial patients had mandated prophylaxis and his do not.",
            "Asked whether we have any data after prior BCMA CAR-T. Said this is now the most common question on his ward round.",
            "Community centre says they cannot take these patients at all without an inpatient bed for step-up.",
            "Reports that a patient developed grade 3 CRS requiring hospitalisation on day 3 of step-up dosing; recovered after tocilizumab.",
            "Says the weekly dosing schedule is the main reason patients decline, not the toxicity.",
            "Raised that the injector pens have been jamming — two of five in the last batch would not deliver the full dose.",
            "Asked about use in a patient with CrCl 24. Said he used it anyway and the patient responded, but he was 'flying blind'.",
            "Notes his older patients seem to do worse but he has no numbers.",
            "Wants to know whether MRD negativity means anything for stopping treatment.",
            "Says the competitor's GPRC5D agent is being preferred locally because of the lower infection signal.",
            "Concerned about the taste changes and weight loss with the GPRC5D class; says patients tolerate ours better on that axis.",
            "Asked whether there is a plan for a randomised trial. Said 'single-arm data will not get this into guidelines'.",
            "A patient became pregnant while on study treatment. Reported to the site; asked what we know about exposure.",
            "Says referral pathways from community to academic centres are the bottleneck, not capacity.",
            "Thinks the step-up schedule could be compressed and wants to know if anyone is studying that.",
            "Reports that one patient stopped responding after four months and he could not tell whether it was antigen loss.",
            "Asked for real-world data on outcomes in patients who would not have met trial eligibility.",
            "Says the pre-medication requirements are onerous for day-case units.",
            "Two community physicians in the network say they have never seen the product used and would not know how to start.",
            "Raised that the sequencing question is now blocking earlier-line adoption — 'it's a how question, not a whether question'.",
            "Says the response rate is not the interesting number any more; durability is.",
            "Reported a patient hospitalised with pneumonia six weeks after starting; unclear whether treatment-related.",
            "Asked whether hypogammaglobulinaemia management guidance exists. Said practice varies wildly across her network.",
            "Notes that nurses find the step-up dosing paperwork the hardest part of the protocol.",
            "Says the label's four-prior-lines requirement does not match how patients present to him.",
            "Asked whether we have any quality-of-life data at all. Said its absence is 'telling'.",
            "Reports using it in third line off-label in one patient after discussion with the patient; the patient responded.",
            "Says the competitor CAR-T is preferred where a manufacturing slot is available, and ours is the fallback.",
            "Wants to know what happens to patients who progress on our agent — what is left.",
            "Thinks the field is over-indexed on ORR because that is what the trials reported.",
            "Reports that a patient's disease progressed rapidly after a treatment interruption for infection.",
            "Asked whether there is any biomarker for who responds durably.",
            "Says his pharmacy will not stock it because of the storage requirement.",
            "Raised that patients travelling from rural areas cannot manage weekly dosing.",
            "Notes that his MDT has stopped debating whether to use bispecifics and now debates which one.",
            "Says the safety data in older patients is 'basically absent' and he treats a lot of older patients.",
            "Asked directly whether we would fund an investigator-initiated study on outpatient step-up dosing.",
            "Reports a patient with grade 2 ICANS that resolved without intervention; had not expected neurotoxicity.",
            "Says the guidelines will not move until there is a randomised trial and everyone knows it.",
            "Thinks combination with an anti-CD38 in earlier lines is where the field is going.",
            "Reports two patients whose response deepened after six months — asked if that is expected.",
            "Says the competitor's field team have been more visible than ours.",
            "Asked whether the extramedullary disease subgroup is large enough to say anything.",
            "Notes that infection prophylaxis practice at her centre now diverges from the label because of local experience.",
            "Says the biggest unmet need is not another agent, it is knowing what to do after they all fail.",
            "Reports a patient who received a double dose in error owing to a scheduling mix-up; no ill effects observed.",
            "Asked whether the product can be given in a day unit or requires overnight stay, and said the answer determines whether she uses it.",
            "Thinks patient selection is the whole game and nobody has published on it.",
            "Says a competitor's real-world dataset was presented at the last congress and ours was not.",
            "Reports declining response over three cycles in one patient with no clear explanation.",
            "Asked what proportion of trial patients were still on treatment at two years.",
        ],
        "congress": [
            ("NVB-201 updated analysis: 24-month follow-up", "Nordvant", "single-arm, n=168", "ORR 62.5%; mDOR now 19.6 mo; 41% of responders remain in response at 24 mo"),
            ("VELTRAXA real-world outcomes in 412 patients across 28 centres", "Competitor A", "retrospective cohort", "ORR 54% in real-world use vs 61% in trial; infection-related mortality 4.1%"),
            ("TARRICEL: outpatient step-up dosing feasibility", "Competitor B", "prospective, n=94", "No grade ≥3 CRS with outpatient step-up; 2 admissions for observation"),
            ("Sequencing after BCMA-directed therapy: a multicentre retrospective analysis", "Academic consortium", "retrospective, n=286", "ORR 31% with second BCMA agent vs 58% switching target class"),
            ("CELVARIS 3-year follow-up", "Competitor C", "single-arm, n=97", "36% progression-free at 3 years; no new safety signals"),
            ("Infection prophylaxis practice variation in bispecific therapy", "Investigator-initiated", "survey, 62 centres", "IVIG use ranges 12%–91% across centres; no consensus"),
            ("Health-related quality of life with T-cell redirecting therapy", "Competitor B", "PRO sub-study, n=140", "Treatment burden scores worsen in first 8 weeks then recover"),
            ("Predictors of durable response: a pooled biomarker analysis", "Academic", "pooled, n=511", "Baseline soluble BCMA and prior lines predict durability; no validated cut-off"),
            ("Phase 3 randomised trial of TARRICEL vs standard of care: enrolment complete", "Competitor B", "announcement", "Readout expected H2 next year"),
            ("Extramedullary disease outcomes with bispecific therapy", "Academic", "pooled, n=88", "ORR 38% vs 64% without EMD; poor durability"),
            ("Renal impairment sub-analysis of VELTRAXA", "Competitor A", "subgroup, n=34", "No dose adjustment required down to CrCl 20; small numbers"),
            ("Cost-effectiveness of bispecific antibodies in later-line myeloma", "HTA group", "economic model", "ICER above conventional thresholds at current pricing"),
        ],
        "announcements": [
            ("Competitor B", "Phase 3 enrolment complete for TARRICEL vs standard of care; topline expected H2 next year. Company states this will be 'the first randomised evidence in the class'."),
            ("Competitor A", "Label expanded to include patients with moderate renal impairment following submission of subgroup data."),
            ("Competitor C", "Manufacturing capacity doubled; slot wait time reduced from 6 weeks to under 3."),
            ("Competitor B", "Subcutaneous fixed-duration regimen entering phase 2; company framing the class competition around 'treatment burden, not response rate'."),
        ],
    },
    # ---------------------------------------------------------------------
    "immunology-ad": {
        "label": "Immunology — moderate-to-severe atopic dermatitis",
        "company": "Nordvant Biopharma",
        "product": "DERMALYX",
        "generic": "lyxekimab",
        "code": "NVB-3310",
        "moa": "anti-IL-13/IL-31 bispecific monoclonal antibody, subcutaneous, every 4 weeks",
        "indication": (
            "adults and adolescents aged 12 years and older with moderate-to-severe "
            "atopic dermatitis whose disease is not adequately controlled with topical "
            "prescription therapies"
        ),
        "pivotal": "NVB-330 / NVB-331",
        "pivotal_design": "two identical randomised, double-blind, placebo-controlled phase 3 trials",
        "pivotal_n": 1204,
        "key_results": [
            ("EASI-75 at week 16", "68.2% vs 24.1% placebo (difference 44.1 pp, 95% CI 38.6–49.6)", "co-primary"),
            ("IGA 0/1 at week 16", "47.9% vs 12.3% placebo", "co-primary"),
            ("Peak Pruritus NRS ≥4-point improvement", "61.4% vs 19.8% placebo", "key secondary, alpha-controlled"),
            ("Time to itch improvement", "median 3 days", "exploratory"),
            ("Maintenance of response to week 52", "78% of week-16 responders", "open-label extension"),
        ],
        "safety": [
            ("Conjunctivitis", "9.8%", "vs 2.1% placebo; mostly mild"),
            ("Injection site reactions", "11.2%", "grade ≥3: 0.3%"),
            ("Headache", "6.4%", "vs 5.9% placebo"),
            ("Herpes simplex infection", "3.1%", "vs 1.8% placebo"),
            ("Serious adverse events", "3.4%", "vs 3.9% placebo"),
            ("Discontinuation due to adverse events", "1.8%", ""),
        ],
        "competitors": [
            ("EBRIZUMA (competitor A)", "anti-IL-13 monoclonal", "established, EASI-75 ~60%, well-characterised long-term safety"),
            ("JAKVERA (competitor B)", "oral JAK1 inhibitor", "faster onset, EASI-75 ~72%, boxed warning"),
            ("CUTIVANT (competitor C)", "anti-IL-31 monoclonal", "itch-focused positioning, modest EASI response"),
        ],
        "gaps": [
            "No head-to-head against oral JAK inhibitors, which is the comparison clinicians actually make",
            "Long-term safety beyond 52 weeks in adolescents",
            "Efficacy in skin of colour — trial populations were predominantly white and EASI performs differently",
            "Whether early itch response predicts durable disease control",
            "Sequencing after JAK inhibitor failure",
            "No data in patients with concurrent asthma requiring biologic therapy",
        ],
        "kols": [
            {
                "name": "Dr Priya Raghunathan",
                "role": "Consultant Dermatologist, Head of Inflammatory Skin Disease",
                "inst": "Fictional Royal Infirmary, Manchester",
                "focus": "Outcome measure validity in skin of colour; patient-reported outcomes",
                "stance": "difficult",
                "notes": (
                    "Her objection is methodological and she is right about it. She argues "
                    "EASI systematically underestimates severity in darker skin because "
                    "erythema is harder to score, and that trial populations do not reflect "
                    "her clinic. She has declined two advisory boards on the grounds that "
                    "'you already know what you want to hear'."
                ),
                "pubs": [
                    "Performance of EASI across Fitzpatrick skin types: a validation study (2025)",
                    "Ethnic representation in atopic dermatitis trials: a systematic review (2024)",
                    "What patients mean by 'clear': a qualitative study (2024)",
                ],
            },
            {
                "name": "Prof Anton Bergström",
                "role": "Professor of Dermatology",
                "inst": "Nordfjord University Hospital (fictional)",
                "focus": "Type 2 inflammation across organ systems; atopic comorbidity",
                "stance": "engaged",
                "notes": (
                    "Interested in whether treating skin disease modifies airway outcomes. "
                    "Has proposed an investigator-initiated study twice."
                ),
                "pubs": [
                    "Atopic march and biologic intervention: a cohort analysis (2025)",
                    "Shared type 2 pathways in dermatology and respiratory medicine (2023)",
                ],
            },
            {
                "name": "Dr Thomas Achebe",
                "role": "Consultant Dermatologist, district general",
                "inst": "Eastvale District Hospital (fictional)",
                "focus": "Access, biologic prescribing thresholds, service delivery",
                "stance": "practical",
                "notes": (
                    "Prescribes under tight formulary constraints and describes the "
                    "reimbursement threshold as the real determinant of practice, "
                    "not the evidence."
                ),
                "pubs": ["Biologic access inequity in atopic dermatitis: a service evaluation (2024)"],
            },
        ],
        "observations": [
            "Says EASI underestimates severity in her patients with darker skin and she does not trust the trial numbers as a result.",
            "Asked whether the trials reported outcomes by Fitzpatrick skin type. Said the answer 'not pre-specified' is inadequate.",
            "Reports that patients prioritise itch relief over clearance and the trials led on EASI.",
            "Says the every-4-week dosing is a genuine advantage over the JAK inhibitors' daily oral, for adherence.",
            "Two patients developed conjunctivitis severe enough to need ophthalmology referral.",
            "A patient reported a severe injection site reaction with swelling extending beyond the injection area; treated with antihistamines.",
            "Thinks the JAK boxed warning is over-weighted by prescribers relative to the actual event rates.",
            "Asked directly for a head-to-head against the JAK inhibitor. Said 'that is the comparison I make every clinic'.",
            "Says patients ask about the speed of itch relief and the JAK is faster.",
            "Reports a patient who became pregnant on treatment; treatment was stopped, asked what data exist.",
            "Says the formulary threshold in her region is stricter than the label and that is what determines who gets treated.",
            "Notes that adolescents drop off treatment more than adults and nobody has studied why.",
            "Asked whether there is any signal on asthma outcomes in patients with both conditions.",
            "Reports a patient hospitalised with eczema herpeticum eight weeks after starting; unclear relationship.",
            "Says the pre-filled pen is difficult for patients with hand eczema to operate.",
            "Two of the pens in a recent batch leaked on injection; patients unsure whether they got the full dose.",
            "Thinks the 52-week extension data is not long enough for a chronic disease people take lifelong.",
            "Reports using it in a patient with concurrent severe asthma already on a biologic; both continued, no issues so far.",
            "Says the competitor's field team have been running better educational meetings.",
            "Asked whether early itch response predicts who will still be responding at a year.",
            "Reports one patient whose disease flared badly on stopping and asks whether there is rebound.",
            "Says the trials excluded exactly the patients she struggles with — those with prior biologic failure.",
            "Notes that GP referral thresholds vary enormously and many patients arrive far too late.",
            "Asked whether we have any data in patients who failed a JAK inhibitor.",
            "Says the conjunctivitis rate in practice feels higher than the label but she has not counted.",
            "Reports a patient who stopped responding after seven months with no clear explanation.",
            "Thinks the whole field over-measures clearance and under-measures sleep.",
            "Says her nurses find the injection training straightforward, which is not true of the competitor device.",
            "Asked whether the adolescent data are strong enough to justify use at 12 rather than 16.",
            "Reports that a patient used it every two weeks instead of four having misunderstood the schedule; no adverse effects.",
            "Says the biggest practical barrier is the wait for funding approval, not the clinical decision.",
            "Notes that patients in her clinic with skin of colour are under-represented in every dataset she has seen.",
            "Asked whether there is any biomarker to predict response.",
            "Reports a cluster of three patients with worsening after an initial good response at around month five.",
            "Says the itch NRS is the outcome patients actually care about and it is buried as a secondary.",
            "Thinks the competitor's positioning on itch is effective even though their EASI data are weaker.",
            "Asked what happens to patients who fail this — 'what's next, and is there anything?'",
            "Reports that the storage requirements are a problem for patients without reliable refrigeration.",
            "Says adherence in adolescents is the single biggest determinant of outcome in her practice.",
            "Notes she has stopped using the competitor's IL-31 agent because the EASI response was disappointing.",
            "Asked whether we would support an investigator-initiated study on airway outcomes.",
            "Reports a patient with a herpes zoster reactivation; recovered, unclear attribution.",
            "Says guideline positioning is what will determine uptake and the guidelines lag by two years.",
            "Thinks combination with topical therapy is under-studied and everyone does it anyway.",
            "Reports two patients who describe the injection as considerably more painful than their previous biologic.",
            "Says the trial population's mean baseline EASI was higher than most of her clinic.",
            "Asked whether the effect holds in patients with predominantly head-and-neck disease.",
            "Notes that quality-of-life improvement in her patients seems larger than the EASI change would suggest.",
            "Reports a patient who developed a persistent facial redness that did not respond to treatment.",
            "Says the every-4-week schedule means patients forget, and asks whether reminder support exists.",
            "Thinks the real competitor is not another biologic, it is patients giving up and self-managing.",
            "Asked for real-world persistence data — 'how many are still on it at two years?'",
            "Reports one patient who had no response at all by week 24 and asks whether that is expected.",
            "Says her department cannot absorb more biologic monitoring without more nursing time.",
        ],
        "congress": [
            ("NVB-330/331 pooled 52-week analysis", "Nordvant", "randomised, n=1204", "EASI-75 maintained in 78% of week-16 responders; no new safety signals"),
            ("JAKVERA vs EBRIZUMA head-to-head at week 24", "Competitor B", "randomised, n=692", "EASI-90 superior for JAK (52% vs 39%); higher herpes zoster rate"),
            ("Real-world persistence with biologics in atopic dermatitis", "Registry", "retrospective, n=3,140", "24-month persistence 61% biologics vs 44% oral JAK"),
            ("EASI performance across skin types: a multicentre validation", "Academic", "prospective, n=418", "EASI underestimates severity in Fitzpatrick V–VI; erythema scoring the main driver"),
            ("Adolescent long-term safety pooled analysis", "Competitor A", "pooled, n=560", "No growth or developmental signals to 3 years"),
            ("Itch response as a predictor of durable control", "Academic", "post hoc, n=890", "Week-4 itch response predicts week-52 EASI-75 (OR 3.1)"),
            ("Atopic march: does biologic treatment of AD modify asthma incidence?", "Investigator-initiated", "cohort, n=2,210", "Signal toward reduced asthma incidence; confounding by indication not excluded"),
            ("Sequencing after JAK inhibitor failure", "Academic", "retrospective, n=176", "EASI-75 in 48% switching to biologic after JAK failure"),
            ("Cost-effectiveness of biologics vs oral JAK in moderate-to-severe AD", "HTA group", "economic model", "Sensitive to persistence assumptions; biologics favoured on long-term safety"),
            ("CUTIVANT itch-focused phase 3", "Competitor C", "randomised, n=540", "Strong itch NRS response, EASI-75 only 41%"),
            ("Patient-reported priorities in atopic dermatitis: a discrete choice experiment", "Academic", "survey, n=1,020", "Sleep and itch ranked above visible clearance"),
        ],
        "announcements": [
            ("Competitor B", "Head-to-head superiority data against the leading IL-13 agent presented; company repositioning around 'speed and depth of response'."),
            ("Competitor A", "Long-term adolescent safety database now exceeds 3 years; company emphasising 'the longest safety record in the class'."),
            ("Competitor C", "Pivoting positioning entirely to itch after disappointing EASI results."),
            ("Competitor B", "Regulatory label update adding a warning on herpes zoster following post-marketing review."),
        ],
    },
    # ---------------------------------------------------------------------
    "cardiometabolic-obesity": {
        "label": "Cardiometabolic — obesity and weight management",
        "company": "Nordvant Biopharma",
        "product": "ADIPOSYN",
        "generic": "trelagludide",
        "code": "NVB-4402",
        "moa": "GLP-1/GIP/glucagon triple receptor agonist, subcutaneous, weekly",
        "indication": (
            "adults with an initial body mass index of 30 kg/m² or greater, or 27 kg/m² "
            "or greater with at least one weight-related comorbidity, as an adjunct to a "
            "reduced-calorie diet and increased physical activity"
        ),
        "pivotal": "NVB-440",
        "pivotal_design": "randomised, double-blind, placebo-controlled phase 3",
        "pivotal_n": 2280,
        "key_results": [
            ("Mean weight change at week 72", "−22.4% vs −2.6% placebo (difference −19.8 pp, 95% CI −21.1 to −18.5)", "co-primary"),
            ("≥20% weight reduction at week 72", "61.3% vs 4.1% placebo", "co-primary"),
            ("Waist circumference change", "−18.2 cm vs −3.1 cm", "key secondary"),
            ("HbA1c change (prediabetes subgroup)", "−0.7% vs −0.1%", "secondary"),
            ("Weight regain at 1 year post-discontinuation", "mean 68% of lost weight regained", "off-treatment extension"),
        ],
        "safety": [
            ("Nausea", "48.1%", "grade ≥3: 2.4%; mostly during titration"),
            ("Vomiting", "27.3%", "grade ≥3: 1.9%"),
            ("Diarrhoea", "24.6%", "grade ≥3: 1.1%"),
            ("Constipation", "21.0%", ""),
            ("Gallbladder-related events", "3.2%", "vs 0.9% placebo"),
            ("Discontinuation due to adverse events", "11.4%", "predominantly gastrointestinal"),
        ],
        "competitors": [
            ("SLENDARA (competitor A)", "GLP-1 receptor agonist", "established, −15% weight, CV outcomes trial positive"),
            ("DUOMETRIX (competitor B)", "GLP-1/GIP dual agonist", "−21% weight, largest current share, supply-constrained"),
            ("ORAVELDA (competitor C)", "oral GLP-1", "−13% weight, oral administration the main differentiator"),
        ],
        "gaps": [
            "No cardiovascular outcomes trial — the comparison the field now expects",
            "What happens after discontinuation, and whether any regimen prevents regain",
            "Lean mass preservation: DXA sub-study was small and underpowered",
            "Efficacy and safety in patients over 75",
            "No data in patients with established heart failure with preserved ejection fraction",
            "Long-term gallbladder and pancreatic safety beyond 72 weeks",
        ],
        "kols": [
            {
                "name": "Dr Ines Ferreira",
                "role": "Consultant Endocrinologist, Obesity Medicine lead",
                "inst": "Fictional Metabolic Institute, Lisbon",
                "focus": "Weight regain, lean mass, long-term management as chronic disease",
                "stance": "difficult",
                "notes": (
                    "Her criticism is that the field markets weight loss and ignores what "
                    "happens afterwards. She has said publicly that '68% regain is the "
                    "headline finding of that trial and nobody presents it'. She is not "
                    "opposed to the class — she prescribes it heavily — she objects to the "
                    "framing."
                ),
                "pubs": [
                    "Weight regain after incretin discontinuation: a systematic review (2025)",
                    "Lean mass loss with pharmacological weight management (2024)",
                    "Obesity as a chronic relapsing disease: implications for stopping rules (2024)",
                ],
            },
            {
                "name": "Prof Daniel Whitmore",
                "role": "Professor of Cardiometabolic Medicine",
                "inst": "Kingsbridge University (fictional)",
                "focus": "Cardiovascular outcomes; HFpEF",
                "stance": "engaged",
                "notes": (
                    "Runs a CV outcomes programme. His view is that without a CVOT this "
                    "agent will not enter cardiology practice regardless of weight data."
                ),
                "pubs": [
                    "Incretin therapy and cardiovascular outcomes: where the evidence stands (2025)",
                    "Weight loss and HFpEF: mechanism and evidence (2024)",
                ],
            },
            {
                "name": "Dr Yuki Tanabe",
                "role": "Primary care physician, obesity service lead",
                "inst": "Harborview Community Health (fictional)",
                "focus": "Delivery at scale in primary care; access and adherence",
                "stance": "practical",
                "notes": (
                    "Where most of these prescriptions will actually be written. Her "
                    "concerns are titration support, supply, and what to tell patients who "
                    "cannot continue."
                ),
                "pubs": ["Delivering obesity pharmacotherapy in primary care: a service model (2025)"],
            },
        ],
        "observations": [
            "Says the 68% regain figure is the most important number in the trial and it is never in the slide deck.",
            "Asked directly whether there is a cardiovascular outcomes trial. Said without one this will not enter cardiology practice.",
            "Reports that a patient was hospitalised with acute pancreatitis during titration; recovered, investigation ongoing.",
            "Says the titration schedule is too fast for her older patients and she slows it routinely.",
            "Two patients discontinued because of intractable nausea despite dose reduction.",
            "Asked about lean mass. Said the DXA sub-study was 'too small to reassure anyone'.",
            "Reports that patients are asking about stopping and she has no evidence-based answer.",
            "Says supply constraints on the competitor product are driving patients to ours by default, not by choice.",
            "Reports a patient who became pregnant while on treatment; treatment stopped immediately, asked what data exist.",
            "Notes that gallbladder events in her practice seem more frequent than the label suggests.",
            "Says the weekly injection is manageable but patients would prefer oral.",
            "Asked whether there is any data in patients over 75. Said she treats many.",
            "Reports using it in a patient with HFpEF off-label; symptoms improved markedly.",
            "Says primary care cannot deliver the titration support the protocol assumes.",
            "Two pens in a recent batch would not prime; patients missed doses.",
            "Asked whether weight loss translates into any hard outcome or just the number on the scale.",
            "Says her patients regain rapidly and blame themselves, which is a harm in itself.",
            "Reports one patient with severe dehydration requiring intravenous fluids after persistent vomiting.",
            "Thinks the discontinuation rate in the trial understates real-world discontinuation considerably.",
            "Asked whether there is a maintenance dose strategy anyone has studied.",
            "Says insurance coverage is the single biggest determinant of who gets treated.",
            "Notes that patients with binge eating disorder respond differently and nobody studies them.",
            "Reports a patient whose diabetes control improved so much they stopped their oral agents.",
            "Says the competitor's CV outcomes data is what cardiologists cite and we have nothing comparable.",
            "Asked whether muscle mass loss matters clinically or is a surrogate concern.",
            "Reports declining effect in one patient after eight months at a stable dose.",
            "Says the nausea is manageable but the anticipatory nausea before injection is not.",
            "Notes that the trial excluded patients with significant psychiatric history, who are a large part of her clinic.",
            "Asked whether we would support an investigator-initiated study on discontinuation strategies.",
            "Reports that a patient took a double dose after confusing the pen strengths; monitored, no harm.",
            "Says patients ask about facial appearance changes and there is nothing in the label about it.",
            "Thinks the field is heading toward combination with resistance training and nobody has trial data.",
            "Reports a patient with a new gallstone requiring cholecystectomy at month five.",
            "Says primary care colleagues are prescribing without any structured support and outcomes are worse.",
            "Asked what proportion of trial patients were still on treatment at 72 weeks.",
            "Notes that the competitor's oral formulation is preferred by needle-averse patients even at lower efficacy.",
            "Reports one patient who lost weight rapidly then developed severe fatigue and stopped.",
            "Says the biggest question in her clinic is 'for how long', and there is no answer.",
            "Asked whether the effect differs by ethnicity; said the trial population was not representative of her practice.",
            "Reports a patient with worsening gastroparesis symptoms who had pre-existing diabetes.",
            "Says the storage and travel requirements are a real barrier for shift workers.",
            "Thinks the weight regain data should be in the label and is not.",
            "Reports two patients who stopped because of cost when insurance changed.",
            "Asked whether there is any signal on bone density.",
            "Says her service cannot scale to demand and the waiting list is over a year.",
            "Notes that patients who lose weight quickly seem to regain fastest, but she has no data.",
            "Reports a patient who developed severe constipation requiring hospital assessment.",
            "Asked whether there is guidance on managing patients who plateau.",
            "Says the competitor field team have been more present in primary care than ours.",
            "Reports one patient using it for cosmetic weight loss at a BMI of 26, obtained privately.",
            "Thinks the real unmet need is maintenance, not induction of weight loss.",
            "Asked whether combination with an oral agent has been studied.",
            "Reports a patient whose HbA1c fell below the prediabetes threshold and asks whether treatment can stop.",
            "Says she cannot answer patient questions about long-term safety and it undermines the conversation.",
        ],
        "congress": [
            ("NVB-440 72-week primary analysis", "Nordvant", "randomised, n=2280", "−22.4% weight vs −2.6% placebo; 61.3% achieved ≥20% reduction"),
            ("NVB-440 off-treatment extension", "Nordvant", "extension, n=640", "Mean 68% of lost weight regained by 1 year off treatment"),
            ("SLENDARA cardiovascular outcomes trial: final results", "Competitor A", "randomised CVOT, n=17,600", "17% reduction in MACE (HR 0.83, 95% CI 0.74–0.93)"),
            ("DUOMETRIX vs SLENDARA head-to-head", "Competitor B", "randomised, n=1,410", "−20.9% vs −14.8% weight at 72 weeks"),
            ("Lean mass changes with incretin therapy: pooled DXA analysis", "Academic", "pooled, n=412", "25–39% of total weight lost is lean mass; clinical significance unclear"),
            ("Maintenance dosing after target weight: a randomised withdrawal study", "Competitor A", "randomised withdrawal, n=520", "Continued low-dose maintains 82% of loss vs 31% with withdrawal"),
            ("ORAVELDA oral formulation phase 3", "Competitor C", "randomised, n=980", "−13.1% weight; strong patient preference for oral"),
            ("Real-world discontinuation and persistence with incretin therapy", "Claims analysis", "retrospective, n=88,400", "58% discontinue within 12 months; cost and GI intolerance the main drivers"),
            ("Gallbladder and pancreatic events: a pooled safety analysis", "Academic", "pooled, n=24,100", "Gallbladder events elevated (RR 1.9); pancreatitis signal not confirmed"),
            ("Weight loss and HFpEF outcomes", "Academic", "randomised, n=529", "Improved KCCQ score and 6-minute walk distance"),
            ("Obesity pharmacotherapy in primary care: implementation outcomes", "Health system", "prospective service evaluation", "Structured support doubles 12-month persistence"),
        ],
        "announcements": [
            ("Competitor A", "Cardiovascular outcomes trial met its primary endpoint; company repositioning entirely around 'outcomes, not weight'."),
            ("Competitor B", "Supply constraints easing; manufacturing capacity to triple within 18 months."),
            ("Competitor C", "Oral formulation approved; positioning on 'no needles' despite lower efficacy."),
            ("Competitor A", "Maintenance-dose randomised withdrawal data published; company now promoting a defined maintenance strategy."),
        ],
    },
}


# --------------------------------------------------------------------------
# Emitters
# --------------------------------------------------------------------------


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def product_profile(ta: dict) -> str:
    rows = "\n".join(
        f"| {name} | {result} | {note} |" for name, result, note in ta["key_results"]
    )
    safety = "\n".join(
        f"| {name} | {rate} | {note} |" for name, rate, note in ta["safety"]
    )
    return f"""{BANNER}
# Product profile — {ta['product']} ({ta['generic']})

**{ta['company']}** · development code {ta['code']}

## Mechanism and administration

{ta['moa']}

## Approved indication (US)

{ta['product']} is indicated for the treatment of {ta['indication']}.

> Uses outside this wording are **not approved**. Any discussion of them is
> governed by the unsolicited-request pathway.

## Pivotal evidence — {ta['pivotal']}

**Design:** {ta['pivotal_design']}, N={ta['pivotal_n']}

| Endpoint | Result | Note |
| --- | --- | --- |
{rows}

## Safety ({ta['pivotal']} safety population)

| Event | Any grade | Note |
| --- | --- | --- |
{safety}

## Competitive context

| Product | Class | Position |
| --- | --- | --- |
""" + "\n".join(
        f"| {n} | {c} | {p} |" for n, c, p in ta["competitors"]
    ) + """

---

*All figures above are invented for workshop use. Cite this file only as a labelled synthetic source, never as real clinical evidence.*
"""


def evidence_landscape(ta: dict) -> str:
    gaps = "\n".join(f"- {g}" for g in ta["gaps"])
    return f"""{BANNER}
# Evidence landscape — {ta['label']}

## Where the evidence stands

{ta['product']} is supported by {ta['pivotal_design']} evidence ({ta['pivotal']},
N={ta['pivotal_n']}). The strength of what can be claimed follows directly from
that design — see `evidence-appraisal` before quoting any of it.

## What competitors have

""" + "\n".join(
        f"- **{n}** ({c}) — {p}" for n, c, p in ta["competitors"]
    ) + f"""

## What nobody has answered

{gaps}

## How the field's attention is moving

The dimension on which products in this area are compared has shifted over the
last two years. Read the congress abstracts and competitor announcements
together and ask what clinicians are now comparing on — it is not what they
were comparing on when the pivotal programme was designed.

---

*Synthetic. Written to behave like a real landscape summary.*
"""


def kol_dossiers(ta: dict) -> str:
    out = [BANNER, f"# KOL dossiers — {ta['label']}\n"]
    out.append(
        "> These are personal data about named professionals, even when "
        "fictional. Publication records are public; interaction history and "
        "internal assessments are not. Handle accordingly.\n"
    )
    for k in ta["kols"]:
        out.append(f"## {k['name']}")
        out.append(f"**{k['role']}** · {k['inst']}\n")
        out.append(f"**Scientific focus:** {k['focus']}\n")
        out.append(f"**Background:** {k['notes']}\n")
        out.append("**Recent publications:**\n")
        for p in k["pubs"]:
            out.append(f"- {p}")
        out.append("")
    out.append("---\n\n*Fictional individuals and institutions.*\n")
    return "\n".join(out)


def interaction_notes(ta: dict, rng: random.Random) -> str:
    out = [BANNER, f"# Prior interaction notes — {ta['label']}\n"]
    for k in ta["kols"]:
        out.append(f"## {k['name']} — last interaction")
        if k["stance"] == "difficult":
            out.append(
                f"Approximately 5 months ago. Difficult conversation. {k['notes']}\n\n"
                f"Left unresolved: she asked for something we did not have and we "
                f"offered a different dataset instead, which she noticed. Do not "
                f"repeat that.\n"
            )
        elif k["stance"] == "engaged":
            out.append(
                f"Approximately 3 months ago. Constructive. {k['notes']}\n\n"
                f"Left unresolved: an outstanding request that has not been "
                f"actioned. Address it before anything else.\n"
            )
        else:
            out.append(
                f"Approximately 2 months ago, brief. {k['notes']}\n\n"
                f"Left unresolved: asked a practical delivery question we deferred.\n"
            )
    out.append("---\n\n*Synthetic interaction records.*\n")
    return "\n".join(out)


def field_observations(ta: dict, rng: random.Random) -> list[dict]:
    """One row per observation, with plausible structured metadata.

    The observation TEXT is hand-written per therapeutic area; only the
    surrounding metadata is generated. That keeps the material realistic enough
    for the insight exercise to be worth doing.
    """
    msls = [f"MSL-{i:02d}" for i in range(1, 8)]

    # A contact is a person, so their setting and country are properties of THEM
    # and must not vary between records. Randomising these per row produced a
    # dataset where one HCP appeared as Community/FR and Academic/US, which makes
    # contact-level frequency claims meaningless — and de-duplicating by contact
    # is the core of the insight exercise. Fix the attributes to the contact.
    contacts = {
        f"HCP-{i:03d}": {
            "setting": rng.choice(SETTINGS),
            "country": rng.choice(COUNTRIES),
        }
        for i in range(101, 141)
    }
    contact_ids = list(contacts)

    rows = []
    for i, text in enumerate(ta["observations"], 1):
        # Several MSLs report on the same contacts, so working out whether a
        # repeated theme is a pattern (many clinicians) or an echo (one
        # clinician, several MSLs) is a real exercise rather than a formality.
        cid = rng.choice(contact_ids)
        rows.append(
            {
                "record_id": f"OBS-{i:03d}",
                "date": f"2026-{rng.choice(['04','05','06'])}-{rng.randint(1, 28):02d}",
                "msl": rng.choice(msls),
                "contact_id": cid,
                "setting": contacts[cid]["setting"],
                "country": contacts[cid]["country"],
                "channel": rng.choice(
                    ["Face-to-face", "Face-to-face", "Virtual", "Congress", "Phone"]
                ),
                "observation": text,
            }
        )
    return rows


def congress_abstracts(ta: dict) -> str:
    out = [BANNER, f"# Congress abstracts — {ta['label']}\n"]
    out.append(
        "> **Evidence tier: `[abstract]`.** Not peer-reviewed, methods "
        "incomplete, and results change materially before full publication more "
        "often than people assume. Label every citation accordingly.\n"
    )
    for i, (title, sponsor, design, result) in enumerate(ta["congress"], 1):
        out.append(f"### Abstract {1000 + i} — {title}")
        out.append(f"**Presenter/sponsor:** {sponsor} · **Design:** {design}\n")
        out.append(f"{result}\n")
    out.append("---\n\n*Synthetic abstracts. Do not cite.*\n")
    return "\n".join(out)


def competitor_announcements(ta: dict) -> str:
    out = [BANNER, f"# Competitor announcements and press releases — {ta['label']}\n"]
    out.append(
        "> Corporate communications, not evidence. Read them for what changed "
        "competitively and for how the field is being framed — not as data.\n"
    )
    for who, what in ta["announcements"]:
        out.append(f"### {who}\n\n{what}\n")
    out.append("---\n\n*Synthetic.*\n")
    return "\n".join(out)


def medical_plan(ta: dict) -> str:
    return f"""{BANNER}
# Medical plan — {ta['label']} — current year

> This is the plan as it stands. It has the problems real medical plans have.
> Read it critically.

## Strategic imperatives

1. Establish {ta['product']} as a scientifically credible option in its approved
   population.
2. Build the evidence base to support earlier-line use.
3. Strengthen relationships with the scientific community.
4. Support appropriate use through education.

## Planned activities

| # | Activity | Owner | Timing |
| --- | --- | --- | --- |
| 1 | Advisory board on treatment sequencing | Medical Strategy | Q3 |
| 2 | 14 KOL engagement meetings | Field Medical | Ongoing |
| 3 | Congress symposium at the major annual meeting | Sci Comms | Q4 |
| 4 | Publish the 24-month follow-up analysis | Publications | Q3 |
| 5 | Investigator-initiated study programme | Evidence Generation | Ongoing |
| 6 | Field training on the updated data | Medical Excellence | Q2 |
| 7 | Achieve guideline inclusion | Medical Strategy | Q4 |
| 8 | Real-world evidence feasibility assessment | HEOR | Q3 |
| 9 | Standard response document refresh | Medical Information | Q2 |
| 10 | Increase MSL interaction volume by 20% | Field Medical | Ongoing |
| 11 | Regional scientific exchange meetings | Field Medical | Q2–Q4 |
| 12 | Publication of the pooled safety analysis | Publications | Q4 |

## Success measures

- Number of KOL interactions completed
- Number of publications submitted
- Congress symposium attendance
- Field training completion rate

---

*Synthetic. Note that several activities do not trace to an imperative, and
that at least one measure cannot come back negative.*
"""


def publication_plan(ta: dict) -> str:
    return f"""{BANNER}
# Publication plan — {ta['label']} — current year

> Sequenced by data availability, which is how most publication plans are built.
> Whether that is a strategy is the question.

| # | Planned output | Type | Data source | Target | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | {ta['pivotal']} primary results | Manuscript | Pivotal trial | High-impact journal | Published |
| 2 | 24-month follow-up | Manuscript | Pivotal trial | Specialty journal | In draft |
| 3 | Pooled safety analysis | Manuscript | Pooled programme | Specialty journal | Planned Q4 |
| 4 | Subgroup analysis by baseline severity | Abstract | Pivotal trial | Annual congress | Planned |
| 5 | Subgroup analysis by age | Abstract | Pivotal trial | Annual congress | Planned |
| 6 | Subgroup analysis by prior therapy | Abstract | Pivotal trial | Regional congress | Planned |
| 7 | Health economic model | Manuscript | Modelling | HEOR journal | Planned |
| 8 | Mechanism review | Review | Literature | Review journal | Planned |
| 9 | Patient-reported outcomes analysis | Abstract | Pivotal trial | Annual congress | Under discussion |

## Data on file, not currently planned for publication

- Extended safety follow-up beyond the primary analysis
- An analysis addressing one of the questions in `evidence-landscape.md`
- A negative sub-study result

---

*Synthetic. Note the ratio of subgroup analyses to new questions answered, and
what sits unpublished at the bottom.*
"""


def readme(ta_key: str, ta: dict, n_obs: int, extra_files: list[str]) -> str:
    return f"""{BANNER}
# Data pack — {ta['label']}

Everything here is invented. Fictional company ({ta['company']}), fictional
product ({ta['product']}), fictional experts, fictional institutions. It is
written to behave like real material so the exercise is worth doing.

## What's in here

| File | Contents |
| --- | --- |
| `product-profile.md` | The compound, its approved indication, pivotal evidence and safety |
| `evidence-landscape.md` | What is known, what competitors have, what nobody has answered |
| `kol-dossiers.md` | Three experts, including one who is deliberately difficult |
| `interaction-notes.md` | What happened at the last meeting with each |
| `field-observations.csv` | {n_obs} field interaction records from one quarter |
| `congress-abstracts.md` | What was presented at the recent congress |
| `competitor-announcements.md` | Press releases and corporate statements |
| `medical-plan.md` | This year's plan, with the problems real plans have |
| `publication-plan.md` | What is currently planned |

### Extended cross-functional exercises

The pack also contains {len(extra_files)} deliberately imperfect source
artefacts covering advisory boards, Medical Information and safety intake,
field planning, metrics, education, IIS review, RWE, payer/HTA, guideline and
launch readiness, integrated evidence planning, scientific platforms,
publication development, MLR review, terminology mapping, document ingestion,
data visualisation and spreadsheet analysis.

See [`../SKILL-COVERAGE.md`](../SKILL-COVERAGE.md) for the exact skill-to-file
map and suggested workshop jobs. The files are inputs, not worked answers.

## A note on the field observations

They contain things a careful reader should escalate before doing any analysis
at all. That is deliberate — finding them is part of the exercise, not a trick.

---

*Synthetic data. Not for any purpose other than training.*
"""


def main() -> int:
    total = 0
    for key, ta in TAS.items():
        # Python's built-in hash is salted per process, so it cannot make
        # regenerated fixtures reproducible. CRC32 is stable across runtimes.
        rng = random.Random(zlib.crc32(key.encode("utf-8")))
        out = HERE / key

        obs = field_observations(ta, rng)
        csv_path = out / "field-observations.csv"
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with csv_path.open("w", encoding="utf-8", newline="") as fh:
            fh.write(CSV_BANNER)
            w = csv.DictWriter(
                fh, fieldnames=list(obs[0].keys()), lineterminator="\n"
            )
            w.writeheader()
            w.writerows(obs)

        write(out / "product-profile.md", product_profile(ta))
        write(out / "evidence-landscape.md", evidence_landscape(ta))
        write(out / "kol-dossiers.md", kol_dossiers(ta))
        write(out / "interaction-notes.md", interaction_notes(ta, rng))
        write(out / "congress-abstracts.md", congress_abstracts(ta))
        write(out / "competitor-announcements.md", competitor_announcements(ta))
        write(out / "medical-plan.md", medical_plan(ta))
        write(out / "publication-plan.md", publication_plan(ta))
        extra = render_artifacts(ta, rng)
        for filename, content in extra.items():
            write(out / filename, content)
        write(out / "README.md", readme(key, ta, len(obs), sorted(extra)))

        count = 10 + len(extra)
        print(f"  {key}: {count} files, {len(obs)} field observations")
        total += count

    print(f"\nWrote {total} files across {len(TAS)} therapeutic areas.")
    print("All carry a SYNTHETIC DATA banner; validate_skills.py enforces it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
