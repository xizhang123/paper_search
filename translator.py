import requests
from typing import Optional

class RWKVTranslator:
    def __init__(self, api_base: str = "http://127.0.0.1:8000"):
        """初始化翻译器

        Args:
            api_base (str): API服务器地址
        """
        self.api_base = api_base.rstrip("/")
        self.default_params = {
            "max_tokens": 1000,
            "temperature": 1.0,
            "top_p": 0.3,
            "presence_penalty": 0,
            "frequency_penalty": 1,
            "decay": 0.996,
            "stream": False,
            "stop": "\n\n"
        }
        self.service_offline_msg = "翻译服务不在线，请运行RWKV并保证启动合适的模型，但注意，如果查询结果中存在具有CCF等级的文章，每篇摘要将花费数分钟，并且只在结束时写入文件！"

    def check_service(self) -> bool:
        """检查翻译服务是否在线

        Returns:
            bool: 服务是否在线
        """
        try:
            response = requests.get(f"{self.api_base}")
            return response.status_code == 200
        except:
            return False

    def _make_request(self, prompt: str) -> Optional[str]:
        try:
            response = requests.post(
                f"{self.api_base}/completions",
                json={"prompt": prompt, **(self.default_params)},
            )
            response.raise_for_status()
            full_text = response.json()['choices'][0]['text']
            return full_text.strip()
        except Exception as e:
            print(f"API request error: {str(e)}")
            return None

    def translate_to_chinese(self, text: str) -> str:
        if not self.check_service():
            return self.service_offline_msg
        prompt = f"Translate this into Chinese.\n\nEnglish:{text}\n\nChinese:"
        result = self._make_request(prompt)
        return result if result is not None else self.service_offline_msg

    def translate_to_english(self, text: str) -> str:
        if not self.check_service():
            return self.service_offline_msg
        prompt = f"Translate this into English.\n\nChinese:{text}\n\nEnglish:"
        result = self._make_request(prompt)
        return result if result is not None else self.service_offline_msg

translator = RWKVTranslator()

def translate_zh_en(q: str) -> Optional[str]:
    """将中文翻译为英文"""
    return translator.translate_to_english(q)

def translate_en_zh(q: str) -> Optional[str]:
    """将英文翻译为中文"""
    return translator.translate_to_chinese(q)