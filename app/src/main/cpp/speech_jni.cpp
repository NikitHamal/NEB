// JNI bridge for the on-device speech engines used by Notes.
//
//  - Speech to text: Cactus Whistle on the Needle engine (statically linked, see needle/).
//  - Text to speech: Gradium Phonon, libptts_ffi.so, opened with dlopen so the app still
//    runs on ABIs and phones where that library is not shipped.
//
// Both engines are process-global or single-threaded: the Kotlin side serialises every call.

#include <jni.h>
#include <android/log.h>
#include <dlfcn.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstddef>
#include <string>
#include <vector>

#include "tiny_voca.h"

#ifndef NEB_NO_NEEDLE
#include "needle.h"
#endif

#define LOG_TAG "NebSpeech"
#define LOGE(...) __android_log_print(ANDROID_LOG_ERROR, LOG_TAG, __VA_ARGS__)

namespace {

std::string toStd(JNIEnv* env, jstring s) {
    if (s == nullptr) return std::string();
    const char* c = env->GetStringUTFChars(s, nullptr);
    std::string out(c ? c : "");
    if (c) env->ReleaseStringUTFChars(s, c);
    return out;
}

jstring toJava(JNIEnv* env, const char* s) {
    return env->NewStringUTF(s ? s : "");
}

// ------------------------------------------------------------------ Whistle / Shruti (STT)

#ifndef NEB_NO_NEEDLE
void* gModelMap = nullptr;
size_t gModelLen = 0;
std::vector<char> gSttStreamBuf;
#endif

}  // namespace

