# AI-Generated Misinformation Risk Assessment Tool

A small Flask web application built to accompany the MSc Cyber Security
dissertation *"AI-Generated Misinformation as an Emerging Cybersecurity
Threat: Governance and Regulatory Challenges in the Era of Generative AI."*

It implements the calculation logic from **Appendix K (AI-Generated
Misinformation Risk Assessment Matrix)** as a working tool, and provides
two public-facing screens described in the dissertation's artefact list
(Section 3.6): a curated fact-checking resource list and guidance for
recognising AI-generated content.

## Purpose, Rationale, Benefits and Limitations

### Purpose

This tool operationalises the risk-assessment and verification process
set out in Appendix K, turning its five-indicator likelihood calculation,
impact rating and 5x5 risk matrix into a usable web application, alongside
two public-facing resources (fact-checkers, AI-content recognition
guidance) drawn from the dissertation's wider artefact set (Section 3.6).

### Why this tool was prepared

The dissertation finds that current cybersecurity governance and
regulatory frameworks - including ISO/IEC 27001:2022, ISO/IEC 42001:2023,
NIST CSF 2.0 and the NIST AI RMF - provide adaptable foundations but do
not consistently specify how organisations should classify, verify,
escalate and respond to externally generated misinformation (National
Institute of Standards and Technology, 2023; International Organization
for Standardization, 2022, 2023). Because AI-generated misinformation is
a socio-technical threat - harm can occur through manipulated trust and
decision-making without any technical system being compromised (Malatji,
Von Solms and Marnewick, 2019) - governance principles need to be
operationalised into a concrete, repeatable practice rather than left as
abstract guidance. This tool exists to do exactly that.

### Benefits

- Converts a semi-quantitative methodology grounded in ISO 31000's
  likelihood-times-consequence model (International Organization for
  Standardization, 2018) into a consistent, auditable, repeatable score
  that supports proportionate escalation rather than ad hoc judgement.
- Makes free, independent verification resources accessible to
  non-specialists, addressing the dissertation's finding that public
  participants wanted accessible mechanisms for assessing potentially
  misleading information.
- Displays an independent-confirmation reminder on every result,
  consistent with the recommendation that high-impact instructions should
  always be verified through an established secondary channel rather than
  accepted on the strength of a detection score alone.

### Limitations

- The output is a semi-quantitative governance rating, not a statistical
  probability or forensic proof that content is AI-generated.
- Automated content-authenticity detection remains inherently uncertain
  and can be unreliable, so it should inform - not determine - the final
  score (National Institute of Standards and Technology, 2024; Sadasivan
  et al., 2023; Mirsky and Lee, 2021).
- The underlying method has not been tested for inter-rater reliability
  or validated across specific sectors, both identified as directions for
  future research.
- The framework was developed from cross-sectional qualitative research
  with 25 cybersecurity professionals and 25 public participants recruited
  through purposive, convenience and snowball sampling, which limits the
  generalisability of the underlying evidence base.

### Academic references

International Organization for Standardization (ISO) (2018) *ISO
31000:2018 Risk Management - Guidelines*. 2nd edn. Geneva: ISO.

International Organization for Standardization (ISO) (2022) *ISO/IEC
27001:2022 Information Security, Cybersecurity and Privacy Protection -
Information Security Management Systems - Requirements*. Geneva: ISO.

International Organization for Standardization (ISO) (2023) *ISO/IEC
42001:2023 Information Technology - Artificial Intelligence - Management
System*. Geneva: ISO.

Malatji, M., Von Solms, S. and Marnewick, A. (2019) 'Socio-technical
systems cybersecurity framework', *Information & Computer Security*,
27(2), pp. 233-272. doi: 10.1108/ICS-03-2018-0031.

Mirsky, Y. and Lee, W. (2021) 'The creation and detection of deepfakes: A
survey', *ACM Computing Surveys*, 54(1), Article 7, pp. 1-41. doi:
10.1145/3425780.

National Institute of Standards and Technology (NIST) (2023)
*Artificial Intelligence Risk Management Framework (AI RMF 1.0)*. NIST AI
100-1. Gaithersburg, MD: NIST. doi: 10.6028/NIST.AI.100-1.

National Institute of Standards and Technology (NIST) (2024) *Reducing
Risks Posed by Synthetic Content: An Overview of Technical Approaches to
Digital Content Transparency*. NIST AI 100-4. Gaithersburg, MD: NIST. doi:
10.6028/NIST.AI.100-4.

Sadasivan, V.S., Kumar, A., Balasubramanian, S., Wang, W. and Feizi, S.
(2023) 'Can AI-generated text be reliably detected?', *arXiv*. doi:
10.48550/arXiv.2303.11156.

The code is intentionally simple (plain functions, no database, no
JavaScript frameworks) so that it is easy to read, run and mark at MSc
level, while still being ready to push to GitHub and deploy publicly.

## Which screens are public and which need a login

| Screen | Route | Access |
|---|---|---|
| Home | `/` | **Public** |
| Fact-Checker Resources | `/fact-checkers` | **Public** |
| AI Content Checklist | `/ai-checklist` | **Public** |
| Login | `/login` | Public (this *is* the sign-in form) |
| Dashboard | `/dashboard` | Requires login |
| Risk Matrix Tool | `/risk-matrix` | Requires login |

The two informational screens are open to everyone because they are
designed to be shared publicly. Only the Risk Matrix tool - an
organisational/professional artefact from Appendix K - sits behind a
login, since it is intended for cybersecurity or risk analysts rather
than the general public.

## Project structure

