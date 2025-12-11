"""Simple in-memory cache with TTL support."""
import time
import threading
from typing import Any, Dict, Optional


class SimpleCache:
    """Thread-safe in-memory cache with TTL."""
    
    def __init__(self):
        self._cache: Dict[str, Any] = {}
        self._expiry: Dict[str, float] = {}
        self._lock = threading.Lock()
        
    def set(self, key: str, value: Any, ttl_seconds: int) -> None:
        """Set a value with TTL."""
        with self._lock:
            self._cache[key] = value
            self._expiry[key] = time.time() + ttl_seconds
            
    def get(self, key: str) -> Optional[Any]:
        """Get a value if not expired."""
        with self._lock:
            if key in self._cache:
                if time.time() < self._expiry[key]:
                    return self._cache[key]
                else:
                    # Expired, clean up
                    self._cleanup_key(key)
            return None
            
    def _cleanup_key(self, key: str) -> None:
        """Remove a key from cache (internal, no lock)."""
        self._cache.pop(key, None)
        self._expiry.pop(key, None)
        
    def cleanup_expired(self) -> int:
        """Remove all expired entries. Returns count of removed items."""
        with self._lock:
            current_time = time.time()
            expired_keys = [
                key for key, expiry_time in self._expiry.items()
                if current_time >= expiry_time
            ]
            for key in expired_keys:
                self._cleanup_key(key)
            return len(expired_keys)
            
    def clear(self) -> None:
        """Clear all cache entries."""
        with self._lock:
            self._cache.clear()
            self._expiry.clear()
            
    def size(self) -> int:
        """Get current cache size."""
        with self._lock:
            return len(self._cache)


# Global cache instance
cache_manager = SimpleCache()
