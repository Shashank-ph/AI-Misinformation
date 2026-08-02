 # AI-Generated Misinformation Risk Assessment Tool

A small Flask web application built to accompany the MSc Cyber Security
dissertation *"AI-Generated Misinformation as an Emerging Cybersecurity
Threat: Governance and Regulatory Challenges in the Era of Generative AI."*

It implements the calculation logic from **Appendix O (AI-Generated
Misinformation Risk Assessment Matrix)** as a working tool, and provides
two public-facing screens described in the dissertation's artefact list
(Section 3.6): a curated fact-checking resource list and guidance for
recognising AI-generated content.

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
organisational/professional artefact from Appendix O - sits behind a
login, since it is intended for cybersecurity or risk analysts rather
than the general public.

## Project structure

```
ai_misinfo_webapp/
├── app.py                  Flask routes (public pages, login, dashboard, risk matrix)
├── risk_engine.py           Appendix O logic and reference data (pure Python, no Flask)
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

| Appendix O section | Where it is implemented |
|---|---|
| O.2 / O.3 Likelihood indicators & calculation | `risk_engine.LIKELIHOOD_INDICATORS`, `calculate_likelihood_score()`, `likelihood_rating_from_score()` |
| O.4 Impact assessment | `risk_engine.IMPACT_FACTORS`, `impact_rating_from_factors()` (uses the maximum, not average, per Appendix O.4) |
| O.5 5x5 risk matrix (Table O.4) | `risk_engine.RISK_MATRIX`, `get_risk_level()` |
| O.6 Response requirements (Table O.5) | `risk_engine.RESPONSE_REQUIREMENTS` |
| O.9 Verification checklist (Table O.7) | `risk_engine.VERIFICATION_CHECKLIST`, shown on the Risk Matrix screen |
| O.9 Verification conclusions (Table O.9) | `risk_engine.VERIFICATION_CONCLUSIONS`, shown on the results panel |
| O.10 Content-specific checks (Table O.8) | `risk_engine.CONTENT_SPECIFIC_CHECKS`, shown on the AI Content Checklist screen |
| O.12 Independent confirmation rule | `risk_engine.INDEPENDENT_CONFIRMATION_ITEMS`, shown as a warning box on every result |

The worked example in Appendix O.7 (scores 4, 5, 4, 5, 4 for likelihood
and a Severe impact) was used to test `risk_engine.py` and correctly
produces a likelihood score of 4.4 (High) combined with Severe impact to
give an overall Extreme risk rating.

## Important limitations (read before relying on this publicly)

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
  (see Appendix O.13, Minimum Verification Record) to a database for
  audit purposes.
- Set `SECRET_KEY` via an environment variable on any public host. Never
  deploy with the fallback development key left in place.
- Debug mode is off by default (`FLASK_DEBUG` must be explicitly set to
  `1` to enable it). Never enable debug mode on a public deployment, as
  it can expose source code and internal state to visitors.
- The risk matrix is a semi-quantitative governance aid, not a forensic
  or statistical tool. As Appendix O states, it supports prioritisation
  and escalation; it does not prove that content is or is not
  AI-generated. This is why the Independent Confirmation Rule (O.12) is
  shown on every result regardless of the calculated score.
- The fact-checker and AI-detection tool lists are illustrative. They
  point to real, currently operating services, but they should be
  reviewed periodically to confirm links are still active and to add new
  tools as detection technology develops.
