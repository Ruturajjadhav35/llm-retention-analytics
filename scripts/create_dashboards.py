
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

# ============================================
# SETUP
# ============================================

os.makedirs('dashboards', exist_ok=True)

plt.rcParams['figure.dpi'] = 150
plt.rcParams['savefig.dpi'] = 150
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

COLORS = {
    'blue':   '#3498db',
    'green':  '#2ecc71',
    'red':    '#e74c3c',
    'orange': '#f39c12',
    'purple': '#9b59b6',
    'teal':   '#1abc9c',
    'dark':   '#2c3e50',
    'gray':   '#95a5a6',
}

SEGMENT_COLORS = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12']

print("=" * 70)
print("CREATING PYTHON DASHBOARDS (FIXED VERSION)")
print("=" * 70)
print()

# ============================================
# LOAD ALL DATA
# ============================================

print("Loading data from results folder...")

df_segments   = pd.read_csv('results/user_segments.csv')
df_events     = pd.read_csv('results/event_types.csv')
df_features   = pd.read_csv('results/feature_adoption.csv')
df_retention  = pd.read_csv('results/retention_by_segment.csv')
df_conversion = pd.read_csv('results/conversion_rate.csv')

# Pull conversion values
free_users     = int(df_conversion['free_users'].values[0])
upgraded_users = int(df_conversion['upgraded_users'].values[0])
not_converted  = free_users - upgraded_users
conv_rate      = float(df_conversion['conversion_rate'].values[0])

print("  ✓ All files loaded!")
print()

# ============================================
# DASHBOARD 1: USER SEGMENT DISTRIBUTION
# ============================================

print("Creating Dashboard 1: User Segment Distribution...")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
fig.patch.set_facecolor('white')
fig.suptitle('User Segment Distribution', fontsize=18,
             fontweight='bold', color=COLORS['dark'], y=1.02)

# Donut chart
wedges, texts, autotexts = ax1.pie(
    df_segments['user_count'],
    labels=df_segments['user_segment'],
    autopct='%1.1f%%',
    colors=SEGMENT_COLORS,
    startangle=90,
    pctdistance=0.82,
    wedgeprops=dict(width=0.6, edgecolor='white', linewidth=3)
)
for t in texts:
    t.set_fontsize(12)
    t.set_fontweight('bold')
for at in autotexts:
    at.set_fontsize(10)
    at.set_fontweight('bold')
    at.set_color('white')

ax1.set_title('Breakdown by Segment', fontsize=13,
              fontweight='bold', color=COLORS['dark'], pad=15)

# Horizontal bar chart
df_seg_sorted = df_segments.sort_values('user_count', ascending=True)
bars = ax2.barh(df_seg_sorted['user_segment'],
                df_seg_sorted['user_count'],
                color=SEGMENT_COLORS, height=0.5, edgecolor='white')

for bar in bars:
    val = bar.get_width()
    ax2.text(val + 100, bar.get_y() + bar.get_height() / 2,
             f'{val:,.0f}', va='center', fontsize=11,
             fontweight='bold', color=COLORS['dark'])

ax2.set_title('User Count by Segment', fontsize=13,
              fontweight='bold', color=COLORS['dark'], pad=15)
ax2.set_xlabel('Number of Users', fontsize=11)
ax2.grid(axis='x', alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig('dashboards/01_user_segments.png',
            bbox_inches='tight', facecolor='white')
plt.close()
print("  ✓ Saved: dashboards/01_user_segments.png")
print()

# ============================================
# DASHBOARD 2: EVENT TYPE ANALYSIS
# ============================================

print("Creating Dashboard 2: Event Type Analysis...")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
fig.patch.set_facecolor('white')
fig.suptitle('Platform Usage — Event Type Analysis', fontsize=18,
             fontweight='bold', color=COLORS['dark'], y=1.02)

event_colors = [COLORS['blue'], COLORS['green'], COLORS['orange'],
                COLORS['red'], COLORS['purple'], COLORS['teal'], COLORS['gray']]

# Total events bar
df_ev = df_events.sort_values('event_count', ascending=False)
bars = ax1.bar(range(len(df_ev)), df_ev['event_count'],
               color=event_colors, edgecolor='white', linewidth=1.5)
ax1.set_xticks(range(len(df_ev)))
ax1.set_xticklabels(df_ev['event_type'], rotation=40, ha='right', fontsize=9)
ax1.set_title('Total Events by Type', fontsize=13,
              fontweight='bold', color=COLORS['dark'], pad=15)
ax1.set_ylabel('Event Count', fontsize=11)
ax1.grid(axis='y', alpha=0.3, linestyle='--')

for bar in bars:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width() / 2., height,
             f'{height:,.0f}', ha='center', va='bottom',
             fontsize=8, fontweight='bold')

