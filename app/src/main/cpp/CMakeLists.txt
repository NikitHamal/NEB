cmake_minimum_required(VERSION 3.22.1)
project(neb_speech LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_library(neb_speech SHARED speech_jni.cpp)

# 16 KB page alignment (Google Play, Android 15+).
target_link_options(neb_speech PRIVATE -Wl,-z,max-page-size=16384)
target_compile_options(neb_speech PRIVATE -O2 -fvisibility=hidden)

find_library(log-lib log)
target_link_libraries(neb_speech PRIVATE ${log-lib} dl)

# Whistle speech recognition runs on the Needle engine. Prebuilt static libraries exist
# for arm64-v8a and armeabi-v7a only; other ABIs (x86 emulators) build a stub that
# reports the engine as unavailable.
set(NEEDLE_LIB ${CMAKE_CURRENT_SOURCE_DIR}/needle/${ANDROID_ABI}/libneedle.a)
if(EXISTS ${NEEDLE_LIB})
    add_library(needle STATIC IMPORTED)
    set_target_properties(needle PROPERTIES IMPORTED_LOCATION ${NEEDLE_LIB})
    target_include_directories(neb_speech PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/needle)
    target_link_libraries(neb_speech PRIVATE needle m)
else()
    target_compile_definitions(neb_speech PRIVATE NEB_NO_NEEDLE=1)
endif()
