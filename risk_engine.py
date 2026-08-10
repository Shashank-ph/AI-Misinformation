"""
risk_engine.py

Python implementation of the AI-Generated Misinformation Risk
Assessment Matrix:

    "AI-Generated Misinformation as an Emerging Cybersecurity Threat:
    Governance and Regulatory Challenges in the Era of Generative AI"

All reference data (indicators, matrix, checklists, resources)
is stored as simple Python lists/dictionaries so it can be inspected
or edited without touching the Flask routes in app.py.

Sections map directly onto Appendix K of the dissertation:
    K.2 (2.1-2.3)  Likelihood indicators, calculation and rating
    K.2 (2.4) / K.3  Impact assessment and rating
    K.4            5x5 risk matrix
    K.5            Response requirements
    K.8            Verification checklist (Section 8)
    K.9            Content-specific verification checks (Section 9)
    K.10           Verification conclusions (Section 10)
    K.11           Independent confirmation rule (Section 11)
    K.12           Minimum verification record (Section 12)
"""

# ---------------------------------------------------------------------------
# K.2 (2.1-2.3) - Likelihood indicators
# ---------------------------------------------------------------------------
# Each indicator is scored 1-5 by the user. 1 = low suspicion, 5 = high
# suspicion. The five scores are averaged to produce the likelihood score.

LIKELIHOOD_INDICATORS = [
    {
        "key": "source_credibility",
        "label": "Source credibility",
        "level_1": "Verified official or accountable source",
        "level_2": "Source is generally recognised but not fully verified, or minor inconsistencies exist",
        "level_3": "Source partially verifiable or indirect",
        "level_4": "Source shows meaningful signs of being unreliable, unofficial or difficult to verify",
        "level_5": "Anonymous, impersonated or demonstrably unreliable source",
    },
    {
        "key": "content_authenticity",
        "label": "Content authenticity",
        "level_1": "No material anomalies; independently corroborated",
        "level_2": "Minor stylistic or technical oddities that do not clearly indicate manipulation",
        "level_3": "Some visual, audio, textual or contextual anomalies",
        "level_4": "Multiple anomalies, or a single strong technical indicator suggesting alteration",
        "level_5": "Strong artefacts or reliable detection evidence of synthetic alteration",
    },
    {
        "key": "metadata_integrity",
        "label": "Metadata integrity",
        "level_1": "Metadata / provenance present and consistent",
        "level_2": "Metadata present but has minor gaps or inconsistencies",
        "level_3": "Metadata incomplete or inconclusive",
        "level_4": "Metadata largely missing or shows signs of tampering",
        "level_5": "Metadata absent, contradictory or shows evidence of manipulation",
    },
    {
        "key": "fact_consistency",
        "label": "Fact consistency",
        "level_1": "Consistent with authoritative sources and confirmed timelines",
        "level_2": "Broadly consistent, with minor unverified details",
        "level_3": "Important claims remain unverified",
        "level_4": "Significant claims conflict with available evidence",
        "level_5": "Directly contradicted by authoritative evidence or established facts",
    },
    {
        "key": "propagation_pattern",
        "label": "Propagation pattern",
        "level_1": "Normal and traceable distribution",
        "level_2": "Slightly unusual spread that is still plausibly organic",
        "level_3": "Unusual spread requiring examination",
        "level_4": "Spread pattern shows signs of coordination or inauthentic amplification",
        "level_5": "Coordinated amplification, bot-like behaviour or unexplained viral growth",
    },
]

LIKELIHOOD_LABELS = {
    1: "Very Low",
    2: "Low",
    3: "Medium",
    4: "High",
    5: "Very High",
}

# ---------------------------------------------------------------------------
# K.2 (2.4) / K.3 - Impact factors
# ---------------------------------------------------------------------------
# Impact is assessed across three factors. Where several
# impact categories apply, the highest reasonably supported impact score
# should be selected, the overall impact rating is the MAXIMUM of the
# three factor scores, not an average.

IMPACT_FACTORS = [
    {"key": "potential_harm", "label": "Potential harm"},
    {"key": "audience_reach", "label": "Audience reach"},
    {"key": "subject_sensitivity", "label": "Sensitivity of subject matter"},
]

IMPACT_LABELS = {
    1: "Insignificant",
    2: "Minor",
    3: "Moderate",
    4: "Major",
    5: "Severe",
}