# Unique users horizontal bar
df_ev_u = df_events.sort_values('unique_users', ascending=True)
bars2 = ax2.barh(range(len(df_ev_u)), df_ev_u['unique_users'],
                  color=event_colors, edgecolor='white')
ax2.set_yticks(range(len(df_ev_u)))
ax2.set_yticklabels(df_ev_u['event_type'], fontsize=10)
ax2.set_title('Unique Users per Event Type', fontsize=13,
              fontweight='bold', color=COLORS['dark'], pad=15)
ax2.set_xlabel('Unique Users', fontsize=11)
ax2.grid(axis='x', alpha=0.3, linestyle='--')

for bar in bars2:
    val = bar.get_width()
    ax2.text(val + 50, bar.get_y() + bar.get_height() / 2,
             f'{val:,.0f}', va='center', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('dashboards/02_event_types.png',
            bbox_inches='tight', facecolor='white')
plt.close()
print("  ✓ Saved: dashboards/02_event_types.png")
print()

# ============================================
# DASHBOARD 3: FEATURE ADOPTION
# ============================================

print("Creating Dashboard 3: Feature Adoption Analysis...")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
fig.patch.set_facecolor('white')
fig.suptitle('Feature Adoption Analysis', fontsize=18,
             fontweight='bold', color=COLORS['dark'], y=1.02)

# Adoption rate horizontal bar  (uses: adoption_rate ✓)
df_feat = df_features.sort_values('adoption_rate', ascending=True)
bar_colors = plt.cm.RdYlGn(
    df_feat['adoption_rate'] / df_feat['adoption_rate'].max())

bars = ax1.barh(df_feat['feature_used'], df_feat['adoption_rate'],
                color=bar_colors, edgecolor='white')
ax1.set_title('Feature Adoption Rate (%)', fontsize=13,
              fontweight='bold', color=COLORS['dark'], pad=15)
ax1.set_xlabel('Adoption Rate (%)', fontsize=11)
ax1.grid(axis='x', alpha=0.3, linestyle='--')

for bar in bars:
    val = bar.get_width()
    ax1.text(val + 0.3, bar.get_y() + bar.get_height() / 2,
             f'{val:.1f}%', va='center', fontsize=10, fontweight='bold')

# Users using each feature (uses: users_using_feature ✓)
df_feat2 = df_features.sort_values('users_using_feature', ascending=False)
bars2 = ax2.bar(range(len(df_feat2)), df_feat2['users_using_feature'],
                color=COLORS['blue'], alpha=0.85, edgecolor='white')
ax2.set_xticks(range(len(df_feat2)))
ax2.set_xticklabels(df_feat2['feature_used'], rotation=40,
                     ha='right', fontsize=9)
ax2.set_title('Total Users per Feature', fontsize=13,
              fontweight='bold', color=COLORS['dark'], pad=15)
ax2.set_ylabel('Users', fontsize=11)
ax2.grid(axis='y', alpha=0.3, linestyle='--')

for bar in bars2:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width() / 2., height,
             f'{height:,.0f}', ha='center', va='bottom',
             fontsize=8, fontweight='bold')

plt.tight_layout()
plt.savefig('dashboards/03_feature_adoption.png',
            bbox_inches='tight', facecolor='white')
plt.close()
print("  ✓ Saved: dashboards/03_feature_adoption.png")
print()

