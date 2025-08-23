import os

MY_API_KEY = os.getenv("MCA_API_KEY", "dummy_key_here")
ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", "NJSOJQKBF4BHH7Y6")
SEC_USER_AGENT = os.getenv("SEC_USER_AGENT", "chillakalyan78@gmail.com HackathonApp/1.0")

COMPANIES = {
    "INFY.NS": {"name": "Infosys", "adr": "INFY", "cin": "L85110KA1981PLC013115"},
    "RELIANCE.NS": {"name": "Reliance Industries", "adr": None, "cin": "L17110MH1973PLC019786"},
    "HDFCBANK.NS": {"name": "HDFC Bank", "adr": "HDB", "cin": "L65920MH1994PLC080618"},
    "TCS.NS": {"name": "Tata Consultancy Services", "adr": None, "cin": "L22210MH1995PLC084781"},
}
# Then in your pipeline/prototype, you just do:
from src.utils.config import COMPANIES, ALPHAVANTAGE_API_KEY
