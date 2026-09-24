
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Supermarket Intelligence Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# PROFESSIONAL CSS
# =========================================================
st.markdown("""
<style>
    .main {
        background-color: #f6f8fb;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1450px;
    }

    .dashboard-title {
        font-size: 2.25rem;
        font-weight: 800;
        margin-bottom: 0.1rem;
    }

    .dashboard-subtitle {
        color: #667085;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }

    .section-title {
        font-size: 1.25rem;
        font-weight: 750;
        margin-top: 1rem;
        margin-bottom: 0.75rem;
    }

    .kpi-card {
        background: white;
        border-radius: 14px;
        padding: 18px 20px;
        border: 1px solid #e6eaf0;
        box-shadow: 0 2px 8px rgba(16, 24, 40, 0.05);
        min-height: 125px;
    }

    .kpi-label {
        color: #667085;
        font-size: 0.88rem;
        font-weight: 600;
    }

    .kpi-value {
        font-size: 1.65rem;
        font-weight: 800;
        margin-top: 7px;
    }

    .kpi-note {
        color: #667085;
        font-size: 0.78rem;
        margin-top: 5px;
    }

    .insight-card {
        background: white;
        border: 1px solid #e6eaf0;
        border-radius: 14px;
        padding: 18px;
        min-height: 130px;
        box-shadow: 0 2px 8px rgba(16, 24, 40, 0.04);
    }

    .insight-title {
        font-weight: 750;
        margin-bottom: 8px;
    }

    .insight-text {
        color: #475467;
        line-height: 1.55;
    }

    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #e6eaf0;
        padding: 15px;
        border-radius: 14px;
        box-shadow: 0 2px 8px rgba(16, 24, 40, 0.04);
    }

    [data-testid="stSidebar"] {
        border-right: 1px solid #e6eaf0;
    }

    .footer {
        text-align: center;
        color: #98a2b3;
        font-size: 0.8rem;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #e6eaf0;
    }
</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================
@st.cache_data
def load_data():
    df = pd.read_csv("supermarket_sales.csv")
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    if "sales" not in df.columns and {
        "quantity", "unit_price"
    }.issubset(df.columns):
        df["sales"] = df["quantity"] * df["unit_price"]

    return df


try:
    df = load_data()
except FileNotFoundError:
    st.error(
        "supermarket_sales.csv was not found. "
        "Keep app.py and supermarket_sales.csv in the same folder."
    )
    st.stop()


# =========================================================
# HEADER
# =========================================================
st.markdown(
    '<div class="dashboard-title">🛒 Supermarket Intelligence Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'Interactive sales analytics for products, branches, customers, payments and ratings'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR FILTERS
# =========================================================
st.sidebar.title("Dashboard Controls")
st.sidebar.caption("Use the filters to explore the data.")

def filter_options(column):
    if column in df.columns:
        return ["All"] + sorted(df[column].dropna().unique().tolist())
    return ["All"]

selected_branch = st.sidebar.selectbox(
    "🏢 Branch",
    filter_options("branch")
)

selected_customer = st.sidebar.selectbox(
    "👥 Customer Type",
    filter_options("customer_type")
)

selected_payment = st.sidebar.selectbox(
    "💳 Payment Method",
    filter_options("payment_method")
)

st.sidebar.divider()

if st.sidebar.button("🔄 Reset Filters", use_container_width=True):
    st.rerun()

st.sidebar.divider()
st.sidebar.caption(f"Dataset records: {len(df):,}")
st.sidebar.caption("Dashboard built with Python + Streamlit")


# =========================================================
# FILTER DATA
# =========================================================
data = df.copy()

if selected_branch != "All" and "branch" in data.columns:
    data = data[data["branch"] == selected_branch]

if selected_customer != "All" and "customer_type" in data.columns:
    data = data[data["customer_type"] == selected_customer]

if selected_payment != "All" and "payment_method" in data.columns:
    data = data[data["payment_method"] == selected_payment]


# =========================================================
# KPI VALUES
# =========================================================
total_sales = data["sales"].sum()
transactions = len(data)
avg_transaction = data["sales"].mean() if transactions else 0
total_quantity = data["quantity"].sum() if "quantity" in data.columns else 0
avg_rating = data["rating"].mean() if "rating" in data.columns and transactions else 0


# =========================================================
# KPI ROW
# =========================================================
st.markdown('<div class="section-title">Executive Overview</div>', unsafe_allow_html=True)

k1, k2, k3, k4, k5 = st.columns(5)

k1.metric("Total Sales", f"₹{total_sales:,.2f}")
k2.metric("Transactions", f"{transactions:,}")
k3.metric("Avg. Transaction", f"₹{avg_transaction:,.2f}")
k4.metric("Units Sold", f"{total_quantity:,}")
k5.metric("Avg. Rating", f"{avg_rating:.2f}/5")


# =========================================================
# TOP INSIGHTS
# =========================================================
st.markdown('<div class="section-title">Key Business Insights</div>', unsafe_allow_html=True)

ins1, ins2, ins3 = st.columns(3)

if "product" in data.columns and len(data):
    product_sales = data.groupby("product")["sales"].sum().sort_values(ascending=False)
    top_product = product_sales.index[0]
    top_product_sales = product_sales.iloc[0]
else:
    top_product = "N/A"
    top_product_sales = 0

if "branch" in data.columns and len(data):
    branch_sales = data.groupby(["branch", "city"])["sales"].sum().sort_values(ascending=False)
    top_branch = branch_sales.index[0]
    top_branch_sales = branch_sales.iloc[0]
else:
    top_branch = ("N/A", "N/A")
    top_branch_sales = 0

if "payment_method" in data.columns and len(data):
    payment_counts = data["payment_method"].value_counts()
    top_payment = payment_counts.index[0]
    top_payment_count = payment_counts.iloc[0]
else:
    top_payment = "N/A"
    top_payment_count = 0

with ins1:
    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-title">🏆 Top Product</div>
            <div class="insight-text">
                <b>{top_product}</b> generated
                <b>₹{top_product_sales:,.2f}</b> in sales.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with ins2:
    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-title">🏢 Leading Branch</div>
            <div class="insight-text">
                <b>Branch {top_branch[0]}</b> ({top_branch[1]})
                generated <b>₹{top_branch_sales:,.2f}</b>.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with ins3:
    st.markdown(
        f"""
        <div class="insight-card">
            <div class="insight-title">💳 Preferred Payment</div>
            <div class="insight-text">
                <b>{top_payment}</b> was used for
                <b>{top_payment_count:,}</b> transactions.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# SALES ANALYSIS
# =========================================================
st.markdown('<div class="section-title">Sales Performance</div>', unsafe_allow_html=True)

left, right = st.columns(2)

with left:
    st.markdown("#### Product Sales")

    if "product" in data.columns and len(data):
        ps = data.groupby("product")["sales"].sum().sort_values(ascending=False)

        fig, ax = plt.subplots(figsize=(8, 4.5))
        ps.plot(kind="bar", ax=ax)
        ax.set_xlabel("")
        ax.set_ylabel("Sales (₹)")
        ax.set_title("Sales by Product")
        ax.grid(axis="y", alpha=0.2)
        plt.xticks(rotation=35)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

with right:
    st.markdown("#### Branch Performance")

    if "branch" in data.columns and len(data):
        bs = data.groupby("branch")["sales"].sum().sort_values(ascending=False)

        fig, ax = plt.subplots(figsize=(8, 4.5))
        bs.plot(kind="bar", ax=ax)
        ax.set_xlabel("")
        ax.set_ylabel("Sales (₹)")
        ax.set_title("Sales by Branch")
        ax.grid(axis="y", alpha=0.2)
        plt.xticks(rotation=0)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)


