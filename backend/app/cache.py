import hashlib
import json
import pickle
from functools import wraps

import redis

redis_client = redis.Redis(host="localhost", port=6379, db=1, decode_responses=True)


def cache_key_generator(*args, **kwargs):
    """Generate cache key from function arguments"""
    key_data = str(args) + str(sorted(kwargs.items()))
    return hashlib.md5(key_data.encode()).hexdigest()


def cache_result(expiration=0):
    """Decorator to cache function results"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            cache_key = f"{func.__name__}:{cache_key_generator(*args, **kwargs)}"

            try:
                cached_result = redis_client.get(cache_key)
                if cached_result:
                    return json.loads(cached_result)
            except Exception as e:
                print(f"Cache get error: {e}")

            result = func(*args, **kwargs)

            try:
                redis_client.setex(
                    cache_key, expiration, json.dumps(result, default=str)
                )
            except Exception as e:
                print(f"Cache set error: {e}")

            return result

        return wrapper

    return decorator


def invalidate_cache(pattern):
    """Invalidate cache entries matching pattern"""
    try:
        keys = redis_client.keys(pattern)
        if keys:
            redis_client.delete(*keys)
    except Exception as e:
        print(f"Cache invalidation error: {e}")


class CacheManager:
    """Cache manager for common operations"""

    @staticmethod
    def get_cached_data(key):
        """Get generic cached data by key"""
        try:
            cached = redis_client.get(key)
            if cached:
                return json.loads(cached)
        except Exception as e:
            print(f"Cache get error for {key}: {e}")
        return None

    @staticmethod
    def set_cached_data(key, data, expiration=5):
        """Set generic cached data with key"""
        try:
            redis_client.setex(key, expiration, json.dumps(data, default=str))
            return True
        except Exception as e:
            print(f"Cache set error for {key}: {e}")
            return False

    @staticmethod
    def get_subjects():
        """Get cached subjects"""
        cache_key = "subjects:all"
        try:
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
        except:
            pass
        return None

    @staticmethod
    def set_subjects(subjects, expiration=600):
        """Cache subjects"""
        cache_key = "subjects:all"
        try:
            redis_client.setex(cache_key, expiration, json.dumps(subjects, default=str))
        except Exception as e:
            print(f"Cache set error: {e}")

    @staticmethod
    def get_user_quizzes(user_id):
        """Get cached user quizzes"""
        cache_key = f"user_quizzes:{user_id}"
        try:
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
        except:
            pass
        return None

    @staticmethod
    def set_user_quizzes(user_id, quizzes, expiration=300):
        """Cache user quizzes"""
        cache_key = f"user_quizzes:{user_id}"
        try:
            redis_client.setex(cache_key, expiration, json.dumps(quizzes, default=str))
        except Exception as e:
            print(f"Cache set error: {e}")

    @staticmethod
    def invalidate_user_cache(user_id):
        """Invalidate all cache for a user"""
        pattern = f"user_quizzes:{user_id}*"
        invalidate_cache(pattern)

    @staticmethod
    def invalidate_quizzes_cache():
        """Invalidate all quizzes cache"""
        invalidate_cache("quizzes:*")

    @staticmethod
    def invalidate_subjects_cache():
        """Invalidate subjects cache"""
        invalidate_cache("subjects:*")

    @staticmethod
    def invalidate_chapters_cache(subject_id=None):
        """Invalidate chapters cache for a specific subject or all chapters"""
        if subject_id:
            invalidate_cache(f"chapters:subject:{subject_id}*")
        else:
            invalidate_cache("chapters:*")

    @staticmethod
    def invalidate_dashboard_cache():
        """Invalidate dashboard cache for all users"""
        invalidate_cache("user_quizzes:*")


def rate_limit(max_requests=100, window=3600):
    """Rate limiting decorator"""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            client_ip = "127.0.0.1"

            rate_key = f"rate_limit:{client_ip}:{func.__name__}"

            try:

                current_requests = redis_client.get(rate_key)

                if current_requests is None:

                    redis_client.setex(rate_key, window, 1)
                elif int(current_requests) >= max_requests:

                    return {"error": "Rate limit exceeded"}, 429
                else:

                    redis_client.incr(rate_key)

            except Exception as e:
                print(f"Rate limiting error: {e}")

                pass

            return func(*args, **kwargs)

        return wrapper

    return decorator
