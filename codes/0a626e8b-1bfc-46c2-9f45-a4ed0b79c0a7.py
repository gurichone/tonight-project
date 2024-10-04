
import google.generativeai as genai



# Google Generative AI（Gemini API）のAPIキー設定
genai.configure(api_key="AIzaSyAx46slXSnBOfnkCFK3MlKNnmoDuziwrpU")
# Geminiモデルの設定
model = genai.GenerativeModel('gemini-pro')
# セッション状態にメッセージリストがない場合は初期化
prompt = input("Your message:")
response = model.generate_content(prompt)
# 応答をテキストとして取得（ここではresponse.textと仮定）
assistant_response = response.text
print(f"Assistant: {assistant_response}")
