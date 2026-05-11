import os
from cerebras.cloud.sdk import Cerebras

client = Cerebras(
    # This is the default and can be omitted
    api_key="csk-jmy8hkcrmf8y6pp4ekwfjx2fj5m5pkee9cf22f6dew9xe9jy",  # 直接写在这里
)


chat_completion = client.chat.completions.create(
    messages=[
        {"role": "system", "content": "你是一个有帮助的助手"},
        {"role": "user", "content": "你好，请介绍一下自己"}
    ],
    model="qwen-3-235b-a22b-instruct-2507",  # 使用第一个模型
)

print(chat_completion.choices[0].message.content)
