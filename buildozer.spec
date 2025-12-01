[app]
title = Beta
package.name = beta
package.domain = org.sulpik
source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,ttf,db,sql
source.exclude_dirs = tests, __pycache__
version = 0.1
requirements = python3,kivy,pyjnius
android.orientation = portrait
android.api = 31
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.arch = arm64-v8a

[buildozer]
log_level = 2