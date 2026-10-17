import os
import sys
import shutil

# ═══════════════════════════════════════════════════════
#   RUN.PY  —  bot.so লোডার (Android/Termux fix)
# ═══════════════════════════════════════════════════════

cur_dir = os.path.dirname(os.path.abspath(__file__))
target_so = None

# ১. ফাইলের নাম bot. দিয়ে শুরু এবং .so দিয়ে শেষ হলেই সেটা নাও
for f in os.listdir(cur_dir):
    if f.startswith("bot.") and f.endswith(".so"):
        target_so = os.path.join(cur_dir, f)
        break

if target_so is None:
    print("❌ ERROR: bot.so ফাইল পাওয়া যায়নি!")
    print(f"   Directory: {cur_dir}")
    print(f"   Files: {os.listdir(cur_dir)}")
    sys.exit(1)

print(f"✓ Found: {os.path.basename(target_so)}")

# ─────────────────────────────────────────────
# Android এ .so ফাইল সরাসরি লোড করতে সমস্যা হয়
# তাই cache directory তে কপি করে import করি
# ─────────────────────────────────────────────
if "/storage/emulated/" in cur_dir or "/sdcard" in cur_dir:
    cache_dir = os.path.expanduser("~/.cache_bot_runner")
    os.makedirs(cache_dir, exist_ok=True)

    # ক্যাশে ফাইলের নাম ঠিকভাবে bot.so হিসেবে সেভ করো
    cache_so = os.path.join(cache_dir, "bot.so")
    shutil.copy2(target_so, cache_so)
    print(f"✓ Cached to: {cache_so}")

    if cache_dir not in sys.path:
        sys.path.insert(0, cache_dir)

    import bot
else:
    if cur_dir not in sys.path:
        sys.path.insert(0, cur_dir)
    import bot

# ─────────────────────────────────────────────
# main() কল
# ─────────────────────────────────────────────
if hasattr(bot, "main"):
    bot.main()
elif hasattr(bot, "run"):
    bot.run()
else:
    print("❌ ERROR: bot module এ main() বা run() ফাংশন নেই!")
    sys.exit(1)