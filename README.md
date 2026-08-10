# AI-Generated Misinformation Risk Assessment Tool

## Introduction

The **AI-Generated Misinformation Risk Assessment Tool** is a Flask-based web application prepared as part of the **Artefact Submission for the MSc Cyber Security Dissertation**, *AI-Generated Misinformation as an Emerging Cybersecurity Threat: Governance and Regulatory Challenges in the Era of Generative AI*.

The tool is an **original contribution of the dissertation project** and translates the research findings into a practical decision-support resource for assessing suspected AI-generated misinformation. It combines a semi-quantitative risk assessment workflow with verification guidance, fact-checking resources and content-specific checks for text, images, audio, video and multimodal content.

**Public access:** [Deployed Artefact](https://ai-misinformation.onrender.com/)


## Purpose

The purpose of the tool is to provide a structured and repeatable way to support the assessment of suspected AI-generated misinformation. It is intended to help users:

- assess five likelihood indicators: source credibility, content authenticity, metadata integrity, factual consistency and propagation pattern;
- combine likelihood with impact through a 5×5 risk matrix;
- apply proportionate response and escalation guidance;
- review practical verification steps before relying on automated detection outputs;
- access fact-checking and content-verification resources; and
- reinforce independent confirmation for high-impact instructions or communications.

The application is designed as a governance and decision-support tool, not as an automated system for proving whether content is AI-generated.

## Benefits

- Provides a consistent and transparent assessment method rather than relying only on informal judgement.
- Connects content verification with likelihood, impact and proportionate escalation.
- Encourages users to combine technical indicators with source, contextual and factual verification.
- Supports organisational decision-making where synthetic content may affect financial, operational, reputational, regulatory or safety outcomes.
- Provides accessible public-facing guidance and independent fact-checking resources.
- Demonstrates how the dissertation's original cybersecurity-governance contribution can be operationalised as a practical web application.

## Limitations

- The output is a semi-quantitative governance rating, not a statistical probability, forensic conclusion or proof of AI generation.
- Automated AI-content detection remains uncertain and may produce false positives or false negatives; detector outputs should therefore inform, rather than determine, the assessment (Mirsky and Lee, 2021; NIST, 2024).
- The underlying assessment method has not yet been tested for inter-rater reliability or validated across multiple industry sectors.
- The research underpinning the tool was qualitative and cross-sectional; its findings are analytically useful but are not statistically generalisable to all organisations or populations.
- The tool depends partly on external verification and fact-checking services whose availability, functionality or URLs may change over time.

## Academic References

International Organization for Standardization (ISO) (2018) *ISO 31000:2018 Risk Management — Guidelines*. 2nd edn. Geneva: ISO.

International Organization for Standardization (ISO) (2022) *ISO/IEC 27001:2022 Information Security, Cybersecurity and Privacy Protection — Information Security Management Systems — Requirements*. Geneva: ISO.

International Organization for Standardization (ISO) (2023) *ISO/IEC 42001:2023 Information Technology — Artificial Intelligence — Management System*. Geneva: ISO.

Malatji, M., Von Solms, S. and Marnewick, A. (2019) 'Socio-technical systems cybersecurity framework', *Information & Computer Security*, 27(2), pp. 233–272. doi: 10.1108/ICS-03-2018-0031.

Mirsky, Y. and Lee, W. (2021) 'The creation and detection of deepfakes: A survey', *ACM Computing Surveys*, 54(1), Article 7, pp. 1–41. doi: 10.1145/3425780.

National Institute of Standards and Technology (NIST) (2023) *Artificial Intelligence Risk Management Framework (AI RMF 1.0)*. NIST AI 100-1. Gaithersburg, MD: NIST. doi: 10.6028/NIST.AI.100-1.

National Institute of Standards and Technology (NIST) (2024) *Reducing Risks Posed by Synthetic Content: An Overview of Technical Approaches to Digital Content Transparency*. NIST AI 100-4. Gaithersburg, MD: NIST. doi: 10.6028/NIST.AI.100-4.

## Project Structure

```text
ai_misinfo_webapp/
├── app.py                  Flask routes, authentication and application flow
├── risk_engine.py          Risk-scoring and verification logic
├── requirements.txt        Python dependencies
├── Procfile                Production start command for Gunicorn
├── .gitignore
├── README.md
├── static/
│   └── style.css
└── templates/
    ├── base.html
    ├── home.html
    ├── login.html
    ├── dashboard.html
    ├── risk_matrix.html
    ├── fact_checkers.html
    └── ai_checklist.html
```

### Run Locally

1. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   On Windows:

   ```powershell
   venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:

   ```bash
   python app.py
   ```

4. Open:

   ```text
   http://127.0.0.1:5000/
   ```

### Run Publicly

The project can be deployed to a Python-compatible hosting platform such as Render, Railway, PythonAnywhere or another Gunicorn-compatible service.

A typical deployment workflow is:

1. Push the project to a private or public GitHub repository.
2. Create a new web service on the selected hosting platform and connect the repository.
3. Use the build command:

   ```bash
   pip install -r requirements.txt
   ```

4. Use the start command:

   ```bash
   gunicorn app:app
   ```

5. Configure the following environment variables on the hosting platform:

   ```text
   SECRET_KEY=<long-random-secret>
   APP_USERNAME=<chosen-username>
   APP_PASSWORD=<strong-password>
   ```

6. Deploy the application and verify that the public URL is accessible: `https://ai-misinformation.onrender.com/`.

## Notes

- This application was developed specifically as part of the **Artefact Submission for the MSc Cyber Security Dissertation** and represents an original contribution of the research project.
- The application is an academic prototype and should not be treated as a production-grade security or forensic platform without further engineering and validation.
- Authentication is intentionally lightweight and is suitable only for demonstration/prototype use. A production system should implement secure password hashing, account management, access control and stronger session-security controls.
- Risk assessments are calculated and displayed but are not persistently stored. A production deployment would require secure database-backed audit records if assessment history must be retained.
- `SECRET_KEY`, usernames and passwords should be configured through environment variables and must not be committed to the source repository.
- Debug mode must remain disabled on publicly accessible deployments.
- The tool does not independently establish authenticity or malicious intent. High-impact instructions should always be confirmed through a trusted secondary communication channel regardless of the calculated risk score.
- External fact-checking and AI-detection resources should be reviewed periodically because service availability and detection capabilities can change.
- Future development should include sector-specific validation, inter-rater reliability testing, stronger authentication, persistent audit logging and usability evaluation with organisational users.
