"""
Vendor Performance Analytics Platform
Streamlit App

Features:
- Upload vendor data (CSV/Excel)
- Display and filter data
- KPI calculations
- Visualizations (bar, line, pie, scatter)
- Leaderboard (top/bottom 5)
- Export filtered data
- Summary dashboard
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
from io import BytesIO

# =====================
# Data Preprocessing
# =====================
def load_data(uploaded_file=None):
    """
    Load data from uploaded file or return sample data if None.
    """
    if uploaded_file:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    else:
        df = generate_sample_data()
    return df

def generate_sample_data():
    """
    Generate sample vendor data for demonstration.
    """
    np.random.seed(42)
    vendors = [f"Vendor {i+1}" for i in range(15)]
    categories = np.random.choice(['Raw Material', 'Packaging', 'Services'], 15)
    regions = np.random.choice(['North', 'South', 'East', 'West'], 15)
    data = []
    for i in range(15):
        for month in pd.date_range('2023-01-01', '2023-06-01', freq='MS'):
            data.append({
                'Vendor': vendors[i],
                'Category': categories[i],
                'Region': regions[i],
                'Date': month,
                'OnTimeDeliveries': np.random.randint(8, 15),
                'TotalDeliveries': np.random.randint(10, 16),
                'Defects': np.random.randint(0, 3),
                'TotalUnits': np.random.randint(100, 200),
                'Spend': np.random.randint(10000, 50000),
                'Compliant': np.random.choice([1, 0], p=[0.9, 0.1]),
                'LeadTime': np.random.uniform(2, 10)
            })
    return pd.DataFrame(data)

# =====================
# KPI Calculation
# =====================
def calculate_kpis(df):
    """
    Calculate KPIs for each vendor.
    """
    kpi_df = df.groupby('Vendor').agg({
        'OnTimeDeliveries': 'sum',
        'TotalDeliveries': 'sum',
        'Defects': 'sum',
        'TotalUnits': 'sum',
        'Spend': 'sum',
        'Compliant': 'mean',
        'LeadTime': 'mean',
        'Category': 'first',
        'Region': 'first'
    }).reset_index()
    kpi_df['OnTimeDeliveryRate'] = kpi_df['OnTimeDeliveries'] / kpi_df['TotalDeliveries']
    kpi_df['QualityScore'] = 1 - (kpi_df['Defects'] / kpi_df['TotalUnits'])
    kpi_df['ComplianceRate'] = kpi_df['Compliant']
    kpi_df['AvgLeadTime'] = kpi_df['LeadTime']
    # Overall Score (weighted sum)
    kpi_df['OverallScore'] = (
        kpi_df['OnTimeDeliveryRate']*0.3 +
        kpi_df['QualityScore']*0.3 +
        kpi_df['ComplianceRate']*0.2 +
        (1 - (kpi_df['AvgLeadTime']/kpi_df['AvgLeadTime'].max()))*0.2
    )
    return kpi_df

# =====================
# Filtering
# =====================
def filter_data(df, date_range, category, region):
    """
    Filter data by date range, category, and region.
    """
    # Ensure date_range values are pandas Timestamps for comparison
    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])
    mask = (pd.to_datetime(df['Date']) >= start_date) & (pd.to_datetime(df['Date']) <= end_date)
    if category != 'All' and 'Category' in df.columns:
        mask &= (df['Category'] == category)
    if region != 'All' and 'Region' in df.columns:
        mask &= (df['Region'] == region)
    return df[mask]

# =====================
# Visualizations
# =====================
def plot_vendor_comparison(kpi_df):
    fig = px.bar(kpi_df, x='Vendor', y='OverallScore', color='Category', title='Vendor Performance Comparison')
    return fig

def plot_vendor_trends(df, vendor):
    vendor_df = df[df['Vendor'] == vendor]
    fig = px.line(vendor_df, x='Date', y='OnTimeDeliveries', title=f'{vendor} On-Time Deliveries Over Time')
    return fig

def plot_spend_distribution(kpi_df, by='Vendor'):
    fig = px.pie(kpi_df, names=by, values='Spend', title=f'Spend Distribution by {by}')
    return fig

def plot_quality_vs_leadtime(kpi_df):
    fig = px.scatter(kpi_df, x='AvgLeadTime', y='QualityScore', size='Spend', color='Vendor',
                     title='Quality vs Lead Time', hover_name='Vendor')
    return fig

# =====================
# Leaderboard
# =====================
def get_leaderboard(kpi_df, n=5):
    top = kpi_df.nlargest(n, 'OverallScore')
    bottom = kpi_df.nsmallest(n, 'OverallScore')
    return top, bottom

# =====================
# Export
# =====================
def export_to_csv(df):
    output = BytesIO()
    df.to_csv(output, index=False)
    return output.getvalue()

REQUIRED_FIELDS = [
    ('Vendor', 'Vendor Name'),
    ('OnTimeDeliveries', 'On-Time Deliveries'),
    ('TotalDeliveries', 'Total Deliveries'),
    ('Defects', 'Defects'),
    ('TotalUnits', 'Total Units'),
    ('Spend', 'Spend'),
    ('Compliant', 'Compliant'),
    ('LeadTime', 'Lead Time'),
    ('Category', 'Category'),
    ('Region', 'Region'),
    ('Date', 'Date'),
]

def get_column_mapping(df):
    """
    Show sidebar UI for user to map their columns to required dashboard fields.
    Returns a dict: dashboard_field -> user_column
    """
    mapping = {}
    st.sidebar.markdown('---')
    st.sidebar.header('Column Mapping')
    for field, label in REQUIRED_FIELDS:
        options = ['(None)'] + list(df.columns)
        default = field if field in df.columns else options[0]
        sel = st.sidebar.selectbox(f"Select column for '{label}'", options, index=options.index(default) if default in options else 0)
        mapping[field] = sel if sel != '(None)' else None
    return mapping

def remap_df(df, mapping):
    """
    Return a new DataFrame with columns renamed to dashboard fields using the mapping.
    Only keeps mapped columns.
    """
    col_map = {v: k for k, v in mapping.items() if v is not None}
    df2 = df[[v for v in mapping.values() if v is not None]].rename(columns=col_map)
    return df2

# =====================
# Streamlit Layout
# =====================
def main():
    st.set_page_config(page_title="Vendor Performance Analytics", layout="wide")
    st.title("Vendor Performance Analytics Platform")
    st.markdown("""
    Vendor Performance Analytics Dashboard (Sample Data Only)  
    [Sample Data Source](https://github.com/Rolakamin/Supplier-Quality-and-Performance/blob/main/supplier%20data.xlsx)
    """)
    st.info("This dashboard uses only built-in sample data. Uploading files is disabled.")

    # Use only sample data
    df = generate_sample_data()

    # Sidebar filters
    st.sidebar.header("Filter Options")
    # Date range filter
    if 'Date' in df.columns:
        min_date, max_date = df['Date'].min(), df['Date'].max()
        date_range = st.sidebar.date_input("Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)
    else:
        date_range = None
    # Category filter
    if 'Category' in df.columns:
        categories = ['All'] + sorted(df['Category'].unique().tolist())
        category = st.sidebar.selectbox("Vendor Category", categories)
    else:
        category = 'All'
    # Region filter
    if 'Region' in df.columns:
        regions = ['All'] + sorted(df['Region'].unique().tolist())
        region = st.sidebar.selectbox("Region", regions)
    else:
        region = 'All'

    # Filter data
    filtered_df = df.copy()
    if date_range and 'Date' in filtered_df.columns:
        start_date = pd.to_datetime(date_range[0])
        end_date = pd.to_datetime(date_range[1])
        filtered_df = filtered_df[(filtered_df['Date'] >= start_date) & (filtered_df['Date'] <= end_date)]
    if category != 'All' and 'Category' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['Category'] == category]
    if region != 'All' and 'Region' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['Region'] == region]

    kpi_df = calculate_kpis(filtered_df)

    # Export
    st.sidebar.markdown("---")
    csv = export_to_csv(kpi_df)
    st.sidebar.download_button(
        label="Export Filtered Data (CSV)",
        data=csv,
        file_name="vendor_performance_filtered.csv",
        mime="text/csv"
    )

    # Summary Dashboard
    st.subheader("Performance Summary Dashboard")
    kpi_cols = st.columns(5)
    kpi_vals = {
        'On-Time Delivery Rate': kpi_df['OnTimeDeliveryRate'].mean() if not kpi_df.empty else 0,
        'Quality Score': kpi_df['QualityScore'].mean() if not kpi_df.empty else 0,
        'Total Spend': kpi_df['Spend'].sum() if not kpi_df.empty else 0,
        'Compliance Rate': kpi_df['ComplianceRate'].mean() if not kpi_df.empty else 0,
        'Avg Lead Time': kpi_df['AvgLeadTime'].mean() if not kpi_df.empty else 0,
    }
    for i, (k, v) in enumerate(kpi_vals.items()):
        if k == 'Total Spend':
            kpi_cols[i].metric(k, f"${v:,.0f}")
        elif k == 'Avg Lead Time':
            kpi_cols[i].metric(k, f"{v:.2f} days")
        else:
            kpi_cols[i].metric(k, f"{v:.2%}")

    # Charts
    st.subheader("Visual Analytics")
    chart1, chart2 = st.columns(2)
    with chart1:
        st.plotly_chart(plot_vendor_comparison(kpi_df), use_container_width=True)
    with chart2:
        st.plotly_chart(plot_spend_distribution(kpi_df, by='Vendor'), use_container_width=True)
    chart3, chart4 = st.columns(2)
    with chart3:
        st.plotly_chart(plot_spend_distribution(kpi_df, by='Region'), use_container_width=True)
    with chart4:
        st.plotly_chart(plot_quality_vs_leadtime(kpi_df), use_container_width=True)

    # Vendor trend (selectable)
    st.subheader("Vendor Trend Over Time")
    vendor_list = kpi_df['Vendor'].tolist()
    if vendor_list:
        selected_vendor = st.selectbox("Select Vendor", vendor_list)
        st.plotly_chart(plot_vendor_trends(filtered_df, selected_vendor), use_container_width=True)

    # Leaderboard
    st.subheader("Leaderboard: Top & Bottom 5 Vendors")
    top, bottom = get_leaderboard(kpi_df)
    st.markdown("**Top 5 Vendors**")
    st.dataframe(top[['Vendor', 'OverallScore', 'OnTimeDeliveryRate', 'QualityScore', 'ComplianceRate', 'AvgLeadTime', 'Spend']].round(3))
    st.markdown("**Bottom 5 Vendors**")
    st.dataframe(bottom[['Vendor', 'OverallScore', 'OnTimeDeliveryRate', 'QualityScore', 'ComplianceRate', 'AvgLeadTime', 'Spend']].round(3))

    # Raw/Filtered Data Table
    st.subheader("Raw / Filtered Data Table")
    st.dataframe(filtered_df)

if __name__ == "__main__":
    main() 