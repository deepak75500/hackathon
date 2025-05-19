import random
from collections import deque
def calculate_demand_score(hour):
    base_score = 0
    if 11 <= hour <= 14:
        base_score += 0.5
    elif hour == 10 or hour == 16:
        base_score += 0.2
    else:
        base_score += 0.35

    user_bias = {10: 0.1, 11: 0.3, 12: 0.4, 13: 0.5, 14: 0.4, 15: 0.3, 16: 0.2}
    base_score += user_bias.get(hour, 0)
    weekday_bias = 0.1
    jitter = random.uniform(-0.05, 0.05)
    return base_score + weekday_bias + jitter

user_queue = deque(["Alice", "Bob", "Charlie", "Dana", "Eve", "Frank"])
def generate_slots(start_hour=10, end_hour=17):
    slots = {}
    for hour in range(start_hour, end_hour):
        time_label = f"{hour}:00 - {hour+1}:00"
        score = calculate_demand_score(hour)

        if score > 0.65 and user_queue:
            assigned_user = user_queue.popleft()
            slots[time_label] = assigned_user
        else:
            slots[time_label] = None
    return slots
