import streamlit as st
import pandas as pd
import numpy as np
import joblib

st.set_page_config(page_title='Nassau Candy Optimization', page_icon='🍫', layout='wide')

@st.cache_resource
def load_model():
    return joblib.load('lead_time_prediction_model.pkl')

@st.cache_data
def load_data():
    df = pd.read_csv('Nassau Candy Distributor.csv')
    recommendations = pd.read_csv('regional_reallocation_recommendations.csv')
    product_region = pd.read_csv('product_region_analysis.csv')
    return df, recommendations, product_region

try:
    model = load_model()
    df, recommendations, product_region = load_data()
except Exception as e:
    st.error('Required project files could not be loaded.')
    st.code(str(e))
    st.stop()

st.title('🍫 Nassau Candy Distributor')
st.subheader('Regional Reallocation & Shipping Optimization Dashboard')
st.info('This dashboard uses historical product-region performance to simulate potential regional reallocation scenarios. The dataset does not contain an explicit factory identifier, so Region is used as the operational allocation dimension.')

df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
df['Ship Date'] = pd.to_datetime(df['Ship Date'], dayfirst=True)
df['Lead Time'] = (df['Ship Date'] - df['Order Date']).dt.days

total_orders = df['Order ID'].nunique()
total_sales = df['Sales'].sum()
total_profit = df['Gross Profit'].sum()
avg_lead_time = df['Lead Time'].mean()
avg_margin = ((df['Gross Profit'] / df['Sales']) * 100).mean()

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric('Total Orders', f'{total_orders:,}')
c2.metric('Total Sales', f'${total_sales:,.2f}')
c3.metric('Gross Profit', f'${total_profit:,.2f}')
c4.metric('Avg Lead Time', f'{avg_lead_time:,.1f} days')
c5.metric('Avg Profit Margin', f'{avg_margin:.2f}%')
st.divider()

st.sidebar.header('Dashboard Filters')
regions = sorted(df['Region'].dropna().unique())
divisions = sorted(df['Division'].dropna().unique())
ship_modes = sorted(df['Ship Mode'].dropna().unique())
selected_region = st.sidebar.selectbox('Region', ['All'] + regions)
selected_division = st.sidebar.selectbox('Division', ['All'] + divisions)
selected_ship_mode = st.sidebar.selectbox('Ship Mode', ['All'] + ship_modes)
filtered_df = df.copy()
if selected_region != 'All': filtered_df = filtered_df[filtered_df['Region'] == selected_region]
if selected_division != 'All': filtered_df = filtered_df[filtered_df['Division'] == selected_division]
if selected_ship_mode != 'All': filtered_df = filtered_df[filtered_df['Ship Mode'] == selected_ship_mode]

st.header('📊 Business Overview')
col1, col2 = st.columns(2)
with col1:
    st.bar_chart(filtered_df.groupby('Region')['Sales'].sum().sort_values(ascending=False))
    st.caption('Sales by Region')
with col2:
    st.bar_chart(filtered_df.groupby('Region')['Lead Time'].mean().sort_values(ascending=False))
    st.caption('Average Lead Time by Region')

st.header('📦 Product Analysis')
products = sorted(product_region['Product Name'].dropna().unique())
selected_product = st.selectbox('Select a product', products)
product_data = product_region[product_region['Product Name'] == selected_product].copy()
if not product_data.empty:
    st.dataframe(product_data[['Product Name','Region','Orders','Sales','Gross_Profit','Avg_Lead_Time','Avg_Profit_Margin']].round(2), use_container_width=True, hide_index=True)

st.header('🔄 Regional Reallocation Simulator')
rec = recommendations[recommendations['Product Name'] == selected_product].copy()
if rec.empty:
    st.warning('No recommendation is available for this product.')
