import time
import redis

from flask import Flask, jsonify

from settings import AMOUNT_LIMITS_CONFIG, REDIS_HOST, REDIS_PORT

app = Flask(__name__)
redis_conn = redis.Redis(REDIS_HOST, REDIS_PORT)

max_interval = max(AMOUNT_LIMITS_CONFIG)
min_interval = min(AMOUNT_LIMITS_CONFIG)
max_amount = AMOUNT_LIMITS_CONFIG[min_interval]


class Transaction:

    @classmethod
    def add_transaction(cls, amount, tr_time):
        redis_conn.set(tr_time, amount, ex=max_interval)

    @classmethod
    def verify(cls, amount, tr_time):
        if amount > max_amount:
            return f'{max_amount}/{min_interval}'
        temp = {interval: 0 for interval in AMOUNT_LIMITS_CONFIG}
        for key in redis_conn.keys():
            for interval, limit in AMOUNT_LIMITS_CONFIG.items():
                if tr_time - float(key) < interval:
                    temp[interval] += int(redis_conn.get(key))
                    if temp[interval] + amount > limit:
                        return f'{limit}/{interval}'


@app.route('/request/<int:amount>')
def request(amount):
    now = time.time()
    error = Transaction.verify(amount, now)
    if error:
        return jsonify({'error': f'amount limit exceeded ({error}sec)'})

    Transaction.add_transaction(amount, now)
    return jsonify({'result': 'OK'})