```
ai_misinfo_webapp/
├── app.py                  Flask routes (public pages, login, dashboard, risk matrix)
├── risk_engine.py           Appendix K logic and reference data (pure Python, no Flask)
├── requirements.txt
├── Procfile                 tells hosting platforms how to start the app (gunicorn)
├── .gitignore
├── README.md
├── static/
│   └── style.css
└── templates/
    ├── base.html            shared layout, navigation, flash messages
    ├── home.html            public landing page
    ├── login.html
    ├── dashboard.html
    ├── risk_matrix.html      main tool: scoring form + calculated result (login required)
    ├── fact_checkers.html    free fact-checking resources (public)
    └── ai_checklist.html     content-specific checks + AI checker tool list (public)
```

## Running it locally

1. Create and activate a virtual environment (optional but recommended):

   ```
   python3 -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   ```

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Run the application:

   ```
   python app.py
   ```

4. Open a browser at `http://127.0.0.1:5000/`. The home page, fact-checker
   resources and AI content checklist are open immediately. To use the
   Risk Matrix tool, click **Analyst Login** and sign in with the demo
   credentials shown on the login page (username `analyst`, password
   `ChangeMe123`).

## Putting it on GitHub

```
cd ai_misinfo_webapp
git init
git add .
git commit -m "Initial commit: AI-generated misinformation risk assessment tool"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo-name>.git
git push -u origin main
```

The `.gitignore` file already excludes virtual environments, `__pycache__`,
and any `.env` file, so secrets are never committed.

## Deploying it publicly (example: Render, free tier)

Any Python-friendly host that reads a `Procfile` (Render, Railway,
Heroku-style platforms, PythonAnywhere, etc.) will work. Using Render as
an example:

1. Push the project to GitHub as shown above.
2. Create a free account at render.com and choose **New -> Web Service**,
   then connect your GitHub repository.
3. Set the build command to `pip install -r requirements.txt`.
4. Set the start command to `gunicorn app:app` (this is what the
   `Procfile` already specifies).
5. Add these environment variables in the host's dashboard (do not put
   real values in code or in GitHub):
   - `SECRET_KEY` - any long random string
   - `APP_USERNAME` - the login username you want to use
   - `APP_PASSWORD` - a strong password of your choice
6. Deploy. The platform will give you a public URL such as
   `https://your-app-name.onrender.com`.

Because the fact-checker and AI-checklist pages do not require a login,
anyone with the link can use them immediately. Only people you give the
`APP_USERNAME` / `APP_PASSWORD` to will be able to reach the Risk Matrix
tool.

## Mapping to the dissertation

| Appendix K section | Where it is implemented |
|---|---|
| K.2 (2.1-2.3) Likelihood indicators & calculation | `risk_engine.LIKELIHOOD_INDICATORS`, `calculate_likelihood_score()`, `likelihood_rating_from_score()` |
| K.2 (2.4) / K.3 Impact assessment | `risk_engine.IMPACT_FACTORS`, `impact_rating_from_factors()` (uses the maximum, not average, per Appendix K) |
| K.4 5x5 risk matrix (Table K.4) | `risk_engine.RISK_MATRIX`, `get_risk_level()` |
| K.5 Response requirements (Table K.5) | `risk_engine.RESPONSE_REQUIREMENTS` |
| K.8 Verification checklist (Table K.7) | `risk_engine.VERIFICATION_CHECKLIST`, shown on the Risk Matrix screen |
| K.10 Verification conclusions (Table K.8) | `risk_engine.VERIFICATION_CONCLUSIONS`, shown on the results panel |
| K.9 Content-specific checks | `risk_engine.CONTENT_SPECIFIC_CHECKS`, shown on the AI Content Checklist screen |
| K.11 Independent confirmation rule | `risk_engine.INDEPENDENT_CONFIRMATION_ITEMS`, shown as a warning box on every result |

The worked example in Appendix K, Section 6 (scores 4, 5, 4, 5, 4 for likelihood
and a Severe impact) was used to test `risk_engine.py` and correctly
produces a likelihood score of 4.4 (High) combined with Severe impact to
give an overall Extreme risk rating.

## Technical and Deployment Limitations (read before relying on this publicly)

This started as an MSc dissertation prototype. Before treating it as a
fully public production service, be aware that:

- Authentication is a small username/password check (`DEMO_USERS` in
  `app.py`), configurable via the `APP_USERNAME` / `APP_PASSWORD`
  environment variables. It does not hash passwords or support multiple
  accounts. A real production system would store salted password hashes
  in a database (e.g. `werkzeug.security.generate_password_hash` /
  `check_password_hash`) and support proper account management.
- No persistent storage. Risk assessments are calculated and displayed
  but not saved anywhere. A production version would log each assessment
  (see Appendix K, Section 12, Minimum Verification Record) to a database for
  audit purposes.
- Set `SECRET_KEY` via an environment variable on any public host. Never
  deploy with the fallback development key left in place.
- Debug mode is off by default (`FLASK_DEBUG` must be explicitly set to
  `1` to enable it). Never enable debug mode on a public deployment, as
  it can expose source code and internal state to visitors.
- The risk matrix is a semi-quantitative governance aid, not a forensic
  or statistical tool. As Appendix K states, it supports prioritisation
  and escalation; it does not prove that content is or is not
  AI-generated. This is why the Independent Confirmation Rule (Section 11) is
  shown on every result regardless of the calculated score.
- The fact-checker and AI-detection tool lists are illustrative. They
  point to real, currently operating services, but they should be
  reviewed periodically to confirm links are still active and to add new
  tools as detection technology develops.
