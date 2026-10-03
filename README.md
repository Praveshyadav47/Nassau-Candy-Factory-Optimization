\# Nassau Candy Distributor – Regional Reallocation \& Shipping Optimization



\## 📌 Project Overview



This project analyzes Nassau Candy Distributor data to identify regional sales and profitability patterns, evaluate shipping lead times, and simulate potential regional reallocation scenarios.



A machine learning model is also developed to predict shipping lead time using order-time information.



\## 🎯 Objectives



\- Analyze sales and profitability across regions and divisions

\- Study shipping lead-time patterns

\- Compare product performance across regions

\- Identify historical regional scenarios with lower average lead times

\- Build a lead-time prediction model

\- Develop an interactive Streamlit dashboard



\## 🛠️ Technologies Used



\- Python

\- Pandas

\- NumPy

\- Matplotlib

\- Seaborn

\- Scikit-learn

\- Streamlit

\- Jupyter Notebook

\- Git \& GitHub



\## 📊 Key Analysis



The project includes:



\- Regional sales analysis

\- Product-level analysis

\- Division-level analysis

\- Shipping mode analysis

\- Product × Region lead-time analysis

\- Profit margin analysis

\- Regional reallocation scenario analysis



\## 🤖 Machine Learning



A Random Forest Regression model was developed to predict shipping lead time.



\### Model Performance



| Metric | Result |

|---|---:|

| MAE | 179.75 days |

| RMSE | 203.05 days |

| R² | 0.4170 |



The model uses information available around order time, including:



\- Product

\- Region

\- Division

\- Ship Mode

\- Order Year

\- Order Month

\- Sales

\- Units

\- Gross Profit

\- Cost



\## 🔄 Regional Reallocation Scenario



The dashboard compares historical average lead times for products across regions.



For example, for \*\*Wonka Bar - Milk Chocolate\*\*:



\- Current average lead time: 1314.26 days

\- Lower historical regional average: 1289.73 days

\- Potential historical reduction: 24.53 days

\- Potential reduction: 1.87%



These values represent historical scenario analysis and should not be interpreted as guaranteed future delivery improvements.



\## 📈 Streamlit Dashboard



The interactive dashboard provides:



\- Business KPIs

\- Regional sales analysis

\- Regional lead-time analysis

\- Product analysis

\- Regional reallocation simulator

\- Confidence score

\- Lead-time prediction

\- Model performance metrics



\## ⚠️ Limitations



The dataset does not contain an explicit factory identifier. Therefore, Region is used as the operational allocation dimension for the reallocation scenario.



The confidence score is a project-defined sample-size heuristic and is not a statistical probability.



The machine learning model provides predictions based on historical data and should not be interpreted as guaranteed delivery times.



\## 👨‍💻 Project



\*\*Unified Mentor Data Analyst Internship\*\*



Developed using Python, Pandas, NumPy, Scikit-learn and Streamlit.

