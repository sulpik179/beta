[app]

# (str) Title of your application
title = Beta

# (str) Package name
package.name = beta

# (str) Package domain (reverse DNS)
package.domain = org.betaapp

# (str) Application version
version = 0.1.0

# (list) Application requirements
requirements = python3==3.11.9, kivy==2.3.0, sqlite3, certifi, android

# (str) Source directory
source.dir = .

# (list) Include patterns
source.include_patterns = 
    assets/**,
    gui/**,
    db_manager.py,
    main.py,
    main.kv

# (list) Exclude unnecessary files
source.exclude_patterns = 
    .git/**,
    .github/**,
    README.md,
    LICENSE,
    *.yml,
    *.spec,
    *.log

# (str) App icon — 512x512 PNG
icon.filename = %(source.dir)s/assets/icon.png

# (str) Orientation
orientation = portrait

# (list) Android permissions
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

# (int) Target and min API
android.api = 34
android.minapi = 21

# (bool) AndroidX support — REQUIRED
android.enable_androidx = True

# (str) Gradle version — compatible with API 34
android.gradle_dependencies = com.android.tools.build:gradle:7.4.2

# (str) Bootstrap — standard for Kivy
p4a.bootstrap = sdl2

# (str) Use develop branch for latest fixes
p4a.branch = develop

# (bool) Clean build (safe in CI)
build.clean = True


[buildozer]

# (int) Log level
log_level = 2

# (str) Build dirs
build_dir = .buildozer
bin_dir = bin
