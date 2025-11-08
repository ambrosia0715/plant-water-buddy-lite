# Flutter
-keep class io.flutter.app.** { *; }
-keep class io.flutter.plugin.** { *; }
-keep class io.flutter.util.** { *; }
-keep class io.flutter.view.** { *; }
-keep class io.flutter.** { *; }
-keep class io.flutter.plugins.** { *; }
-keep class io.flutter.embedding.** { *; }

# Dart
-keep class * extends io.flutter.embedding.engine.plugins.FlutterPlugin { *; }

# Play Core (Deferred Components)
-keep class com.google.android.play.core.** { *; }
-dontwarn com.google.android.play.core.**

# Google Mobile Ads
-keep public class com.google.android.gms.ads.** { public *; }
-keep public class com.google.ads.** { public *; }
-dontwarn com.google.android.gms.ads.**

# Hive
-keep class * extends com.hivedb.** { *; }
-keepclassmembers class * extends com.hivedb.** { *; }
-keep class * implements com.hivedb.** { *; }

# Notification
-keep class com.dexterous.** { *; }
-keep class androidx.core.app.NotificationCompat** { *; }
-dontwarn com.dexterous.**

# Android Alarm Manager
-keep class dev.fluttercommunity.plus.androidalarmmanager.** { *; }

# Gson
-keepattributes Signature
-keepattributes *Annotation*
-dontwarn sun.misc.**
-keep class * implements com.google.gson.TypeAdapter
-keep class * implements com.google.gson.TypeAdapterFactory
-keep class * implements com.google.gson.JsonSerializer
-keep class * implements com.google.gson.JsonDeserializer

# Keep generic signature
-keep,allowobfuscation,allowshrinking interface retrofit2.Call
-keep,allowobfuscation,allowshrinking class retrofit2.Response

# Preserve line number information
-keepattributes SourceFile,LineNumberTable
-renamesourcefileattribute SourceFile
