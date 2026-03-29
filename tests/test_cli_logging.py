"""Tests for CLI logging behavior."""

import io
import logging

from EvoScientist.cli import commands


class _FakeStderr(io.StringIO):
    encoding = "gbk"


def test_warning_handler_avoids_rich_on_non_utf_console(monkeypatch):
    """Warnings should bypass Rich entirely if the console can't encode the symbol."""
    root_logger = logging.getLogger()
    old_handlers = root_logger.handlers[:]
    old_level = root_logger.level

    try:
        commands._configure_logging()
        handler = root_logger.handlers[0]

        stderr = _FakeStderr()
        calls = []

        def fake_print(message, *args, **kwargs):
            calls.append(message)

        monkeypatch.setattr(commands.console, "print", fake_print)
        monkeypatch.setattr(commands.sys, "stderr", stderr)

        record = logging.LogRecord(
            name="test",
            level=logging.WARNING,
            pathname=__file__,
            lineno=1,
            msg="hello",
            args=(),
            exc_info=None,
        )

        handler.emit(record)

        assert calls == []
        assert stderr.getvalue() == "Warning: hello\n"
    finally:
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        for handler in old_handlers:
            root_logger.addHandler(handler)
        root_logger.setLevel(old_level)


def test_warning_handler_falls_back_for_non_utf_console(monkeypatch):
    """Warnings should degrade to ASCII if the console can't print the symbol."""
    root_logger = logging.getLogger()
    old_handlers = root_logger.handlers[:]
    old_level = root_logger.level

    try:
        commands._configure_logging()
        handler = root_logger.handlers[0]

        calls = []
        stderr = io.StringIO()

        def fake_print(message, *args, **kwargs):
            calls.append(message)
            raise UnicodeEncodeError("gbk", "⚠", 0, 1, "illegal multibyte sequence")

        monkeypatch.setattr(commands.console, "print", fake_print)
        monkeypatch.setattr(commands.sys, "stderr", stderr)

        record = logging.LogRecord(
            name="test",
            level=logging.WARNING,
            pathname=__file__,
            lineno=1,
            msg="hello",
            args=(),
            exc_info=None,
        )

        handler.emit(record)

        assert len(calls) == 1
        assert stderr.getvalue() == "Warning: hello\n"
    finally:
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        for handler in old_handlers:
            root_logger.addHandler(handler)
        root_logger.setLevel(old_level)
