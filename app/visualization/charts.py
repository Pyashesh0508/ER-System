"""Plotly visualization charts for employee attendance and workforce insights."""

from typing import Optional
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from app.config import (
    COL_EMP_ID,
    COL_NAME,
    COL_DEPT,
    COL_WORKING_DAYS,
    COL_PRESENT_DAYS,
    COL_ABSENT_DAYS,
    COL_LEAVE_DAYS,
    COL_ATTENDANCE_PCT,
    COLOR_PRESENT,
    COLOR_ABSENT,
    COLOR_LEAVE,
    COLOR_PRIMARY,
    COLOR_ACCENT,
    DEFAULT_ATTENDANCE_THRESHOLD,
)
from app.analysis.attendance import calculate_attendance_percentage
from app.analysis.department import get_department_summary


def chart_department_attendance(df: pd.DataFrame) -> go.Figure:
    """Create department-wise average attendance bar chart with benchmark line."""
    dept_df = get_department_summary(df)
    if dept_df.empty:
        return go.Figure()

    fig = px.bar(
        dept_df,
        x=COL_DEPT,
        y="Average_Attendance_Pct",
        text="Average_Attendance_Pct",
        color="Average_Attendance_Pct",
        color_continuous_scale="Blues",
        labels={
            COL_DEPT: "Department",
            "Average_Attendance_Pct": "Avg Attendance (%)",
        },
        title="Department-Wise Average Attendance Rate (%)",
    )

    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Average Attendance: %{y:.2f}%<extra></extra>",
    )

    overall_avg = df[COL_ATTENDANCE_PCT].mean() if COL_ATTENDANCE_PCT in df.columns else 0.0
    if overall_avg > 0:
        fig.add_hline(
            y=overall_avg,
            line_dash="dash",
            line_color="crimson",
            annotation_text=f"Company Avg ({overall_avg:.1f}%)",
            annotation_position="top right",
        )

    fig.update_layout(
        template="plotly_white",
        yaxis=dict(range=[0, 110], title="Average Attendance (%)"),
        xaxis_title="Department",
        coloraxis_showscale=False,
        margin=dict(l=40, r=40, t=60, b=40),
        height=420,
    )
    return fig


def chart_present_absent_leave_donut(df: pd.DataFrame) -> go.Figure:
    """Create donut chart showing overall present vs absent vs leave days."""
    if df.empty:
        return go.Figure()

    total_present = df[COL_PRESENT_DAYS].sum()
    total_absent = df[COL_ABSENT_DAYS].sum()
    total_leave = df[COL_LEAVE_DAYS].sum()

    labels = ["Present Days", "Absent Days", "Leave Days"]
    values = [total_present, total_absent, total_leave]
    colors = [COLOR_PRESENT, COLOR_ABSENT, COLOR_LEAVE]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.55,
                marker=dict(colors=colors),
                textinfo="label+percent",
                hovertemplate="<b>%{label}</b><br>Total Days: %{value}<br>Share: %{percent}<extra></extra>",
            )
        ]
    )

    fig.update_layout(
        title="Overall Workforce Time Distribution (Days)",
        template="plotly_white",
        margin=dict(l=20, r=20, t=50, b=20),
        height=380,
        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
    )
    return fig


def chart_attendance_distribution(df: pd.DataFrame) -> go.Figure:
    """Create attendance percentage distribution histogram with threshold marker."""
    if df.empty:
        return go.Figure()

    if COL_ATTENDANCE_PCT not in df.columns:
        df = calculate_attendance_percentage(df)

    fig = px.histogram(
        df,
        x=COL_ATTENDANCE_PCT,
        nbins=12,
        marginal="box",
        labels={COL_ATTENDANCE_PCT: "Attendance Percentage (%)"},
        title="Employee Attendance Distribution (%)",
        color_discrete_sequence=[COLOR_PRIMARY],
    )

    fig.update_layout(
        template="plotly_white",
        xaxis_title="Attendance Percentage (%)",
        yaxis_title="Number of Employees",
        margin=dict(l=40, r=40, t=60, b=40),
        height=400,
    )
    return fig


def chart_employee_attendance_ranking(
    df: pd.DataFrame, threshold: float = DEFAULT_ATTENDANCE_THRESHOLD
) -> go.Figure:
    """Create horizontal bar chart of all employees sorted by attendance percentage."""
    if df.empty:
        return go.Figure()

    if COL_ATTENDANCE_PCT not in df.columns:
        df = calculate_attendance_percentage(df)

    sorted_df = df.sort_values(by=COL_ATTENDANCE_PCT, ascending=True)

    colors = [
        COLOR_ABSENT if val < threshold else COLOR_PRESENT
        for val in sorted_df[COL_ATTENDANCE_PCT]
    ]

    fig = go.Figure(
        go.Bar(
            x=sorted_df[COL_ATTENDANCE_PCT],
            y=sorted_df[COL_NAME],
            orientation="h",
            marker=dict(color=colors),
            text=sorted_df[COL_ATTENDANCE_PCT].apply(lambda x: f"{x:.1f}%"),
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Attendance: %{x:.2f}%<extra></extra>",
        )
    )

    fig.add_vline(
        x=threshold,
        line_dash="dash",
        line_color="#E65100",
        annotation_text=f"Threshold ({threshold}%)",
        annotation_position="top left",
    )

    dynamic_height = max(400, len(sorted_df) * 24)

    fig.update_layout(
        title="Employee Attendance Ranking & Benchmark Comparison",
        template="plotly_white",
        xaxis=dict(range=[0, 115], title="Attendance Percentage (%)"),
        yaxis_title="Employee",
        margin=dict(l=60, r=60, t=50, b=40),
        height=dynamic_height,
    )
    return fig


