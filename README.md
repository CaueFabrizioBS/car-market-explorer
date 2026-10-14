# Car Market Explorer

**[Open the live app](https://car-market-explorer.onrender.com)**

An interactive dashboard that explores a dataset of used car listings. The project practices real-world data work from start to finish: cleaning messy data, exploring it in a notebook, building a Streamlit web app and deploying it to the cloud.

## What the app answers

* How are car prices distributed?
* How does mileage affect price?
* How does price change with the condition of the vehicle?
* Which brands and which specific cars dominate the listings?
* How do listings split by transmission type and by 4WD?

## Repository structure

```
car-market-explorer/
├── .streamlit/
│   └── config.toml
├── datasets/
│   ├── vehicles.csv
│   └── vehicles_clean.csv
├── notebooks/
│   └── EDA.ipynb
├── .gitignore
├── app.py
├── README.md
└── requirements.txt
```

* `datasets/`: the raw listings and the cleaned version used by the app.
* `notebooks/EDA.ipynb`: the full cleaning process and the chart tests.
* `app.py`: the Streamlit dashboard.
* `requirements.txt`: the libraries needed to run the project.
* `.streamlit/config.toml`: Streamlit server settings used for the deployment.

## Data cleaning and analysis

The complete analysis is in `notebooks/EDA.ipynb`. In short, the raw data (51,525 listings) went through these steps:

* Standardized text columns and fixed implicit duplicates in vehicle names (for example, "ford f150" and "ford f-150").
* Checked for fully duplicated rows (none found).
* Treated unrealistic odometer values (under 500 miles, except for cars marked "new") as missing.
* Filled missing values with the median or mode of similar vehicles instead of a single overall value.
* Converted columns to the right data types.
* Removed outliers using cutoffs chosen from cumulative curves: price below 100 USD, odometer above 300k miles and model year before 1975.
* Split the vehicle name into "car_name", "brand" and "model".
* Exported the final dataset (50,240 listings) to `datasets/vehicles_clean.csv`.

The notebook also tests the 7 charts that were moved into the app.

## The web app

The app (`app.py`) loads the cleaned dataset and shows:

* a text header;
* a histogram of listing prices;
* a scatter plot of price vs. odometer, with a trendline;
* a box plot of price by condition;
* bar charts of the top 10 brands and the top 5 most listed cars;
* pie charts of transmission type and 4WD share.

The sidebar has two filters, and every chart updates when they change:

* **Brands:** a multi-select box to compare specific brands.
* **Show only 4WD listings:** a checkbox.

## Run locally

```
git clone https://github.com/CaueFabrizioBS/car-market-explorer.git
cd car-market-explorer
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # macOS / Linux
pip install -r requirements.txt
streamlit run app.py
```

## Tech stack

Python, pandas, Plotly Express, statsmodels, Streamlit, Jupyter Notebook. Deployed on Render.
