from datetime import datetime

from scryfall import get_set_data

local_set_cache = dict()


def ensure_set(set_code):
    if set_code not in local_set_cache:
        local_set_cache[set_code] = get_set_data(set_code)


def get_set_date(set_code):
    ensure_set(set_code)
    if set_code in local_set_cache:
        date_string = local_set_cache[set_code].get("released_at", "0001-01-01")
        return datetime.strptime(date_string, "%Y-%m-%d")
    else:
        return datetime.min


def get_set_order(set_code):
    ensure_set(set_code)
    if set_code in local_set_cache:
        return local_set_cache[set_code].get("released_at", "0000-01-01") + local_set_cache[set_code].get("name",
                                                                                                          set_code)
    else:
        print("unknown set '" + set_code + "'")
        return set_code


def get_set_name(set_code):
    ensure_set(set_code)
    if set_code in local_set_cache:
        return set_code[set].get("name", set_code)
    else:
        print("unknown set '" + set_code + "'")
        return set_code
