"""auto_pipeline.config — 加载 api_config.json 和环境变量中的 API keys"""

import json
import os
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]  # E:\codex-token
_CONFIG_PATH = _REPO_ROOT / "secrets" / "api_config.json"


def load_config():
    """返回 api_config.json 的 dict"""
    with open(_CONFIG_PATH, encoding="utf-8") as f:
        return json.load(f)


def resolve_scripts_dir():
    """返回 ppt-master 脚本目录的绝对路径"""
    cfg = load_config()
    return str((_REPO_ROOT / cfg["pipeline"]["scripts_dir"]).resolve())


def resolve_project_dir():
    """返回 projects 目录的绝对路径"""
    cfg = load_config()
    return (_REPO_ROOT / cfg["pipeline"]["project_dir"]).resolve()


def get_strategist_config():
    cfg = load_config()["strategist"]
    key = os.environ.get(cfg["api_key_env"]) or os.environ.get("DEEPSEEK_API_KEY", "")
    return {
        "api_key": key,
        "model": cfg["model"],
        "endpoint": cfg["endpoint"],
    }


def get_executor_config():
    cfg = load_config()["executor"]
    key = os.environ.get(cfg["api_key_env"]) or os.environ.get("JOJOCODE_TEXT_KEY", "")
    return {
        "api_key": key,
        "model": cfg["model"],
        "fallback": cfg.get("model_fallback", ""),
        "endpoint": cfg["endpoint"],
    }


def get_image_gen_config():
    cfg = load_config()["image_gen"]
    key = os.environ.get(cfg["api_key_env"]) or os.environ.get("JOJOCODE_IMAGE_KEY", "")
    return {
        "api_key": key,
        "model": cfg["model"],
        "endpoint": cfg["endpoint"],
        "backend": cfg["env_config"]["IMAGE_BACKEND"],
        "base_url": cfg["env_config"].get("OPENAI_BASE_URL", cfg["endpoint"]),
        "env_config": cfg.get("env_config", {}),
    }
