# config/settings.py
import os
from pathlib import Path


class Config:
    # 浏览器配置
    HEADLESS = True
    SLOW_MO = 300

    # 视口配置
    VIEWPORT_WIDTH = 1920
    VIEWPORT_HEIGHT = 1080

    # 截图配置
    SCREENSHOT_ON_EACH_TEST = False  # 每个用例后是否截图
    # 登录配置
    AUTO_LOGIN = False
    DEFAULT_USERNAME = "00012A"
    DEFAULT_PASSWORD = "a222222"

    CI_URL = "https://3d-viewer.jlc.com/"
    PROD_URL = "https://3d-viewer.jlc.com/"
    TEST_URL = "https://3d-viewer.jlc.com/"
    ENV = None
    BASE_URL = "https://3d-viewer.jlc.com/"

    # 测试数据
    TEST_MODEL_PATH = r"D:\三维\建模模型\方程式测试模型\BJSU (1).SLDASM"
    # 模型配置
    AUTO_NAVIGATE_TO_DESIGNER = False
    AUTO_UPLOAD_MODEL = True

    # 超时设置
    DEFAULT_TIMEOUT = 30000  # 30秒
    MODEL_LOAD_TIMEOUT = 60000  # 60秒

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