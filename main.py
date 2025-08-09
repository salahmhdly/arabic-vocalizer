from flask import Flask, request, jsonify
from flask_cors import CORS
import mishkal.tashkeel

# 1. تهيئة تطبيق فلاسك
app = Flask(__name__)
CORS(app)

# --- التغيير المهم ---
# 2. لقد حذفنا إنشاء كائن التشكيل من هنا.
# لن ننشئه بشكل عام، بل سننشئه داخل كل طلب.
# vocalizer = mishkal.tashkeel.TashkeelClass()  <-- هذا السطر تم حذفه

@app.route('/api/tashkeel', methods=['POST'])
def api_tashkeel():
    # 3. إنشاء كائن تشكيل جديد مع كل طلب يدخل
    # هذا يضمن أن الكائن وقاعدة بياناته يتم إنشاؤهما في نفس خيط المعالجة
    vocalizer = mishkal.tashkeel.TashkeelClass()

    data = request.get_json()

    if not data or 'text' not in data:
        return jsonify({"error": "الرجاء إرسال كائن JSON يحتوي على مفتاح 'text'"}), 400

    text_to_vocalize = data['text']

    # 4. تشكيل النص باستخدام الكائن الجديد
    vocalized_text = vocalizer.tashkeel(text_to_vocalize)

    return jsonify({
        "original_text": text_to_vocalize,
        "vocalized_text": vocalized_text
    })

@app.route('/')
def home():
    return "خادم التشكيل API يعمل. (نسخة محدثة لحل مشكلة Threading)"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
