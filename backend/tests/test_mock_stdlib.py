import time
from unittest.mock import patch

def now_ms() -> int:
    return int(time.time() * 1000)

def test_patch_time():
    with patch("time.time", return_value=123.456):
        assert now_ms() == 123456
