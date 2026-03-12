import requests
from bs4 import BeautifulSoup

def get_live_data():
    url = "https://clashofclans.fandom.com/wiki/Barbarian_King"
    print("--- جاري الاتصال بمصدر البيانات للتحديث ---")
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'class': 'wikitable'})
        rows = table.find_all('tr')
        first_level_data = rows[1].find_all('td')
        dps_value = first_level_data[1].text.strip()
        print(f"✅ نجاح! القوة المحدثة للملك (مستوى 1) هي: {dps_value} DPS")
    except Exception as e:
        print(f"❌ خطأ: {e}")

if __name__ == "__main__":
    get_live_data()
