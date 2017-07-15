github\_contributions\.GithubContributions
------------------------------------------

.. autoclass:: github_contributions.contributions.GithubContributions
    :members:
    :undoc-members:
    :show-inheritance:

.. py:class:: github_contributions.contributions.Day

    Data container object for contribution data of a given day.

    .. py:attribute:: date

        Date associated with the day

    .. py:attribute:: count

        Number of contributions done by the user on this day

    .. py:attribute:: level

        "Contribution level" of the day.

        Corresponds to the color displayed in the contribution graph. Has a value between 0 and 4 (inclusive)