else:
    r = rec.iloc[0]
    current_lead = float(r['Current_Avg_Lead_Time'])
    best_region = r['Best_Region']
    best_lead = float(r['Best_Avg_Lead_Time'])
    reduction_days = float(r['Lead_Time_Reduction_Days'])
    reduction_pct = float(r['Lead_Time_Reduction_%'])
    confidence = float(r['Confidence Score'])
    category = r['Recommendation']
    a,b,c,d,e = st.columns(5)
    a.metric('Current Avg Lead Time', f'{current_lead:.2f} days')
    b.metric('Suggested Region', str(best_region))
    c.metric('Best Historical Lead Time', f'{best_lead:.2f} days')
    d.metric('Potential Reduction', f'{reduction_days:.2f} days')
    e.metric('Reduction %', f'{reduction_pct:.2f}%')
    st.progress(min(max(confidence/100,0),1), text=f'Scenario Confidence Score: {confidence:.1f}%')
    if category == 'Strong Scenario': st.success(f'Scenario category: {category}')
    elif category == 'Moderate Scenario': st.info(f'Scenario category: {category}')
    elif category == 'Low-Confidence Scenario': st.warning(f'Scenario category: {category}')
    else: st.info(f'Scenario category: {category}')
    st.caption('The confidence score is a project-defined sample-size heuristic, not a statistical probability.')

st.header('🤖 Lead-Time Prediction')
st.write('Enter order-time information below to generate a lead-time prediction from the trained Random Forest model.')
col1,col2,col3 = st.columns(3)
with col1:
    prediction_region = st.selectbox('Prediction Region', regions, key='prediction_region')
    prediction_division = st.selectbox('Prediction Division', divisions, key='prediction_division')
    prediction_ship_mode = st.selectbox('Prediction Ship Mode', ship_modes, key='prediction_ship_mode')
with col2:
    prediction_product = st.selectbox('Prediction Product', products, key='prediction_product')
    order_year = st.number_input('Order Year', min_value=2020, max_value=2035, value=2025, step=1)
    order_month = st.number_input('Order Month', min_value=1, max_value=12, value=1, step=1)
with col3:
    sales = st.number_input('Sales', min_value=0.0, value=100.0)
    units = st.number_input('Units', min_value=0, value=10, step=1)
    gross_profit = st.number_input('Gross Profit', min_value=0.0, value=50.0)
    cost = st.number_input('Cost', min_value=0.0, value=50.0)
if st.button('Predict Lead Time', type='primary'):
    input_data = pd.DataFrame([{'Product Name':prediction_product,'Ship Mode':prediction_ship_mode,'Division':prediction_division,'Region':prediction_region,'Sales':sales,'Units':units,'Gross Profit':gross_profit,'Cost':cost,'Order Year':order_year,'Order Month':order_month}])
    prediction = model.predict(input_data)[0]
    st.success(f'Predicted Shipping Lead Time: {prediction:.2f} days')

st.header('📈 Model Performance')
m1,m2,m3 = st.columns(3)
m1.metric('MAE','179.75 days')
m2.metric('RMSE','203.05 days')
m3.metric('R²','0.4170')
st.caption('These are test-set metrics from the Random Forest baseline model. They indicate moderate predictive signal, but predictions should not be interpreted as guaranteed delivery times.')

with st.expander('ℹ️ Methodology & Limitations'):
    st.markdown('''**Data analysis**\n- Python\n- Pandas\n- NumPy\n- Matplotlib\n- Seaborn\n\n**Machine learning**\n- Scikit-learn\n- Random Forest Regressor\n- One-hot encoding for categorical variables\n\n**Scenario analysis**\n- Historical average lead time by Product × Region\n- Best region identified using the lowest observed average lead time\n- Confidence score based on historical sample size\n\n**Important limitation**\n- The supplied dataset does not contain a factory identifier.\n- Therefore, the dashboard treats Region as the operational allocation dimension and presents the result as a regional reallocation scenario.\n- Historical scenario reductions are not guarantees of future performance.''')

st.caption('Unified Mentor Data Analyst Internship Project')
