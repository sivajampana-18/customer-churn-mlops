from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "data" / "customer_churn.csv"

def generate_data(n_rows=2500, seed=42):
    rng = np.random.default_rng(seed)
    tenure = rng.integers(0, 73, n_rows)
    monthly = np.round(rng.uniform(20, 120, n_rows), 2)
    contract = rng.choice(["Month-to-month", "One year", "Two year"], n_rows, p=[.55, .25, .20])
    internet = rng.choice(["DSL", "Fiber optic", "No"], n_rows, p=[.35, .50, .15])
    support = rng.choice(["Yes", "No"], n_rows, p=[.35, .65])
    security = rng.choice(["Yes", "No"], n_rows, p=[.40, .60])
    payment = rng.choice(["Electronic check", "Mailed check", "Bank transfer", "Credit card"], n_rows)
    paperless = rng.choice(["Yes", "No"], n_rows)
    senior = rng.choice([0, 1], n_rows, p=[.84, .16])
    partner = rng.choice(["Yes", "No"], n_rows)
    dependents = rng.choice(["Yes", "No"], n_rows, p=[.30, .70])
    total = np.round(tenure * monthly, 2)
    logit = (-1.1 + 1.25*(contract == "Month-to-month") - .85*(contract == "Two year")
             + .018*(monthly-65) - .035*tenure + .65*(support == "No")
             + .45*(security == "No") + .35*(payment == "Electronic check")
             + .25*(internet == "Fiber optic") + .25*(senior == 1)
             - .25*(partner == "Yes") - .20*(dependents == "Yes"))
    p = 1 / (1 + np.exp(-logit))
    churn = rng.binomial(1, p)
    return pd.DataFrame({
        "tenure": tenure, "monthly_charges": monthly, "total_charges": total,
        "contract": contract, "internet_service": internet, "tech_support": support,
        "online_security": security, "payment_method": payment,
        "paperless_billing": paperless, "senior_citizen": senior,
        "partner": partner, "dependents": dependents, "churn": churn
    })

def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    df = generate_data()
    df.to_csv(OUTPUT, index=False)
    print(f"Generated {len(df)} rows at {OUTPUT}")
    print(f"Demo churn rate: {df.churn.mean():.1%}")

if __name__ == "__main__":
    main()
