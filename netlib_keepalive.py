import os
import time
import requests
from playwright.sync_api import sync_playwright

UZANTONOMO = os.environ.get("UZANTONOMO", "")
PASVORTO = os.environ.get("PASVORTO", "")
TELEGRAM_SIGNALO = os.environ.get("TELEGRAM_SIGNALO", "")
TELEGRAM_BABILO_ID = os.environ.get("TELEGRAM_BABILO_ID", "")

fail_msgs = [
    "Invalid credentials.",
    "Not connected to server.",
    "Error with the login: login size should be between 2 and 50"
]

report = ["🌐 netlib.re 域名保活报告"]

def login_account(playwright):
    report.append(f"🧑‍💻 开始登录账号: {UZANTONOMO}")
    try:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://www.netlib.re/", timeout=60000)
        time.sleep(3)

        report.append("👆 点击登录按钮")
        page.get_by_text("Login").click()
        time.sleep(2)

        report.append("✍️ 输入账号密码")
        page.get_by_role("textbox", name="Username").fill(UZANTONOMO)
        page.get_by_role("textbox", name="Password").fill(PASVORTO)
        page.get_by_role("button", name="Validate").click()
        page.wait_for_load_state("networkidle")
        time.sleep(2)

        success_text = "You are the exclusive owner of the following domains."
        if page.query_selector(f"text={success_text}"):
            report.append(f"✅ 登录成功，账号 {UZANTONOMO} 保活成功")
        else:
            fail_reason = None
            for msg in fail_msgs:
                if page.query_selector(f"text={msg}"):
                    fail_reason = msg
                    break
            if fail_reason:
                report.append(f"❌ 登录失败：{fail_reason}")
            else:
                report.append("⚠️ 登录结果未知，可能页面更新")

        context.close()
        browser.close()

    except Exception as e:
        report.append(f"⚠️ 登录异常：{e}")

def send_to_telegram(text):
    if not TELEGRAM_SIGNALO or not TELEGRAM_BABILO_ID:
        print("⚠️ 未配置 Telegram 通知参数，跳过发送")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_SIGNALO}/sendMessage"
    payload = {"chat_id": TELEGRAM_BABILO_ID, "text": text}
    try:
        r = requests.post(url, data=payload)
        print("📨 Telegram 通知已发送" if r.status_code == 200 else f"⚠️ Telegram 发送失败: {r.text}")
    except Exception as e:
        print(f"⚠️ Telegram 异常: {e}")

if __name__ == "__main__":
    with sync_playwright() as p:
        login_account(p)
    summary = "\n".join(report)
    print(summary)
    send_to_telegram(summary)
