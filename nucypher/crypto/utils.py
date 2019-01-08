"""
This file is part of nucypher.

nucypher is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

nucypher is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with nucypher.  If not, see <https://www.gnu.org/licenses/>.
"""
from typing import Any
from eth_keys import KeyAPI as EthKeyAPI
from umbral.keys import UmbralPublicKey

from nucypher.crypto.api import keccak_digest


def fingerprint_from_key(public_key: Any):
    """
    Hashes a key using keccak-256 and returns the hexdigest in bytes.
    :return: Hexdigest fingerprint of key (keccak-256) in bytes
    """
    return keccak_digest(bytes(public_key)).hex().encode()


def canonical_address_from_umbral_key(public_key: UmbralPublicKey) -> bytes:
    pubkey_raw_bytes = public_key.to_bytes(is_compressed=False)[1:]
    eth_pubkey = EthKeyAPI.PublicKey(pubkey_raw_bytes)
    canonical_address = eth_pubkey.to_canonical_address()
    return canonical_address