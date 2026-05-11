# common/assertions/base_assertion.py
import allure
from typing import Any, Callable, Optional, List
from allure_commons.types import AttachmentType
from common.utils.logger import log


class BaseAssertion:
    """
    基础断言类
    职责：提供通用断言方法，支持 Allure 报告
    """

    def __init__(self, screenshot_callback: Optional[Callable] = None):
        """
        初始化断言器
        :param screenshot_callback: 失败时回调函数（用于截图）
        """
        self.screenshot_callback = screenshot_callback
        self._errors: List[str] = []  # 软断言错误收集

    # ==================== 硬断言 ====================

    def assert_true(self, condition: bool, message: str = "断言失败"):
        """断言为真"""
        if not condition:
            self._on_fail(message)
            raise AssertionError(message)
        log.success(f"✅ 断言通过: {message}")

    def assert_false(self, condition: bool, message: str = "断言失败"):
        """断言为假"""
        self.assert_true(not condition, message)

    def assert_equal(self, actual: Any, expected: Any, message: str = None):
        """断言相等"""
        msg = message or f"期望 '{expected}', 实际 '{actual}'"
        self.assert_true(actual == expected, msg)

    def assert_not_equal(self, actual: Any, expected: Any, message: str = None):
        """断言不相等"""
        msg = message or f"值不应等于 '{expected}'"
        self.assert_true(actual != expected, msg)

    def assert_is_none(self, value: Any, message: str = "值应为None"):
        """断言为None"""
        self.assert_true(value is None, message)

    def assert_is_not_none(self, value: Any, message: str = "值不应为None"):
        """断言不为None"""
        self.assert_true(value is not None, message)

    def assert_in(self, item: Any, container: list, message: str = None):
        """断言元素在列表中"""
        msg = message or f"'{item}' 不在 {container} 中"
        self.assert_true(item in container, msg)

    def assert_not_in(self, item: Any, container: list, message: str = None):
        """断言元素不在列表中"""
        msg = message or f"'{item}' 在 {container} 中"
        self.assert_true(item not in container, msg)

    def assert_is_instance(self, obj: Any, expected_type: type, message: str = None):
        """断言对象类型"""
        msg = message or f"类型应为 {expected_type}, 实际 {type(obj)}"
        self.assert_true(isinstance(obj, expected_type), msg)

    def assert_greater(self, value: Any, threshold: Any, message: str = None):
        """断言大于"""
        msg = message or f"{value} 应大于 {threshold}"
        self.assert_true(value > threshold, msg)

    def assert_less(self, value: Any, threshold: Any, message: str = None):
        """断言小于"""
        msg = message or f"{value} 应小于 {threshold}"
        self.assert_true(value < threshold, msg)

    def assert_between(self, value: Any, min_val: Any, max_val: Any, message: str = None):
        """断言在区间内"""
        msg = message or f"{value} 应在 [{min_val}, {max_val}] 之间"
        self.assert_true(min_val <= value <= max_val, msg)

    def assert_contains(self, text: str, substring: str, message: str = None):
        """断言字符串包含子串"""
        msg = message or f"'{text}' 应包含 '{substring}'"
        self.assert_true(substring in text, msg)

    def assert_starts_with(self, text: str, prefix: str, message: str = None):
        """断言字符串以...开头"""
        msg = message or f"'{text}' 应以 '{prefix}' 开头"
        self.assert_true(text.startswith(prefix), msg)

    def assert_ends_with(self, text: str, suffix: str, message: str = None):
        """断言字符串以...结尾"""
        msg = message or f"'{text}' 应以 '{suffix}' 结尾"
        self.assert_true(text.endswith(suffix), msg)

    def assert_regex_match(self, text: str, pattern: str, message: str = None):
        """断言正则匹配"""
        import re
        msg = message or f"'{text}' 不匹配正则 '{pattern}'"
        self.assert_true(re.match(pattern, text) is not None, msg)

    # ==================== 软断言 ====================

    def soft_assert_true(self, condition: bool, message: str = "断言失败"):
        """软断言 - 失败不中断，继续执行"""
        if not condition:
            self._errors.append(message)
            self._on_fail(message, is_soft=True)
        else:
            log.success(f"✅ 软断言通过: {message}")

    def soft_assert_equal(self, actual: Any, expected: Any, message: str = None):
        """软断言相等"""
        msg = message or f"期望 '{expected}', 实际 '{actual}'"
        self.soft_assert_true(actual == expected, msg)

    def assert_all(self):
        """断言所有软断言都通过"""
        if self._errors:
            error_msg = f"软断言失败 ({len(self._errors)} 个错误):\n" + "\n".join(self._errors)
            self._errors.clear()
            raise AssertionError(error_msg)

    def clear_soft_assertions(self):
        """清空软断言错误"""
        self._errors.clear()

    # ==================== 私有方法 ====================

    def _on_fail(self, message: str, is_soft: bool = False):
        """断言失败时的处理"""
        # 记录日志
        log.error(f"❌ 断言失败: {message}")

        # 附加到 Allure
        allure.attach(
            message,
            name=f"断言失败 - {message[:50]}",
            attachment_type=AttachmentType.TEXT
        )

        # 调用截图回调
        if self.screenshot_callback and not is_soft:
            try:
                self.screenshot_callback()
            except Exception as e:
                log.error(f"截图回调失败: {e}")