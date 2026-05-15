"""
Reusable Plotly chart functions for NovaSales Dashboard.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

COLORS = {
    'primary': '#6C63FF',
    'success': '#22C55E',
    'warning': '#F59E0B',
    'danger': '#EF4444',
    'neutral': '#64748B',
    'bg': '#0F172A',
    'card': '#1E293B',
    'text': '#F1F5F9',
}

REGION_COLORS = {
    'North': '#6C63FF',
    'South': '#22C55E',
    'East': '#F59E0B',
    'West': '#EF4444',
}

PRODUCT_COLORS = {
    'CloudCore': '#818CF8',
    'DataSync': '#34D399',
    'SecureAPI': '#FBBF24',
}


def monthly_payout_trend(df):
    monthly = (
        df.groupby(['month', 'month_label'], as_index=False)
        .agg(total_payout=('total_payout', 'sum'),
             commission=('commission_earned', 'sum'))
        .sort_values('month')
    )

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly['month_label'], y=monthly['total_payout'],
        name='Total Payout', mode='lines+markers',
        line=dict(color=COLORS['primary'], width=3),
        marker=dict(size=8),
        fill='tozeroy', fillcolor='rgba(108,99,255,0.15)',
    ))
    fig.add_trace(go.Scatter(
        x=monthly['month_label'], y=monthly['commission'],
        name='Commission Only', mode='lines+markers',
        line=dict(color=COLORS['success'], width=2, dash='dash'),
        marker=dict(size=6),
    ))
    fig.update_layout(
        title='Monthly Payout Trend (2024)',
        xaxis_title='Month', yaxis_title='Amount (Rs.)',
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['text']),
        legend=dict(orientation='h', y=1.1), hovermode='x unified',
    )
    return fig


def attainment_gauge(attainment_pct, rep_name):
    color = (COLORS['danger'] if attainment_pct < 60 else
             COLORS['warning'] if attainment_pct < 85 else
             COLORS['success'])

    fig = go.Figure(go.Indicator(
        mode='gauge+number+delta',
        value=attainment_pct,
        delta={'reference': 100, 'suffix': '%'},
        title={'text': f"{rep_name}<br>Quota Attainment", 'font': {'size': 14}},
        number={'suffix': '%', 'font': {'size': 28}},
        gauge={
            'axis': {'range': [0, 150], 'ticksuffix': '%'},
            'bar': {'color': color, 'thickness': 0.3},
            'steps': [
                {'range': [0, 50], 'color': 'rgba(239,68,68,0.2)'},
                {'range': [50, 80], 'color': 'rgba(245,158,11,0.2)'},
                {'range': [80, 100], 'color': 'rgba(34,197,94,0.2)'},
                {'range': [100, 150], 'color': 'rgba(108,99,255,0.2)'},
            ],
            'threshold': {
                'line': {'color': 'white', 'width': 3},
                'thickness': 0.8, 'value': 100,
            },
        }
    ))
    fig.update_layout(
        height=280, paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['text']),
        margin=dict(t=60, b=10, l=20, r=20),
    )
    return fig


def rep_quota_vs_actual_bar(rep_df):
    rep_df = rep_df.sort_values('month')
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=rep_df['month_label'], y=rep_df['monthly_target'],
        name='Quota', marker_color='rgba(108,99,255,0.5)',
        marker_line_color=COLORS['primary'], marker_line_width=1.5,
    ))
    fig.add_trace(go.Bar(
        x=rep_df['month_label'], y=rep_df['actual_sales'],
        name='Actual Sales', marker_color=COLORS['success'],
    ))
    fig.update_layout(
        barmode='group', title='Monthly Quota vs Actual Sales',
        xaxis_title='Month', yaxis_title='Amount (Rs.)',
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['text']),
        legend=dict(orientation='h', y=1.1),
    )
    return fig


def commission_line_chart(rep_df):
    rep_df = rep_df.sort_values('month')
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=rep_df['month_label'], y=rep_df['commission_earned'],
        mode='lines+markers', name='Commission',
        line=dict(color=COLORS['warning'], width=3),
        marker=dict(size=8, color=COLORS['warning']),
        fill='tozeroy', fillcolor='rgba(245,158,11,0.15)',
    ))
    fig.add_trace(go.Scatter(
        x=rep_df['month_label'], y=rep_df['bonus_earned'],
        mode='lines+markers', name='Bonus',
        line=dict(color=COLORS['success'], width=2, dash='dot'),
        marker=dict(size=6),
    ))
    fig.update_layout(
        title='Commission & Bonus Earned Per Month',
        xaxis_title='Month', yaxis_title='Amount (Rs.)',
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['text']), hovermode='x unified',
    )
    return fig


def region_heatmap(df):
    pivot = (
        df.groupby(['region', 'month_label', 'month'])['attainment_pct_display']
        .mean().reset_index().sort_values('month')
        .pivot(index='region', columns='month_label', values='attainment_pct_display')
    )
    month_order = ['Jan 2024', 'Feb 2024', 'Mar 2024', 'Apr 2024',
                   'May 2024', 'Jun 2024', 'Jul 2024', 'Aug 2024',
                   'Sep 2024', 'Oct 2024', 'Nov 2024', 'Dec 2024']
    pivot = pivot.reindex(columns=[c for c in month_order if c in pivot.columns])

    fig = go.Figure(go.Heatmap(
        z=pivot.values, x=pivot.columns.tolist(), y=pivot.index.tolist(),
        colorscale=[
            [0.00, '#EF4444'], [0.33, '#F59E0B'],
            [0.66, '#22C55E'], [1.00, '#6C63FF'],
        ],
        zmin=50, zmax=130,
        text=pivot.values.round(1), texttemplate='%{text}%',
        textfont=dict(size=11),
        hovertemplate='Region: %{y}<br>Month: %{x}<br>Attainment: %{z:.1f}%<extra></extra>',
        colorbar=dict(title='Attainment %', ticksuffix='%'),
    ))
    fig.update_layout(
        title='Region x Month Quota Attainment Heatmap',
        xaxis_title='Month', yaxis_title='Region',
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['text']), height=300,
    )
    return fig


def product_region_bar(df):
    agg = (
        df.groupby(['region', 'product_line'])['attainment_pct_display']
        .mean().reset_index()
    )
    fig = px.bar(
        agg, x='region', y='attainment_pct_display', color='product_line',
        barmode='group', title='Product Line Performance by Region',
        labels={'attainment_pct_display': 'Avg Attainment %', 'region': 'Region'},
        color_discrete_map=PRODUCT_COLORS,
    )
    fig.add_hline(y=100, line_dash='dash', line_color='white',
                  annotation_text='Quota Line', annotation_position='top right')
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['text']), legend_title='Product Line',
    )
    return fig


def waterfall_payout(df):
    agg = (
        df.groupby('region')
        .agg(base=('monthly_base', 'sum'),
             commission=('commission_earned', 'sum'),
             bonus=('bonus_earned', 'sum'))
        .reset_index()
    )
    fig = go.Figure(go.Bar(
        x=agg['region'], y=agg['base'],
        name='Base Salary (Monthly)', marker_color='rgba(108,99,255,0.7)',
    ))
    fig.add_trace(go.Bar(
        x=agg['region'], y=agg['commission'],
        name='Commission', marker_color=COLORS['warning'],
    ))
    fig.add_trace(go.Bar(
        x=agg['region'], y=agg['bonus'],
        name='Bonus', marker_color=COLORS['success'],
    ))
    fig.update_layout(
        barmode='stack', title='Total Payout Breakdown by Region',
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['text']), yaxis_title='Amount (Rs.)',
    )
    return fig