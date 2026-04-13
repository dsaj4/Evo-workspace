from __future__ import annotations

import importlib.util
import shutil
from pathlib import Path

import pandas as pd


MODULE_PATH = Path(__file__).resolve().parents[1] / "workspace" / "preprocess_data.py"
SPEC = importlib.util.spec_from_file_location("thesis_preprocess", MODULE_PATH)
assert SPEC and SPEC.loader
preprocess_data = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(preprocess_data)


def test_parse_source_metadata_extracts_date_and_query() -> None:
    metadata = preprocess_data.parse_source_metadata(
        "search_comments_2026-04-12_AI编程"
    )

    assert metadata["source_date"] == "2026-04-12"
    assert metadata["source_query"] == "AI编程"


def test_parse_source_metadata_handles_plain_date_file() -> None:
    metadata = preprocess_data.parse_source_metadata("search_comments_2025-08-25")

    assert metadata["source_date"] == "2025-08-25"
    assert metadata["source_query"] == ""


def test_convert_timestamps_uses_publish_time_when_create_time_missing() -> None:
    df = pd.DataFrame(
        [
            {
                "platform": "zhihu",
                "publish_time": 1755530205,
                "source_date": "2025-08-01",
                "content": "测试评论",
            }
        ]
    )

    converted = preprocess_data.convert_timestamps(df)
    expected = (
        pd.to_datetime(pd.Series([1755530205]), unit="s", utc=True)
        .dt.tz_convert("Asia/Shanghai")
        .dt.tz_localize(None)
        .iloc[0]
    )

    assert converted.loc[0, "timestamp"] == expected
    assert converted.loc[0, "source_date_parsed"] == pd.Timestamp("2025-08-01")
    assert converted.loc[0, "date"] == expected.date()


def test_load_all_data_includes_weibo(monkeypatch) -> None:
    called_platforms: list[str] = []

    def fake_load_platform_data(platform: str) -> pd.DataFrame:
        called_platforms.append(platform)
        return pd.DataFrame([{"platform": platform, "content": "x"}])

    monkeypatch.setattr(preprocess_data, "load_platform_data", fake_load_platform_data)

    combined = preprocess_data.load_all_data()

    assert set(called_platforms) == {"bili", "zhihu", "weibo", "xhs"}
    assert set(combined["platform"]) == {"bili", "zhihu", "weibo", "xhs"}


def test_save_daily_data_falls_back_to_csv_when_parquet_engine_missing(monkeypatch) -> None:
    daily_df = pd.DataFrame([{"date": pd.Timestamp("2026-04-13"), "value": 1}])
    output_dir = MODULE_PATH.resolve().parents[1] / "workspace" / "_pytest_tmp_save_daily"
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    def fake_to_parquet(self, path, index=False):  # noqa: ARG001
        raise ImportError("missing parquet engine")

    monkeypatch.setattr(pd.DataFrame, "to_parquet", fake_to_parquet)

    saved_path = preprocess_data.save_daily_data(daily_df, output_dir)

    assert saved_path.suffix == ".csv"
    assert saved_path.exists()
