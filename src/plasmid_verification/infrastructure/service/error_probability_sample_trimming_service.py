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


"""Provide a service that trims samples based on smoothed Phred quality."""

from typing import Tuple

import numpy as np

from plasmid_verification.domain.model import Sample
from plasmid_verification.domain.service import SampleTrimmingService


class ErrorProbabilitySampleTrimmingService(SampleTrimmingService):
    """Define a service that trims samples based on the smoothed Phred quality."""

    @classmethod
    def trim(
        cls,
        sample: Sample,
        *,
        prefix: str = "",
        suffix: str = "_trimmed",
        cutoff: float = 0.05,
        **kwargs,
    ) -> Tuple[Sample, int, int, np.ndarray]:
        """
        Trim a sequencing sample based on the smoothed quality values and a threshold.

        Implement Richard Mott's alternative trimming method for finding the
        maximum scoring subsequence. Please see `-trim_alt` at the following link for
        more information:
        http://www.phrap.org/phredphrap/phred.html

        Args:
            sample: A sequencing sample.
            prefix:
            suffix:
            cutoff:
            **kwargs:

        Returns:
            tuple:
                Sample: The trimmed sequencing sample.
                int: The start position of the trimmed sequence with respect to the
                    original sample.
                int: The end position of the trimmed sequence with respect to the
                    original sample.
                numpy.ndarray: The scores used by the trimming method.


        """
        # Transform the quality values back to error probabilities.
        transform = cutoff - np.power(10.0, sample.phred_quality / -10.0)
        scores = cls.clamped_cumulative_sum(transform)
        start, end = cls.find_max_scoring_subsequence(scores)
        return (
            Sample(
                identifier=f"{prefix}{sample.identifier}{suffix}",
                sequence=sample.sequence[start:end],
                phred_quality=sample.phred_quality[start:end],
            ),
            start,
            end,
            scores,
        )

    @classmethod
    def clamped_cumulative_sum(cls, values: np.ndarray) -> np.ndarray:
        """
        Compute the cumulative sum of the given values but clamp the minimum at zero.

        Args:
            values: The vector of values to sum up.

        Returns:
            Cumulative sum of the given values but sums below zero are clamped to zero.

        """
        result = np.zeros_like(values)
        for idx in range(1, len(result)):
            result[idx] = result[idx - 1] + values[idx]
            if result[idx] < 0.0:
                result[idx] = 0.0
        return result

    @classmethod
    def find_max_scoring_subsequence(cls, scores: np.ndarray) -> Tuple[int, int]:
        max_idx = scores.argmax()
        # Index locations where the given condition is true.
        zero_locations = np.nonzero(scores == 0.0)[0]
        # In which segment, flanked by zeros, is the maximum location?
        max_location = np.searchsorted(zero_locations, max_idx)
        return int(zero_locations[max_location - 1]) + 1, int(max_idx)
