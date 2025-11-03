# netlib_keepalive
每三十天登陆一次


## 在仓库中打开：
Settings → Secrets → Actions → New repository secret

添加以下四个：

名称	值示例

UZANTONOMO	你的 netlib 用户名  

PASVORTO	你的 netlib 密码

TELEGRAM_SIGNALO	你的 Telegram Bot Token

TELEGRAM_BABILO_ID	你的 Chat ID


登录成功：Telegram 通知

🌐 netlib.re 域名保活报告

✅ 登录成功，账号 xxx 保活成功


登录失败：Telegram 通知 + 截图

❌ 登录失败：Invalid credentials.

📸 捕获失败页面截图


（截图会以图片消息附带在 Telegram 上）

#----------------------------------------------------------------------------

# js为cf保活脚本

1.在 Worker 设置中添加环境变量（Variables）  

变量名	内容

UZANTONOMO	netlib 用户名

PASVORTO	netlib 密码

TELEGRAM_SIGNALO	Telegram Bot Token

TELEGRAM_BABILO_ID	Telegram Chat ID

2.添加 Cron 触发器（自动运行）

在 Worker 的「Triggers → Cron Triggers」里添加：

0 0 */10 * *    # 每10天执行一次


3.也可以添加多个，例如：

0 8 * * *       # 每天上午8点执行


效果示例（Telegram 通知）

成功：

🌐 netlib.re 域名保活报告

🧑‍💻 正在登录账号：myuser

✅ 登录成功，账号保活成功！


失败：

🌐 netlib.re 域名保活报告

🧑‍💻 正在登录账号：myuser

❌ 登录失败：Invalid credentials
