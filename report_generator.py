import json
from datetime import datetime

def generate_json_report(analysis_type: str, data: dict) -> str:
    report = {
        "report_id": f"REP-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "generated_at": datetime.now().isoformat(),
        "analysis_type": analysis_type,
        "results": data
    }
    return json.dumps(report, indent=2)

def generate_html_report(title: str, results: dict, report_type: str) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    verdict = results.get("verdict", "N/A")
    confidence = results.get("confidence", "N/A")
    is_alert = "Fake" in verdict or "Manipulated" in verdict or "Potential" in verdict

    badge_color = "#ef4444" if is_alert else "#10b981"
    badge_bg = "#fef2f2" if is_alert else "#ecfdf5"

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{title} - Forensic Verification Report</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #0f172a;
            color: #f1f5f9;
            padding: 40px 20px;
        }}
        .container {{
            max-width: 820px;
            margin: 0 auto;
            background: #1e293b;
            border-radius: 16px;
            padding: 35px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        .header {{
            border-bottom: 1px solid #334155;
            padding-bottom: 20px;
            margin-bottom: 25px;
        }}
        .badge {{
            display: inline-block;
            background-color: {badge_bg};
            color: {badge_color};
            border: 1px solid {badge_color};
            padding: 8px 18px;
            border-radius: 9999px;
            font-weight: 800;
            font-size: 16px;
        }}
        .metric-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 25px 0;
        }}
        .card {{
            background: #0f172a;
            border: 1px solid #334155;
            border-radius: 10px;
            padding: 16px;
        }}
        .label {{
            font-size: 11px;
            text-transform: uppercase;
            color: #94a3b8;
            font-weight: 700;
            letter-spacing: 0.05em;
        }}
        .val {{
            font-size: 24px;
            font-weight: 800;
            margin-top: 6px;
        }}
        ul {{
            padding-left: 20px;
            line-height: 1.7;
            color: #cbd5e1;
        }}
        li {{
            margin-bottom: 8px;
        }}
        .footer {{
            margin-top: 35px;
            border-top: 1px solid #334155;
            padding-top: 15px;
            font-size: 12px;
            color: #64748b;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 style="margin: 0 0 8px 0; color: #f8fafc; font-size: 26px;">🛡️ AI Media Forensic Verification Certificate</h1>
            <p style="margin: 0; color: #94a3b8; font-size: 14px;">Audit Timestamp: {timestamp} | Classification Track: {report_type}</p>
        </div>

        <div style="margin-bottom: 20px;">
            <div class="label" style="margin-bottom: 8px;">Final Classification Verdict</div>
            <span class="badge">{verdict}</span>
        </div>

        <div class="metric-grid">
            <div class="card">
                <div class="label">Confidence Score</div>
                <div class="val" style="color: #818cf8;">{confidence}%</div>
            </div>
            <div class="card">
                <div class="label">Integrity Status</div>
                <div class="val" style="color: {badge_color};">{results.get('status_badge', results.get('prediction', 'Verified'))}</div>
            </div>
            <div class="card">
                <div class="label">Risk Index</div>
                <div class="val" style="color: #f59e0b;">{results.get('risk_level', results.get('risk_classification', 'Low Risk'))}</div>
            </div>
        </div>

        <h3 style="color: #e2e8f0; margin-top: 25px;">Forensic Findings & Indicator Signals</h3>
        <ul>
    """

    if "explanation" in results:
        for exp in results["explanation"]:
            html += f"<li>{exp}</li>"
    elif "indicators" in results:
        for ind in results["indicators"]:
            html += f"<li><strong>{ind['factor']}</strong>: {ind['status']} — {ind['details']} ({ind.get('score_impact', '')})</li>"

    html += f"""
        </ul>

        <div class="footer">
            Digital Certificate autonomously synthesized by AI Integrity Shield Forensic Engine. For academic, research, and investigative review.
        </div>
    </div>
</body>
</html>
"""
    return html
