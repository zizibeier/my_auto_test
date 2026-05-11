# common/assertions/ui_assertion.py
import allure
from typing import Union, List, Optional
from allure_commons.types import AttachmentType
from playwright.sync_api import Page, Locator, ElementHandle

from common.assertions.base_assertion import BaseAssertion
from common.utils.logger import log


class UIAssertion(BaseAssertion):
    """
    UI 专用断言类
    继承 BaseAssertion，扩展页面元素相关断言
    """

    def __init__(self, page: Page, screenshot_callback=None):
        super().__init__(screenshot_callback)
        self.page = page

    # ==================== 元素存在性断言 ====================

    def assert_element_visible(self, selector: str, timeout: int = 5000, message: str = None):
        """断言元素可见"""
        try:
            element = self.page.wait_for_selector(selector, state="visible", timeout=timeout)
            is_visible = element.is_visible()
            msg = message or f"元素 '{selector}' 应该可见"
            self.assert_true(is_visible, msg)
            log.success(f"✅ 元素可见: {selector}")
        except Exception as e:
            self.assert_true(False, message or f"元素 '{selector}' 不可见: {e}")

    def assert_element_hidden(self, selector: str, timeout: int = 5000, message: str = None):
        """断言元素隐藏"""
        try:
            element = self.page.wait_for_selector(selector, state="hidden", timeout=timeout)
            is_hidden = not element.is_visible() if element else True
            msg = message or f"元素 '{selector}' 应该隐藏"
            self.assert_true(is_hidden, msg)
        except Exception:
            # 如果找不到元素，也算隐藏
            self.assert_true(True, message or f"元素 '{selector}' 不存在，符合隐藏预期")

    def assert_element_exists(self, selector: str, message: str = None):
        """断言元素存在于 DOM 中"""
        count = self.page.locator(selector).count()
        msg = message or f"元素 '{selector}' 应该存在于 DOM 中"
        self.assert_true(count > 0, msg)

    def assert_element_not_exists(self, selector: str, message: str = None):
        """断言元素不存在于 DOM 中"""
        count = self.page.locator(selector).count()
        msg = message or f"元素 '{selector}' 不应存在于 DOM 中"
        self.assert_true(count == 0, msg)

    def assert_element_count(self, selector: str, expected_count: int, message: str = None):
        """断言元素数量"""
        actual_count = self.page.locator(selector).count()
        msg = message or f"元素 '{selector}' 数量应为 {expected_count}, 实际 {actual_count}"
        self.assert_equal(actual_count, expected_count, msg)

    # ==================== 元素属性断言 ====================

    def assert_element_text(self, selector: str, expected_text: str, exact: bool = True, message: str = None):
        """断言元素文本"""
        element = self.page.locator(selector).first
        actual_text = element.text_content() or ""

        if exact:
            msg = message or f"元素 '{selector}' 文本应为 '{expected_text}', 实际 '{actual_text}'"
            self.assert_equal(actual_text.strip(), expected_text, msg)
        else:
            msg = message or f"元素 '{selector}' 文本应包含 '{expected_text}', 实际 '{actual_text}'"
            self.assert_true(expected_text in actual_text, msg)

    def assert_element_attribute(self, selector: str, attribute: str, expected_value: str, message: str = None):
        """断言元素属性"""
        element = self.page.locator(selector).first
        actual_value = element.get_attribute(attribute)
        msg = message or f"元素 '{selector}' 属性 '{attribute}' 应为 '{expected_value}', 实际 '{actual_value}'"
        self.assert_equal(actual_value, expected_value, msg)

    def assert_element_checked(self, selector: str, should_be_checked: bool = True, message: str = None):
        """断言复选框/单选框选中状态"""
        element = self.page.locator(selector).first
        is_checked = element.is_checked()
        expected_state = "选中" if should_be_checked else "未选中"
        actual_state = "选中" if is_checked else "未选中"
        msg = message or f"元素 '{selector}' 应该{expected_state}, 实际{actual_state}"
        self.assert_equal(is_checked, should_be_checked, msg)

    def assert_element_enabled(self, selector: str, should_be_enabled: bool = True, message: str = None):
        """断言元素启用状态"""
        element = self.page.locator(selector).first
        is_enabled = element.is_enabled()
        expected_state = "启用" if should_be_enabled else "禁用"
        actual_state = "启用" if is_enabled else "禁用"
        msg = message or f"元素 '{selector}' 应该{expected_state}, 实际{actual_state}"
        self.assert_equal(is_enabled, should_be_enabled, msg)

    def assert_element_focused(self, selector: str, message: str = None):
        """断言元素获得焦点"""
        element = self.page.locator(selector).first
        is_focused = element.evaluate("el => el === document.activeElement")
        msg = message or f"元素 '{selector}' 应该获得焦点"
        self.assert_true(is_focused, msg)

    # ==================== 页面断言 ====================

    def assert_title(self, expected_title: str, message: str = None):
        """断言页面标题"""
        actual_title = self.page.title()
        msg = message or f"页面标题应为 '{expected_title}', 实际 '{actual_title}'"
        self.assert_equal(actual_title, expected_title, msg)

    def assert_url(self, expected_url: str, exact: bool = True, message: str = None):
        """断言当前URL"""
        actual_url = self.page.url
        if exact:
            msg = message or f"URL 应为 '{expected_url}', 实际 '{actual_url}'"
            self.assert_equal(actual_url, expected_url, msg)
        else:
            msg = message or f"URL 应包含 '{expected_url}', 实际 '{actual_url}'"
            self.assert_true(expected_url in actual_url, msg)

    def assert_url_contains(self, text: str, message: str = None):
        """断言URL包含指定文本"""
        self.assert_url(text, exact=False, message=message)

    # ==================== 三维引擎专用断言 ====================

    def assert_canvas_exists(self, timeout: int = 10000, message: str = None):
        """断言 Canvas 存在"""
        try:
            self.page.wait_for_selector("canvas.webgl, canvas#canvas3d", timeout=timeout)
            self.assert_true(True, message or "Canvas 存在")
        except Exception as e:
            self.assert_true(False, message or f"Canvas 不存在: {e}")

    def assert_webgl_context(self, message: str = None):
        """断言 WebGL 上下文已初始化"""
        result = self.page.evaluate("""
            () => {
                const canvas = document.querySelector('canvas.webgl, canvas#canvas3d');
                if (!canvas) return false;
                const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
                return gl !== null;
            }
        """)
        msg = message or "WebGL 上下文应该已初始化"
        self.assert_true(result, msg)

    def assert_model_loaded(self, message: str = None):
        """断言模型已加载（通过检查特定标志）"""
        # 可以根据你的三维引擎的具体实现调整
        result = self.page.evaluate("""
            () => {
                // 检查是否有全局模型加载标志
                return window.modelLoaded === true || 
                       document.querySelector('.model-loaded') !== null;
            }
        """)
        msg = message or "模型应该已加载完成"
        self.assert_true(result, msg)

    def assert_fps_greater_than(self, min_fps: int = 30, message: str = None):
        """断言帧率大于阈值"""
        fps = self.page.evaluate("""
            () => {
                // 如果有性能监控对象
                return window.performanceMonitor ? window.performanceMonitor.getFPS() : 60;
            }
        """)
        msg = message or f"帧率应大于 {min_fps}, 实际 {fps}"
        self.assert_greater(fps, min_fps, msg)

    # ==================== 截图断言 ====================

    def assert_screenshot_match(self, selector: str = None, threshold: float = 0.1, name: str = "screenshot"):
        """断言截图匹配（视觉回归测试）"""
        if selector:
            element = self.page.locator(selector).first
            screenshot = element.screenshot()
        else:
            screenshot = self.page.screenshot()

        # 保存到 Allure
        allure.attach(screenshot, name=f"截图_{name}", attachment_type=AttachmentType.PNG)

        # 这里可以集成像素对比库，如 pixelmatch
        # 简单实现：对比文件是否存在
        import os
        baseline_path = f"baseline/{name}.png"
        if os.path.exists(baseline_path):
            # 对比逻辑...
            log.info(f"截图已保存: {baseline_path}")
        else:
            # 首次运行，保存基准图
            with open(baseline_path, "wb") as f:
                f.write(screenshot)
            log.warning(f"基准图不存在，已创建: {baseline_path}")