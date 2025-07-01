import time
from collections import defaultdict

from fastapi import HTTPException, status

# set the query to only 2 queries per 5 min
AUTH_RATE_LIMIT = 2
AUTH_TIME_WINDOW_SECONDS = 300

user_requests = defaultdict(list)


# --- Throttling dependency ---
def apply_rate_limit(user_id: str):
    current_time = time.time()
    rate_limit = AUTH_RATE_LIMIT
    time_window = AUTH_TIME_WINDOW_SECONDS

    # Filter out requests older than the time window
    user_requests[user_id] = [
        t for t in user_requests[user_id] if t > current_time - time_window
    ]

    if len(user_requests[user_id]) >= rate_limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests. Try again later.",
        )
    else:
        # prints current usage for debugging, can be removed
        current_usage = len(user_requests[user_id])
        print(f"User {user_id}: {current_usage + 1}/{rate_limit} requests used.")

    user_requests[user_id].append(current_time)
    return True