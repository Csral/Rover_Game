import random

class Event:
    def __init__(self, id, name, priority, duration, expire_time, impact, benefit, category_hint):
        self.id = id
        self.name = name
        self.priority = priority  # 0 to 5
        self.duration = duration  # active processing duration
        self.total_duration = duration
        self.expire_time = expire_time  # time until event auto-expires
        self.impact = impact  # HP loss if missed
        self.benefit = benefit  # Score gain if completed
        self.category_hint = category_hint  # vague hint for player

    def modify_priority(self, delta):
        self.priority = max(0, min(5, self.priority + delta))

    def hint_text(self):
        """Returns vague hint text for UI/logs."""
        return f"{self.category_hint}"

# Possible event templates
EVENT_NAMES = [
    "Analyze Soil", "Radiation Spike", "Camera Malfunction", "Solar Panel Clean",
    "Antenna Recalibration", "Path Obstruction", "Thermal Regulation Check",
    "Battery Drain Alert", "Sample Preservation", "Gyroscope Drift"
]

CATEGORY_HINTS = [
    "Power", "Navigation", "Communication", "Thermal", "Sensors", "Sample Ops"
]

def generate_random_event(event_id):
    name = random.choice(EVENT_NAMES)
    priority = random.randint(0, 5)
    duration = random.uniform(5, 15)   # active duration
    expire_time = random.uniform(8, 20)  # time to expire from incoming
    impact = random.randint(5, 15)      # HP loss on fail
    benefit = random.randint(10, 25)    # Score gain on completion
    category_hint = random.choice(CATEGORY_HINTS)

    return Event(
        id=event_id,
        name=name,
        priority=priority,
        duration=duration,
        expire_time=expire_time,
        impact=impact,
        benefit=benefit,
        category_hint=category_hint
    )