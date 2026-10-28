# Open "Grade XI, Physics - Circular Motion" the way a notification would.
adb shell am start -n com.neb.ians/com.neb.ians.MainActivity \
  --ez neb_extra_is_notification true --es neb_extra_verb open \
  --es neb_extra_target_type resource --es neb_extra_target_id 05211640-0b00-473a-a59d-c1ec6eb755cb
sleep 6
