# ============================================================
# FUTURE INTERNS – Task 3: Marketing Funnel & Conversion Analysis
# Tool: Python (Google Colab ready)
# Repository: FUTURE_DS_03
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (12, 5)

# ============================================================
# STEP 1: Load Data
# ============================================================
df = pd.read_csv("funnel_data.csv", parse_dates=["Date"])
print("Dataset Shape:", df.shape)
print(df.head())

# ============================================================
# STEP 2: Overview
# ============================================================
print("\nMissing values:\n", df.isnull().sum())
print("\nBasic Stats:\n", df.describe())

# ============================================================
# STEP 3: KPI Summary
# ============================================================
total_impressions = df["Impressions"].sum()
total_clicks = df["Clicks"].sum()
total_signups = df["Signups"].sum()
total_trials = df["Trials"].sum()
total_purchases = df["Purchases"].sum()
total_revenue = df["Revenue"].sum()

ctr = total_clicks / total_impressions * 100
signup_rate = total_signups / total_clicks * 100
trial_rate = total_trials / total_signups * 100
purchase_rate = total_purchases / total_trials * 100
overall_conversion = total_purchases / total_impressions * 100

print("\n========== KEY PERFORMANCE INDICATORS ==========")
print(f"  Total Impressions    : {total_impressions:,}")
print(f"  Total Clicks         : {total_clicks:,}")
print(f"  Total Signups        : {total_signups:,}")
print(f"  Total Trials         : {total_trials:,}")
print(f"  Total Purchases      : {total_purchases:,}")
print(f"  Total Revenue        : ${total_revenue:,.2f}")
print(f"  Click-Through Rate   : {ctr:.2f}%")
print(f"  Signup Rate          : {signup_rate:.2f}%")
print(f"  Trial Rate           : {trial_rate:.2f}%")
print(f"  Purchase Rate        : {purchase_rate:.2f}%")
print(f"  Overall Conversion   : {overall_conversion:.4f}%")
print("=================================================")

# ============================================================
# STEP 4: Funnel Chart (Bar)
# ============================================================
funnel_stages = ["Impressions", "Clicks", "Signups", "Trials", "Purchases"]
funnel_values = [total_impressions, total_clicks, total_signups, total_trials, total_purchases]
colors = ["#3498db", "#2ecc71", "#f39c12", "#e67e22", "#e74c3c"]

fig, ax = plt.subplots()
bars = ax.bar(funnel_stages, funnel_values, color=colors)
ax.set_title("Marketing Funnel Overview", fontsize=16, fontweight="bold")
ax.set_ylabel("Count")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
for bar in bars:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(funnel_values)*0.01,
            f"{bar.get_height():,.0f}", ha="center", fontsize=9)
plt.tight_layout()
plt.savefig("funnel_overview.png", dpi=150)
plt.show()

# ============================================================
# STEP 5: Conversion Rate by Channel (Bar)
# ============================================================
channel_conv = df.groupby("Channel").apply(
    lambda x: x["Purchases"].sum() / x["Clicks"].sum() * 100
).reset_index()
channel_conv.columns = ["Channel", "Conversion_Rate"]
channel_conv = channel_conv.sort_values("Conversion_Rate", ascending=False)

fig, ax = plt.subplots()
bars = ax.bar(channel_conv["Channel"], channel_conv["Conversion_Rate"],
              color=sns.color_palette("viridis", len(channel_conv)))
ax.set_title("Conversion Rate by Channel (Clicks → Purchases)", fontsize=16, fontweight="bold")
ax.set_xlabel("Channel")
ax.set_ylabel("Conversion Rate (%)")
for bar in bars:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
            f"{bar.get_height():.1f}%", ha="center", fontsize=10)
plt.tight_layout()
plt.savefig("conversion_by_channel.png", dpi=150)
plt.show()

# ============================================================
# STEP 6: Revenue by Channel (Bar)
# ============================================================
rev_by_channel = df.groupby("Channel")["Revenue"].sum().sort_values(ascending=False)

