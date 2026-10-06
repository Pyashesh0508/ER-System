"""Custom CSS styles for modern, clean dashboard presentation."""

CUSTOM_CSS = """
<style>
    /* Global Font & Header adjustments */
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2.5rem;
    }
    
    /* KPI Card styling */
    .kpi-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 16px 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        transition: transform 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
        margin-bottom: 12px;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .kpi-title {
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748b;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1e293b;
        line-height: 1.2;
    }
    .kpi-subtext {
        font-size: 0.78rem;
        color: #94a3b8;
        margin-top: 4px;
    }

    /* Insight alert cards */
    .insight-card {
        border-left: 4px solid;
        border-radius: 6px;
        padding: 14px 18px;
        margin-bottom: 14px;
        background-color: #f8fafc;
    }
    .insight-success {
        border-color: #16a34a;
        background-color: #f0fdf4;
    }
    .insight-warning {
        border-color: #ea580c;
        background-color: #fff7ed;
    }
    .insight-alert {
        border-color: #dc2626;
        background-color: #fef2f2;
    }
    .insight-info {
        border-color: #2563eb;
        background-color: #eff6ff;
    }

    /* Badges */
    .badge {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .badge-success { background-color: #dcfce7; color: #15803d; }
    .badge-warning { background-color: #fef3c7; color: #b45309; }
    .badge-danger { background-color: #fee2e2; color: #b91c1c; }

    /* Footer styling */
    .footer-text {
        text-align: center;
        color: #94a3b8;
        font-size: 0.8rem;
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #e2e8f0;
    }
</style>
"""
