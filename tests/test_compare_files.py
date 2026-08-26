"""Tests for shared file comparison."""

from pup_core.compare.files import classify_file_relationship


def test_same_text_is_same() -> None:
    """Equal text is classified as the same."""
    assert (
        classify_file_relationship(
            left_exists=True,
            right_exists=True,
            left_text="same",
            right_text="same",
        )
        == "same"
    )


def test_left_only_is_reported() -> None:
    """A file present only on the left is classified explicitly."""
    assert (
        classify_file_relationship(
            left_exists=True,
            right_exists=False,
            left_text="left",
            right_text=None,
        )
        == "left-only"
    )
