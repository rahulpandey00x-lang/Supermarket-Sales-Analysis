# 🛒 Supermarket Intelligence Dashboard

A professional **Supermarket Sales Analysis** web dashboard built with **Python, Pandas, Matplotlib, and Streamlit**.

The project analyzes supermarket sales transactions and presents useful insights about:

- Products
- Branches
- Cities
- Customer types
- Payment methods
- Quantity and sales
- Customer ratings
- Business decisions

## 📌 Project Objective

The objective of this project is to analyze supermarket sales data and convert the data into useful business insights.

The project follows these main analysis steps:

1. Load the CSV dataset.
2. Check and process the data.
3. Calculate sales using quantity and unit price when required.
4. Summarize sales using totals, counts, and averages.
5. Create charts for comparison.
6. Use the results to support business decisions.

## 📊 Dashboard Features

### Executive Overview
- Total Sales
- Total Transactions
- Average Transaction
- Units Sold
- Average Customer Rating

### Interactive Filters
The dashboard allows filtering by:

- Branch
- Customer Type
- Payment Method

### Sales Analysis
- Sales by Product
- Sales by Branch
- Top-selling product
- Best-performing branch

### Customer Analysis
- Average spending by customer type
- Customer rating distribution

### Payment Analysis
- Payment method usage
- Most-used payment method

### Category Analysis
The dashboard supports category analysis if a `category` column is available in the CSV dataset.

### Data Export
Filtered transaction data can be downloaded directly from the dashboard as a CSV file.

## 🗂️ Project Structure

```text
Supermarket-Sales-Analysis/
│
├── app.py
├── supermarket_sales.csv
├── requirements.txt
└── README.md
```

## 🛠️ Technologies Used

- Python
- Streamlit
- Pandas
- Matplotlib
- CSV

## ⚙️ Installation

### 1. Install Python

Make sure Python is installed on your computer.

Check the installation:

```bash
python --version
```

### 2. Open the project folder

Open the project folder in VS Code.

### 3. Install required libraries

Run:

```bash
pip install -r requirements.txt
```

## ▶️ Run the Dashboard

After installation, run:

```bash
python -m streamlit run app.py
```

The Streamlit server will start and the dashboard will open in your browser.

If it does not open automatically, use the local URL shown in the terminal, normally:

```text
http://localhost:8501
```

## 📁 Dataset

The dashboard reads:

```text
supermarket_sales.csv
```

The current project dataset contains 500 sales transactions and includes fields such as:

- transaction_id
- product
- branch
- city
- customer_type
- quantity
- unit_price
- payment_method
- rating
- sales

## 💡 Business Insights

The analysis can help a supermarket:

- Plan inventory around high-selling products.
- Compare branch performance.
- Understand customer spending patterns.
- Monitor popular payment methods.
- Track customer satisfaction through ratings.
- Support membership and customer-service decisions.

## ⚠️ Dataset Note

The provided project PDF describes the expected analysis and reports specific findings, but it does not contain the original 500 transaction rows.

Therefore, if this project uses a generated/practice CSV, its calculated results may differ from the figures reported in the PDF.

The category analysis also requires a `category` column in the dataset.

## 🚀 Future Improvements

Possible future versions can include:

- MySQL database integration
- Login system
- Date-based sales trends
- Profit and cost analysis
- Advanced KPI cards
- Interactive Plotly charts
- Machine learning sales forecasting
- Product recommendation system
- Cloud deployment
- Automated report generation

## 👨‍💻 Author

**Rahul Pandey**

Data Analytics / Data Science Student Project
