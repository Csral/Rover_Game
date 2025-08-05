import random
from utils import WHITE, ORANGE, RED

# Categories to hint at event relevance
CATEGORIES = ["Power", "Navigation", "Communication", "Thermal", "Sensors", "Sample Ops"]

# Possible log severities
LOG_TYPES = [
    ("INFO", WHITE),
    ("WARN", ORANGE),
    ("ERR", RED),
]

def random_hex():
    return "".join(random.choice("0123456789ABCDEF") for _ in range(8))

def generate_log():
    """Generates pseudo-random system log messages with categories or random dumps."""
    log_type, color = random.choice(LOG_TYPES)
    category = random.choice(CATEGORIES)

    # 50% chance of hint log, 50% chance of random memory dump
    if random.random() < 0.5:
        # Hint log
        message = f"{log_type}: {category} anomaly at 0x{random_hex()} :: code {random.randint(100,999)}"
    else:
        # Random memory dump style log
        message = f"MEMDUMP[{random.randint(1000,9999)}]: 0x{random_hex()} 0x{random_hex()} 0x{random_hex()}"

    return (message, color)