extern "C" {

JNIEXPORT jboolean JNICALL
Java_com_neb_ians_speech_NativeSpeech_sttCompiled(JNIEnv*, jobject) {
#ifndef NEB_NO_NEEDLE
    return JNI_TRUE;
#else
    return JNI_FALSE;
#endif
}

// Maps the .cact read-only and hands it to the engine. The mapping is kept for the life of
// the process: the engine has no unload call and may keep pointing into it.
JNIEXPORT jint JNICALL
Java_com_neb_ians_speech_NativeSpeech_sttLoad(JNIEnv* env, jobject, jstring path) {
#ifdef NEB_NO_NEEDLE
    (void) env; (void) path;
    return -1;
#else
    std::string p = toStd(env, path);
    int fd = open(p.c_str(), O_RDONLY | O_CLOEXEC);
    if (fd < 0) return -2;
    struct stat st;
    if (fstat(fd, &st) != 0 || st.st_size <= 0) { close(fd); return -3; }
    void* map = mmap(nullptr, (size_t) st.st_size, PROT_READ, MAP_PRIVATE, fd, 0);
    close(fd);
    if (map == MAP_FAILED) return -4;
    madvise(map, (size_t) st.st_size, MADV_WILLNEED | MADV_SEQUENTIAL);
    int rc = -5;
    try {
        rc = needle_load(reinterpret_cast<const unsigned char*>(map), (unsigned long long) st.st_size);
    } catch (...) {
        rc = -6;
    }
    if (rc < 0) {
        munmap(map, (size_t) st.st_size);
        return rc;
    }
    if (gModelMap != nullptr && gModelLen > 0) {
        munmap(gModelMap, gModelLen);
    }
    gModelMap = map;
    gModelLen = (size_t) st.st_size;
    return needle_models();
#endif
}

JNIEXPORT void JNICALL
Java_com_neb_ians_speech_NativeSpeech_sttReset(JNIEnv*, jobject) {
#ifndef NEB_NO_NEEDLE
    try { needle_reset(); } catch (...) {}
#endif
}

JNIEXPORT void JNICALL
Java_com_neb_ians_speech_NativeSpeech_sttAdviseIdle(JNIEnv*, jobject) {
#ifndef NEB_NO_NEEDLE
    if (gModelMap != nullptr && gModelLen > 0) {
        madvise(gModelMap, gModelLen, MADV_DONTNEED);
    }
    std::vector<char>().swap(gSttStreamBuf);
#endif
}

JNIEXPORT jstring JNICALL
Java_com_neb_ians_speech_NativeSpeech_sttError(JNIEnv* env, jobject) {
#ifdef NEB_NO_NEEDLE
    return toJava(env, "This device build has no speech engine");
#else
    return toJava(env, needle_last_error());
#endif
}

JNIEXPORT jstring JNICALL
Java_com_neb_ians_speech_NativeSpeech_sttStream(
        JNIEnv* env, jobject, jfloatArray pcm, jint samples, jstring lang, jstring keywords) {
#ifdef NEB_NO_NEEDLE
    (void) env; (void) pcm; (void) samples; (void) lang; (void) keywords;
    return nullptr;
#else
    std::string l = toStd(env, lang), k = toStd(env, keywords);
    jfloat* data = env->GetFloatArrayElements(pcm, nullptr);
    if (data == nullptr) return nullptr;
    if (gSttStreamBuf.size() < (1 << 17)) gSttStreamBuf.resize(1 << 17, 0);
    const int cap = (int) gSttStreamBuf.size();
    gSttStreamBuf[0] = '\0';
    int rc = -1;
    try {
        rc = needle_stream_transcribe_process(data, samples, l.empty() ? nullptr : l.c_str(),
                                              k.empty() ? nullptr : k.c_str(), gSttStreamBuf.data(), cap);
    } catch (...) {
        rc = -1;
    }
    env->ReleaseFloatArrayElements(pcm, data, JNI_ABORT);
    if (rc < 0) return nullptr;
    return toJava(env, gSttStreamBuf.data());
#endif
}

JNIEXPORT jstring JNICALL
Java_com_neb_ians_speech_NativeSpeech_sttStop(JNIEnv* env, jobject) {
#ifdef NEB_NO_NEEDLE
    (void) env;
    return nullptr;
#else
    if (gSttStreamBuf.size() < (1 << 17)) gSttStreamBuf.resize(1 << 17, 0);
    const int cap = (int) gSttStreamBuf.size();
    gSttStreamBuf[0] = '\0';
    int rc = -1;
    try {
        rc = needle_stream_transcribe_stop(gSttStreamBuf.data(), cap);
    } catch (...) {
        rc = -1;
    }
    if (rc < 0) return nullptr;
    return toJava(env, gSttStreamBuf.data());
#endif
}

}  // extern "C"

// ------------------------------------------------------------------ Phonon (TTS)

