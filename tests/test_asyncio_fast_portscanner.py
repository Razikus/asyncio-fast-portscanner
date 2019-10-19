#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `asyncio_fast_portscanner` package."""

import pytest

from click.testing import CliRunner

from asyncio_fast_portscanner import asyncio_fast_portscanner
from asyncio_fast_portscanner import cli
import json


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    """ Test for RANGE + additional port"""
    result = runner.invoke(cli.scan, ["192.168.0-2.0-255", "22", "-r", "RANGE", "-t", "2", "-a"])
    assert result.exit_code == 0
    unJsoned = json.loads(result.output)
    assert len(unJsoned) == 256 * 3

    """ Test for smaller range"""
    result = runner.invoke(cli.scan, ["192.168.2.1-128", "22", "-r", "RANGE", "-t", "0.3", "-a"])
    assert result.exit_code == 0
    unJsoned = json.loads(result.output)
    assert len(unJsoned) == 128

    """ Test for CIDR + additional port"""
    result = runner.invoke(cli.scan, ["192.168.0.0/16", "22", "33", "-r", "CIDR", "-t", "5", "-a"])
    assert result.exit_code == 0
    unJsoned = json.loads(result.output)
    assert len(unJsoned) == 256 * 256
