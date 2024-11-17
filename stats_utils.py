import json
import os
import time
from datetime import datetime

class StatsTracker:
    def __init__(self, stats_file="stats.json"):
        self.stats_file = stats_file
        self.start_time = None
        self.themes_start = None
        self.posts_start = None
        
    def start_tracking(self):
        self.start_time = time.time()
        
    def start_themes(self):
        self.themes_start = time.time()
        
    def start_posts(self):
        self.posts_start = time.time()
        
    def save_stats(self, themes_count):
        themes_duration = time.time() - self.themes_start if self.themes_start else 0
        posts_duration = time.time() - self.posts_start if self.posts_start else 0
        total_duration = time.time() - self.start_time
        
        stats = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "themes_count": themes_count,
            "themes_generation_time": round(themes_duration, 2),
            "posts_generation_time": round(posts_duration, 2),
            "total_time": round(total_duration, 2)
        }
        
        existing_stats = []
        if os.path.exists(self.stats_file):
            with open(self.stats_file, 'r') as f:
                try:
                    existing_stats = json.load(f)
                except json.JSONDecodeError:
                    existing_stats = []
        
        existing_stats.append(stats)
        
        with open(self.stats_file, 'w') as f:
            json.dump(existing_stats, f, indent=2)
            
        return stats