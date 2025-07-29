# Vendor Performance Analytics Dashboard

Live Demo: [https://vendor-analytics-app.streamlit.app](https://vendor-analytics-app.streamlit.app)

This is an interactive **Vendor Performance Analytics Dashboard** built using **Python** and **Streamlit**, designed to monitor, filter, and visualize vendor performance using demo data. It features KPI summaries, dynamic charts, vendor comparisons, and export functionality in a modern, responsive layout.

---

## Features

### 1. Data Source

**Sample Data Only:**

- The dashboard uses built-in, randomly generated sample data for 15 vendors.
- Covers multiple months, categories, and regions.
- No file upload is required — always uses demo data.

---

### 2. Sidebar Filters

- **Date Range Filter**  
  Select a start and end date to filter the dataset (if the sample data includes a 'Date' column).

- **Vendor Category Filter**  
  Filter by vendor category (e.g., Raw Material, Packaging, Services).

- **Region Filter**  
  Filter by region (e.g., North, South, East, West).

---

### 3. Main Dashboard Area

#### A. Title and Description

- Project title and brief description.
- Includes a link to the sample data source (if applicable).

#### B. Performance Summary Dashboard (KPIs)

- On-Time Delivery Rate: Average percentage of on-time deliveries.
- Quality Score: Average quality score, typically based on defect rate.
- Total Spend: Total spend across all filtered vendors.
- Compliance Rate: Average compliance percentage.
- Average Lead Time: Mean delivery lead time in days.

#### C. Visual Analytics

- **Bar Chart**  
  Vendor performance comparison (overall score by vendor, colored by category).

- **Pie Chart**  
  Spend distribution by vendor.

- **Pie Chart**  
  Spend distribution by region.

- **Scatter Plot**  
  Quality vs. Lead Time (bubble size represents spend, color represents vendor).

#### D. Vendor Trend Over Time

- **Line Chart**  
  On-time delivery trends over time for a selected vendor.

#### E. Leaderboard

- **Top 5 Vendors**  
  Table showing the top five vendors by overall performance score.

- **Bottom 5 Vendors**  
  Table showing the bottom five vendors by overall performance score.

#### F. Raw / Filtered Data Table

- Interactive data table showing the currently filtered dataset.

---

### 4. Export Option

- **Download Filtered Data**  
  Exports the currently filtered and scored data to a downloadable CSV file.

---

### 5. Professional UI/UX

- Streamlit sidebar for filters and controls.
- Central display area for KPIs, charts, and tables.
- Clean, responsive design optimized for readability and usability.

---

### 6. Modular, Maintainable Code

- Separate functions for:
  - Sample data generation
  - Data preprocessing
  - KPI calculation
  - Filtering logic
  - Visualizations (bar, pie, line, scatter)
  - Leaderboard creation
  - CSV export
  - Streamlit layout and UI
- Code is well-commented and structured for easy maintenance and future extensions.


