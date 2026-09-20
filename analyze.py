import os
import requests

API_KEY = os.getenv("OPENCODE_API_KEY")
MODEL = os.getenv("OPENCODE_MODEL", "GLM-5.3-Flash")
URL = "https://openrouter.ai/api/v1/chat/completions"

if not API_KEY:
    print("❌ 错误：环境变量中缺少 OPENCODE_API_KEY！")
    exit(1)

# 读取 mingshi.txt 并截取前 2000 字符
try:
    with open("mingshi.txt", "r", encoding="utf-8") as f:
        text_data = f.read()[:2000]
except FileNotFoundError:
    print("❌ 错误：未找到 mingshi.txt 文件！")
    exit(1)

prompt = f"""
分析以下《明史》文本：
1. 提取高频词。
2. 提取主要人物/奸臣名字及官职。
3. 给出简短结论。

文本：
{text_data}

直接输出一份简洁美观的 HTML 代码（含基础 CSS 样式）。
要求：只输出原生 HTML 代码，严禁使用 ```html 包装。
"""

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "model": MODEL,
    "messages": [{"role": "user", "content": prompt}]
}

print("正在发送请求给模型，请稍候...")

try:
    response = requests.post(URL, json=payload, headers=headers, timeout=30)
    
    if response.status_code == 200:
        html_code = response.json()['choices'][0]['message']['content']
        html_code = html_code.replace("```html", "").replace("```", "").strip()
        
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html_code)
            
        print("✅ 成功！已成功生成 index.html 文件。")
    else:
        print(f"❌ 失败 (状态码 {response.status_code}):", response.text)

except Exception as e:
    print(f"❌ 发生错误:", e)