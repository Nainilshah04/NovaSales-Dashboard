"""
Reusable Plotly chart functions for NovaSales Dashboard.
Adapts dynamically to Light & Dark themes.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import streamlit as st

def get_theme_colors():
    """Returns dynamic color palette based on current theme."""
    theme = st.session_state.get('theme', 'dark')
    
    if theme == 'dark':
        return {
            'primary': '#A78BFA',      # Purple 300
            'success': '#34D399',      # Emerald 400
            'warning': '#FBBF24',      # Amber 400
            'danger': '#F87171',       # Red 400
            'neutral': '#94A3B8',      # Slate 400
            'text': '#F8FAFC',         # Slate 50
            'grid': 'rgba(255, 255, 255, 0.08)',
            'fill_primary': 'rgba(167, 139, 250, 0.08)',
            'fill_warning': 'rgba(251, 191, 36, 0.08)',
            'axis_title': '#94A3B8',
            'steps_danger': 'rgba(248, 113, 113, 0.15)',
            'steps_warning': 'rgba(251, 191, 36, 0.15)',
            'steps_success': 'rgba(52, 211, 153, 0.15)',
            'steps_primary': 'rgba(167, 139, 250, 0.15)',
            'regions': {
                'North': '#A78BFA',
                'South': '#34D399',
                'East': '#FBBF24',
                'West': '#F87171',
            },
            'products': {
                'CloudCore': '#C084FC',
                'DataSync': '#2DD4BF',
                'SecureAPI': '#FBBF24',
            }
        }
    else:
        return {
            'primary': '#6D28D9',      # Purple 700
            'success': '#10B981',      # Emerald 500
            'warning': '#D97706',      # Amber 600
            'danger': '#DC2626',       # Red 600
            'neutral': '#475569',      # Slate 600
            'text': '#0F172A',         # Slate 900
            'grid': '#E2E8F0',         # Slate 200
            'fill_primary': 'rgba(109, 40, 217, 0.06)',
            'fill_warning': 'rgba(217, 119, 6, 0.06)',
            'axis_title': '#475569',
            'steps_danger': 'rgba(220, 38, 38, 0.08)',
            'steps_warning': 'rgba(217, 119, 6, 0.08)',
            'steps_success': 'rgba(16, 185, 129, 0.08)',
            'steps_primary': 'rgba(109, 40, 217, 0.08)',
            'regions': {
                'North': '#6D28D9',
                'South': '#10B981',
                'East': '#D97706',
                'West': '#DC2626',
            },
            'products': {
                'CloudCore': '#7C3AED',
                'DataSync': '#0D9488',
                'SecureAPI': '#B45309',
            }
        }

def monthly_payout_trend(df):
    c = get_theme_colors()
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
        line=dict(color=c['primary'], width=3),
        marker=dict(size=8),
        fill='tozeroy', fillcolor=c['fill_primary'],
    ))
    fig.add_trace(go.Scatter(
        x=monthly['month_label'], y=monthly['commission'],
        name='Commission Only', mode='lines+markers',
        line=dict(color=c['success'], width=2, dash='dash'),
        marker=dict(size=6),
    ))
    
    fig.update_layout(
        title=None,
        xaxis=dict(title='Month', gridcolor=c['grid'], color=c['text']),
        yaxis=dict(title='Amount (₹)', gridcolor=c['grid'], color=c['text']),
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=c['text'], family='Inter'),
        legend=dict(orientation='h', y=1.12, font=dict(size=11)), 
        hovermode='x unified',
        margin=dict(t=30, b=30, l=10, r=10),
    )
    return fig


def attainment_gauge(attainment_pct, rep_name):
    c = get_theme_colors()
    color = (c['danger'] if attainment_pct < 60 else
             c['warning'] if attainment_pct < 85 else
             c['success'])

    fig = go.Figure(go.Indicator(
        mode='gauge+number+delta',
        value=attainment_pct,
        delta={'reference': 100, 'suffix': '%'},
        title={'text': f"<b>{rep_name}</b><br><span style='font-size:12px;color:{c['neutral']}'>Quota Attainment</span>", 'font': {'size': 14, 'family': 'Inter'}},
        number={'suffix': '%', 'font': {'size': 28, 'family': 'Inter'}, 'valueformat': '.1f'},
        gauge={
            'axis': {'range': [0, 150], 'ticksuffix': '%'},
            'bar': {'color': color, 'thickness': 0.28},
            'steps': [
                {'range': [0, 50], 'color': c['steps_danger']},
                {'range': [50, 80], 'color': c['steps_warning']},
                {'range': [80, 100], 'color': c['steps_success']},
                {'range': [100, 150], 'color': c['steps_primary']},
            ],
            'threshold': {
                'line': {'color': c['text'], 'width': 3},
                'thickness': 0.8, 'value': 100,
            },
        }
    ))
    fig.update_layout(
        height=260, paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=c['text'], family='Inter'),
        margin=dict(t=30, b=10, l=20, r=20),
    )
    return fig


def rep_quota_vs_actual_bar(rep_df):
    c = get_theme_colors()
    rep_df = rep_df.sort_values('month')
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=rep_df['month_label'], y=rep_df['monthly_target'],
        name='Quota', marker_color=c['fill_primary'],
        marker_line_color=c['primary'], marker_line_width=1.5,
    ))
    fig.add_trace(go.Bar(
        x=rep_df['month_label'], y=rep_df['actual_sales'],
        name='Actual Sales', marker_color=c['success'],
    ))
    
    fig.update_layout(
        barmode='group', 
        title=None,
        xaxis=dict(title='Month', color=c['text'], gridcolor=c['grid']),
        yaxis=dict(title='Amount (₹)', color=c['text'], gridcolor=c['grid']),
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=c['text'], family='Inter'),
        legend=dict(orientation='h', y=1.12, font=dict(size=11)),
        margin=dict(t=30, b=30, l=10, r=10),
    )
    return fig


def commission_line_chart(rep_df):
    c = get_theme_colors()
    rep_df = rep_df.sort_values('month')
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=rep_df['month_label'], y=rep_df['commission_earned'],
        mode='lines+markers', name='Commission',
        line=dict(color=c['warning'], width=3),
        marker=dict(size=8, color=c['warning']),
        fill='tozeroy', fillcolor=c['fill_warning'],
    ))
    fig.add_trace(go.Scatter(
        x=rep_df['month_label'], y=rep_df['bonus_earned'],
        mode='lines+markers', name='Bonus',
        line=dict(color=c['success'], width=2, dash='dot'),
        marker=dict(size=6),
    ))
    
    fig.update_layout(
        title=None,
        xaxis=dict(title='Month', color=c['text'], gridcolor=c['grid']),
        yaxis=dict(title='Amount (₹)', color=c['text'], gridcolor=c['grid']),
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=c['text'], family='Inter'), 
        hovermode='x unified',
        legend=dict(orientation='h', y=1.12, font=dict(size=11)),
        margin=dict(t=30, b=30, l=10, r=10),
    )
    return fig


def region_heatmap(df):
    c = get_theme_colors()
    pivot = (
        df.groupby(['region', 'month_label', 'month'])['attainment_pct_display']
        .mean().reset_index().sort_values('month')
        .pivot(index='region', columns='month_label', values='attainment_pct_display')
    )
    month_order = ['Jan 2024', 'Feb 2024', 'Mar 2024', 'Apr 2024',
                   'May 2024', 'Jun 2024', 'Jul 2024', 'Aug 2024',
                   'Sep 2024', 'Oct 2024', 'Nov 2024', 'Dec 2024']
    pivot = pivot.reindex(columns=[col for col in month_order if col in pivot.columns])

    # Dynamic colormap based on theme contrast
    colorscale = [
        [0.00, c['danger']], 
        [0.45, c['warning']],
        [0.75, c['success']], 
        [1.00, c['primary']],
    ]

    fig = go.Figure(go.Heatmap(
        z=pivot.values, x=pivot.columns.tolist(), y=pivot.index.tolist(),
        colorscale=colorscale,
        zmin=50, zmax=130,
        text=pivot.values.round(1), texttemplate='%{text}%',
        textfont=dict(size=11, family='Inter', color='#FFFFFF'), # Keep labels white for contrast on heat color
        hovertemplate='Region: %{y}<br>Month: %{x}<br>Attainment: %{z:.1f}%<extra></extra>',
        colorbar=dict(title='Attainment %', ticksuffix='%', tickcolor=c['text']),
    ))
    
    fig.update_layout(
        title=None,
        xaxis=dict(title='Month', color=c['text']),
        yaxis=dict(title='Region', color=c['text']),
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=c['text'], family='Inter'), 
        height=320,
        margin=dict(t=30, b=30, l=10, r=10),
    )
    return fig


def product_region_bar(df):
    c = get_theme_colors()
    agg = (
        df.groupby(['region', 'product_line'])['attainment_pct_display']
        .mean().reset_index()
    )
    fig = px.bar(
        agg, x='region', y='attainment_pct_display', color='product_line',
        barmode='group', title=None,
        labels={'attainment_pct_display': 'Avg Attainment %', 'region': 'Region'},
        color_discrete_map=c['products'],
    )
    fig.add_hline(y=100, line_dash='dash', line_color=c['text'],
                  annotation_text='Quota Line', annotation_position='top right',
                  annotation_font=dict(color=c['text']))
                  
    fig.update_layout(
        xaxis=dict(color=c['text'], gridcolor='rgba(0,0,0,0)'),
        yaxis=dict(color=c['text'], gridcolor=c['grid']),
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=c['text'], family='Inter'), 
        legend_title='Product Line',
        legend=dict(font=dict(size=11)),
        margin=dict(t=30, b=30, l=10, r=10),
    )
    return fig


def waterfall_payout(df):
    c = get_theme_colors()
    agg = (
        df.groupby('region')
        .agg(base=('monthly_base', 'sum'),
             commission=('commission_earned', 'sum'),
             bonus=('bonus_earned', 'sum'))
        .reset_index()
    )
    fig = go.Figure(go.Bar(
        x=agg['region'], y=agg['base'],
        name='Base Salary (Monthly)', marker_color=c['fill_primary'],
        marker_line_color=c['primary'], marker_line_width=1.5,
    ))
    fig.add_trace(go.Bar(
        x=agg['region'], y=agg['commission'],
        name='Commission', marker_color=c['warning'],
    ))
    fig.add_trace(go.Bar(
        x=agg['region'], y=agg['bonus'],
        name='Bonus', marker_color=c['success'],
    ))
    
    fig.update_layout(
        barmode='stack', 
        title=None,
        xaxis=dict(color=c['text'], gridcolor='rgba(0,0,0,0)'),
        yaxis=dict(title='Amount (₹)', color=c['text'], gridcolor=c['grid']),
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=c['text'], family='Inter'),
        legend=dict(orientation='h', y=1.12, font=dict(size=11)),
        margin=dict(t=30, b=30, l=10, r=10),
    )
    return fig