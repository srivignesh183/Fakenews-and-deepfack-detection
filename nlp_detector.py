import re
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Robust multi-domain training corpus spanning journalism, science, policy, and misinformation
BASE_TRAINING_CORPUS = [
    # Category: Credible / Official Journalism (Label 1)
    ("Official health authorities reported a steady decline in seasonal viral infections following nationwide preventative vaccination programs.", 1),
    ("The central bank announced an adjustment in benchmark interest rates to combat inflation, according to official economic releases.", 1),
    ("NASA's James Webb Space Telescope detected chemical signatures in an exoplanet atmosphere, scientists published in peer-reviewed journals.", 1),
    ("The United Nations General Assembly convened in Geneva to discuss humanitarian aid and climate disaster resilience.", 1),
    ("The Supreme Court delivered its ruling on environmental regulations after months of constitutional hearings.", 1),
    ("Meteorological departments issued heavy rainfall alerts for coastal districts as seasonal monsoon winds intensified.", 1),
    ("The Ministry of Transport published quarterly road safety statistics showing increased public transit ridership.", 1),
    ("Pharmaceutical researchers launched phase III clinical trials for a preventative malaria vaccine with university partners.", 1),
    ("Global trade representatives concluded bilateral discussions regarding technology supply chains and semiconductor tariffs.", 1),
    ("City council members voted unanimously to fund public library expansions and educational literacy grants.", 1),
    ("Automakers reported steady quarterly revenue alongside investments in electric vehicle battery infrastructure.", 1),
    ("Independent auditors published annual findings on state infrastructure expenditure and procurement transparency.", 1),
    ("Archaeologists uncovered 2,000-year-old trade relics along ancient maritime shipping routes.", 1),
    ("Government statistics bureau released consumer price index indicators highlighting moderating food prices.", 1),
    ("Universities worldwide collaborated on open-source quantum computing algorithms validated through experimental simulations.", 1),
    ("Renewable energy installations hit record capacity according to reports published by international energy agencies.", 1),
    ("Diplomatic envoys held high-level peace talks in Norway, reaffirming international legal treaties and humanitarian corridors.", 1),
    ("Agricultural scientists engineered drought-tolerant grain variants showing high yields in dryland farming zones.", 1),
    ("National oceanic monitoring services tracked migration patterns of marine wildlife using satellite telemetry beacons.", 1),
    ("Public cybersecurity centers issued standardized guidance on patch management for critical enterprise software.", 1),
    ("The international labor organization published employment index showing gradual wage normalization across services.", 1),
    ("Civil defense teams conducted earthquake preparedness drills across western coastal municipalities yesterday.", 1),

    # Category: Misinformation / Clickbait / Fabrications (Label 0)
    ("SHOCKING SECRET: Miracle kitchen fruit cures terminal cancer in 24 hours! Big Pharma wants this deleted immediately!", 0),
    ("URGENT: Government insider leaks secret mind-control chips hidden in local drinking tap water! Share before it gets taken down!", 0),
    ("You won't believe what this world leader said about aliens living under Antarctica! Exposed proofs inside!", 0),
    ("BREAKING: Celebrities caught drinking secret anti-aging serum made in underground laboratories!", 0),
    ("PROOF: 5G cell towers are weaponized frequency transmitters causing widespread mass illness overnight!", 0),
    ("Doctors are STUNNED: Rub this common household spice on your forehead to instantly reverse diabetes!", 0),
    ("LEAKED DOCUMENTS: Bill Gates admitted depopulation agenda in secret recorded meeting! Viral truth!", 0),
    ("BOMBSHELL: Lunar eclipse was faked by Hollywood directors using military hologram projectors!", 0),
    ("MIRACLE CURE: Drink pure onion juice twice daily to detox all vaccine nanobots from your bloodstream!", 0),
    ("EXPOSED: Massive financial collapse planned for tomorrow morning! Banks will seize all private savings accounts!", 0),
    ("Secret ancient manuscript discovered: Extraterrestrial beings built world monuments and run world government!", 0),
    ("SHOCKING: Eating raw potato skins guarantees complete immunity from all known infectious diseases!", 0),
    ("Government covertly replaced city pigeons with surveillance micro-drones equipped with facial recognition cameras!", 0),
    ("SCANDAL: World leaders secretly signed treaty surrendering national sovereignty to Martian overlords!", 0),
    ("100% Guaranteed lottery winning loophole discovered by rogue mathematician before he mysteriously disappeared!", 0),
    ("UNBELIEVABLE: Put aluminum foil in your shoes to eliminate all bodily toxins and bypass government radar!", 0),
    ("CONFIRMED: The earth is actually hollow and hosting secret billionaire underground civilizations!", 0),
    ("WARNING: Modern sunscreen lotions are designed to alter your DNA! Don't let your children use them!", 0),
    ("EXPOSED: Ancient energy grid found under pyramids powers free limitless electricity that energy companies hide!", 0),
    ("DEADLY CONSPIRACY: Cloud seeding planes are dropping zombie mind-control dust over major cities!", 0),
    ("THEY ARE LYING TO YOU: Tap water causes instant genetic mutations that doctors refuse to discuss!", 0),
    ("SHADOW GOV LEAK: Secret space lasers responsible for all recent wildfire occurrences across continents!", 0)
]

