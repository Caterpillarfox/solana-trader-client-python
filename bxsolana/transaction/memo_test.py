import base64
import unittest

import base58
from solana.keypair import Keypair
from .memo import Memo

from solana.publickey import PublicKey
from solana.blockhash import Blockhash

# key generated for this test
RANDOM_PRIVATE_KEY = "3KWC65p6AvMjvpR2r1qLTC4HVSH4jEFr5TMQxagMLo1o3j4yVYzKsfbB3jKtu3yGEHjx2Cc3L5t8wSo91vpjT63t"
# UNSIGNED_TX_BASE64 = "AgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQD6Amzo3TOF19nBfTBPCjx2oV1dRi5AtFA3kxVbfyOai9/PDbvr0d9iYkVVYCo+5heOy6m60Ua60t+EF+kXEJAgAFD4ls26fgpAnCYufUzDrXMMpDjMYkf2Y2FHuxqKE+2+IrRVKOQVHKKvreZyvh3wca8QpEP1VhjdfPmQtxZk41vr2EwvsYrtYZ9UZjJlPvBgKfAqhkvzgphnGBuyDfHXFcMEoHX5xmEhJgK0YZx3BKh/s3nhpE7IFyBzqsKBqiTDd6jfzI9XsPznt1ZnWa9u9nVKg1KibD5ElrzSfbftYpluJAIIlGU8/d+nt+YMlmaCc2otsPg4VkklsRB3oh4DbXlwD0JuFuuM8DEZF1+YBRQ0SVXONw52WUDzwpQ5VF+0Wppt/RXFB3Bfkzm5U8Gk39vJzBht0vYt9IqVgEXip2UlkfJvXwRhxAEL1cyMpwZt2lhKbucXk0xnet9MJfvRVqLWrj7TJ6D4hJp3KUHZcFDzpujLjdOrzbFHCIfIK1TT82BpuIV/6rgYT7aH9jRhjANdrEOdwa6ztVmKDwAAAAAAEGp9UXGSxcUSGMyUw9SvF/WNruCJuh/UTj29mKAAAAAAbd9uHXZaGT2cvhRs7reawctIXtX1s3kTqM9YV+/wCpAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACFDy1uAqR6+CTQmradxC1wyyjL+iSft+5XudJWwSdi7817DQWO+TIR4kugIb5dD6FCxudqoRDfwOC8xhRQk5dqBA0CAAE0AAAAAIB3jgYAAAAApQAAAAAAAAAG3fbh12Whk9nL4UbO63msHLSF7V9bN5E6jPWFfv8AqQwEAQoACwEBDgwCAwQFBgcBAAgJDAszAAoAAAABAAAAwAslCgAAAAABAAAAAAAAAACXePYDAAAAAAAAAAAAAAAAAAAAAAAAAP//DAMBAAABCQ=="
# EXPECTED = b"AjRa6pZdYfbPV1vu4H+dziK+qYoeS4rPJX1B8rHYRo3p7a57JsRkgKe14FC+YWwEgq2i9onrSkTV8FTDph7rhg0QD6Amzo3TOF19nBfTBPCjx2oV1dRi5AtFA3kxVbfyOai9/PDbvr0d9iYkVVYCo+5heOy6m60Ua60t+EF+kXEJAgAFD4ls26fgpAnCYufUzDrXMMpDjMYkf2Y2FHuxqKE+2+IrRVKOQVHKKvreZyvh3wca8QpEP1VhjdfPmQtxZk41vr2EwvsYrtYZ9UZjJlPvBgKfAqhkvzgphnGBuyDfHXFcMEoHX5xmEhJgK0YZx3BKh/s3nhpE7IFyBzqsKBqiTDd6jfzI9XsPznt1ZnWa9u9nVKg1KibD5ElrzSfbftYpluJAIIlGU8/d+nt+YMlmaCc2otsPg4VkklsRB3oh4DbXlwD0JuFuuM8DEZF1+YBRQ0SVXONw52WUDzwpQ5VF+0Wppt/RXFB3Bfkzm5U8Gk39vJzBht0vYt9IqVgEXip2UlkfJvXwRhxAEL1cyMpwZt2lhKbucXk0xnet9MJfvRVqLWrj7TJ6D4hJp3KUHZcFDzpujLjdOrzbFHCIfIK1TT82BpuIV/6rgYT7aH9jRhjANdrEOdwa6ztVmKDwAAAAAAEGp9UXGSxcUSGMyUw9SvF/WNruCJuh/UTj29mKAAAAAAbd9uHXZaGT2cvhRs7reawctIXtX1s3kTqM9YV+/wCpAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACFDy1uAqR6+CTQmradxC1wyyjL+iSft+5XudJWwSdi7817DQWO+TIR4kugIb5dD6FCxudqoRDfwOC8xhRQk5dqBA0CAAE0AAAAAIB3jgYAAAAApQAAAAAAAAAG3fbh12Whk9nL4UbO63msHLSF7V9bN5E6jPWFfv8AqQwEAQoACwEBDgwCAwQFBgcBAAgJDAszAAoAAAABAAAAwAslCgAAAAABAAAAAAAAAACXePYDAAAAAAAAAAAAAAAAAAAAAAAAAP//DAMBAAABCQ=="


class TestMemo(unittest.TestCase):
    def test_adding_memo_to_serialized_tx(self):
        pkey_bytes = bytes(RANDOM_PRIVATE_KEY, encoding="utf-8")
        pkey_bytes_base58 = base58.b58decode(pkey_bytes)
        kp = Keypair.from_secret_key(pkey_bytes_base58)

        instruction = Memo.create_trader_api_memo_instruction("hi from dev")

        recent_block_hash = Blockhash(str(PublicKey(3)))
        instructions = [instruction]

        tx_serialized = Memo.build_fully_signed_txn(recent_block_hash, kp.public_key, instructions, kp)

        txbase64_str = base64.encodebytes(tx_serialized).decode('utf-8')
        print("txbase64_str", txbase64_str)

        tx_bytes = Memo.add_memo_to_serialized_txn(txbase64_str, "hi from dev2", kp.public_key,  kp)
        print("tx_bytes", tx_bytes)
