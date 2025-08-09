from flask import Flask, request, jsonify
from flask_cors import CORS
# 1. استيراد المكتبة الجديدة
from camel_tools.diacritizer.api import Diacritizer

# 2. تهيئة المُشكّل (Diacritizer)
# سنستخدم النموذج الافتراضي 'catib_aljazeera' وهو دقيق جدًا
# سيتم تحميل النموذج في الذاكرة عند بدء تشغيل الخادم لأول مرة
diac = Diacritizer.from_pretrained()

app = Flask(__name__)
CORS(app)

@app.route('/api/tashkeel', methods=['POST'])
def api_tashkeel():
    data = request.get_json()

    if not data or 'text' not in data:
        return jsonify({"error": "الرجاء إرسال كائن JSON يحتوي على مفتاح 'text'"}), 400

    text_to_vocalize = data['text']
        
    # التحقق من أن النص ليس فارغًا
    if not text_to_vocalize.strip():
        return jsonify({
            "original_text": text_to_vocalize,
            "vocalized_text": ""
        })

    # 3. استخدام CAMeL Tools للتشكيل
    # المكتبة تتوقع قائمة من الجمل، لذلك نضع النص في قائمة
    # ثم نأخذ النتيجة الأولى من القائمة الناتجة
    try:
        vocalized_lines = diac.diacritize([text_to_vocalize])
        vocalized_text = vocalized_lines[0]
    except Exception as e:
        # في حال حدوث أي خطأ غير متوقع من المكتبة
        print(f"Error during diacritization: {e}")
        return jsonify({"error": "حدث خطأ داخلي أثناء محاولة تشكيل النص."}), 500

    return jsonify({
        "original_text": text_to_vocalize,
        "vocalized_text": vocalized_text
    })

@app.route('/')
def home():
    return "خادم التشكيل API يعمل. (النسخة المطورة باستخدام CAMeL Tools)"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