IMPACT_CRITERIA = {
    1: "Very limited reach and no material financial, operational, reputational, "
       "regulatory or safety consequence.",
    2: "Localised confusion or limited harm that can be corrected quickly.",
    3: "Measurable reputational, financial or operational effect affecting a "
       "defined stakeholder group.",
    4: "Significant organisational disruption, financial loss, regulatory "
       "exposure or broad public circulation.",
    5: "Potential for serious safety consequences, systemic financial harm, "
       "election interference, critical-infrastructure disruption or extensive "
       "societal impact.",
}

# ---------------------------------------------------------------------------
# K.4 - 5x5 Risk Matrix (Table K.4)
# ---------------------------------------------------------------------------
# Keyed by likelihood rating (1-5). Each value is a list of 5 risk levels
# for impact ratings 1-5 respectively.

RISK_MATRIX = {
    5: ["Moderate", "High",     "High",     "Extreme",  "Extreme"],
    4: ["Moderate", "Moderate", "High",     "High",     "Extreme"],
    3: ["Low",      "Moderate", "Moderate", "High",     "High"],
    2: ["Low",      "Low",      "Moderate", "Moderate", "High"],
    1: ["Low",      "Low",      "Low",      "Moderate", "Moderate"],
}

RISK_LEVEL_ORDER = ["Low", "Moderate", "High", "Extreme"]

# ---------------------------------------------------------------------------
# K.5 - Response requirements (Table K.5)
# ---------------------------------------------------------------------------
# Each entry expands on the minimum response defined in Table K.5, adding a
# short explanation of what the risk level typically means (the issue) and
# the recommended course of action (the probable solution), so the tool
# gives the user actionable guidance rather than a single instruction line.

RESPONSE_REQUIREMENTS = {
    "Low": (
        "At this level, the available indicators suggest the content is "
        "unlikely to be maliciously AI-generated, or the potential "
        "consequences are minimal even if it were. The main risk is that a "
        "low-priority item is later found to be more significant than first "
        "assessed. The recommended response is to record the assessment "
        "where appropriate, retain the original content and any supporting "
        "evidence, and continue routine monitoring in case new information "
        "emerges. No further escalation is required unless the likelihood "
        "or impact rating changes."
    ),
    "Moderate": (
        "A Moderate rating means several indicators raise a credible "
        "concern, but the evidence is not yet strong enough, or the "
        "potential impact not severe enough, to justify a full incident "
        "response. Left unaddressed, moderate-risk content can still cause "
        "measurable reputational, financial or operational harm to a "
        "defined stakeholder group. The recommended response is to conduct "
        "further verification using the checklist in this tool, notify the "
        "relevant business owner so they are aware of the exposure, and "
        "document the assessment decision and rationale for audit purposes. "
        "The case should be re-assessed if new evidence emerges or the "
        "content continues to spread."
    ),
    "High": (
        "A High rating means multiple indicators strongly suggest "
        "AI-generated or manipulated content combined with a significant "
        "potential impact, such as major disruption, financial loss or "
        "broad public circulation. Informal or single-owner handling is no "
        "longer sufficient at this stage, because the organisation is "
        "exposed to material harm if the content is not addressed quickly "
        "and correctly. The recommended response is to initiate a formal "
        "cross-functional review involving cybersecurity, risk, legal and "
        "communications, preserve all available evidence in line with the "
        "verification record requirements, and begin containment actions "
        "such as restricting further distribution while the assessment is "
        "finalised. Senior stakeholders should be kept informed throughout, "
        "since the case may escalate to Extreme if the situation develops."
    ),
    "Extreme": (
        "An Extreme rating indicates a strong likelihood of deliberate "
        "AI-generated misinformation combined with the potential for "
        "serious safety, financial, regulatory or societal harm, such as "
        "election interference or critical-infrastructure disruption. This "
        "combination requires an immediate, coordinated response rather "
        "than routine escalation, because delay can allow the harm to "
        "compound rapidly as the content spreads. The recommended response "
        "is to activate the organisation's incident or crisis-management "
        "process immediately, escalate to executive leadership without "
        "delay, and consider urgent notification to the public, affected "
        "platforms, regulators or law enforcement as appropriate to the "
        "nature of the harm. All evidence must be preserved throughout the "
        "response to support any subsequent investigation, regulatory "
        "enquiry or legal action."
    ),
}

# ---------------------------------------------------------------------------
# K.8 - Verification checklist (Table K.7, Section 8)
# ---------------------------------------------------------------------------

