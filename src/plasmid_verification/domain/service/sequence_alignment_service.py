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


"""Provide an abstract interface for a sequence alignment service."""


from abc import ABC, abstractmethod

from Bio.Seq import Seq

from ..model import SequenceAlignment


class SequenceAlignmentService(ABC):
    """Define the abstract interface for a sequence alignment service."""

    @classmethod
    @abstractmethod
    def align(
        cls,
        query: Seq,
        target: Seq,
        gap_open_penalty: float = 2.0,
        gap_extension_penalty: float = 10.0,
        **kwargs,
    ) -> SequenceAlignment:
        """Return a local alignment of two given sequences."""
