"""
app.py

Flask web application for the AI-Generated Misinformation Risk Assessment
Matrix, built to accompany an MSc Cyber Security dissertation:

    "AI-Generated Misinformation as an Emerging Cybersecurity Threat:
    Governance and Regulatory Challenges in the Era of Generative AI"

Screens
-------
1. /              - public home page (no login required)
2. /fact-checkers - PUBLIC: free, independent fact-checking resources for
                    India / EU / USA / International
3. /ai-checklist  - PUBLIC: guidance and free tools to help recognise
                    AI-generated content ("AI checker list")
4. /login         - login screen for the professional/analyst area
5. /dashboard     - landing page after login, links to all tools
6. /risk-matrix   - LOGIN REQUIRED: analyst enters scores, the 5x5 matrix
                    from Appendix O is calculated and displayed

The two public screens are intentionally NOT behind login, because they
are designed to be shared with members of the public. Only the Risk
Matrix tool (an organisational/professional artefact) requires sign-in.

The code is deliberately kept simple (function-based Flask routes, no
database, no JavaScript frameworks) so that it is easy to read, run and
mark at MSc level. See README.md for setup and deployment instructions.
"""

import os
from functools import wraps

from flask import Flask, flash, redirect, render_template, request, session, url_for

import risk_engine as engine

app = Flask(__name__)

# The secret key is read from an environment variable so that it is never
# committed to GitHub. If SECRET_KEY is not set (e.g. running locally for
# the first time), a fallback development value is used instead - this
# fallback must NOT be relied on for any public deployment.
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-before-any-real-deployment")


# ---------------------------------------------------------------------------
# Demonstration authentication
# ---------------------------------------------------------------------------
# This is a small username/password dictionary used to demonstrate access
# control for this MSc-level prototype. Credentials can optionally be
# overridden with environment variables (useful when hosting publicly, so
# the real password is not stored in the GitHub repository). This is still
# NOT suitable for a real production system - see README.md for what a
# production version would need instead (hashed passwords in a database,
# HTTPS, account lockout, etc.).
DEMO_USERS = {
    os.environ.get("APP_USERNAME", "analyst"): os.environ.get("APP_PASSWORD", "ChangeMe123"),
}


def login_required(view_function):
    """Redirects any request to /login if the user is not signed in."""

    @wraps(view_function)
    def wrapped_view(*args, **kwargs):
        if "username" not in session:
            flash("Please log in to continue.")
            return redirect(url_for("login"))
        return view_function(*args, **kwargs)

    return wrapped_view


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def home():
    """Public home page. No login required."""
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if DEMO_USERS.get(username) == password:
            session["username"] = username
            return redirect(url_for("dashboard"))

        flash("Invalid username or password. Please try again.")

    return render_template("login.html", demo_users=DEMO_USERS)


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("home"))


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", username=session["username"])


@app.route("/risk-matrix", methods=["GET", "POST"])
@login_required
def risk_matrix():
    result = None

    if request.method == "POST":
        try:
            # Likelihood indicator scores (Appendix O, Table O.1)
            source_credibility = int(request.form["source_credibility"])
            content_authenticity = int(request.form["content_authenticity"])
            metadata_integrity = int(request.form["metadata_integrity"])
            fact_consistency = int(request.form["fact_consistency"])
            propagation_pattern = int(request.form["propagation_pattern"])

            # Impact factor scores (Appendix O, Table O.3)
            potential_harm = int(request.form["potential_harm"])
            audience_reach = int(request.form["audience_reach"])
            subject_sensitivity = int(request.form["subject_sensitivity"])

            all_scores = [
                source_credibility, content_authenticity, metadata_integrity,
                fact_consistency, propagation_pattern,
                potential_harm, audience_reach, subject_sensitivity,
            ]
            if any(score < 1 or score > 5 for score in all_scores):
                raise ValueError("Scores must be between 1 and 5.")

            result = engine.assess_risk(
                source_credibility, content_authenticity, metadata_integrity,
                fact_consistency, propagation_pattern,
                potential_harm, audience_reach, subject_sensitivity,
            )
            result["case_reference"] = request.form.get("case_reference", "").strip() or "Not provided"
            result["content_description"] = request.form.get("content_description", "").strip() or "Not provided"

        except (KeyError, ValueError):
            flash("Please complete every field with a score between 1 and 5.")

    return render_template(
        "risk_matrix.html",
        indicators=engine.LIKELIHOOD_INDICATORS,
        impact_factors=engine.IMPACT_FACTORS,
        impact_criteria=engine.IMPACT_CRITERIA,
        impact_labels=engine.IMPACT_LABELS,
        likelihood_labels=engine.LIKELIHOOD_LABELS,
        checklist_steps=engine.VERIFICATION_CHECKLIST,
        verification_conclusions=engine.VERIFICATION_CONCLUSIONS,
        confirmation_items=engine.INDEPENDENT_CONFIRMATION_ITEMS,
        matrix=engine.RISK_MATRIX,
        result=result,
        form_values=request.form if request.method == "POST" else {},
    )


@app.route("/fact-checkers")
def fact_checkers():
    """Public screen - free fact-checking resources. No login required."""
    return render_template("fact_checkers.html", resources=engine.FACT_CHECK_RESOURCES)


@app.route("/ai-checklist")
def ai_checklist():
    """Public screen - AI content recognition guidance. No login required."""
    return render_template(
        "ai_checklist.html",
        content_checks=engine.CONTENT_SPECIFIC_CHECKS,
        ai_tools=engine.AI_CHECKER_TOOLS,
    )


if __name__ == "__main__":
    # debug mode is OFF by default and only enabled if FLASK_DEBUG=1 is set
    # in the environment. Never enable debug mode in a public deployment.
    debug_mode = os.environ.get("FLASK_DEBUG", "0") == "1"
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=debug_mode)

