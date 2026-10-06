"""Workforce Insights page view."""

import streamlit as st
import pandas as pd

from app.analysis.insights import generate_workforce_insights
from app.ui.components import render_page_header, render_insight_card


def render_insights_view(df: pd.DataFrame, threshold: float = 80.0):
    """Render Workforce Insights page."""
    render_page_header(
        "Automated Workforce Insights",
        "Rule-based analytical observations derived from current attendance statistics.",
    )

    insights = generate_workforce_insights(df, threshold=threshold)

    # Filter by category
    categories = ["All Categories"] + sorted(list({ins["category"] for ins in insights}))
    selected_cat = st.selectbox("Filter Insights by Category:", categories)

    st.markdown("---")

    filtered_insights = (
        insights
        if selected_cat == "All Categories"
        else [ins for ins in insights if ins["category"] == selected_cat]
    )

    if not filtered_insights:
        st.info("No insights matching the selected category filter.")
    else:
        for ins in filtered_insights:
            render_insight_card(
                category=ins["category"],
                title=ins["title"],
                message=ins["message"],
                type_str=ins["type"],
            )

    st.markdown("---")
    st.markdown("### 📌 Managerial Action Checklist")
    st.markdown(
        """
        - **Supervisory Reviews:** Schedule 1-on-1 check-ins with individuals falling below the attendance benchmark.
        - **Workload Balance:** Verify whether departments experiencing high unplanned absences are facing workload fatigue.
        - **Leave Planning:** Promote 48-hour advance notice for planned leaves to streamline shift schedules.
        - **Recognition:** Celebrate team members with 100% attendance during monthly or quarterly team meetings.
        """
    )