namespace {

struct PttsHandle;
struct PttsResult {
    uint32_t frames;
    size_t samples;
    double ttfa_ms;
    double total_ms;
};
typedef bool (*PttsFrameFn)(const float* pcm, size_t n, void* user);

struct PttsApi {
    void* lib = nullptr;
    PttsHandle* (*ptts_new)(const char*, uint32_t, const char*) = nullptr;
    bool (*ptts_speak)(PttsHandle*, const char*, PttsFrameFn, void*, PttsResult*) = nullptr;
    const char* (*ptts_voices)(const PttsHandle*) = nullptr;
    bool (*ptts_set_voice)(PttsHandle*, const char*) = nullptr;
    bool (*ptts_set_language)(PttsHandle*, const char*) = nullptr;
    const char* (*ptts_last_error)(const PttsHandle*) = nullptr;
    void (*ptts_free)(PttsHandle*) = nullptr;
    bool tried = false;
    bool ok = false;
};

PttsApi gTts;

bool openTts() {
    if (gTts.tried) return gTts.ok;
    gTts.tried = true;
    gTts.lib = dlopen("libptts_ffi.so", RTLD_NOW | RTLD_LOCAL);
    if (gTts.lib == nullptr) {
        LOGE("libptts_ffi.so unavailable: %s", dlerror());
        return false;
    }
#define BIND(name) gTts.name = reinterpret_cast<decltype(gTts.name)>(dlsym(gTts.lib, #name))
    BIND(ptts_new);
    BIND(ptts_speak);
    BIND(ptts_voices);
    BIND(ptts_set_voice);
    BIND(ptts_set_language);
    BIND(ptts_last_error);
    BIND(ptts_free);
#undef BIND
    gTts.ok = gTts.ptts_new && gTts.ptts_speak && gTts.ptts_voices && gTts.ptts_set_voice &&
              gTts.ptts_set_language && gTts.ptts_last_error && gTts.ptts_free;
    return gTts.ok;
}

struct SpeakCtx {
    JNIEnv* env;
    jobject sink;
    jmethodID onPcm;
    jfloatArray cachedArr = nullptr;
    jsize cachedCap = 0;
    bool failed = false;
};

bool onFrame(const float* pcm, size_t n, void* user) {
    SpeakCtx* ctx = static_cast<SpeakCtx*>(user);
    JNIEnv* env = ctx->env;
    jsize len = (jsize) n;
    if (ctx->cachedArr == nullptr || ctx->cachedCap != len) {
        if (ctx->cachedArr != nullptr) env->DeleteLocalRef(ctx->cachedArr);
        ctx->cachedArr = env->NewFloatArray(len);
        ctx->cachedCap = len;
    }
    if (ctx->cachedArr == nullptr) { ctx->failed = true; return false; }
    env->SetFloatArrayRegion(ctx->cachedArr, 0, len, pcm);
    jboolean keep = env->CallBooleanMethod(ctx->sink, ctx->onPcm, ctx->cachedArr);
    if (env->ExceptionCheck()) {
        env->ExceptionClear();
        ctx->failed = true;
        return false;
    }
    return keep == JNI_TRUE;
}

std::string gVocaLastError;

}  // namespace

