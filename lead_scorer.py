# lead_scorer.py
# lead_scorer.py
import pandas as pd

def score_leads(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df['intent_score'] = 0
    if 'demo_requested' in df.columns: df['intent_score'] += df['demo_requested'].astype(int) * 40
    if 'visited_pricing' in df.columns: df['intent_score'] += df['visited_pricing'].astype(int) * 25
    if 'email_opens' in df.columns: df['intent_score'] += df['email_opens'].clip(upper=10) * 2
    df['conversion_probability'] = df['intent_score'].clip(upper=100).round().astype(int)
    df['recommended_action'] = df['conversion_probability'].apply(
        lambda x: 'call_within_1hr' if x >= 80 else 'send_email' if x >= 50 else 'nurture'
    )
    return df.sort_values('conversion_probability', ascending=False)

if __name__ == "__main__":
    data = pd.DataFrame([{
        "lead_id": "L-2049", "company": "Acme Corp", "industry": "SaaS",
        "company_size": "51-200", "website_traffic": 45000,
        "demo_requested": True, "visited_pricing": True, "email_opens": 5, "recency_days": 3
    }, {
        "lead_id": "L-1883", "company": "Beta Labs", "industry": "EdTech",
        "company_size": "1-10", "website_traffic": 2000,
        "demo_requested": False, "visited_pricing": False, "email_opens": 2, "recency_days": 14
    }])
    result = score_leads(data)
    print(result[['lead_id', 'company', 'conversion_probability', 'recommended_action']])