"""
This file is part of nucypher.

nucypher is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

nucypher is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with nucypher.  If not, see <https://www.gnu.org/licenses/>.
"""

import base64

from bytestring_splitter import BytestringKwargifier


class Card:

    _specification = NotImplemented

    def __bytes__(self):
        return NotImplemented

    def to_hex(self) -> str:
        return bytes(self).hex()

    def __hex__(self) -> str:
        return self.to_hex()

    def to_base64(self) -> str:
        return base64.urlsafe_b64encode(bytes(self)).decode()

    def to_qr_code(self):
        pass  # TODO

    @classmethod
    def from_bytes(cls, data: bytes):
        return BytestringKwargifier(cls, **cls._specification)(data)

    @classmethod
    def from_hex(cls, hexdata: str):
        return cls.from_bytes(bytes.fromhex(hexdata))

    @classmethod
    def from_base64(cls, b64data: str):
        return cls.from_bytes(base64.urlsafe_b64decode(b64data))

    @classmethod
    def from_qr_code(cls, qr_code):
        pass  # TODO

    def keys(self):
        return self._specification.keys()

    def __getitem__(self, key):
        return getattr(self, key)

    def __repr__(self):
        attrs = (f'{field}={self[field]}' for field in self.keys())
        return f'{self.__class__.__name__}({", ".join(attrs)})'

    def __eq__(self, other):
        return dict(self) == dict(other)


class AliceCard(Card):

    _specification = dict(alice_verifying_key=(bytes, 33))

    def __init__(self, alice_verifying_key):
        self.alice_verifying_key = bytes(alice_verifying_key)

    def __bytes__(self):
        return bytes(self.alice_verifying_key)


class BobCard(Card):

    _specification = dict(bob_verifying_key=(bytes, 33), bob_encrypting_key=(bytes, 33))

    def __init__(self, bob_verifying_key, bob_encrypting_key):
        self.bob_verifying_key = bytes(bob_verifying_key)
        self.bob_encrypting_key = bytes(bob_encrypting_key)

    def __bytes__(self):
        return bytes(self.bob_verifying_key) + bytes(self.bob_encrypting_key)


class PolicyCard(Card):

    _specification = dict(alice_verifying_key=(bytes, 33), policy_encrypting_key=(bytes, 33))

    def __init__(self, alice_verifying_key, policy_encrypting_key):
        self.alice_verifying_key = bytes(alice_verifying_key)
        self.policy_encrypting_key = bytes(policy_encrypting_key)

    def __bytes__(self):
        return bytes(self.alice_verifying_key) + bytes(self.policy_encrypting_key)





