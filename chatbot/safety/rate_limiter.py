"""
Rate Limiter module.
Provides an in-memory sliding-window IP rate limiter to protect public Chatbot endpoints.
"""

import time
from collections import defaultdict
from typing import Dict, List, Tuple


class RateLimiter:
    """
    Sliding-window in-memory IP rate limiter.
    Tracks timestamp requests per client IP to prevent bot abuse and quota exhaustion.
    """

    def __init__(self, max_requests: int = 20, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._requests: Dict[str, List[float]] = defaultdict(list)

    def is_allowed(self, client_ip: str) -> Tuple[bool, int]:
        """
        Checks if the client IP is within rate limits.
        Returns: (is_allowed: bool, retry_after_seconds: int)
        """
        if not client_ip:
            client_ip = "anonymous"

        current_time = time.time()
        cutoff_time = current_time - self.window_seconds

        # Prune timestamps older than window_seconds
        timestamps = [ts for ts in self._requests[client_ip] if ts > cutoff_time]
        self._requests[client_ip] = timestamps

        if len(timestamps) >= self.max_requests:
            # Calculate wait time until the oldest request leaves the sliding window
            oldest_ts = timestamps[0]
            retry_after = max(1, int(self.window_seconds - (current_time - oldest_ts)))
            return False, retry_after

        # Record this request
        self._requests[client_ip].append(current_time)
        return True, 0

    def reset(self, client_ip: str = None):
        """
        Clears rate limit records (useful for testing).
        """
        if client_ip:
            self._requests.pop(client_ip, None)
        else:
            self._requests.clear()
