import os
import shutil

project_dir = "android_project"
app_dir = os.path.join(project_dir, "app")
src_main = os.path.join(app_dir, "src", "main")
java_dir = os.path.join(src_main, "java", "com", "ranjeetcybercafe", "app")
res_dir = os.path.join(src_main, "res")
assets_dir = os.path.join(src_main, "assets")

# Create directories
os.makedirs(java_dir, exist_ok=True)
os.makedirs(os.path.join(res_dir, "values"), exist_ok=True)
os.makedirs(os.path.join(res_dir, "mipmap-hdpi"), exist_ok=True)
os.makedirs(assets_dir, exist_ok=True)

# 1. settings.gradle
with open(os.path.join(project_dir, "settings.gradle"), "w", encoding="utf-8") as f:
    f.write("""rootProject.name = "Ranjeet Cyber Cafe"
include ':app'
""")

# 2. build.gradle (Project)
with open(os.path.join(project_dir, "build.gradle"), "w", encoding="utf-8") as f:
    f.write("""buildscript {
    repositories {
        google()
        mavenCentral()
    }
    dependencies {
        classpath "com.android.tools.build:gradle:8.0.2"
    }
}
allprojects {
    repositories {
        google()
        mavenCentral()
    }
}
""")

# 3. gradle.properties
with open(os.path.join(project_dir, "gradle.properties"), "w", encoding="utf-8") as f:
    f.write("""org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
android.nonTransitiveRClass=true
""")

# 4. app/build.gradle
with open(os.path.join(app_dir, "build.gradle"), "w", encoding="utf-8") as f:
    f.write("""plugins {
    id 'com.android.application'
}

android {
    namespace 'com.ranjeetcybercafe.app'
    compileSdk 33

    defaultConfig {
        applicationId "com.ranjeetcybercafe.app"
        minSdk 21
        targetSdk 33
        versionCode 1
        versionName "1.0"
    }

    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }
}

dependencies {
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.9.0'
}
""")

# 5. AndroidManifest.xml
with open(os.path.join(src_main, "AndroidManifest.xml"), "w", encoding="utf-8") as f:
    f.write("""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.ranjeetcybercafe.app">

    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher"
        android:supportsRtl="true"
        android:theme="@style/Theme.AppCompat.Light.NoActionBar">
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:configChanges="orientation|keyboardHidden|screenSize">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
""")

# 6. strings.xml
with open(os.path.join(res_dir, "values", "strings.xml"), "w", encoding="utf-8") as f:
    f.write("""<resources>
    <string name="app_name">Ranjeet Cyber Cafe</string>
</resources>
""")

# 7. MainActivity.java
with open(os.path.join(java_dir, "MainActivity.java"), "w", encoding="utf-8") as f:
    f.write("""package com.ranjeetcybercafe.app;

import android.os.Bundle;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {

    private WebView webView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        webView = new WebView(this);
        setContentView(webView);
        
        WebSettings webSettings = webView.getSettings();
        webSettings.setJavaScriptEnabled(true);
        webSettings.setDomStorageEnabled(true);
        webSettings.setAllowFileAccessFromFileURLs(true);
        webSettings.setAllowUniversalAccessFromFileURLs(true);

        // Required to open links inside the WebView instead of external browser
        webView.setWebViewClient(new WebViewClient());
        webView.loadUrl("file:///android_asset/index.html");
    }

    @Override
    public void onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }
}
""")

# Dummy icon files (1x1 pixel base64 encoded just so Android Studio doesn't crash on missing icon)
import base64
ic_launcher_data = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAFElEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==")
with open(os.path.join(res_dir, "mipmap-hdpi", "ic_launcher.png"), "wb") as f:
    f.write(ic_launcher_data)

# Now, copy the current folder web files into assets
current_dir = "."
for filename in os.listdir(current_dir):
    if filename.endswith(".html") or filename.endswith(".css") or filename.endswith(".js") or filename.endswith(".png") or filename.endswith(".jpg"):
        # Copy to assets
        src = os.path.join(current_dir, filename)
        dst = os.path.join(assets_dir, filename)
        try:
            shutil.copy2(src, dst)
            print(f"Copied {filename} to assets")
        except Exception as e:
            print(f"Failed to copy {filename}: {e}")

print("Android project generated successfully!")