extern "C" {

JNIEXPORT jboolean JNICALL
Java_com_neb_ians_speech_NativeSpeech_ttsAvailable(JNIEnv*, jobject) {
    return openTts() ? JNI_TRUE : JNI_FALSE;
}

JNIEXPORT jlong JNICALL
Java_com_neb_ians_speech_NativeSpeech_ttsLoad(JNIEnv* env, jobject, jstring dir, jstring lang, jint threads) {
    if (!openTts()) return 0;
    char buf[16];
    snprintf(buf, sizeof(buf), "%d", threads > 0 ? threads : 2);
    setenv("RAYON_NUM_THREADS", buf, 0);
    std::string d = toStd(env, dir), l = toStd(env, lang);
    PttsHandle* h = gTts.ptts_new(d.c_str(), 0, l.c_str());
    return reinterpret_cast<jlong>(h);
}

JNIEXPORT jstring JNICALL
Java_com_neb_ians_speech_NativeSpeech_ttsError(JNIEnv* env, jobject, jlong handle) {
    if (!gTts.ok) return toJava(env, "Text to speech is not available on this device");
    return toJava(env, gTts.ptts_last_error(reinterpret_cast<PttsHandle*>(handle)));
}

JNIEXPORT jobjectArray JNICALL
Java_com_neb_ians_speech_NativeSpeech_ttsVoices(JNIEnv* env, jobject, jlong handle) {
    jclass str = env->FindClass("java/lang/String");
    std::vector<std::string> names;
    if (gTts.ok && handle != 0) {
        const char* p = gTts.ptts_voices(reinterpret_cast<PttsHandle*>(handle));
        while (p && *p) {
            names.emplace_back(p);
            p += names.back().size() + 1;
        }
    }
    jobjectArray arr = env->NewObjectArray((jsize) names.size(), str, nullptr);
    for (size_t i = 0; i < names.size(); i++) {
        jstring s = env->NewStringUTF(names[i].c_str());
        env->SetObjectArrayElement(arr, (jsize) i, s);
        env->DeleteLocalRef(s);
    }
    return arr;
}

JNIEXPORT jboolean JNICALL
Java_com_neb_ians_speech_NativeSpeech_ttsSetVoice(JNIEnv* env, jobject, jlong handle, jstring name) {
    if (!gTts.ok || handle == 0) return JNI_FALSE;
    std::string n = toStd(env, name);
    return gTts.ptts_set_voice(reinterpret_cast<PttsHandle*>(handle), n.c_str()) ? JNI_TRUE : JNI_FALSE;
}

// sink.onPcm(FloatArray): Boolean, 24 kHz mono floats; return false to stop early.
JNIEXPORT jboolean JNICALL
Java_com_neb_ians_speech_NativeSpeech_ttsSpeak(JNIEnv* env, jobject, jlong handle, jstring text, jobject sink) {
    if (!gTts.ok || handle == 0) return JNI_FALSE;
    jclass cls = env->GetObjectClass(sink);
    jmethodID mid = env->GetMethodID(cls, "onPcm", "([F)Z");
    if (mid == nullptr) return JNI_FALSE;
    std::string t = toStd(env, text);
    SpeakCtx ctx{env, sink, mid};
    PttsResult res{};
    bool ok = gTts.ptts_speak(reinterpret_cast<PttsHandle*>(handle), t.c_str(), onFrame, &ctx, &res);
    if (ctx.cachedArr != nullptr) env->DeleteLocalRef(ctx.cachedArr);
    return (ok && !ctx.failed) ? JNI_TRUE : JNI_FALSE;
}

JNIEXPORT void JNICALL
Java_com_neb_ians_speech_NativeSpeech_ttsFree(JNIEnv*, jobject, jlong handle) {
    if (gTts.ok && handle != 0) gTts.ptts_free(reinterpret_cast<PttsHandle*>(handle));
}

// ------------------------------------------------------------------ TinyVoca (TTS, all ABIs)

JNIEXPORT jlong JNICALL
Java_com_neb_ians_speech_NativeSpeech_vocaLoad(JNIEnv* env, jobject, jstring path) {
    std::string p = toStd(env, path);
    gVocaLastError.clear();
    neb_voca::VocaModel* m = neb_voca::voca_load(p.c_str(), &gVocaLastError);
    return reinterpret_cast<jlong>(m);
}

JNIEXPORT jstring JNICALL
Java_com_neb_ians_speech_NativeSpeech_vocaError(JNIEnv* env, jobject) {
    return toJava(env, gVocaLastError.empty() ? "Could not load TinyVoca model" : gVocaLastError.c_str());
}

JNIEXPORT jboolean JNICALL
Java_com_neb_ians_speech_NativeSpeech_vocaSpeak(
        JNIEnv* env, jobject, jlong handle, jstring text, jint voiceId, jfloat speed, jobject sink) {
    if (handle == 0 || sink == nullptr) return JNI_FALSE;
    jclass cls = env->GetObjectClass(sink);
    jmethodID mid = env->GetMethodID(cls, "onPcm", "([F)Z");
    if (mid == nullptr) return JNI_FALSE;
    std::string t = toStd(env, text);
    SpeakCtx ctx{env, sink, mid};
    gVocaLastError.clear();
    bool ok = neb_voca::voca_speak(
        reinterpret_cast<neb_voca::VocaModel*>(handle),
        t.c_str(),
        (int) voiceId,
        (float) speed,
        onFrame,
        &ctx,
        &gVocaLastError
    );
    if (ctx.cachedArr != nullptr) env->DeleteLocalRef(ctx.cachedArr);
    return (ok && !ctx.failed) ? JNI_TRUE : JNI_FALSE;
}

JNIEXPORT void JNICALL
Java_com_neb_ians_speech_NativeSpeech_vocaFree(JNIEnv*, jobject, jlong handle) {
    if (handle != 0) neb_voca::voca_free(reinterpret_cast<neb_voca::VocaModel*>(handle));
}

}  // extern "C"
