"""Core ULID generation logic for ulid-cli.

Implements the ULID spec: https://github.com/ulid/spec
A ULID is a 128-bit value made of a 48-bit millisecond Unix timestamp
followed by 80 bits of randomness, rendered as 26 characters of Crockford
Base32 (which excludes the visually ambiguous letters I, L, O, and U).
"""
from __future__ import annotations

import os
import time

# Crockford Base32 alphabet: excludes I, L, O, U to avoid visual ambiguity.
CROCKFORD_ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"

TIME_LEN = 10  # 48 bits of timestamp -> 10 Crockford Base32 characters
RANDOM_LEN = 16  # 80 bits of randomness -> 16 Crockford Base32 characters
ULID_LEN = TIME_LEN + RANDOM_LEN


def encode_crockford32(value: int, length: int) -> str:
    """Encode a non-negative integer as a fixed-length Crockford Base32 string."""
    if value < 0:
        raise ValueError("value must not be negative")

    chars = ["0"] * length
    for i in range(length - 1, -1, -1):
        chars[i] = CROCKFORD_ALPHABET[value & 0x1F]
        value >>= 5

    if value != 0:
        raise ValueError("value does not fit in the given length")

    return "".join(chars)


def generate_ulid(timestamp_ms: int | None = None, randomness: bytes | None = None) -> str:
    """Generate a ULID string.

    `timestamp_ms` defaults to the current Unix time in milliseconds;
    `randomness` defaults to 10 cryptographically random bytes. Both are
    overridable, primarily so tests (and callers wanting reproducible
    output) can pin the result.
    """
    if timestamp_ms is None:
        timestamp_ms = int(time.time() * 1000)
    if timestamp_ms < 0 or timestamp_ms >= 2 ** 48:
        raise ValueError("timestamp_ms must fit in 48 bits (0 <= t < 2**48)")

    if randomness is None:
        randomness = os.urandom(10)
    if len(randomness) != 10:
        raise ValueError("randomness must be exactly 10 bytes (80 bits)")

    time_part = encode_crockford32(timestamp_ms, TIME_LEN)
    random_part = encode_crockford32(int.from_bytes(randomness, "big"), RANDOM_LEN)
    return time_part + random_part
