from pathlib import Path
import tempfile
import time
import pickle
import pytest
from museums_db import utils

def test_save_and_load_cache():
    # Setup temp files
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        cache_file = tmpdir_path / "cache.pkl"
        meta_file = tmpdir_path / "meta.txt"
        data = {"a": 1, "b": 2}
        # Save cache
        utils.save_cache(data, cache_file, meta_file)
        # Load cache (should be valid)
        loaded = utils.load_cache(cache_file, meta_file, cache_duration=60)
        assert loaded == data
        # Load cache (should be expired)
        time.sleep(2)
        loaded_expired = utils.load_cache(cache_file, meta_file, cache_duration=0)
        assert loaded_expired is None

def test_load_cache_missing_files():
    # Non-existent files
    loaded = utils.load_cache("missing_cache.pkl", "missing_meta.txt", cache_duration=60)
    assert loaded is None

def test_save_cache_overwrites():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        cache_file = tmpdir_path / "cache.pkl"
        meta_file = tmpdir_path / "meta.txt"
        data1 = {"x": 42}
        data2 = {"y": 99}
        utils.save_cache(data1, cache_file, meta_file)
        utils.save_cache(data2, cache_file, meta_file)
        loaded = utils.load_cache(cache_file, meta_file, cache_duration=60)
        assert loaded == data2

def test_save_cache_handles_exceptions():
    # Try saving to a directory (should fail)
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        cache_file = tmpdir_path  # Not a file
        meta_file = tmpdir_path / "meta.txt"
        try:
            utils.save_cache({"fail": True}, cache_file, meta_file)
        except Exception:
            pass  # Should not raise
        # No cache file should be created
    assert not cache_file.is_file()
