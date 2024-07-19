import tracemalloc
import gc

class MemoryMonitor:
    @staticmethod
    def start():
        tracemalloc.start()

    @staticmethod
    def stop():
        tracemalloc.stop()

    @staticmethod
    def display_top_stats(limit=10):
        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics('lineno')
        print("[ Top memory-consuming lines ]")
        for stat in top_stats[:limit]:
            print(stat)

    @staticmethod
    def collect_garbage():
        gc.collect()