SENSATIONAL_LEXICON = {
    "shocking", "miracle", "secret", "leaks", "leaked", "bombshell", "urgent", "cure", "cures",
    "pharma", "chips", "proof", "proven", "exposed", "scandal", "depopulation", "nanobots",
    "hologram", "hoax", "conspiracy", "faked", "unbelievable", "aliens", "covertly", "loophole",
    "instant", "instantly", "banned", "deleted", "forbidden", "viral", "drones", "deadly",
    "toxins", "whistleblower", "surrender", "overlords", "zombie", "radar", "mutations", "lasers"
}

JOURNALISTIC_ANCHORS = {
    "official", "authorities", "announced", "published", "peer-reviewed", "journal",
    "scientists", "researchers", "spokesperson", "reuters", "verified", "statistics",
    "bureau", "auditors", "clinical", "trials", "court", "ruling", "documented", "envoys",
    "agency", "guidance", "telemetry", "infrastructure", "expenditure", "diplomatic", "treaties"
}

class AdvancedFakeNewsDetector:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            sublinear_tf=True,
            max_features=2000
        )
        self.model = LogisticRegression(C=1.2, max_iter=200, random_state=42)
        self.training_samples = list(BASE_TRAINING_CORPUS)
        self._fit_pipeline()

    def _fit_pipeline(self):
        texts = [t[0] for t in self.training_samples]
        labels = [t[1] for t in self.training_samples]
        X = self.vectorizer.fit_transform(texts)
        self.model.fit(X, labels)

    def retrain(self, df: pd.DataFrame, text_col: str, label_col: str):
        try:
            new_samples = []
            for _, r in df.iterrows():
                t = str(r[text_col]).strip()
                val = r[label_col]
                lbl = 1 if str(val).lower() in ("1", "real", "credible", "true") else 0
                if len(t) > 5:
                    new_samples.append((t, lbl))

            if len(new_samples) < 4:
                return False, "Dataset must provide at least 4 valid samples."

            self.training_samples = list(BASE_TRAINING_CORPUS) + new_samples
            self._fit_pipeline()
            return True, f"Successfully retrained! Active corpus size: {len(self.training_samples)} articles."
        except Exception as e:
            return False, f"Retraining failed: {str(e)}"

    def analyze_text(self, text: str):
        if not text or not text.strip():
            return {"error": "Input text is empty. Please provide an article snippet or headline."}

        cleaned = text.strip()
        words = re.findall(r'\b[a-zA-Z]{3,}\b', cleaned.lower())
        total_words = max(len(words), 1)

        # 1. Machine Learning Inference
        vec = self.vectorizer.transform([cleaned])
        probs = self.model.predict_proba(vec)[0]  # [prob_fake, prob_real]
        raw_prob_fake = float(probs[0])
        raw_prob_real = float(probs[1])

        # 2. Extract specific linguistic signals
        sensational_found = [w for w in set(words) if w in SENSATIONAL_LEXICON]
        credible_found = [w for w in set(words) if w in JOURNALISTIC_ANCHORS]
        
        # Stylistic Metrics
        caps_chars = sum(1 for c in cleaned if c.isupper())
        total_chars = max(len(cleaned), 1)
        caps_ratio = (caps_chars / total_chars) * 100.0
        exclamation_count = cleaned.count('!')
        question_count = cleaned.count('?')

        # 3. Multi-Factor Scoring Synthesis
        # Sensational density penalty
        sensational_density = (len(sensational_found) / total_words) * 100.0
        sensational_penalty = min(len(sensational_found) * 0.14 + (0.16 if caps_ratio > 18.0 else 0.0) + (0.12 if exclamation_count >= 2 else 0.0), 0.50)
        
        # Credibility bonus
        credibility_bonus = min(len(credible_found) * 0.14, 0.40)

        # Calibrated final probabilities
        adjusted_fake_prob = float(np.clip(raw_prob_fake + sensational_penalty - credibility_bonus, 0.04, 0.98))
        adjusted_real_prob = float(1.0 - adjusted_fake_prob)

        if adjusted_fake_prob >= 0.50:
            verdict = "Fake"
            prediction = "Potential Misinformation / Fake"
            confidence = round(adjusted_fake_prob * 100.0, 1)
            risk_level = "High Risk" if adjusted_fake_prob > 0.75 else "Moderate Risk"
        else:
            verdict = "Real"
            prediction = "Likely Credible / Authentic"
            confidence = round(adjusted_real_prob * 100.0, 1)
            risk_level = "Low Risk"

        # 4. Detailed Dimensional Radar/Factor Breakdown
        dimension_scores = {
            "Semantic Model Credibility": round(adjusted_real_prob * 100, 1),
            "Sensationalism Resistance": round(max(100.0 - (len(sensational_found) * 25.0 + caps_ratio), 5.0), 1),
            "Journalistic Attribution": round(min(len(credible_found) * 35.0 + (30.0 if len(words) > 15 else 10.0), 98.0), 1),
            "Emotional Neutrality": round(max(100.0 - (exclamation_count * 30.0 + question_count * 15.0), 10.0), 1),
            "Stylistic Professionalism": round(max(100.0 - (caps_ratio * 2.5), 15.0), 1)
        }

        # 5. Explanations
        explanation = []
        if sensational_found:
            explanation.append(f"Detected **{len(sensational_found)} sensationalist clickbait terms**: {', '.join(sorted(sensational_found))}.")
        if caps_ratio > 18.0:
            explanation.append(f"Unusually high uppercase text proportion (**{caps_ratio:.1f}%**), indicative of emotional agitation.")
        if exclamation_count >= 2:
            explanation.append(f"High exclamation punctuation density (**{exclamation_count} occurrences**).")
        if credible_found:
            explanation.append(f"Identified **{len(credible_found)} institutional credibility anchors**: {', '.join(sorted(credible_found))}.")
        if not explanation:
            explanation.append("Linguistic syntax and tone align with neutral informative journalism.")

        highlighted_html = self._generate_annotated_html(cleaned, sensational_found, credible_found)

        return {
            "verdict": verdict,
            "prediction": prediction,
            "confidence": confidence,
            "risk_level": risk_level,
            "prob_fake": round(adjusted_fake_prob * 100, 1),
            "prob_real": round(adjusted_real_prob * 100, 1),
            "flagged_keywords": sensational_found,
            "credible_keywords": credible_found,
            "dimension_scores": dimension_scores,
            "explanation": explanation,
            "word_count": len(words),
            "caps_ratio": round(caps_ratio, 1),
            "exclamation_count": exclamation_count,
            "highlighted_html": highlighted_html,
            "total_corpus_size": len(self.training_samples)
        }

    def _generate_annotated_html(self, text: str, sensational: list, credible: list) -> str:
        tokens = re.split(r'(\s+|[.,!?;:"\'()]+)', text)
        sens_set = set(s.lower() for s in sensational)
        cred_set = set(c.lower() for c in credible)

        out = []
        for token in tokens:
            lower = token.lower().strip()
            if lower in sens_set:
                out.append(f"<span style='background: rgba(239, 68, 68, 0.25); color: #fca5a5; border-bottom: 2px solid #ef4444; padding: 2px 6px; border-radius: 4px; font-weight: 700;' title='Sensational Clickbait Trigger'>{token}</span>")
            elif lower in cred_set:
                out.append(f"<span style='background: rgba(16, 185, 129, 0.25); color: #6ee7b7; border-bottom: 2px solid #10b981; padding: 2px 6px; border-radius: 4px; font-weight: 700;' title='Journalistic Credibility Anchor'>{token}</span>")
            elif token.isupper() and len(token) > 2 and token.isalpha():
                out.append(f"<span style='background: rgba(245, 158, 11, 0.25); color: #fcd34d; padding: 2px 5px; border-radius: 4px; font-weight: 600;' title='High-emphasis capital'>{token}</span>")
            else:
                out.append(token)
        return "".join(out)

# Backward-compatibility alias
FakeNewsDetector = AdvancedFakeNewsDetector
