$projectDir = "android_project"
$appDir = Join-Path $projectDir "app"
$srcMain = Join-Path $appDir "src\main"
$javaDir = Join-Path $srcMain "java\com\ranjeetcybercafe\app"
$resDir = Join-Path $srcMain "res"
$assetsDir = Join-Path $srcMain "assets"

# Create directories
New-Item -ItemType Directory -Force -Path $javaDir | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $resDir "values") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $resDir "mipmap-hdpi") | Out-Null
New-Item -ItemType Directory -Force -Path $assetsDir | Out-Null

# 1. settings.gradle
@"
rootProject.name = "Ranjeet Cyber Cafe"
include ':app'
"@ | Out-File -FilePath (Join-Path $projectDir "settings.gradle") -Encoding UTF8

# 2. build.gradle (Project)
@"
buildscript {
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
"@ | Out-File -FilePath (Join-Path $projectDir "build.gradle") -Encoding UTF8

# 3. gradle.properties
@"
org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
android.nonTransitiveRClass=true
"@ | Out-File -FilePath (Join-Path $projectDir "gradle.properties") -Encoding UTF8

# 4. app/build.gradle
@"
plugins {
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
"@ | Out-File -FilePath (Join-Path $appDir "build.gradle") -Encoding UTF8

# 5. AndroidManifest.xml
@"
<?xml version="1.0" encoding="utf-8"?>
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
"@ | Out-File -FilePath (Join-Path $srcMain "AndroidManifest.xml") -Encoding UTF8

# 6. strings.xml
@"
<resources>
    <string name="app_name">Ranjeet Cyber Cafe</string>
</resources>
"@ | Out-File -FilePath (Join-Path $resDir "values\strings.xml") -Encoding UTF8

# 7. MainActivity.java
@"
package com.ranjeetcybercafe.app;

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
"@ | Out-File -FilePath (Join-Path $javaDir "MainActivity.java") -Encoding UTF8

# Dummy icon
$iconBase64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAFElEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
$iconBytes = [System.Convert]::FromBase64String($iconBase64)
[System.IO.File]::WriteAllBytes((Join-Path $resDir "mipmap-hdpi\ic_launcher.png"), $iconBytes)
[System.IO.File]::WriteAllBytes((Join-Path $resDir "mipmap-hdpi\ic_launcher_round.png"), $iconBytes)

# Copy web files
$currentDir = "."
$filesToCopy = Get-ChildItem -Path $currentDir | Where-Object { 
    $_.Extension -match "\.(html|css|js|png|jpg|jpeg|gif)$" 
}

foreach ($file in $filesToCopy) {
    $destPath = Join-Path $assetsDir $file.Name
    Copy-Item -Path $file.FullName -Destination $destPath -Force
    Write-Host "Copied $($file.Name) to assets"
}

Write-Host "Android project generated successfully!"
