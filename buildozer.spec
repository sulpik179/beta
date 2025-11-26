[app]

# (str) Title of your application
title = beta

# (str) Package name
package.name = beta

# (str) Package domain
package.domain = org.example

# (str) Application version
version = 1.0

# (list) Application requirements
requirements = python3, kivy, sqlite3

# (str) Source code where the main.py live
source.dir = .

# (list) List of inclusions using pattern matching
source.include_patterns = assets/**, gui/**, db_manager.py, main.py, main.kv

# (list) Source files to exclude
source.exclude_exts = spec

# (str) Presplash of the application
presplash.filename = %(source.dir)s/assets/presplash.jpg  # или убери эту строку

# (str) Icon of the application
icon.filename = %(source.dir)s/assets/icon.png  # или убери

# (str) Supported orientation (one of landscape, portrait or all)
orientation = portrait

# (list) Permissions
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 30

# (int) Minimum API
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 30

# (str) Android NDK version to use
android.ndk = 25b  

# (bool) Enable AndroidX support
android.enable_androidx = True

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

android.accept_sdk_license = True
