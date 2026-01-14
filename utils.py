import json
import logging

CFG_FILE = "config.json"

def load_config(guildID):
    try:
        with open(CFG_FILE, "r", encoding="utf-8") as f:
            cfg = json.load(f)
    except FileNotFoundError:
        return {}

    return cfg.get(str(guildID), {})

def save_config(guildID, data):
    try:
        with open(CFG_FILE, "r") as f:
            cfg = json.load(f)
    except FileNotFoundError:
        cfg = {}

    cfg[str(guildID)] = data

    with open(CFG_FILE, "w") as f:
        json.dump(cfg, f, indent=4)



logging.basicConfig(filename='createdChannels.log', encoding='utf-8', level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)