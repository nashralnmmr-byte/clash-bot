import requests
from bs4 import BeautifulSoup
import json
import os

# 1. إنشاء مجلد البيانات إذا لم يكن موجوداً
if not os.path.exists('data'):
    os.makedirs('data')

def save_to_json(filename, data):
    # دالة لحفظ البيانات في ملفات بشكل مرتب
    with open(f'data/{filename}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"✅ تم حفظ ملف: {filename}.json بنجاح داخل مجلد data.")

def scrape_clash_data():
    print("--- 🚀 جاري تشغيل المحرك الذكي للموسوعة ---")
    
    # رابط تجريبي (صفحة الملك البربري)
    url = "https://clashofclans.fandom.com/wiki/Barbarian_King"
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # استخراج اسم الصفحة من الموقع
        title = soup.find('h1', id='firstHeading').text.strip()
        
        # تجهيز البيانات كـ "قاموس" (بديل ممتاز وسريع لـ pandas)
        test_data = {
            "hero_name": title,
            "status": "المحرك يعمل بكفاءة عالية",
            "ready_for_telegram": True
        }
        
        # حفظ البيانات
        save_to_json('heroes_test', test_data)
        print("🎉 مبروك! بيئتك البرمجية جاهزة 100% والمحرك يعمل بدون باندس.")
        
    except Exception as e:
        print(f"❌ حدث خطأ: {e}")

if __name__ == "__main__":
    scrape_clash_data()