def chart_department_leaves_absences(df: pd.DataFrame) -> go.Figure:
    """Create grouped bar chart comparing average leaves vs average absences per department."""
    dept_df = get_department_summary(df)
    if dept_df.empty:
        return go.Figure()

    fig = go.Figure(
        data=[
            go.Bar(
                name="Avg Leave Days",
                x=dept_df[COL_DEPT],
                y=dept_df["Avg_Leave_Days"],
                marker_color=COLOR_LEAVE,
                text=dept_df["Avg_Leave_Days"].apply(lambda v: f"{v:.1f}"),
                textposition="outside",
            ),
            go.Bar(
                name="Avg Absent Days",
                x=dept_df[COL_DEPT],
                y=dept_df["Avg_Absent_Days"],
                marker_color=COLOR_ABSENT,
                text=dept_df["Avg_Absent_Days"].apply(lambda v: f"{v:.1f}"),
                textposition="outside",
            ),
        ]
    )

    fig.update_layout(
        barmode="group",
        title="Department Average: Planned Leaves vs Unplanned Absences",
        template="plotly_white",
        xaxis_title="Department",
        yaxis_title="Average Days per Employee",
        margin=dict(l=40, r=40, t=60, b=40),
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def chart_low_attendance_employees(
    df: pd.DataFrame, threshold: float = DEFAULT_ATTENDANCE_THRESHOLD
) -> go.Figure:
    """Create focused bar chart of employees falling strictly below attendance threshold."""
    if df.empty:
        return go.Figure()

    if COL_ATTENDANCE_PCT not in df.columns:
        df = calculate_attendance_percentage(df)

    low_df = df[df[COL_ATTENDANCE_PCT] < threshold].sort_values(
        by=COL_ATTENDANCE_PCT, ascending=True
    )

    if low_df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="No employees found below the selected attendance threshold.",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=14, color="gray"),
        )
        fig.update_layout(
            title=f"Employees Below {threshold}% Attendance Benchmark",
            template="plotly_white",
            height=300,
        )
        return fig

    fig = px.bar(
        low_df,
        x=COL_NAME,
        y=COL_ATTENDANCE_PCT,
        color=COL_DEPT,
        text=COL_ATTENDANCE_PCT,
        labels={
            COL_NAME: "Employee Name",
            COL_ATTENDANCE_PCT: "Attendance (%)",
            COL_DEPT: "Department",
        },
        title=f"Employees Below {threshold}% Attendance Benchmark ({len(low_df)} Identified)",
    )

    fig.add_hline(
        y=threshold,
        line_dash="dot",
        line_color="red",
        annotation_text=f"Benchmark ({threshold}%)",
    )

    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
        hovertemplate="<b>%{x}</b> (%{customdata[0]})<br>Attendance: %{y:.2f}%<extra></extra>",
        customdata=low_df[[COL_DEPT]],
    )

    fig.update_layout(
        template="plotly_white",
        yaxis=dict(range=[0, max(threshold + 15, 100)]),
        margin=dict(l=40, r=40, t=60, b=40),
        height=420,
    )
    return fig


def chart_single_employee_breakdown(emp_row: pd.Series) -> go.Figure:
    """Create individual employee attendance breakdown donut chart."""
    labels = ["Present Days", "Absent Days", "Leave Days"]
    values = [
        int(emp_row[COL_PRESENT_DAYS]),
        int(emp_row[COL_ABSENT_DAYS]),
        int(emp_row[COL_LEAVE_DAYS]),
    ]
    colors = [COLOR_PRESENT, COLOR_ABSENT, COLOR_LEAVE]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.6,
                marker=dict(colors=colors),
                textinfo="label+value",
                hovertemplate="<b>%{label}</b>: %{value} days<extra></extra>",
            )
        ]
    )

    pct = emp_row.get(COL_ATTENDANCE_PCT, 0.0)
    fig.update_layout(
        title=f"Day Breakdown for {emp_row[COL_NAME]} ({pct:.1f}% Attendance)",
        template="plotly_white",
        margin=dict(l=20, r=20, t=50, b=20),
        height=320,
        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
    )
    return fig
