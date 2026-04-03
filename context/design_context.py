# context/context.py
from playwright.sync_api import Page
from pages.base_page import BasePage
from methods.view_methods import ViewMethods
from methods.measure_methods import MeasurementMethods
from methods.toolbar_methods import ToolbarMethods
from methods.base_methods import BaseMethods
from config.settings import Config
from utils.logger import log
import time


class Context:
    """
    统一上下文
    职责：环境管理、登录、开关、数据
    """

    def __init__(self, page: Page):
        self.page = page
        self.base_page = BasePage(page)
        # 加载主页面定位器
        self.base_page.load_locators("main_page_locators.yaml")


        # 初始化基础方法（传入 self，让 BaseMethods 能访问 Context）
        self.base = BaseMethods(self)

        # 初始化业务方法（传入 self）
        self.view = ViewMethods(self)
        self.measure = MeasurementMethods(self)
        self.toolbar = ToolbarMethods(self)

        # 环境配置
        self.env = Config.ENV
        self.base_url = Config.BASE_URL

        # 登录状态
        self._is_logged_in = False

        # 模型加载状态
        self._model_loaded = False

    # ==================== 环境管理 ====================

    def set_env(self, env: str):
        """设置环境"""
        self.env = env
        if env == "test":
            self.base_url = Config.TEST_URL
        elif env == "prod":
            self.base_url = Config.PROD_URL
        elif env == "ci":
            self.base_url = Config.CI_URL
        return self

    def get_env(self) -> str:
        """获取当前环境"""
        return self.env

    # ==================== 登录管理 ====================

    def login(self, username: str = None, password: str = None):
        """登录"""
        if username is None:
            username = Config.DEFAULT_USERNAME
        if password is None:
            password = Config.DEFAULT_PASSWORD

        self.page.goto(f"{self.base_url}/login")
        self.base_page.fill(selector="input[name='username']", text=username)
        self.base_page.fill(selector="input[name='password']", text=password)
        self.base_page.click(selector="button[type='submit']")
        time.sleep(2)

        self._is_logged_in = True
        print(f"✅ 登录成功: {username}")
        return self

    def is_logged_in(self) -> bool:
        """检查是否已登录"""
        return self._is_logged_in

    def logout(self):
        """登出"""
        self.page.goto(f"{self.base_url}/logout")
        self._is_logged_in = False
        print("✅ 已登出")
        return self

    # ==================== 页面导航 ====================

    def navigate(self, url: str = None):
        """导航到页面"""
        if url is None:
            url = self.base_url
        self.page.goto(url)
        print(f"✅ 页面加载成功: {url}")
        return self

    def navigate_to_designer(self):
        """导航到设计器页面"""
        self.page.goto(f"{self.base_url}/designer")
        return self

    # ==================== 模型上传和加载（使用 base 方法） ====================

    def upload_model(self, file_path: str = None) -> bool:
        """上传模型"""
        if file_path is None:
            file_path = Config.TEST_MODEL_PATH

        try:
            # 使用 base_page 的定位器方法
            file_input = self.base_page.get_element('main_page', 'file_input')
            if file_input.count() > 0:
                file_input.set_input_files(file_path)
                log.info(f"✅ 模型上传成功: {file_path}")
                return True
            return False
        except Exception as e:
            log.error(f"❌ 模型上传失败: {e}")
            return False

    def wait_for_model_load(self, timeout: int = None) -> bool:
        """等待模型加载完成"""
        if timeout is None:
            timeout = Config.MODEL_LOAD_TIMEOUT

        try:
            # 1. 等待加载进度条消失
            loading = self.base_page.get_element('main_page', 'model_loading')
            if loading.count() > 0:
                loading.wait_for(state="detached", timeout=timeout)
                print("✅ 加载进度条消失")

            # 2. 切换到 iframe（使用 base 方法）
            self.base.switch_to_iframe()

            # 3. 等待 Canvas 出现（使用 base 方法）
            self.base.wait_for_canvas(timeout)
            log.info("✅ Canvas 可见，模型加载完成")

            self._model_loaded = True
            return True

        except Exception as e:
            log.error(f"❌ 模型加载超时: {e}")
            return False

    def is_model_loaded(self) -> bool:
        """检查模型是否已加载"""
        return self._model_loaded

    # ==================== 数据管理 ====================

    def set_test_data(self, key: str, value):
        """设置测试数据"""
        if not hasattr(self, '_test_data'):
            self._test_data = {}
        self._test_data[key] = value
        return self

    def get_test_data(self, key: str):
        """获取测试数据"""
        if hasattr(self, '_test_data'):
            return self._test_data.get(key)
        return None

    def clear_test_data(self):
        """清除测试数据"""
        if hasattr(self, '_test_data'):
            self._test_data = {}
        return self

    # ==================== 开关管理 ====================

    def set_feature_switch(self, feature: str, enabled: bool):
        """设置功能开关"""
        self.page.evaluate(f"""
            localStorage.setItem('feature_{feature}', '{enabled}');
        """)
        log.info(f"✅ 功能开关 {feature}: {enabled}")
        return self

    def get_feature_switch(self, feature: str) -> bool:
        """获取功能开关状态"""
        result = self.page.evaluate(f"""
            localStorage.getItem('feature_{feature}');
        """)
        return result == 'true'

    # ==================== 代理 BasePage 方法（便捷方法） ====================

    def click(self, *args, **kwargs):
        return self.base_page.click(*args, **kwargs)

    def fill(self, *args, **kwargs):
        return self.base_page.fill(*args, **kwargs)

    def get_text(self, *args, **kwargs):
        return self.base_page.get_text(*args, **kwargs)

    def screenshot(self, *args, **kwargs):
        return self.base_page.screenshot(*args, **kwargs)

    # ==================== 清理 ====================

    def cleanup(self):
        """清理环境"""
        self.base.switch_to_main()
        self.clear_test_data()
        log.info("✅ 环境清理完成")
        return self