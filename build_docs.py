"""把 index.html（claude.ai 上的版本）轉成 docs/index.html，給 GitHub Pages 用。
執行：python3 build_docs.py
"""
import re

SEED = {
    "5A": ["Jessy", "Brian", "Alex", "Ellison", "Howard", "Jerry", "Linus", "Frankie"],
    "6A": ["Alyssa", "Ariel", "Vanessa", "Anna", "Cynthia", "Vincent", "Sunny", "Phoebe", "Tim", "Rebecca", "Joyce"],
}

src = open("index.html", encoding="utf8").read()

def rep(a, b):
    global src
    assert src.count(a) == 1, a
    src = src.replace(a, b)

# 單獨網頁用本機儲存：沒有 claude.ai 的雲端資料庫時，不顯示「未登入」警告
rep("  setSync(why + '記錄只存在這台裝置。', true); render();",
    "  if (window.claude) setSync(why + '記錄只存在這台裝置。', true); else setSync('');\n  render();")

# 第一次打開時放入兩班名單
rep("mode = 'local'; classes = ensure(store.get('hw-local', {}));",
    """mode = 'local';
  const saved = store.get('hw-local', null);
  classes = ensure(saved || {});
  if (!saved){
    const SEED = __SEED__;
    FIXED.forEach(id => { classes[id].students = (SEED[id] || []).map((n, i) => ({id: 'p' + id + i, name: n})); });
    store.set('hw-local', classes);
  }""".replace("__SEED__", __import__("json").dumps(SEED, ensure_ascii=False)))

head = """<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="作業繳交">
<meta name="theme-color" content="#FFEFF4">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="icon" type="image/png" href="favicon.png">
<link rel="manifest" href="manifest.webmanifest">
<style>
:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
body{margin:0;font:14px -apple-system,BlinkMacSystemFont,sans-serif}
[hidden]:not([hidden=until-found i]){display:none!important}
</style>
"""
# 原檔開頭是 <title>…，直接接在 head 後面
body_start = src.index("<title>")
out = head + src[body_start:]
# <title> 到 <style> 之間是 head 內容；把 </head><body> 補在第一個 <div class="wrap"> 之前
m = out.index('<div class="wrap">')
out = out[:m] + "</head>\n<body>\n" + out[m:] + "\n</body>\n</html>\n"
open("docs/index.html", "w", encoding="utf8").write(out)
print("docs/index.html", len(out), "bytes")
