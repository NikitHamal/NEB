#!/usr/bin/env bash
# Runs on the CI emulator: install the release APK, clean the status bar, run every Maestro flow,
# and keep only screenshots, recordings and view hierarchies. Maestro's own debug output stays out
# of the artifact because it records typed text.
set -u
OUT="$PWD/app-captures"
DBG="$RUNNER_TEMP/maestro-debug"
mkdir -p "$OUT/hier" "$DBG"
APK=$(ls "$PWD"/apk/*.apk | head -1)
touch "$RUNNER_TEMP/start.marker"
adb install -r -g "$APK"
adb shell settings put system screen_off_timeout 1800000
adb shell svc power stayon true
demo_bar() {
  adb shell settings put global sysui_demo_allowed 1
  adb shell am broadcast -a com.android.systemui.demo -e command enter
  adb shell am broadcast -a com.android.systemui.demo -e command clock -e hhmm 1100
  adb shell am broadcast -a com.android.systemui.demo -e command battery -e level 100 -e plugged false
  adb shell am broadcast -a com.android.systemui.demo -e command network -e wifi show -e level 4 -e fully true -e mobile hide
  adb shell am broadcast -a com.android.systemui.demo -e command notifications -e visible false
} > /dev/null
demo_bar
cd "$OUT"
for f in "$GITHUB_WORKSPACE"/tools/reel/capture/app/flows/*.yaml; do
  name=$(basename "$f" .yaml)
  echo "::group::flow $name"
  demo_bar
  pre="${f%.yaml}.pre.sh"
  [ -f "$pre" ] && bash "$pre"
  maestro test --test-output-dir "$DBG/$name" -e NEB_USER="$NEB_USER" -e NEB_PASS="$NEB_PASS" "$f" && echo "flow $name: ok" >> "$OUT/flows.txt" || echo "flow $name: FAILED" >> "$OUT/flows.txt"
  maestro hierarchy > "$OUT/hier/$name.json" 2>/dev/null || true
  adb exec-out screencap -p > "$OUT/end-$name.png" || true
  echo "::endgroup::"
done
for ext in png mp4; do
  find "$GITHUB_WORKSPACE" "$DBG" "$HOME" -path "$OUT" -prune -o -name "*.$ext" -newer "$RUNNER_TEMP/start.marker" -print 2>/dev/null \
    | grep -v -E '/(\.android|\.gradle|\.maestro/(bin|lib))/' | while read -r f; do
      case "$f" in */screenshot-*|*/maestro-debug/*/screenshot*) cp -n "$f" "$OUT/debug-$(basename "$f")";; *) cp -n "$f" "$OUT/";; esac
    done
done
grep -l -i -E "password|$NEB_PASS" "$OUT"/hier/*.json 2>/dev/null | xargs -r rm -f
ls -la "$OUT"
cat "$OUT/flows.txt"
