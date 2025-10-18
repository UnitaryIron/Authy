from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
import os

router = APIRouter()

@router.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(admin_key: str = ""):
    if admin_key != os.getenv("ADMIN_KEY", "streetcat143!$#"):
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    total_auths = len(analytics.auth_events)
    unique_apps = len(set(event['app_id'] for event in analytics.auth_events))
    
    return f"""
    <html>
        <head>
            <title>Logify Analytics</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                .card {{ background: #f5f5f5; padding: 20px; margin: 10px 0; border-radius: 8px; }}
                .metric {{ font-size: 24px; font-weight: bold; color: #333; }}
            </style>
        </head>
        <body>
            <h1> Logify Analytics Dashboard</h1>
            
            <div class="card">
                <h3>Total Authentications</h3>
                <div class="metric">{total_auths}</div>
            </div>
            
            <div class="card">
                <h3>Active Applications</h3>
                <div class="metric">{unique_apps}</div>
            </div>
            
            <div class="card">
                <h3>Recent Activity</h3>
                <pre>{json.dumps(analytics.auth_events[-10:], indent=2)}</pre>
            </div>
        </body>
    </html>
    """
