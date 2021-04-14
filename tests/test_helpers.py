import unittest
from datetime import timedelta

from tests.mocks import request_mock
from helpers import (
    format_timedelta,
    exclude_closeds,
    exclude_releases,
    exclude_merge_backs_from_prod,
    exclude_authors_in_list,
    exclude_hotfixes,
)


class TestHelpers(unittest.TestCase):
    def test_exclude_closed_prs(self):
        prs = [
            {
                "mergedAt": "2021-03-24T11:13:19Z",
                "closedAt": None,
            },
            {
                "mergedAt": None,
                "closedAt": "2021-03-24T11:13:19Z",
            },
            {
                "mergedAt": "2021-03-24T11:13:19Z",
                "closedAt": "2021-03-24T11:13:19Z",
            },
        ]

        closed_prs = exclude_closeds(prs)
        self.assertEqual(len(closed_prs), 2)

    def test_exclude_releases_prs(self):
        prs = [
            {
                "title": "",
                "baseRefName": "production",
                "headRefName": "release/2021-03-24.0",
            },
            {
                "title": "Release 2021-03-24.0",
                "baseRefName": "production",
                "headRefName": "",
            },
            {
                "title": "",
                "baseRefName": "master",
                "headRefName": "",
            },
            {
                "title": "",
                "baseRefName": "production",
                "headRefName": "master",
            },
        ]
        releases_prs = exclude_releases(prs)
        self.assertEqual(len(releases_prs), 1)

    def test_exclude_merge_backs_from_prod(self):
        prs = [
            {
                "baseRefName": "master",
                "headRefName": "production",
            },
            {
                "baseRefName": "master",
                "headRefName": "",
            },
            {
                "baseRefName": "",
                "headRefName": "production",
            },
        ]
        prs_list = exclude_merge_backs_from_prod(prs)
        self.assertEqual(len(prs_list), 2)

    def test_format_time_string(self):
        time = timedelta(seconds=1 * 24 * 60 * 60 + 48035)
        formatted_time = format_timedelta(time)

        hours, remainder = divmod(time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.assertEqual(
            formatted_time, f"{time.days} days {hours} hours {minutes} minutes"
        )

    def test_negative_timedelta_format_time_returns_invalid(self):
        time = timedelta(seconds=1 * 24 * 60 * 60 + 48035)
        formatted_time = format_timedelta(-time)

        self.assertEqual(formatted_time, "Invalid timeframe")

    def test_exclude_authors_from_pr(self):
        prs = [
            {
                "author": {"login": "ladygaga"},
                "headRefName": "production",
            },
            {
                "author": {"login": "beyonce"},
                "headRefName": "production",
            },
            {
                "author": {"login": "beyonce"},
                "headRefName": "production",
            },
            {
                "author": {"login": "grimes"},
                "headRefName": "production",
            },
            {
                "author": {"login": "badgalriri"},
                "headRefName": "production",
            },
            {
                "author": {"login": "katyperry"},
                "headRefName": "production",
            },
        ]

        valid_prs = exclude_authors_in_list(prs, authors=["beyonce", "katyperry"])
        self.assertEqual(len(valid_prs), 3)

    def test_exclude_hotfixes(self):
        prs = [
            {
                "baseRefName": "production",
                "headRefName": "feature/new",
                "title": "Open modal",
            },
            {
                "baseRefName": "production",
                "headRefName": "hf/page",
                "title": "page",
            },
            {
                "baseRefName": "master",
                "headRefName": "feature/test-hotfix",
                "title": "adds test",
            },
        ]
        prs_list = exclude_hotfixes(prs)
        self.assertEqual(len(prs_list), 2)


if __name__ == "__main__":
    unittest.main()