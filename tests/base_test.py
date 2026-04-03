# tests/base_test.py
import pytest
import allure
import time
import logging
from typing import Optional, Any, Callable
from allure_commons.types import AttachmentType
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext

from context.design_context import Context
from config.settings import Config
from utils.logger import log

class BaseTest:
    """
    测试基类
    职责：统一管理测试生命周期、环境、日志、截图
    """

    # 类级别变量，整个测试会话共享
    _browser: Optional[Browser] = None
    _context: Optional[BrowserContext] = None
    _playwright = None

    @classmethod
    def setup_class(cls):
        """测试类级别前置 - 只执行一次"""
        log.section("测试会话开始")
        cls._init_browser()
        cls._init_context()


    @classmethod
    def teardown_class(cls):
        """测试类级别后置 - 只执行一次"""
        log.section("测试会话结束")
        cls._close_browser()
        cls._cleanup_context()



    def setup_method(self):
        """每个测试方法前置 - 每个用例执行前"""
        self._init_test_data()
        self._start_time = time.time()
        log.info(f"开始测试: {self._get_test_name()}")

    def teardown_method(self):
        """每个测试方法后置 - 每个用例执行后"""
        self._record_test_result()
        log.info(f"结束测试: {self._get_test_name()}, 耗时: {self._get_test_duration()}ms")

    # ==================== 私有方法 ====================


    @classmethod
    def _init_browser(cls):
        """初始化浏览器（类级别）"""
        cls._playwright = sync_playwright().start()
        cls._browser = cls._playwright.chromium.launch(
            headless=Config.HEADLESS,
            slow_mo=Config.SLOW_MO,
            args=[
                '--start-maximized',  # 启动时最大化
                '--kiosk',  # 全屏模式（按F11的效果）
                '--disable-infobars'  # 禁用信息栏
            ]
        )
        log.info("✅ 浏览器启动成功")

    @classmethod
    def _close_browser(cls):
        """关闭浏览器（类级别）"""
        if cls._browser:
            cls._browser.close()
        if cls._playwright:
            cls._playwright.stop()
        log.info("✅ 浏览器已关闭")

    @classmethod
    def _init_context(cls):
        """初始化测试上下文（方法级别）"""
        # 创建新的浏览器上下文
        cls._context = cls._browser.new_context(
            no_viewport=True  # 不设置固定视口，使用系统窗口大小

            # viewport={'width': Config.VIEWPORT_WIDTH, 'height': Config.VIEWPORT_HEIGHT}
        )
        cls.page = cls._context.new_page()

        # 初始化 Context（统一上下文）
        cls.ctx = Context(cls.page)

        cls.ctx.navigate()

        # 自动登录（如果配置了）
        if Config.AUTO_LOGIN:
            cls.ctx.login()

        # 自动导航到设计器（如果配置了）
        if Config.AUTO_NAVIGATE_TO_DESIGNER:
            cls.ctx.navigate_to_designer()

        # 自动上传模型（如果配置了）
        if Config.AUTO_UPLOAD_MODEL:
            cls.ctx.upload_model()
            cls.ctx.wait_for_model_load()

        log.info("✅ 测试上下文初始化完成")

    @classmethod
    def _cleanup_context(cls):
        """清理测试上下文（方法级别）"""
        if hasattr(cls, 'ctx'):
            cls.ctx.cleanup()
        if hasattr(cls, '_context'):
            cls._context.close()
        log.info("✅ 测试上下文已清理")

    def _init_test_data(self):
        """初始化测试数据"""
        self.test_data = {}
        self.test_errors = []
        self.test_warnings = []

    def _get_test_name(self) -> str:
        """获取当前测试名称"""
        return getattr(self, '_testMethodName', 'unknown')

    def _get_test_duration(self) -> float:
        """获取测试耗时（毫秒）"""
        if hasattr(self, '_start_time'):
            return (time.time() - self._start_time) * 1000
        return 0

    def _record_test_result(self):
        """记录测试结果"""
        duration = self._get_test_duration()

        # 附加性能数据到 Allure
        allure.attach(
            f"测试耗时: {duration:.2f}ms",
            name="测试性能",
            attachment_type=AttachmentType.TEXT
        )

        # 如果有错误，附加到 Allure
        if self.test_errors:
            allure.attach(
                "\n".join(self.test_errors),
                name="测试错误",
                attachment_type=AttachmentType.TEXT
            )

    # ==================== 公共方法 ====================

    def log_info(self, message: str):
        """记录信息"""
        log.info(message)

    def log_success(self, message: str):
        """记录成功"""
        log.success(message)

    def log_error(self, message: str):
        """记录错误"""
        log.error(message)

    def log_warning(self, message: str):
        """记录警告"""
        log.warning(message)

    def log_step(self, message: str):
        """记录步骤"""
        log.step(message)

    def take_screenshot(self, name: str = "screenshot"):
        """截图"""
        screenshot = self.page.screenshot()
        log.attach_screenshot(screenshot, name)
        return screenshot

    def assert_true(self, condition: bool, message: str = "断言失败"):
        """断言为真"""
        if not condition:
            self.take_screenshot("断言失败截图")
            log.error(message)
        assert condition, message

    def wait(self, seconds: float = 0.5):
        time.sleep(seconds)

    def take_canvas_screenshot(self, name: str = "canvas_screenshot"):
        """截取 Canvas 截图"""
        try:
            canvas = self.ctx.base.get_canvas()
            screenshot = canvas.screenshot()
            allure.attach(screenshot, name=name, attachment_type=AttachmentType.PNG)
            return screenshot
        except Exception as e:
            self.log_error(f"Canvas 截图失败: {e}")
            return None




    def assert_false(self, condition: bool, message: str = "断言失败"):
        """断言为假"""
        self.assert_true(not condition, message)

    def assert_equal(self, actual: Any, expected: Any, message: str = "值不相等"):
        """断言相等"""
        self.assert_true(
            actual == expected,
            f"{message}: 期望 '{expected}', 实际 '{actual}'"
        )

    def assert_not_none(self, value: Any, message: str = "值不应为None"):
        """断言不为None"""
        self.assert_true(value is not None, message)

    def assert_in(self, item: Any, container: list, message: str = "元素不在列表中"):
        """断言元素在列表中"""
        self.assert_true(item in container, f"{message}: '{item}' 不在 {container}")

    # ==================== 性能监控 ====================

    def measure_time(self, func: Callable, *args, **kwargs) -> tuple:
        """测量函数执行时间"""
        start = time.time()
        result = func(*args, **kwargs)
        duration = (time.time() - start) * 1000
        return result, duration

    def assert_performance(self, duration: float, threshold: float = 500):
        """断言性能在阈值内（毫秒）"""
        self.assert_true(
            duration <= threshold,
            f"操作耗时 {duration:.2f}ms 超过阈值 {threshold}ms"
        )
        allure.attach(
            f"操作耗时: {duration:.2f}ms (阈值: {threshold}ms)",
            name="性能数据",
            attachment_type=AttachmentType.TEXT
        )

    # ==================== 数据驱动 ====================

    def set_test_data(self, key: str, value: Any):
        """设置测试数据"""
        self.test_data[key] = value

    def get_test_data(self, key: str) -> Any:
        """获取测试数据"""
        return self.test_data.get(key)

    def clear_test_data(self):
        """清除测试数据"""
        self.test_data.clear()

    # ==================== 重试机制 ====================

    def retry(self, func: Callable, max_retries: int = 3, delay: float = 1) -> bool:
        """重试函数"""
        for attempt in range(max_retries):
            try:
                result = func()
                if result:
                    return True
            except Exception as e:
                self.log_warning(f"第 {attempt + 1} 次尝试失败: {e}")
                time.sleep(delay)
        return False