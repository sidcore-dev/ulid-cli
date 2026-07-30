import unittest

from ulid_cli.core import CROCKFORD_ALPHABET, encode_crockford32, generate_ulid


class TestEncodeCrockford32(unittest.TestCase):
    def test_zero_pads_to_length(self) -> None:
        self.assertEqual(encode_crockford32(0, 4), "0000")

    def test_alphabet_excludes_ambiguous_letters(self) -> None:
        for letter in "ILOU":
            self.assertNotIn(letter, CROCKFORD_ALPHABET)

    def test_value_too_large_raises(self) -> None:
        with self.assertRaises(ValueError):
            encode_crockford32(32 ** 2, 2)

    def test_negative_raises(self) -> None:
        with self.assertRaises(ValueError):
            encode_crockford32(-1, 4)

    def test_round_trip_via_decode(self) -> None:
        encoded = encode_crockford32(12345, 8)
        decoded = 0
        for ch in encoded:
            decoded = decoded * 32 + CROCKFORD_ALPHABET.index(ch)
        self.assertEqual(decoded, 12345)


class TestGenerateUlid(unittest.TestCase):
    def test_length_is_26(self) -> None:
        self.assertEqual(len(generate_ulid()), 26)

    def test_only_valid_alphabet_characters(self) -> None:
        ulid = generate_ulid()
        self.assertTrue(all(ch in CROCKFORD_ALPHABET for ch in ulid))

    def test_deterministic_with_fixed_timestamp_and_randomness(self) -> None:
        randomness = bytes(range(10))
        a = generate_ulid(timestamp_ms=0, randomness=randomness)
        b = generate_ulid(timestamp_ms=0, randomness=randomness)
        self.assertEqual(a, b)

    def test_known_vector(self) -> None:
        # timestamp 0 with all-zero randomness encodes to all "0" characters.
        self.assertEqual(generate_ulid(timestamp_ms=0, randomness=bytes(10)), "0" * 26)

    def test_later_timestamp_sorts_after_earlier_one(self) -> None:
        randomness = bytes(10)
        earlier = generate_ulid(timestamp_ms=1000, randomness=randomness)
        later = generate_ulid(timestamp_ms=2000, randomness=randomness)
        self.assertLess(earlier, later)

    def test_timestamp_out_of_range_raises(self) -> None:
        with self.assertRaises(ValueError):
            generate_ulid(timestamp_ms=2 ** 48)

    def test_wrong_randomness_length_raises(self) -> None:
        with self.assertRaises(ValueError):
            generate_ulid(timestamp_ms=0, randomness=b"short")


if __name__ == "__main__":
    unittest.main()
