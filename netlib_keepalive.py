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
screenshot_path = "login_failed.png"


def send_to_telegram(text, image_path=None):
    """发送消息到 Telegram（可带图片）"""
    if not TELEGRAM_SIGNALO or not TELEGRAM_BABILO_ID:
        print("⚠️ 未配置 Telegram 通知参数，跳过发送")
        return

    base_url = f"https://api.telegram.org/bot{TELEGRAM_SIGNALO}"

    # 1️⃣ 发送文字消息
    try:
        r = requests.post(f"{base_url}/sendMessage", data={
            "chat_id": TELEGRAM_BABILO_ID,
            "text": text
        })
        if r.status_code == 200:
            print("📨 Telegram 文本已发送")
        else:
            print(f"⚠️ Telegram 文本发送失败: {r.text}")
    except Exception as e:
        print(f"⚠️ Telegram 文本异常: {e}")

    # 2️⃣ 若有截图则发送图片
    if image_path and os.path.exists(image_path):
        try:
            with open(image_path, "rb") as photo:
                r = requests.post(f"{base_url}/sendPhoto", data={
                    "chat_id": TELEGRAM_BABILO_ID,
                    "caption": "📸 登录失败截图"
                }, files={"photo": photo})
            if r.status_code == 200:
                print("🖼️ Telegram 截图已发送")
            else:
                print(f"⚠️ Telegram 截图发送失败: {r.text}")
        except Exception as e:
            print(f"⚠️ Telegram 图片异常: {e}")


def login_account(playwright):
    """执行登录"""
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
            context.close()
            browser.close()
            return True

        else:
            fail_reason = None
            for msg in fail_msgs:
                if page.query_selector(f"text={msg}"):
                    fail_reason = msg
                    break
            fail_reason = fail_reason or "未知错误"

            # ⛔ 登录失败截图
            report.append(f"❌ 登录失败：{fail_reason}")
            report.append("📸 捕获失败页面截图")
            page.screenshot(path=screenshot_path)
            context.close()
            browser.close()
            return False

    except Exception as e:
        report.append(f"⚠️ 登录异常：{e}")
        try:
            page.screenshot(path=screenshot_path)
        except:
            pass
        return False


if __name__ == "__main__":
    with sync_playwright() as p:
        success = login_account(p)
    summary = "\n".join(report)
    print(summary)
    # 登录失败时发送截图
    send_to_telegram(summary, image_path=None if success else screenshot_path)
