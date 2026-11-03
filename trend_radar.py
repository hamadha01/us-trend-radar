import time
import requests
from bs4 import BeautifulSoup

# إعدادات بوت تليجرام (ضع بياناتك هنا)
TELEGRAM_BOT_TOKEN = "9034574414:AAHKZ8mCfpeqMNk7OETdTqKJcGmW9oTmjko"  # ضع توكن البوت هنا
TELEGRAM_CHAT_ID = "1532043948"      # ضع رقم الـ Chat ID هنا

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.json()
    except Exception as e:
        print(f"خطأ في إرسال الرسالة إلى تليجرام: {e}")

def check_google_trends():
    print("جاري فحص رادار الترندات في السوق الأمريكي...")
    try:
        # استخدام رابط RSS العام لترندات جوجل في الولايات المتحدة لضمان الاستقرار وعدم حدوث أخطاء 404
        url = "https://trends.google.com/trending/rss?geo=US"
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'xml')
            items = soup.find_all('item')[:5]  # جلب أحدث 5 ترندات ملتهبة
            
            if items:
                alert_text = "🚨 **رادار الترندات - ترند جديد في أمريكا!** 🚨\n\n"
                for idx, item in enumerate(items, 1):
                    title = item.find('title').text
                    traffic = item.find('{https://trends.google.com/trends/trendingsearches}approx_traffic')
                    traffic_text = f" (بحث: {traffic.text})" if traffic else ""
                    alert_text += f"{idx}. *{title}*{traffic_text}\n"
                
                alert_text += "\n💡 *تحرك بسرعة لتصميم ونشر المنتج قبل تشبع السوق!*"
                
                # إرسال التنبيه عبر تليجرام
                send_telegram_alert(alert_text)
                print("تم جلب الترندات وإرسال التنبيه بنجاح!")
        else:
            print(f"فشل الاتصال، رمز الاستجابة: {response.status_code}")
            
    except Exception as e:
        print(f"حدث خطأ أثناء جلب الترندات: {e}")

if __name__ == "__main__":
    # تشغيل الفحص تلقائياً كل 15 دقيقة (900 ثانية)
    while True:
        check_google_trends()
        time.sleep(900)