# ============================================
# DASHBOARD 4: RETENTION ANALYSIS
# ============================================

print("Creating Dashboard 4: Retention Analysis...")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
fig.patch.set_facecolor('white')
fig.suptitle('30-Day Retention Analysis by User Segment', fontsize=18,
             fontweight='bold', color=COLORS['dark'], y=1.02)

# Uses: retention_rate  (NOT retention_rate_30d) ✓
df_ret = df_retention.sort_values('retention_rate', ascending=False)
ret_colors = plt.cm.RdYlGn(df_ret['retention_rate'] / 100)

bars = ax1.bar(df_ret['user_segment'], df_ret['retention_rate'],
               color=ret_colors, edgecolor='white', linewidth=1.5, width=0.5)
ax1.set_title('Retention Rate by Segment', fontsize=13,
              fontweight='bold', color=COLORS['dark'], pad=15)
ax1.set_ylabel('30-Day Retention Rate (%)', fontsize=11)
ax1.set_xlabel('User Segment', fontsize=11)
ax1.set_ylim(0, 110)
ax1.grid(axis='y', alpha=0.3, linestyle='--')
ax1.axhline(y=40, color=COLORS['orange'], linestyle='--',
            linewidth=2, label='Industry Benchmark (40%)')
ax1.legend(fontsize=10)

for bar in bars:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width() / 2., height + 1,
             f'{height:.1f}%', ha='center', va='bottom',
             fontsize=12, fontweight='bold')

# Stacked retained vs churned (uses: retention_rate, total_users ✓)
ax2.bar(df_ret['user_segment'], df_ret['retention_rate'],
        color=COLORS['green'], label='Retained', width=0.5, edgecolor='white')
ax2.bar(df_ret['user_segment'], 100 - df_ret['retention_rate'],
        bottom=df_ret['retention_rate'],
        color=COLORS['red'], label='Churned', width=0.5, edgecolor='white')
ax2.set_title('Retained vs Churned Users', fontsize=13,
              fontweight='bold', color=COLORS['dark'], pad=15)
