[app]

title = beta
package.name = betaapp
package.domain = org.sulpik
source.dir = .
source.include_exts = py, kv, db, ttf, txt, sql, csv

version = 1.0
# ✅ Добавил cython==0.29.33
requirements = python3, kivy==2.1.0, pyjnius==1.4.2, cython==0.29.33, sqlite3
orientation = portrait

fullscreen = 0
log_level = 2

# включаем интернет (если понадобится)
android.permission.INTERNET = True

# иконка (если нет — закомментируй)
# icon.filename = assets/icon.png

# копируем твою папку assets целиком
android.presplash_color = #FFFFFF
android.allow_backup = True

android.accept_sdk_license = True

# важно: включаем assets
source.include_patterns = assets/**, data/**, gui/**, db_manager.py, main.py, main.kv

android.build_tools = 33.0.0  # или 34.0.0

# шрифты
android.include_exts = ttf

# это нужно для корректного копирования БД
android.allow_host_sdcard = True

# Python-for-Android параметры
# ✅ Изменил на develop
p4a.branch = develop

# ✅ Удалил строку
# android.add_compile_options = --disable-remote-debugging

# ✅ Удалил строку
# android.ndk = 25b

android.api = 30
android.minapi = 21


[buildozer]
log_level = 2
warn_on_root = 0