VERIFICATION_CHECKLIST = [
    {
        "step": 1,
        "action": "Preserve the content",
        "detail": "Retain the original file, message, URL, account name, date "
                  "and time. Avoid forwarding or altering the material before "
                  "assessment.",
    },
    {
        "step": 2,
        "action": "Verify the source",
        "detail": "Identify the earliest available source and determine "
                  "whether the account, sender, website or publisher is "
                  "genuine and accountable. Independently contact the "
                  "alleged source where the content could cause significant "
                  "harm.",
    },
    {
        "step": 3,
        "action": "Examine content authenticity",
        "detail": "Review the content for visual, audio, textual or "
                  "contextual anomalies. Compare it with known genuine "
                  "material and use reverse-search or detection tools where "
                  "appropriate.",
    },
    {
        "step": 4,
        "action": "Review metadata integrity",
        "detail": "Examine available creation dates, modification history, "
                  "device information, location data and provenance records.",
    },
    {
        "step": 5,
        "action": "Verify factual consistency",
        "detail": "Separate the content into verifiable claims and compare "
                  "them with primary evidence, official records and "
                  "independent authoritative sources.",
    },
    {
        "step": 6,
        "action": "Examine propagation",
        "detail": "Identify where the content first appeared and how it "
                  "spread. Check for identical postings, coordinated "
                  "amplification, bot-like behaviour or unexplained viral "
                  "growth.",
    },
    {
        "step": 7,
        "action": "Complete the assessment",
        "detail": "Enter the five scores into the Risk Matrix tool, "
                  "determine impact and record the overall risk level and "
                  "verification conclusion.",
    },
]

# ---------------------------------------------------------------------------
# K.10 - Verification conclusions (Table K.8, Section 10)
# ---------------------------------------------------------------------------

VERIFICATION_CONCLUSIONS = [
    {
        "conclusion": "Authentic",
        "meaning": "The source, content and factual claims have been "
                   "independently corroborated, with no material evidence "
                   "of manipulation.",
    },
    {
        "conclusion": "Unverified",
        "meaning": "Available evidence is insufficient to confirm either "
                   "authenticity or manipulation.",
    },
    {
        "conclusion": "Suspected manipulation",
        "meaning": "Multiple indicators suggest synthetic generation, "
                   "alteration or deceptive presentation, but definitive "
                   "confirmation is unavailable.",
    },
    {
        "conclusion": "Confirmed manipulation",
        "meaning": "Reliable technical, source or contextual evidence "
                   "establishes that the content has been generated or "
                   "materially altered.",
    },
    {
        "conclusion": "Authentic but misleading",
        "meaning": "The underlying content is genuine but has been "
                   "miscaptioned, selectively edited, removed from context "
                   "or used to support a false claim.",
    },
]

# ---------------------------------------------------------------------------
# K.9 - Content-specific verification checks (Section 9)
# ---------------------------------------------------------------------------

CONTENT_SPECIFIC_CHECKS = [
    {
        "content_type": "Text",
        "checks": "Verify quotations, statistics, named sources and "
                  "references; confirm that cited reports or events exist; "
                  "identify fabricated citations, unsupported claims or "
                  "internal contradictions.",
    },
    {
        "content_type": "Image",
        "checks": "Conduct a reverse-image search; examine lighting, "
                  "shadows, reflections, text, anatomy and background "
                  "consistency; determine whether the image existed before "
                  "the alleged event.",
    },
    {
        "content_type": "Audio",
        "checks": "Independently contact the alleged speaker; compare the "
                  "recording with trusted samples; examine unusual cadence, "
                  "pronunciation, abrupt transitions and inconsistent "
                  "background noise.",
    },
    {
        "content_type": "Video",
        "checks": "Extract and reverse-search key frames; examine lip "
                  "synchronisation, facial movement, lighting, reflections, "
                  "audio continuity and editing transitions; locate the "
                  "earliest available upload.",
    },
    {
        "content_type": "Multimodal content",
        "checks": "Confirm that the headline, caption, image, audio and "
                  "surrounding context refer to the same event. Genuine "
                  "media presented with a false caption should be classified "
                  "as misleading even where AI generation cannot be "
                  "established.",
    },
]

# ---------------------------------------------------------------------------
# K.11 - Independent confirmation rule (Section 11)
# ---------------------------------------------------------------------------
# Regardless of the calculated score, these actions must be independently
# confirmed through an established channel before anyone acts on them.

INDEPENDENT_CONFIRMATION_ITEMS = [
    "Financial transfers or payment changes",
    "Disclosure of credentials or sensitive information",
    "Changes to accounts, access rights or supplier details",
    "Emergency or safety-related actions",
    "Legal or contractual commitments",
    "Public statements attributed to organisational leaders",
]

