import os
import redis

class CacheService:
    def __init__(self):
        self.redis = redis.Redis(host=os.getenv('REDIS_HOST', 'localhost'), port=6379, db=0, decode_responses=True)
        self.enabled = os.getenv('USE_REDIS', 'false').lower() == 'true'
    def get_link(self, code): return self.redis.get(f"link:{code}") if self.enabled else None
    def set_link(self, code, url): 
        if self.enabled: self.redis.setex(f"link:{code}", 3600, url)
    def invalidate(self, code):
        if self.enabled: self.redis.delete(f"link:{code}")

cache = CacheService()
