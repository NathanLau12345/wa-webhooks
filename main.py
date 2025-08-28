from flask import Flask, request, jsonify
import hmac
import hashlib

app = Flask(__name__)

# 這必須是一個隨機、複雜且保密的字串！
# 實務上應該從環境變數讀取，不要直接寫在程式碼裡。
WEBHOOK_SECRET = "your_webhook_secret_here" 

def verify_signature(payload_body, signature_header):
    """
    驗證簽名是否合法
    payload_body: 原始的請求體資料 (request.data)
    signature_header: 請求頭中的簽名 (request.headers.get('X-Hub-Signature-256'))
    """
    if not signature_header:
        return False
    
    # 計算期望的簽名
    # 使用你的 SECRET 和收到的資料來計算 HMAC SHA256
    expected_signature = hmac.new(
        key=WEBHOOK_SECRET.encode('utf-8'),
        msg=payload_body,
        digestmod=hashlib.sha256
    ).hexdigest()

    # 通常 Header 的格式會像 "sha256=abc123..."，我們需要取出後面的部分
    # 安全地比較兩個簽名是否相同
    return hmac.compare_digest(f"sha256={expected_signature}", signature_header)

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    # 取得原始的請求資料和簽名 Header
    payload_body = request.data
    signature_header = request.headers.get('X-Hub-Signature-256')

    # 驗證簽名
    if not verify_signature(payload_body, signature_header):
        # 簽名驗證失敗，記錄日誌並返回錯誤
        app.logger.error("Webhook 簽名驗證失敗！可能是非法請求。")
        return jsonify({"error": "Invalid signature"}), 401

    # 簽名驗證成功，安全地處理資料
    data = request.json
    app.logger.info(f"收到合法的 Webhook 事件: {data}")

    # ... 這裡是你的業務邏輯 ...

    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(debug=True)