# ---------------------------------------------------------------------------
# Curated fact-checking resources (public-facing screen)
# ---------------------------------------------------------------------------
# Real, free, independently operated fact-checking services, grouped by
# the dissertation's comparative regulatory scope (India / EU / UK / USA)
# plus a Global category for services that are not specific to one
# jurisdiction. Dictionary insertion order controls the display order on
# the Fact-Checkers screen.

FACT_CHECK_RESOURCES = {
    "India": [
        {
            "name": "PIB Fact Check",
            "description": "Government of India unit that verifies claims "
                            "about government policies, schemes and "
                            "announcements.",
            "url": "https://factcheck.pib.gov.in/",
        },
        {
            "name": "BOOM Live",
            "description": "IFCN-certified Indian newsroom fact-checking "
                            "viral claims, images, video and deepfakes.",
            "url": "https://www.boomlive.in/fact-check",
        },
        {
            "name": "Alt News",
            "description": "Independent, non-partisan Indian fact-checking "
                            "initiative debunking misinformation and "
                            "disinformation.",
            "url": "https://www.altnews.in/",
        },
    ],
    "European Union": [
        {
            "name": "EDMO (European Digital Media Observatory)",
            "description": "EU-funded network connecting fact-checkers, "
                            "researchers and media-literacy experts across "
                            "member states.",
            "url": "https://edmo.eu/",
        },
        {
            "name": "EUvsDisinfo",
            "description": "EU East StratCom Task Force project identifying "
                            "and responding to disinformation narratives.",
            "url": "https://euvsdisinfo.eu/",
        },
    ],
    "United Kingdom": [
        {
            "name": "Full Fact",
            "description": "The UK's largest independent fact-checking "
                            "charity, covering politics, health, the economy "
                            "and viral online claims.",
            "url": "https://fullfact.org/",
        },
        {
            "name": "BBC Verify",
            "description": "Specialist BBC News team using open-source "
                            "intelligence, satellite imagery and data "
                            "analysis to verify video, images and claims.",
            "url": "https://www.bbc.com/news/bbcverify",
        },
    ],
    "United States": [
        {
            "name": "Snopes",
            "description": "One of the longest-running independent fact-"
                            "checking websites in the US, covering viral "
                            "claims across topics.",
            "url": "https://www.snopes.com/",
        },
        {
            "name": "PolitiFact",
            "description": "Pulitzer Prize-winning fact-checking service "
                            "rating the accuracy of public statements.",
            "url": "https://www.politifact.com/",
        },
        {
            "name": "FactCheck.org",
            "description": "Nonpartisan project of the Annenberg Public "
                            "Policy Center monitoring factual accuracy in "
                            "US political discourse.",
            "url": "https://www.factcheck.org/",
        },
        {
            "name": "AP Fact Check",
            "description": "Associated Press's ongoing fact-checking "
                            "coverage of news, politics and viral content.",
            "url": "https://apnews.com/ap-fact-check",
        },
        {
            "name": "Check Your Fact",
            "description": "US-based fact-checking outlet reviewing viral "
                            "claims, images and video circulating online.",
            "url": "https://checkyourfact.com/",
        },
    ],
    "Global": [
        {
            "name": "Google Fact Check Explorer",
            "description": "Searches published, independently verified "
                            "fact-checks from accredited organisations "
                            "worldwide.",
            "url": "https://toolbox.google.com/factcheck/explorer",
        },
        {
            "name": "Reuters Fact Check",
            "description": "International news agency's fact-checking "
                            "coverage examining viral social media claims "
                            "and images from around the world.",
            "url": "https://www.reuters.com/fact-check/",
        },
        {
            "name": "NewsGuard",
            "description": "Provides transparent reliability ratings for "
                            "thousands of news and information sources "
                            "worldwide, helping readers judge source "
                            "trustworthiness at a glance.",
            "url": "https://www.newsguardtech.com/",
        },
        {
            "name": "FactOrFake (checkthisfact.com)",
            "description": "Free, donation-funded AI-powered fact-checker "
                            "that cross-references claims against credible "
                            "sources in real time. Being AI-generated "
                            "itself, treat its output as a helpful starting "
                            "point rather than a final verdict.",
            "url": "https://checkthisfact.com/",
        },
    ],
}

# ---------------------------------------------------------------------------
# AI-generated content recognition tools ("AI checker list")
# ---------------------------------------------------------------------------
# Free tools that can support human verification, 
# consistent with the NIST caution applied throughout.

