import hmac
import json
from hashlib import sha256
from operator import itemgetter


def validate_init_data(init_data: dict, bot_token: str) -> bool:
    init_data = init_data.copy()
    hash_ = init_data.pop('hash')
    sorted_init_data = dict(sorted(init_data.items(), key=itemgetter(0)))
    data_to_check = []
    const = b'WebAppData'

    for key, value in sorted_init_data.items():
        if isinstance(value, dict):
            value = json.dumps(value, separators=(',', ':'), ensure_ascii=False)

        data_to_check.append(f'{key}={value}')

    data_check_string = '\n'.join(data_to_check)

    secret_key = hmac.new(const, bot_token.encode(), sha256)
    signature = hmac.new(secret_key.digest(), data_check_string.encode(), sha256)

    return signature.hexdigest() == hash_
