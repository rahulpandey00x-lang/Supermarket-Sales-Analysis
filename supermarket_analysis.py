import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# -----------------------------------
# 1. LOAD DATASET
# -----------------------------------

file_path = "data/supermarket_sales.csv"

df = pd.read_csv(file_path)

print("\n========== SUPERMARKET SALES ANALYSIS ==========\n")

print("First 5 records:")
print(df.head())


# -----------------------------------
# 2. BASIC INFORMATION
# -----------------------------------

print("\nDataset Shape:")
print(df.shape)

print("\nColumn Names:")
print(df.columns.tolist())

print("\nDataset Information:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())


# -----------------------------------
# 3. CLEAN COLUMN NAMES
# -----------------------------------

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

print("\nCleaned Columns:")
print(df.columns.tolist())


# -----------------------------------
# 4. CALCULATE SALES
# -----------------------------------

# If sales column does not exist,
# calculate it using Quantity × Unit Price

if "sales" not in df.columns:

    if "quantity" in df.columns and "unit_price" in df.columns:
        df["sales"] = df["quantity"] * df["unit_price"]

    elif "quantity" in df.columns and "price" in df.columns:
        df["sales"] = df["quantity"] * df["price"]


# -----------------------------------
# 5. BASIC SALES SUMMARY
# -----------------------------------

print("\n========== SALES SUMMARY ==========")

total_sales = df["sales"].sum()
average_sales = df["sales"].mean()
total_transactions = len(df)

print("Total Sales:", round(total_sales, 2))
print("Average Transaction:", round(average_sales, 2))
print("Total Transactions:", total_transactions)


# -----------------------------------
# 6. HIGHEST SELLING PRODUCT
# -----------------------------------

if "product" in df.columns:

    product_sales = (
        df.groupby("product")["sales"]
        .sum()
        .sort_values(ascending=False)
    )

    print("\n========== PRODUCT SALES ==========")
    print(product_sales)

    highest_product = product_sales.idxmax()
    highest_product_sales = product_sales.max()

    print("\nHighest Selling Product:", highest_product)
    print("Sales:", round(highest_product_sales, 2))


# -----------------------------------
# 7. BRANCH PERFORMANCE
# -----------------------------------

if "branch" in df.columns:

    branch_sales = (
        df.groupby("branch")["sales"]
        .sum()
        .sort_values(ascending=False)
    )

    print("\n========== BRANCH PERFORMANCE ==========")
    print(branch_sales)

    best_branch = branch_sales.idxmax()
    best_branch_sales = branch_sales.max()

    print("\nBest Performing Branch:", best_branch)
    print("Sales:", round(best_branch_sales, 2))


# -----------------------------------
# 8. CATEGORY SALES
# -----------------------------------

if "category" in df.columns:

    category_sales = (
        df.groupby("category")["sales"]
        .sum()
        .sort_values(ascending=False)
    )

    print("\n========== CATEGORY SALES ==========")
    print(category_sales)

    top_category = category_sales.idxmax()
    top_category_sales = category_sales.max()

    print("\nHighest Selling Category:", top_category)
    print("Sales:", round(top_category_sales, 2))


# -----------------------------------
# 9. PAYMENT METHOD ANALYSIS
# -----------------------------------

if "payment_method" in df.columns:

    payment_counts = df["payment_method"].value_counts()

    print("\n========== PAYMENT METHODS ==========")
    print(payment_counts)

    most_used_payment = payment_counts.idxmax()
    most_used_payment_count = payment_counts.max()

    print("\nMost Popular Payment Method:",
          most_used_payment)

    print("Transactions:",
          most_used_payment_count)


# -----------------------------------
# 10. CUSTOMER TYPE ANALYSIS
# -----------------------------------

if "customer_type" in df.columns:

    customer_spending = (
        df.groupby("customer_type")["sales"]
        .mean()
        .sort_values(ascending=False)
    )

    print("\n========== CUSTOMER TYPE ==========")
    print(customer_spending)

    print("\nAverage Spending by Customer Type:")
    for customer, value in customer_spending.items():
        print(customer, ":", round(value, 2))


# -----------------------------------
# 11. CUSTOMER RATING
# -----------------------------------

if "rating" in df.columns:

    average_rating = df["rating"].mean()

    print("\n========== CUSTOMER RATING ==========")
    print("Average Customer Rating:",
          round(average_rating, 2), "/ 5")


# -----------------------------------
# 12. CREATE CHART FOLDER
# -----------------------------------

os.makedirs("charts", exist_ok=True)


# -----------------------------------
# 13. PRODUCT SALES CHART
# -----------------------------------

if "product" in df.columns:

    plt.figure(figsize=(10, 6))

    product_sales.plot(kind="bar")

    plt.title("Sales by Product")
    plt.xlabel("Product")
    plt.ylabel("Sales")

    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig("charts/product_sales.png")

    plt.show()


# -----------------------------------
# 14. BRANCH SALES CHART
# -----------------------------------

if "branch" in df.columns:

    plt.figure(figsize=(8, 5))

    branch_sales.plot(kind="bar")

    plt.title("Sales by Branch")
    plt.xlabel("Branch")
    plt.ylabel("Sales")

    plt.tight_layout()

    plt.savefig("charts/branch_sales.png")

    plt.show()


# -----------------------------------
# 15. CATEGORY SALES CHART
# -----------------------------------

if "category" in df.columns:

    plt.figure(figsize=(10, 6))

    category_sales.plot(kind="bar")

    plt.title("Sales by Category")
    plt.xlabel("Category")
    plt.ylabel("Sales")

    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig("charts/category_sales.png")

    plt.show()


# -----------------------------------
# 16. PAYMENT METHOD CHART
# -----------------------------------

if "payment_method" in df.columns:

    plt.figure(figsize=(8, 5))

    payment_counts.plot(kind="bar")

    plt.title("Payment Method Usage")
    plt.xlabel("Payment Method")
    plt.ylabel("Number of Transactions")

    plt.tight_layout()

    plt.savefig("charts/payment_methods.png")

    plt.show()


# -----------------------------------
# 17. CUSTOMER TYPE CHART
# -----------------------------------

if "customer_type" in df.columns:

    plt.figure(figsize=(8, 5))

    customer_spending.plot(kind="bar")

    plt.title("Average Spending by Customer Type")
    plt.xlabel("Customer Type")
    plt.ylabel("Average Sales")

    plt.tight_layout()

    plt.savefig("charts/customer_type_spending.png")

    plt.show()


# -----------------------------------
# 18. FINAL SUMMARY
# -----------------------------------

print("\n==========================================")
print("          FINAL PROJECT SUMMARY")
print("==========================================")

print("Total Sales:", round(total_sales, 2))
print("Total Transactions:", total_transactions)

if "product" in df.columns:
    print("Top Product:", highest_product)

if "branch" in df.columns:
    print("Best Branch:", best_branch)

if "category" in df.columns:
    print("Top Category:", top_category)

if "payment_method" in df.columns:
    print("Most Used Payment:", most_used_payment)

if "rating" in df.columns:
    print("Average Rating:", round(average_rating, 2))

print("\nAnalysis Completed Successfully!")