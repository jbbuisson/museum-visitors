import pickle
import time

def load_cache(cache_file, cache_meta_file, cache_duration):
    try:
        with open(cache_meta_file, "r") as f:
            cache_time = float(f.read().strip())
        if time.time() - cache_time < cache_duration:
            with open(cache_file, "rb") as f:
                print("Loading data from cache")
                data = pickle.load(f)
            return data
    except Exception:
        pass
    return None

def save_cache(data, cache_file, cache_meta_file):
    try:
        with open(cache_file, "wb") as f:
            print("Saving data to cache")
            pickle.dump(data, f)
        with open(cache_meta_file, "w") as f:
            f.write(str(time.time()))
    except Exception:
        pass