# =========================================================
# CUSTOMER & PAYMENT
# =========================================================
st.markdown('<div class="section-title">Customer & Payment Analytics</div>', unsafe_allow_html=True)

left, right = st.columns(2)

with left:
    st.markdown("#### Average Spending by Customer Type")

    if "customer_type" in data.columns and len(data):
        ct = data.groupby("customer_type")["sales"].mean().sort_values(ascending=False)

        fig, ax = plt.subplots(figsize=(8, 4.5))
        ct.plot(kind="bar", ax=ax)
        ax.set_xlabel("")
        ax.set_ylabel("Average Sales (₹)")
        ax.set_title("Customer Spending")
        ax.grid(axis="y", alpha=0.2)
        plt.xticks(rotation=0)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

with right:
    st.markdown("#### Payment Method Usage")

    if "payment_method" in data.columns and len(data):
        pm = data["payment_method"].value_counts()

        fig, ax = plt.subplots(figsize=(8, 4.5))
        pm.plot(kind="bar", ax=ax)
        ax.set_xlabel("")
        ax.set_ylabel("Transactions")
        ax.set_title("Payment Method Usage")
        ax.grid(axis="y", alpha=0.2)
        plt.xticks(rotation=25)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)


# =========================================================
# CATEGORY / RATING
# =========================================================
st.markdown('<div class="section-title">Category & Customer Satisfaction</div>', unsafe_allow_html=True)