fig, ax = plt.subplots()
bars = ax.bar(rev_by_channel.index, rev_by_channel.values,
              color=sns.color_palette("Blues_d", len(rev_by_channel)))
ax.set_title("Total Revenue by Channel", fontsize=16, fontweight="bold")
ax.set_xlabel("Channel")
ax.set_ylabel("Revenue (USD)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
for bar in bars:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1000,
            f"${bar.get_height():,.0f}", ha="center", fontsize=9)
plt.tight_layout()
plt.savefig("revenue_by_channel.png", dpi=150)
plt.show()

# ============================================================
# STEP 7: Drop-off Analysis (Funnel Steps)
# ============================================================
dropoffs = {
    "Impressions→Clicks": (total_impressions - total_clicks) / total_impressions * 100,
    "Clicks→Signups": (total_clicks - total_signups) / total_clicks * 100,
    "Signups→Trials": (total_signups - total_trials) / total_signups * 100,
    "Trials→Purchases": (total_trials - total_purchases) / total_trials * 100,
}

fig, ax = plt.subplots()
bars = ax.barh(list(dropoffs.keys())[::-1], list(dropoffs.values())[::-1], color="#e74c3c")
ax.set_title("Drop-off Rate at Each Funnel Stage", fontsize=16, fontweight="bold")
ax.set_xlabel("Drop-off Rate (%)")
for bar in bars:
    ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
            f"{bar.get_width():.1f}%", va="center", fontsize=10)
plt.tight_layout()
plt.savefig("dropoff_analysis.png", dpi=150)
plt.show()

# ============================================================
# STEP 8: Monthly Revenue Trend (Line)
# ============================================================
df["Month_Num"] = df["Date"].dt.month
month_names = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
monthly = df.groupby("Month_Num")["Revenue"].sum().reset_index()
monthly["Month"] = monthly["Month_Num"].apply(lambda x: month_names[x-1])

fig, ax = plt.subplots()
ax.plot(monthly["Month"], monthly["Revenue"], marker="o", color="#9b59b6", linewidth=2.5)
ax.fill_between(monthly["Month"], monthly["Revenue"], alpha=0.15, color="#9b59b6")
ax.set_title("Monthly Revenue Trend from Campaigns", fontsize=16, fontweight="bold")
ax.set_xlabel("Month")
ax.set_ylabel("Revenue (USD)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
plt.tight_layout()
plt.savefig("monthly_revenue_trend.png", dpi=150)
plt.show()

# ============================================================
# STEP 9: Insights & Recommendations
# ============================================================
best_channel = channel_conv.iloc[0]["Channel"]
worst_channel = channel_conv.iloc[-1]["Channel"]
best_revenue_channel = rev_by_channel.index[0]
biggest_dropoff = max(dropoffs, key=dropoffs.get)

print("""
╔══════════════════════════════════════════════════════════╗
║    MARKETING FUNNEL & CONVERSION ANALYSIS – REPORT      ║
╚══════════════════════════════════════════════════════════╝
""")
print(f"1. BEST CHANNEL   : '{best_channel}' has the highest conversion rate.")
print(f"2. WORST CHANNEL  : '{worst_channel}' needs immediate optimization.")
print(f"3. TOP REVENUE    : '{best_revenue_channel}' generates the most revenue.")
print(f"4. BIGGEST DROP   : '{biggest_dropoff}' stage loses the most leads.")
print(f"5. OVERALL CTR    : {ctr:.2f}% — industry average is ~2-5%.")
print("""
RECOMMENDATIONS:
  → Increase budget allocation to the highest-converting channel.
  → A/B test landing pages to improve the Clicks→Signups conversion.
  → Add incentives (free trials, discounts) at the Trials→Purchases stage.
  → Retarget users who dropped off at the Signups stage with email campaigns.
  → Optimize ad creatives for the lowest-performing channel or pause it.
""")
print("All charts saved as PNG. Upload to your FUTURE_DS_03 GitHub repo.")
