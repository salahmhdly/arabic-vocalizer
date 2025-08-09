# 1. ابدأ من صورة بايثون رسمية كنظام أساسي
FROM python:3.11-slim

# 2. تحديث وتثبيت الأدوات الضرورية (build-essential و cmake)
# هذا يضمن وجودها قبل أي شيء آخر
RUN apt-get update && apt-get install -y build-essential cmake

# 3. تعيين مجلد العمل داخل الحاوية
WORKDIR /app

# 4. نسخ ملف المكتبات أولاً (للاستفادة من التخزين المؤقت)
COPY requirements.txt .

# 5. تثبيت مكتبات البايثون
RUN pip install --no-cache-dir -r requirements.txt

# 6. نسخ باقي كود التطبيق
COPY . .

# 7. تحديد الأمر الذي سيتم تشغيله عند بدء تشغيل الحاوية
CMD ["gunicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