left, right = st.columns(2)

with left:
    st.markdown("#### Category Sales")

    if "category" in data.columns and len(data):
        cs = data.groupby("category")["sales"].sum().sort_values(ascending=False)

        fig, ax = plt.subplots(figsize=(8, 4.5))
        cs.plot(kind="bar", ax=ax)
        ax.set_xlabel("")
        ax.set_ylabel("Sales (₹)")
        ax.set_title("Sales by Category")
        ax.grid(axis="y", alpha=0.2)
        plt.xticks(rotation=35)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
    else:
        st.info(
            "Category analysis is unavailable because the current CSV "
            "does not contain a category column."
        )

with right:
    st.markdown("#### Rating Distribution")

    if "rating" in data.columns and len(data):
        fig, ax = plt.subplots(figsize=(8, 4.5))
        ax.hist(data["rating"].dropna(), bins=10)
        ax.set_xlabel("Rating")
        ax.set_ylabel("Customers")
        ax.set_title("Customer Rating Distribution")
        ax.grid(axis="y", alpha=0.2)
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)


# =========================================================
# DATA TABLE
# =========================================================
with st.expander("📋 View Transaction Data", expanded=False):
    st.dataframe(
        data,
        use_container_width=True,
        height=420
    )

    csv_data = data.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Download Current Data",
        data=csv_data,
        file_name="filtered_supermarket_sales.csv",
        mime="text/csv"
    )


# =========================================================
# BUSINESS DECISIONS
# =========================================================
st.markdown('<div class="section-title">Business Decision Support</div>', unsafe_allow_html=True)

b1, b2, b3 = st.columns(3)

with b1:
    st.markdown(
        """
        <div class="insight-card">
            <div class="insight-title">📦 Inventory</div>
            <div class="insight-text">
                Track high-selling products and consider stock planning
                around strong sales performers.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with b2:
    st.markdown(
        """
        <div class="insight-card">
            <div class="insight-title">💳 Payments</div>
            <div class="insight-text">
                Monitor frequently used payment methods to support
                convenient customer transactions.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with b3:
    st.markdown(
        """
        <div class="insight-card">
            <div class="insight-title">⭐ Customer Service</div>
            <div class="insight-text">
                Use customer ratings and spending patterns to identify
                opportunities for service improvement.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# FOOTER
# =========================================================
st.markdown(
    """
    <div class="footer">
        Supermarket Intelligence Dashboard • Built with Python, Pandas,
        Matplotlib & Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
