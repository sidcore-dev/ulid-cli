# ulid-cli

A small, dependency-free command-line tool that generates ULIDs
(Universally Unique Lexicographically Sortable Identifiers): a 48-bit
millisecond timestamp plus 80 bits of randomness, Crockford Base32
encoded into a 26-character string.

## Why

UUIDs are unique but not sortable and not compact. ULIDs are — they sort
lexicographically by creation time, are URL-safe, and (per the
[ULID spec](https://github.com/ulid/spec)) use a Base32 alphabet that
excludes the visually ambiguous letters `I`, `L`, `O`, and `U`.

## Install

```bash
pip install .
```

This installs a `ulid-cli` command on your PATH.

## Usage

```bash
ulid-cli
```

```
01ARZ3NDEKTSV4RRFFQ69G5FAV
```

Generate several at once:

```bash
ulid-cli --count 3
```

```
01H8XGJVK5N0V6ZQJ5Y8N5T0PC
01H8XGJVK5EFYQY3F5NRSMB4WV
01H8XGJVK5NJTRQ04MPTQK9NK9
```

Generate one for a specific point in time (useful for tests, backfills,
or reproducing a known ID):

```bash
ulid-cli --timestamp 1469918176385
```

```
01ARZ3NDEK6HRVQ0JM7RM6DHYW
```

### Options

| Flag                  | Description                                                     |
|-----------------------|--------------------------------------------------------------------|
| `--count N`           | Number of ULIDs to generate (default: 1)                           |
| `--timestamp UNIX_MS` | Generate for a specific Unix timestamp in milliseconds, instead of now |

### Exit codes

- `0` — success
- `2` — invalid arguments (e.g. `--count 0`, a timestamp that doesn't fit in 48 bits)

## Development

```bash
pip install -e .
python -m unittest discover -s tests -v
```

## License

All rights reserved. This code is public for viewing and reference only —
no license is granted to use, copy, modify, or redistribute it. See
[LICENSE](LICENSE) for details.