ax2.set_ylabel('Percentage (%)', fontsize=11)
ax2.set_xlabel('User Segment', fontsize=11)
ax2.legend(fontsize=10)
ax2.grid(axis='y', alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig('dashboards/04_retention_analysis.png',
            bbox_inches='tight', facecolor='white')
plt.close()
print("  ✓ Saved: dashboards/04_retention_analysis.png")
print()

# ============================================
# DASHBOARD 5: CONVERSION FUNNEL
# ============================================

print("Creating Dashboard 5: Conversion Funnel...")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
fig.patch.set_facecolor('white')
fig.suptitle('Free to Paid Conversion Analysis', fontsize=18,
             fontweight='bold', color=COLORS['dark'], y=1.02)

# Funnel
funnel_values = [free_users, upgraded_users]
funnel_labels = ['Free Users', 'Converted to Paid']
funnel_colors = [COLORS['blue'], COLORS['green']]
funnel_widths = [1.0, conv_rate / 100]

for i, (value, label, color, width) in enumerate(
        zip(funnel_values, funnel_labels, funnel_colors, funnel_widths)):
    left = (1 - width) / 2
    ax1.barh(i, width, left=left, height=0.5, color=color, edgecolor='white')
    ax1.text(0.5, i, f'{label}\n{value:,}',
             ha='center', va='center', fontsize=12,
             fontweight='bold', color='white')

ax1.set_xlim(0, 1)
ax1.set_ylim(-0.5, 1.5)
ax1.axis('off')
ax1.set_title(f'Conversion Funnel  (Rate: {conv_rate:.1f}%)',
              fontsize=13, fontweight='bold', color=COLORS['dark'], pad=15)

# Donut
sizes  = [upgraded_users, not_converted]
labels = [f'Converted\n{upgraded_users:,}', f'Not Converted\n{not_converted:,}']
colors = [COLORS['green'], COLORS['gray']]

wedges, texts, autotexts = ax2.pie(
    sizes, labels=labels, colors=colors, autopct='%1.1f%%',
    startangle=90, pctdistance=0.8,
    wedgeprops=dict(width=0.6, edgecolor='white', linewidth=3)
)
for t in texts:
    t.set_fontsize(11)
for at in autotexts:
    at.set_fontsize(11)
    at.set_fontweight('bold')
    at.set_color('white')

ax2.set_title(f'Conversion Breakdown\n(Total Free: {free_users:,})',
              fontsize=13, fontweight='bold', color=COLORS['dark'], pad=15)

plt.tight_layout()
plt.savefig('dashboards/05_conversion_funnel.png',
            bbox_inches='tight', facecolor='white')
plt.close()
print("  ✓ Saved: dashboards/05_conversion_funnel.png")
print()

# ============================================
# DASHBOARD 6: EXECUTIVE SUMMARY
# ============================================

print("Creating Dashboard 6: Executive Summary Dashboard...")

fig = plt.figure(figsize=(18, 12))
fig.patch.set_facecolor('#f8f9fa')

fig.text(0.5, 0.97, 'LLM Platform Analytics — Executive Summary',
         ha='center', va='top', fontsize=22,
         fontweight='bold', color=COLORS['dark'])
fig.text(0.5, 0.935, 'Retention, Engagement & Conversion Overview',
         ha='center', va='top', fontsize=13, color=COLORS['gray'])

# KPI Cards
kpi_data = [
    (f"{df_segments['user_count'].sum():,}",
     'Total Users',              COLORS['blue']),
    (f"{df_retention['retention_rate'].mean():.1f}%",
     'Avg 30-Day Retention',     COLORS['green']),
    (f"{conv_rate:.1f}%",
     'Free → Paid Conversion',   COLORS['orange']),
    (f"{int(df_events['event_count'].sum()):,}",
     'Total Events',             COLORS['purple']),
]

for i, (value, label, color) in enumerate(kpi_data):
    ax = fig.add_axes([0.05 + i * 0.235, 0.78, 0.20, 0.12])
    ax.set_facecolor(color)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    ax.text(0.5, 0.68, value, ha='center', va='center',
            fontsize=22, fontweight='bold', color='white')
    ax.text(0.5, 0.25, label, ha='center', va='center',
            fontsize=10, color='white', alpha=0.9)

# Chart 1: Segments pie
ax_pie = fig.add_axes([0.03, 0.36, 0.28, 0.38])
ax_pie.pie(df_segments['user_count'],
           labels=df_segments['user_segment'],
           autopct='%1.1f%%', colors=SEGMENT_COLORS,
           startangle=90,
           wedgeprops=dict(edgecolor='white', linewidth=2))
ax_pie.set_title('User Segments', fontsize=13,
                 fontweight='bold', color=COLORS['dark'], pad=10)

# Chart 2: Retention bars (uses: retention_rate ✓)
ax_ret = fig.add_axes([0.36, 0.36, 0.28, 0.38])
df_ret2 = df_retention.sort_values('retention_rate', ascending=True)
ret_bar_colors = plt.cm.RdYlGn(df_ret2['retention_rate'] / 100)
bars = ax_ret.barh(df_ret2['user_segment'],
                    df_ret2['retention_rate'],
                    color=ret_bar_colors, edgecolor='white')
ax_ret.set_title('30-Day Retention by Segment', fontsize=13,
                  fontweight='bold', color=COLORS['dark'], pad=10)
ax_ret.set_xlabel('Retention Rate (%)', fontsize=10)
ax_ret.set_xlim(0, 115)
ax_ret.grid(axis='x', alpha=0.3, linestyle='--')
ax_ret.spines['top'].set_visible(False)
ax_ret.spines['right'].set_visible(False)

for bar in bars:
    val = bar.get_width()
    ax_ret.text(val + 1, bar.get_y() + bar.get_height() / 2,
                f'{val:.1f}%', va='center', fontsize=10, fontweight='bold')

# Chart 3: Feature adoption (uses: adoption_rate, feature_used ✓)
ax_feat = fig.add_axes([0.68, 0.36, 0.30, 0.38])
df_feat_top = df_features.sort_values('adoption_rate', ascending=True).tail(6)
feat_colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(df_feat_top)))
bars3 = ax_feat.barh(df_feat_top['feature_used'],
                      df_feat_top['adoption_rate'],
                      color=feat_colors, edgecolor='white')