AI_CHECKER_TOOLS = [
    {
        "name": "Google Reverse Image Search",
        "content_type": "Image",
        "description": "Finds earlier or alternative appearances of an "
                        "image online, helping establish whether it existed "
                        "before an alleged event.",
        "url": "https://images.google.com/",
        "cost": "Free",
    },
    {
        "name": "TinEye",
        "content_type": "Image",
        "description": "Reverse image search engine specialised in "
                        "tracking where an image first appeared and how it "
                        "has been modified over time.",
        "url": "https://tineye.com/",
        "cost": "Free",
    },
    {
        "name": "InVID-WeVerify",
        "content_type": "Video / Image",
        "description": "EU-funded browser plugin for journalists that "
                        "extracts video keyframes, checks metadata and "
                        "supports reverse-image search on video content.",
        "url": "https://weverify.eu/verification-plugin/",
        "cost": "Free",
    },
    {
        "name": "GPTZero",
        "content_type": "Text",
        "description": "Widely used AI-text detection tool that estimates "
                        "the likelihood that a passage was generated by an "
                        "AI language model.",
        "url": "https://gptzero.me/",
        "cost": "Free tier available",
    },
    {
        "name": "Hive Moderation AI Detector",
        "content_type": "Image / Text",
        "description": "Detection service estimating the probability that "
                        "an image or piece of text was AI-generated.",
        "url": "https://hivemoderation.com/ai-generated-content-detection",
        "cost": "Free tier available",
    },
]

# ---------------------------------------------------------------------------
# Calculation functions (Appendix K, Sections 2 and 3)
# ---------------------------------------------------------------------------

def calculate_likelihood_score(source_credibility, content_authenticity,
                                metadata_integrity, fact_consistency,
                                propagation_pattern):
    """
    K.2.2 Likelihood calculation:
        L = (S + C + M + F + P) / 5
    Returns the raw average as a float (before banding).
    """
    total = (source_credibility + content_authenticity + metadata_integrity
              + fact_consistency + propagation_pattern)
    return total / 5


def likelihood_rating_from_score(score):
    """
    K.2.3 Table K.2 - converts the raw average score into a whole-number
    likelihood rating (1-5) using the stated banding.
    """
    if score <= 1.49:
        return 1
    elif score <= 2.49:
        return 2
    elif score <= 3.49:
        return 3
    elif score <= 4.49:
        return 4
    else:
        return 5


def impact_rating_from_factors(potential_harm, audience_reach, subject_sensitivity):
    """
    K.3 - "Where several impact categories apply, the highest reasonably
    supported impact score should be selected." The overall impact rating
    is therefore the MAXIMUM of the three factor scores, not an average.
    """
    return max(potential_harm, audience_reach, subject_sensitivity)


def get_risk_level(likelihood_rating, impact_rating):
    """K.4 Table K.4 - looks up the overall risk level from the 5x5 matrix."""
    return RISK_MATRIX[likelihood_rating][impact_rating - 1]


def get_response_requirement(risk_level):
    """K.5 Table K.5 - minimum response required for the given risk level."""
    return RESPONSE_REQUIREMENTS[risk_level]


def assess_risk(source_credibility, content_authenticity, metadata_integrity,
                 fact_consistency, propagation_pattern,
                 potential_harm, audience_reach, subject_sensitivity):
    """
    Runs the full Appendix K assessment and returns a dictionary containing
    every intermediate and final value needed by the results screen.
    """
    likelihood_score = calculate_likelihood_score(
        source_credibility, content_authenticity, metadata_integrity,
        fact_consistency, propagation_pattern,
    )
    likelihood_rating = likelihood_rating_from_score(likelihood_score)
    impact_rating = impact_rating_from_factors(
        potential_harm, audience_reach, subject_sensitivity,
    )
    risk_level = get_risk_level(likelihood_rating, impact_rating)
    response = get_response_requirement(risk_level)

    return {
        "indicator_scores": {
            "source_credibility": source_credibility,
            "content_authenticity": content_authenticity,
            "metadata_integrity": metadata_integrity,
            "fact_consistency": fact_consistency,
            "propagation_pattern": propagation_pattern,
        },
        "impact_scores": {
            "potential_harm": potential_harm,
            "audience_reach": audience_reach,
            "subject_sensitivity": subject_sensitivity,
        },
        "likelihood_score": round(likelihood_score, 2),
        "likelihood_rating": likelihood_rating,
        "likelihood_label": LIKELIHOOD_LABELS[likelihood_rating],
        "impact_rating": impact_rating,
        "impact_label": IMPACT_LABELS[impact_rating],
        "risk_level": risk_level,
        "response_requirement": response,
    }
