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

#include <cstring>

#ifdef NDEBUG
#define LOGE(...) ((void)0)
#else
#define LOG_TAG "NebSpeech"
#define LOGE(...) __android_log_print(ANDROID_LOG_ERROR, LOG_TAG, __VA_ARGS__)
#endif

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

std::string unxor(const uint8_t* enc, size_t n, uint8_t k) {
    std::string s(n, '\0');
    for (size_t i = 0; i < n; ++i) s[i] = static_cast<char>(enc[i] ^ static_cast<uint8_t>(k + i * 7u));
    return s;
}

// ------------------------------------------------------------------ Whistle / Shruti (STT)

#ifndef NEB_NO_NEEDLE
void* gModelMap = nullptr;
size_t gModelLen = 0;
std::vector<char> gSttStreamBuf;
#endif

jboolean JNICALL nativeSttCompiled(JNIEnv*, jobject) {
#ifndef NEB_NO_NEEDLE
    return JNI_TRUE;
#else
    return JNI_FALSE;
#endif
}

// Maps the .cact read-only and hands it to the engine. The mapping is kept for the life of
// the process: the engine has no unload call and may keep pointing into it.
jint JNICALL nativeSttLoad(JNIEnv* env, jobject, jstring path) {
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

void JNICALL nativeSttReset(JNIEnv*, jobject) {
#ifndef NEB_NO_NEEDLE
    try { needle_reset(); } catch (...) {}
#endif
}

void JNICALL nativeSttAdviseIdle(JNIEnv*, jobject) {
#ifndef NEB_NO_NEEDLE
    if (gModelMap != nullptr && gModelLen > 0) {
        madvise(gModelMap, gModelLen, MADV_DONTNEED);
    }
    std::vector<char>().swap(gSttStreamBuf);
#endif
}

jstring JNICALL nativeSttError(JNIEnv* env, jobject) {
#ifdef NEB_NO_NEEDLE
    return toJava(env, "This device build has no speech engine");
#else
    return toJava(env, needle_last_error());
#endif
}

jstring JNICALL nativeSttStream(
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

jstring JNICALL nativeSttStop(JNIEnv* env, jobject) {
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

// ------------------------------------------------------------------ Phonon (TTS)

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
    static const uint8_t kPttsLib[14] = {
        0x35,0x09,0x05,0x1e,0x01,0x08,0xf0,0xd5,0xf7,0xfe,0xf6,0x88,0xde,0xdb
    };
    gTts.lib = dlopen(unxor(kPttsLib, 14, 0x59).c_str(), RTLD_NOW | RTLD_LOCAL);
    if (gTts.lib == nullptr) {
        LOGE("tts unavailable: %s", dlerror());
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

jboolean JNICALL nativeTtsAvailable(JNIEnv*, jobject) {
    return openTts() ? JNI_TRUE : JNI_FALSE;
}

jlong JNICALL nativeTtsLoad(JNIEnv* env, jobject, jstring dir, jstring lang, jint threads) {
    if (!openTts()) return 0;
    char buf[16];
    snprintf(buf, sizeof(buf), "%d", threads > 0 ? threads : 2);
    setenv("RAYON_NUM_THREADS", buf, 0);
    std::string d = toStd(env, dir), l = toStd(env, lang);
    PttsHandle* h = gTts.ptts_new(d.c_str(), 0, l.c_str());
    return reinterpret_cast<jlong>(h);
}

jstring JNICALL nativeTtsError(JNIEnv* env, jobject, jlong handle) {
    if (!gTts.ok) return toJava(env, "Text to speech is not available on this device");
    return toJava(env, gTts.ptts_last_error(reinterpret_cast<PttsHandle*>(handle)));
}

jobjectArray JNICALL nativeTtsVoices(JNIEnv* env, jobject, jlong handle) {
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

jboolean JNICALL nativeTtsSetVoice(JNIEnv* env, jobject, jlong handle, jstring name) {
    if (!gTts.ok || handle == 0) return JNI_FALSE;
    std::string n = toStd(env, name);
    return gTts.ptts_set_voice(reinterpret_cast<PttsHandle*>(handle), n.c_str()) ? JNI_TRUE : JNI_FALSE;
}

// sink.onPcm(FloatArray): Boolean, 24 kHz mono floats; return false to stop early.
jboolean JNICALL nativeTtsSpeak(JNIEnv* env, jobject, jlong handle, jstring text, jobject sink) {
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

void JNICALL nativeTtsFree(JNIEnv*, jobject, jlong handle) {
    if (gTts.ok && handle != 0) gTts.ptts_free(reinterpret_cast<PttsHandle*>(handle));
}

// ------------------------------------------------------------------ TinyVoca (TTS, all ABIs)

jlong JNICALL nativeVocaLoad(JNIEnv* env, jobject, jstring path) {
    std::string p = toStd(env, path);
    gVocaLastError.clear();
    neb_voca::VocaModel* m = neb_voca::voca_load(p.c_str(), &gVocaLastError);
    return reinterpret_cast<jlong>(m);
}

jstring JNICALL nativeVocaError(JNIEnv* env, jobject) {
    return toJava(env, gVocaLastError.empty() ? "Could not load TinyVoca model" : gVocaLastError.c_str());
}

jboolean JNICALL nativeVocaSpeak(
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

void JNICALL nativeVocaFree(JNIEnv*, jobject, jlong handle) {
    if (handle != 0) neb_voca::voca_free(reinterpret_cast<neb_voca::VocaModel*>(handle));
}

// ------------------------------------------------------------------ Anti-Tamper & Request Proof (HMAC-SHA256)

inline uint32_t rotr32(uint32_t x, uint32_t n) { return (x >> n) | (x << (32u - n)); }

void sha256_raw(const uint8_t* data, size_t len, uint8_t out[32]) {
    static const uint32_t K[64] = {
        0x428a2f98u,0x71374491u,0xb5c0fbcfu,0xe9b5dba5u,0x3956c25bu,0x59f111f1u,0x923f82a4u,0xab1c5ed5u,
        0xd807aa98u,0x12835b01u,0x243185beu,0x550c7dc3u,0x72be5d74u,0x80deb1feu,0x9bdc06a7u,0xc19bf174u,
        0xe49b69c1u,0xefbe4786u,0x0fc19dc6u,0x240ca1ccu,0x2de92c6fu,0x4a7484aau,0x5cb0a9dcu,0x76f988dau,
        0x983e5152u,0xa831c66du,0xb00327c8u,0xbf597fc7u,0xc6e00bf3u,0xd5a79147u,0x06ca6351u,0x14292967u,
        0x27b70a85u,0x2e1b2138u,0x4d2c6dfcu,0x53380d13u,0x650a7354u,0x766a0abbu,0x81c2c92eu,0x92722c85u,
        0xa2bfe8a1u,0xa81a664bu,0xc24b8b70u,0xc76c51a3u,0xd192e819u,0xd6990624u,0xf40e3585u,0x106aa070u,
        0x19a4c116u,0x1e376c08u,0x2748774cu,0x34b0bcb5u,0x391c0cb3u,0x4ed8aa4au,0x5b9cca4fu,0x682e6ff3u,
        0x748f82eeu,0x78a5636fu,0x84c87814u,0x8cc70208u,0x90befffau,0xa4506cebu,0xbef9a3f7u,0xc67178f2u
    };
    uint32_t h[8] = {
        0x6a09e667u,0xbb67ae85u,0x3c6ef372u,0xa54ff53au,
        0x510e527fu,0x9b05688cu,0x1f83d9abu,0x5be0cd19u
    };
    size_t full = ((len + 9u + 63u) / 64u) * 64u;
    std::vector<uint8_t> msg(full, 0);
    if (len > 0) memcpy(msg.data(), data, len);
    msg[len] = 0x80u;
    uint64_t bits = static_cast<uint64_t>(len) * 8ULL;
    for (int i = 0; i < 8; ++i) msg[full - 1 - i] = static_cast<uint8_t>(bits >> (i * 8));
    for (size_t off = 0; off < full; off += 64) {
        uint32_t w[64];
        for (int i = 0; i < 16; ++i) {
            const uint8_t* p = msg.data() + off + i * 4;
            w[i] = (uint32_t(p[0]) << 24) | (uint32_t(p[1]) << 16) | (uint32_t(p[2]) << 8) | uint32_t(p[3]);
        }
        for (int i = 16; i < 64; ++i) {
            uint32_t s0 = rotr32(w[i - 15], 7) ^ rotr32(w[i - 15], 18) ^ (w[i - 15] >> 3);
            uint32_t s1 = rotr32(w[i - 2], 17) ^ rotr32(w[i - 2], 19) ^ (w[i - 2] >> 10);
            w[i] = w[i - 16] + s0 + w[i - 7] + s1;
        }
        uint32_t a=h[0], b=h[1], c=h[2], d=h[3], e=h[4], f=h[5], g=h[6], hh=h[7];
        for (int i = 0; i < 64; ++i) {
            uint32_t S1 = rotr32(e, 6) ^ rotr32(e, 11) ^ rotr32(e, 25);
            uint32_t ch = (e & f) ^ ((~e) & g);
            uint32_t t1 = hh + S1 + ch + K[i] + w[i];
            uint32_t S0 = rotr32(a, 2) ^ rotr32(a, 13) ^ rotr32(a, 22);
            uint32_t maj = (a & b) ^ (a & c) ^ (b & c);
            uint32_t t2 = S0 + maj;
            hh = g; g = f; f = e; e = d + t1; d = c; c = b; b = a; a = t1 + t2;
        }
        h[0]+=a; h[1]+=b; h[2]+=c; h[3]+=d; h[4]+=e; h[5]+=f; h[6]+=g; h[7]+=hh;
    }
    for (int i = 0; i < 8; ++i) {
        out[i*4+0] = static_cast<uint8_t>(h[i] >> 24);
        out[i*4+1] = static_cast<uint8_t>(h[i] >> 16);
        out[i*4+2] = static_cast<uint8_t>(h[i] >> 8);
        out[i*4+3] = static_cast<uint8_t>(h[i]);
    }
}

jint JNICALL nativeEnvFlags(JNIEnv* env, jobject, jstring apkPath) {
    int flags = 0;
    // "/proc/self/status" XOR (0x41 + i*7)
    static const uint8_t kStatus[17] = {
        0x6e,0x38,0x3d,0x39,0x3e,0x4b,0x18,0x17,0x15,0xe6,0xa8,0xfd,0xe1,0xfd,0xd7,0xdf,0xc2
    };
    FILE* fs = fopen(unxor(kStatus, 17, 0x41).c_str(), "r");
    if (fs) {
        char line[128];
        while (fgets(line, sizeof(line), fs)) {
            if (strncmp(line, "TracerPid:", 10) == 0) {
                if (atoi(line + 10) > 0) flags |= 0x01;
                break;
            }
        }
        fclose(fs);
    }
    // "/proc/self/maps" XOR (0x53 + i*7)
    static const uint8_t kMaps[15] = {
        0x7c,0x2a,0x13,0x07,0x0c,0x59,0x0e,0xe1,0xe7,0xf4,0xb6,0xcd,0xc6,0xde,0xc6
    };
    FILE* fm = fopen(unxor(kMaps, 15, 0x53).c_str(), "r");
    if (fm) {
        char line[512];
        while (fgets(line, sizeof(line), fm)) {
            if (strstr(line, "frida") || strstr(line, "gum-js-loop") ||
                strstr(line, "xposed") || strstr(line, "lspd") ||
                strstr(line, "apkkiller") || strstr(line, "libmthook")) {
                flags |= 0x02;
                break;
            }
        }
        fclose(fm);
    }
    std::string p = toStd(env, apkPath);
    if (!p.empty()) {
        if (p.find("bin.mt.") != std::string::npos || p.find("npmanager") != std::string::npos ||
            p.find("chelpus") != std::string::npos || p.find("luckypatch") != std::string::npos) {
            flags |= 0x04;
        }
    }
    return flags;
}

jstring JNICALL nativeSignProof(JNIEnv* env, jobject, jstring payload) {
    std::string msg = toStd(env, payload);
    static const uint8_t kEnc[12] = {
        0x4d,0x4f,0x53,0x15,0x52,0x75,0x35,0x79,0x28,0x0b,0x0e,0x41
    };
    std::string key = unxor(kEnc, 12, 0x23);
    uint8_t k_ipad[64], k_opad[64];
    memset(k_ipad, 0x36, 64);
    memset(k_opad, 0x5c, 64);
    for (size_t i = 0; i < key.size(); ++i) {
        uint8_t b = static_cast<uint8_t>(key[i]);
        k_ipad[i] ^= b;
        k_opad[i] ^= b;
    }
    std::vector<uint8_t> inner(64 + msg.size());
    memcpy(inner.data(), k_ipad, 64);
    if (!msg.empty()) memcpy(inner.data() + 64, msg.data(), msg.size());
    uint8_t innerHash[32];
    sha256_raw(inner.data(), inner.size(), innerHash);
    uint8_t outer[96];
    memcpy(outer, k_opad, 64);
    memcpy(outer + 64, innerHash, 32);
    uint8_t mac[32];
    sha256_raw(outer, 96, mac);
    char hex[25];
    for (int i = 0; i < 12; ++i) snprintf(hex + i * 2, 3, "%02x", mac[i]);
    hex[24] = '\0';
    return env->NewStringUTF(hex);
}

}  // namespace

extern "C" JNIEXPORT jint JNICALL JNI_OnLoad(JavaVM* vm, void*) {
    JNIEnv* env = nullptr;
    if (vm->GetEnv(reinterpret_cast<void**>(&env), JNI_VERSION_1_6) != JNI_OK || env == nullptr) {
        return JNI_ERR;
    }
    static const uint8_t kClsName[32] = {
        0x54,0x51,0x28,0x63,0x3d,0x3f,0x03,0x47,0x06,0x17,0x13,0xf7,0xa4,0xe1,0xe9,0xc5,
        0xc2,0xcd,0xdd,0x93,0x8d,0xab,0xa5,0xb1,0xa9,0x83,0xbe,0x84,0x9e,0x67,0x6a,0x78
    };
    jclass cls = env->FindClass(unxor(kClsName, 32, 0x37).c_str());
    if (cls == nullptr) {
        env->ExceptionClear();
        return JNI_VERSION_1_6;
    }
    static const JNINativeMethod kMethods[] = {
        {"sttCompiled", "()Z", reinterpret_cast<void*>(nativeSttCompiled)},
        {"sttLoad", "(Ljava/lang/String;)I", reinterpret_cast<void*>(nativeSttLoad)},
        {"sttReset", "()V", reinterpret_cast<void*>(nativeSttReset)},
        {"sttAdviseIdle", "()V", reinterpret_cast<void*>(nativeSttAdviseIdle)},
        {"sttError", "()Ljava/lang/String;", reinterpret_cast<void*>(nativeSttError)},
        {"sttStream", "([FILjava/lang/String;Ljava/lang/String;)Ljava/lang/String;", reinterpret_cast<void*>(nativeSttStream)},
        {"sttStop", "()Ljava/lang/String;", reinterpret_cast<void*>(nativeSttStop)},
        {"ttsAvailable", "()Z", reinterpret_cast<void*>(nativeTtsAvailable)},
        {"ttsLoad", "(Ljava/lang/String;Ljava/lang/String;I)J", reinterpret_cast<void*>(nativeTtsLoad)},
        {"ttsError", "(J)Ljava/lang/String;", reinterpret_cast<void*>(nativeTtsError)},
        {"ttsVoices", "(J)[Ljava/lang/String;", reinterpret_cast<void*>(nativeTtsVoices)},
        {"ttsSetVoice", "(JLjava/lang/String;)Z", reinterpret_cast<void*>(nativeTtsSetVoice)},
        {"ttsSpeak", "(JLjava/lang/String;Lcom/neb/ians/speech/PcmSink;)Z", reinterpret_cast<void*>(nativeTtsSpeak)},
        {"ttsFree", "(J)V", reinterpret_cast<void*>(nativeTtsFree)},
        {"vocaLoad", "(Ljava/lang/String;)J", reinterpret_cast<void*>(nativeVocaLoad)},
        {"vocaError", "()Ljava/lang/String;", reinterpret_cast<void*>(nativeVocaError)},
        {"vocaSpeak", "(JLjava/lang/String;IFLcom/neb/ians/speech/PcmSink;)Z", reinterpret_cast<void*>(nativeVocaSpeak)},
        {"vocaFree", "(J)V", reinterpret_cast<void*>(nativeVocaFree)},
        {"envFlags", "(Ljava/lang/String;)I", reinterpret_cast<void*>(nativeEnvFlags)},
        {"signProof", "(Ljava/lang/String;)Ljava/lang/String;", reinterpret_cast<void*>(nativeSignProof)},
    };
    if (env->RegisterNatives(cls, kMethods, sizeof(kMethods) / sizeof(kMethods[0])) != 0) {
        env->ExceptionClear();
    }
    env->DeleteLocalRef(cls);
    return JNI_VERSION_1_6;
}
