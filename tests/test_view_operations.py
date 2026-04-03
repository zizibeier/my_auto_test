# tests/test_view_operations.py
import allure
from tests.base_test import BaseTest


@allure.feature("视图操作")
class TestViewOperations(BaseTest):
    """视图操作测试"""

    @allure.story("旋转视图")
    def test_rotate_view(self):
        """测试旋转视图"""
        self.log_info("开始测试旋转视图")

        result = self.ctx.view.rotate(100, 50)

        self.assert_true(result, "旋转操作失败")
        self.take_screenshot("旋转后视图")
        self.log_info("旋转测试通过")

    @allure.story("缩放视图")
    def test_zoom_view(self):
        """测试缩放视图"""
        self.log_info("开始测试缩放视图")


        result = self.ctx.view.zoom(200)

        self.assert_true(result, "缩放操作失败")
        self.take_screenshot("缩放后视图")
        self.log_info("缩放测试通过")

    @allure.story("平移视图")
    def test_pan_view(self):
        """测试平移视图"""
        self.log_info("开始测试平移视图")

        result = self.ctx.view.pan(100, 100)

        self.assert_true(result, "平移操作失败")
        self.take_screenshot("平移后视图")
        self.log_info("平移测试通过")

    @allure.story("重置视图")
    def test_reset_view(self):
        """测试重置视图"""
        self.log_info("开始测试重置视图")

        # 先旋转
        self.ctx.view.rotate(100, 50)
        self.wait(0.5)

        # 再重置
        result = self.ctx.view.reset()

        self.assert_true(result, "重置操作失败")
        self.take_screenshot("重置后视图")
        self.log_info("重置测试通过")

    @allure.story("连续操作")
    def test_continuous_operations(self):
        """测试连续操作"""
        self.log_info("开始测试连续操作")

        operations = [
            ("旋转", lambda: self.ctx.view.rotate(50, 30)),
            ("放大", lambda: self.ctx.view.zoom(100)),
            ("平移", lambda: self.ctx.view.pan(50, 50)),
            ("缩小", lambda: self.ctx.view.zoom(-100)),
            ("回到原点", lambda: self.ctx.view.reset()),
        ]

        for op_name, op_func in operations:
            with allure.step(f"执行{op_name}操作"):
                result = op_func()
                self.assert_true(result, f"{op_name}操作失败")
                self.wait(0.3)

        self.take_screenshot("连续操作最终视图")
        self.log_info("连续操作测试通过")

    def wait(self, seconds: float = 0.5):
        """等待"""
        import time
        time.sleep(seconds)


import pytest
import os
import sys

if __name__ == '__main__':
    # 1. 运行测试，生成 allure 原始数据
    exit_code = pytest.main([
        __file__,
        "-v",
        "-s",
        "--alluredir=allure-results",
        "--clean-alluredir"
    ])

    # ============================
    # 2. 关键：用 Python 自带方式生成 HTML 报告（不会报错！）
    # ============================
    try:
        print("\n正在生成 Allure 报告...")
        os.system("cmd /c allure generate allure-results -o allure-report --clean")

        print("✅ 报告生成成功：allure-report/index.html")
    except Exception as e:
        print("⚠️ 报告生成失败，但测试已完成")