# 🩺 Ejento Evaluation Health Check

This project automates scheduled evaluation runs for an agent on the Ejento platform using GitHub Actions, then checks the results and optionally sends an alert if fallback-style responses are detected.

---

## 📦 Features

- Creates an evaluation via Ejento API
- Waits for up to 2 hours for completion
- Downloads evaluation + query results
- Detects fallback responses using fuzzy matching
- Sends an email alert via Gmail if needed
- Scheduled to run every 8 hours via GitHub Actions

---

## 🧪 Local Testing

1. Create a `.env` file in the root directory:
    ```ini
    API_KEY=your_api_key
    BASE_URL=https://idejento.enterprisedb.com
    AGENT_ID=5
    DATASET_IDS=[103]
    METRIC_IDS=[1, 2, 3]
    EMAIL_USER=your_email@gmail.com
    EMAIL_PASS=your_email_password_or_app_password
    EMAIL_TO=recipient@example.com
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the pipeline:
    ```bash
    python run_full_evaluation_pipeline.py
    ```

---

## 🚀 GitHub Actions Deployment

### 🔐 Set Repository Secrets

Go to **Settings > Secrets and Variables > Actions** and add:

| Secret Key     | Description                            |
|----------------|----------------------------------------|
| `API_KEY`      | Ejento API key                         |
| `BASE_URL`     | Ejento base URL (e.g., https://...)    |
| `AGENT_ID`     | Agent ID to evaluate                   |
| `DATASET_IDS`  | JSON list of dataset IDs, e.g., `[103]`|
| `METRIC_IDS`   | JSON list of metric IDs, e.g., `[1,2]` |
| `EMAIL_USER`   | Gmail address to send from             |
| `EMAIL_PASS`   | Gmail app password                     |
| `EMAIL_TO`     | Email to notify if fallback detected   |

---

### 🔁 CI/CD Workflow File

Located at `.github/workflows/eval-health-check.yml`, this runs:

- every 8 hours (cron: `0 */8 * * *`)
- OR manually from the GitHub Actions UI

---

## 📁 File Breakdown

| File                       | Purpose                                           |
|----------------------------|---------------------------------------------------|
| `create_evaluation.py`     | Triggers evaluation run                          |
| `wait_and_check.py`        | Waits and checks if evaluation completes         |
| `get_evaluation.py`        | Downloads metadata and query results             |
| `health_check_and_alert.py`| Detects fallback and sends email                 |
| `run_full_evaluation_pipeline.py` | Orchestrates full pipeline               |
| `requirements.txt`         | Python dependencies                              |
| `.env` (local only)        | Environment variables for local testing          |

---

## 📬 Email Alerts

If any generated response closely matches predefined fallback phrases (e.g. "I don't have enough reliable information..."), an email is sent to `EMAIL_TO`.

---

## 🛡️ Notes

- GitHub Actions will **use repository secrets**, not your `.env` file.
- `.env` is only needed for **local testing**.
- Avoid committing your `.env` to the repo.

---

## 👨‍💻 Maintainer

**Muhammad Abdulbaqi**  
Email: `m.abdulbaqi1702@gmail.com`  
Created as part of the RAI Agent Monitoring at Data Science Dojo

---
