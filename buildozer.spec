[app]

title = Beta
package.name = beta
package.domain = org.betaapp

version = 0.1.0

requirements = python3,kivy==2.3.0,sqlite3,certifi,android,pillow,pyjnius,openssl

source.dir = .
source.include_patterns = assets/**,gui/**,db_manager.py,main.py,main.kv

icon.filename = %(source.dir)s/assets/icon.png

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

android.api = 34
android.minapi = 21
android.sdk = 34
android.ndk = 26b
android.archs = armeabi-v7a, arm64-v8a

android.enable_androidx = True
android.accept_sdk_license = True

p4a.bootstrap = sdl2
p4a.branch = develop

[buildozer]

log_level = 2
warn_on_root = 1
