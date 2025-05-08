from flask import Flask, request, abort
from linebot.v3.webhook import WebhookHandler
from linebot.v3.messaging import MessagingApi, Configuration, ApiClient
from linebot.v3.messaging.models import ReplyMessageRequest, TextMessage
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from linebot.v3.exceptions import InvalidSignatureError

app = Flask(__name__)

# 你的 LINE Channel 資訊
CHANNEL_ACCESS_TOKEN = 'jRb7/Ub298W/nl5G1H8rPF05XC0y6jcDz2huGnFIF3OOLlJuLdrZYkaz8oFNKHaSnNlmyLHgZis3o8oMN3s01c0ynilUBdRSaj7qLhSnXtfDcFtSUmXihD9ax4+yiy9oH3llgz2nIhu692YsytVY2QdB04t89/1O/w1cDnyilFU='
CHANNEL_SECRET = 'f74e26c1beb627f80c90d9ccfce51672'

configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# 表單對應連結（請換成你實際的 Google 表單網址）
FORMS = {
    "手機維修": "https://docs.google.com/forms/d/e/1FAIpQLSf_phone_form_link",
    "電腦維修": "https://docs.google.com/forms/d/e/1FAIpQLSf_computer_form_link",
    "手機解鎖": "https://docs.google.com/forms/d/e/1FAIpQLSf_unlock_form_link"
}

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature')
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    user_text = event.message.text.strip()
    response_text = ""

    for keyword, link in FORMS.items():
        if keyword in user_text:
            # 這裡生成超連結並讓用戶點擊
            response_text = f"📋 請點選下方連結填寫「{keyword}」報修單：\n👉 {link}"
            break

    if not response_text:
        response_text = (
            "歡迎使用007電腦手機工作室報修系統，請輸入以下任一關鍵字開始：\n"
            "📱 手機維修\n💻 電腦維修\n🔓 手機解鎖"
        )

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=response_text)]
            )
        )

if __name__ == "__main__":
    app.run(debug=True)

