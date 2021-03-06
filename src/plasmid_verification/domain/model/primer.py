# Copyright (c) 2021, Moritz E. Beber.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Provide a sequencing primer model."""


from __future__ import annotations

from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord


class Primer:
    def __init__(self, *, identifier: str, sequence: Seq, **kwargs) -> None:
        """"""
        super().__init__(**kwargs)
        self._identifier = identifier
        self._sequence = sequence

    @classmethod
    def from_fasta(cls, record: SeqRecord) -> Primer:
        """"""
        return cls(identifier=record.id, sequence=record.seq)

    def __len__(self) -> int:
        """"""
        return len(self.sequence)

    @property
    def identifier(self) -> str:
        """Return the primer's identifier."""
        return self._identifier

    @property
    def sequence(self) -> Seq:
        """Return the DNA sequence of the primer."""
        return self._sequence
