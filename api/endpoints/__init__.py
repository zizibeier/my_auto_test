# api/endpoints/__init__.py
"""
Endpoints 模块
统一导出所有接口类
"""

from api.endpoints.analysis_endpoints import AnalysisEndpoints

__all__ = [
    "AnalysisEndpoints"
    ]
