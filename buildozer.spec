[app]

title = beta
package.name = betaapp
package.domain = org.sulpik
source.dir = .
source.include_exts = py, kv, db, ttf, txt, sql, csv

version = 1.0
requirements = python3, kivy==2.3.1, sqlite3
orientation = portrait

fullscreen = 0
log_level = 2

# включаем интернет (если понадобится)
android.permission.INTERNET = True

# иконка (если нет — закомментируй)
# icon.filename = assets/icon.png

# копируем твою папку data целиком
android.presplash_color = #FFFFFF
android.allow_backup = True

# важно: включаем assets
android.add_assets = data
android.add_assets = assets

# шрифты
android.include_exts = ttf

# это нужно для корректного копирования БД
android.allow_host_sdcard = True

# Python-for-Android параметры
p4a.branch = master

# чтобы кириллица не ломалась
android.extra_args = --copy-libs

[buildozer]
log_level = 2
warn_on_root = 0
