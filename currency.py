import streamlit as st
import requests
import datetime

# API Key and Base URL
API_KEY = st.secrets["exchange_api_key"]
BASE_URL = 'https://v6.exchangerate-api.com/v6/'

# Currency to Country Mapping
currency_country_mapping = {
    "USD": "United States",
    "EUR": "European Union",
    "JPY": "Japan",
    "CAD": "Canada",
    "AUD": "Australia",
    "PKR": "Pakistan",
    # Add more currencies and countries as needed
}

# Function to fetch exchange rates
def get_exchange_rates(base_currency):
    url = f"{BASE_URL}{API_KEY}/latest/{base_currency}"
    response = requests.get(url)
    data = response.json()
    if data['result'] == 'success':
        return data['conversion_rates']
    else:
        st.error("Error fetching exchange rates")
        return None

# Function to fetch historical data for the past month (adjusted for this example)
def get_historical_data(base_currency):
    end_date = datetime.datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
    url = f"{BASE_URL}{API_KEY}/latest/{base_currency}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        data = response.json()
        if data['result'] == 'success':
            return data['conversion_rates']
        else:
            st.error(f"API Error: {data.get('error-type', 'Unknown error')}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
        return None
    except ValueError as e:
        st.error(f"Failed to parse JSON response: {e}")
        return None

# Streamlit app with full yellow border and centered title
st.markdown("""
    <style>
    body {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    .main {
        padding: 20px;
        box-sizing: border-box;
    }
    .title {
        background-color: pink;
        color: black;
        font-weight: bold;
        font-size: 36px;
        text-transform: uppercase;
        text-align: center;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .content {
        text-align: center;
    }
    .result {
        border: 2px solid pink;
        padding: 10px;
        margin-top: 20px;
    }
    .result h3 {
        color: white;
        background-color: green;
        padding: 10px;
        font-size: 20px;
        border-radius: 5px;
    }
    .result p {
        margin: 5px 0;
        font-size: 16px;
    }
    </style>
    <div class="main">
        <div class="title">Ibn Adam's Exchange</div>
        <div class="content">
""", unsafe_allow_html=True)

# Currency conversion form
with st.form(key='conversion_form'):
    from_currency = st.selectbox("Select the Currency to Convert from:", ["USD", "EUR", "JPY", "CAD", "AUD", "PKR"])
    to_currency = st.selectbox("Select the Currency to Convert into:", ["USD", "EUR", "JPY", "CAD", "AUD", "PKR"])
    amount = st.number_input("Enter amount to be Converted:", min_value=0.0, format="%f")
    
    submit_button = st.form_submit_button(label='Convert')

# Convert currency when form is submitted
if submit_button:
    exchange_rates = get_exchange_rates(from_currency)
    if exchange_rates:
        # Use the conversion rates to calculate the converted amount
        cnv_from = exchange_rates[from_currency]
        cnv_to = exchange_rates[to_currency]
        base_amount = amount / cnv_from
        cnv_amount = base_amount * cnv_to
        
        # Get current date and time
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Display the result with custom styling
        st.markdown(f"""
            <div class="result">
                <h3>Converted Amount = {cnv_amount:.2f} {to_currency} ({currency_country_mapping.get(to_currency, 'Unknown Country')})</h3>
                <p>Conversion Date and Time: {now}</p>
                <p>Conversion Rate: 1 {from_currency} = {cnv_to / cnv_from:.2f} {to_currency}</p>
            </div>
        """, unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)