ax_feat.set_title('Top Feature Adoption', fontsize=13,
                   fontweight='bold', color=COLORS['dark'], pad=10)
ax_feat.set_xlabel('Adoption Rate (%)', fontsize=10)
ax_feat.grid(axis='x', alpha=0.3, linestyle='--')
ax_feat.spines['top'].set_visible(False)
ax_feat.spines['right'].set_visible(False)

for bar in bars3:
    val = bar.get_width()
    ax_feat.text(val + 0.3, bar.get_y() + bar.get_height() / 2,
                 f'{val:.1f}%', va='center', fontsize=10, fontweight='bold')

# Insights panel
ax_ins = fig.add_axes([0.03, 0.04, 0.94, 0.27])
ax_ins.set_facecolor('white')
ax_ins.axis('off')
ax_ins.set_xlim(0, 1)
ax_ins.set_ylim(0, 1)
ax_ins.text(0.5, 0.92, 'KEY INSIGHTS & RECOMMENDATIONS',
            ha='center', va='top', fontsize=14,
            fontweight='bold', color=COLORS['dark'])

best_segment  = df_retention.loc[
    df_retention['retention_rate'].idxmax(), 'user_segment']
worst_segment = df_retention.loc[
    df_retention['retention_rate'].idxmin(), 'user_segment']
best_ret      = df_retention['retention_rate'].max()
worst_ret     = df_retention['retention_rate'].min()
best_feature  = df_features.loc[
    df_features['adoption_rate'].idxmax(), 'feature_used']

insights = [
    ('Best Retention',
     f"{best_segment} leads with\n{best_ret:.1f}% 30-day retention",
     COLORS['green']),
    ('Needs Attention',
     f"{worst_segment} lowest at\n{worst_ret:.1f}% — needs re-engagement",
     COLORS['red']),
    ('Top Feature',
     f"'{best_feature}' has\nhighest adoption rate",
     COLORS['blue']),
    ('Conversion Opportunity',
     f"Only {conv_rate:.1f}% of free users\nconvert — test pricing & onboarding",
     COLORS['orange']),
]

for i, (title, text, color) in enumerate(insights):
    x = 0.01 + (i * 0.25)
    ax_ins.add_patch(mpatches.FancyBboxPatch(
        (x, 0.08), 0.23, 0.75,
        boxstyle="round,pad=0.02",
        facecolor=color, alpha=0.1,
        edgecolor=color, linewidth=1.5))
    ax_ins.text(x + 0.115, 0.72, title,
                ha='center', va='center', fontsize=10,
                fontweight='bold', color=color)
    ax_ins.text(x + 0.115, 0.35, text,
                ha='center', va='center', fontsize=9.5,
                color=COLORS['dark'], multialignment='center')

plt.savefig('dashboards/06_executive_summary.png',
            bbox_inches='tight', facecolor='#f8f9fa')
plt.close()
print("  ✓ Saved: dashboards/06_executive_summary.png")
print()

# ============================================
# DONE
# ============================================

print("=" * 70)
print("ALL DASHBOARDS CREATED SUCCESSFULLY!")
print("=" * 70)
print()
print("Your Dashboards (open the dashboards/ folder to view):")
print()
print("  01_user_segments.png       → User distribution & counts")
print("  02_event_types.png         → Platform usage patterns")
print("  03_feature_adoption.png    → Feature popularity & usage")
print("  04_retention_analysis.png  → 30-day retention by segment")
print("  05_conversion_funnel.png   → Free to paid conversion")
print("  06_executive_summary.png   → Full executive dashboard ⭐")
print()
print("Next steps:")
print("  1. Open dashboards/ folder in Finder to view all charts")
print("  2. Add them to your GitHub README")
print("  3. Share 06_executive_summary.png on LinkedIn!")
print()