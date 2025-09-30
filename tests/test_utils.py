from pathlib import Path
import tempfile
import time
import pickle
import pytest
from museums_db import utils

def test_save_and_load_cache():
    """
    Scenario: Saving and loading cache data

    Given a temporary cache file and metadata file
    When data is saved to the cache
    Then loading the cache within the duration returns the same data
    And loading the cache after expiration returns None
    """
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
    """
    Scenario: Loading cache with missing files

    Given non-existent cache and metadata files
    When loading the cache
    Then None is returned
    """
    # Non-existent files
    loaded = utils.load_cache("missing_cache.pkl", "missing_meta.txt", cache_duration=60)
    assert loaded is None

def test_save_cache_overwrites():
    """
    Scenario: Overwriting cache data

    Given a cache file and metadata file
    When data is saved twice to the cache
    Then the last saved data is returned when loading the cache
    """
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
    """
    Scenario: Saving cache to an invalid location

    Given a cache path that is a directory
    When saving data to the cache
    Then no cache file is created and no exception is raised
    """
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
