# Media Downloader & Converter

أداة سطر أوامر لتنزيل الفيديو والصوت وتحويل الملفات. المطوّر: **MOHAMED HB**

## المتطلبات
- Python 3.9+
- [ffmpeg](https://ffmpeg.org/download.html) مثبت ومضاف إلى PATH

## التثبيت والتشغيل
```bash
git clone https://github.com/medelhabib213/media-toolkit.gitcd media-toolkit
pip install -r requirements.txt
python main.py
```

## استخدام سريع (بدون قائمة)
```bash
python main.py -u "URL"                 # فيديو
python main.py -u "URL" -a -f mp3       # صوت فقط
python main.py -u "URL" -q 720          # جودة 720p
python main.py -c input.mkv -f mp4      # تحويل ملف
```

## تنبيه
استخدم الأداة فقط مع محتوى تملك حق تنزيله، والتزم بشروط الاستخدام وحقوق النشر.
