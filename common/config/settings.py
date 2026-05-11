# config/settings.py
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent

class Config:
    #============UI==========
    # 浏览器配置
    HEADLESS = True
    SLOW_MO = 300

    # 视口配置
    VIEWPORT_WIDTH = 1920
    VIEWPORT_HEIGHT = 1080

    # 截图配置
    SCREENSHOT_ON_EACH_TEST = True  # 每个用例后是否截图
    # 登录配置
    AUTO_LOGIN = False
    DEFAULT_USERNAME = "00012A"
    DEFAULT_PASSWORD = "a222222"

    CI_URL = "https://3d-viewer.jlc.com/"
    PROD_URL = "https://3d-viewer.jlc.com/"
    TEST_URL = "https://test-3d-viewer.jlc.com/"
    ENV = None
    BASE_URL = "https://3d-viewer.jlc.com/"

    # 获取当前文件所在目录
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # 模型上传拼接路径（自动适配 Windows/Linux）
    TEST_MODEL_PATH = os.path.join(BASE_DIR, "files", "气垫.STEP")
    # 模型配置
    AUTO_NAVIGATE_TO_DESIGNER = False
    AUTO_UPLOAD_MODEL = True

    # 超时设置
    DEFAULT_TIMEOUT = 30000  # 30秒
    MODEL_LOAD_TIMEOUT = 60000  # 60秒
    UI_TIMEOUT= 60000
    # 截图设置
    SCREENSHOT_DIR = Path(__file__).parent.parent / "screenshots"

    LOG_DIR = Path(__file__).parent.parent / "logs"


    # 报告设置
    REPORT_DIR = Path(__file__).parent.parent / "reports"

    @classmethod
    def ensure_dirs(cls):
        """确保目录存在"""
        cls.SCREENSHOT_DIR.mkdir(exist_ok=True)
        cls.REPORT_DIR.mkdir(exist_ok=True)

    #================API=================
    API_BASE_URL="https://api.forface3d.com"
    APP_ID='E04FFD0F40B23A84E3282A89E26FEA4B'
    APP_SECRET='7624E8706D9E4FB380199F89F29F3EA4'
    TOKEN_URL='/forface/external/oauth/getAccessToken'

    # 是否自动获取 Token
    API_AUTO_LOGIN = os.getenv("API_AUTO_LOGIN", "True").lower() == "true"

    # API 超时时间
    API_TIMEOUT = 30
    API_MAX_RETRIES = 3
    # ========== Webhook 配置 ==========
    WEBHOOK_BASE_URL = os.getenv("WEBHOOK_BASE_URL", "http://47.94.122.228:5000")
    WEBHOOK_KEY = os.getenv("WEBHOOK_KEY", "AA95CEFE1C638B58E5F2B2D5F228545E")
    WEBHOOK_TIMEOUT = int(os.getenv("WEBHOOK_TIMEOUT", "180"))
    # ========== 文件路径 ==========

    # 测试文件目录
    TEST_FILES_DIR = Path(__file__).parent.parent.parent / "files"

    @classmethod
    def get_test_file_path(cls, filename: str) -> str:
        """获取测试文件路径"""
        return str(cls.TEST_FILES_DIR / filename)
# 环境配置
class TestConfig(Config):
    """测试环境配置"""
    HEADLESS = False
    SLOW_MO = 100  # 慢动作延迟(ms)


class CIConfig(Config):
    """CI环境配置"""
    HEADLESS = True
    SLOW_MO = 0


# config/settings.py 添加邮件配置

# ==================== 邮件配置 ====================
class EmailConfig:
    """邮件配置"""
    # SMTP 服务器配置（以QQ邮箱为例）
    SMTP_SERVER = "smtp.qq.com"
    SMTP_PORT = 465

    # 发件人配置
    # SENDER = "18065155454@163.com"
    # PASSWORD = "HCnBjvVp8c4H3vV5"  # 163邮箱使用授权码，不是密码
    SENDER = "168732019@qq.com"
    PASSWORD = "rmgfhyzltorycadg"  # QQ邮箱使用授权码，不是密码

    # 收件人列表
    RECIPIENTS = [
        "wangziyun@sz-jlc.com"    ]

    # 邮件主题前缀
    SUBJECT_PREFIX = "[自动化测试]"