import numpy

from github_metrics.common import extract_datetime_or_none, get_author_login
from github_metrics.helpers import (
    filter_valid_prs,
    format_timedelta_to_hours,
    format_timedelta_to_text,
    get_time_without_weekend,
)


def get_merged_prs(formatted_pr_list):
    merged_prs = []

    for pr in formatted_pr_list:
        if pr["merged_at"] is not None:
            merged_prs.append(pr)
    return merged_prs


def format_pr_list(pr_list):
    pr_list_with_hours = [
        {
            "title": pr["title"],
            "author": get_author_login(pr),
            "created_at": extract_datetime_or_none(pr.get("createdAt")),
            "merged_at": extract_datetime_or_none(pr.get("mergedAt"))
            if pr.get("mergedAt")
            else None,
        }
        for pr in pr_list
    ]

    return pr_list_with_hours


def calulate_prs_open_to_merge_time_statistics(
    pr_list, include_hotfixes, exclude_authors, filter_authors, exclude_weekends
):
    valid_pr_list = filter_valid_prs(
        pr_list, include_hotfixes, exclude_authors, filter_authors
    )
    formatted_pr_list = format_pr_list(valid_pr_list)
    merged_pr_list = get_merged_prs(formatted_pr_list)

    review_time_list = []

    for pr in merged_pr_list:
        open_pr_duration = pr["merged_at"] - pr["created_at"]
        if exclude_weekends:
            open_pr_duration = get_time_without_weekend(
                pr["created_at"], pr["merged_at"]
            )
        review_time_list.append(open_pr_duration)

    mean = numpy.mean(review_time_list)
    median = numpy.median(review_time_list)
    percentile = numpy.percentile(review_time_list, 95)

    merged_pr_rate = round((len(merged_pr_list) * 100) / len(valid_pr_list), 2)

    print(
        f"     \033[1mOpen to Merge\033[0m\n"
        f"     ----------------------------------\n"
        f"     Merged PRs count: {len(merged_pr_list)}\n"
        f"     Valid Merged PRs rate: {merged_pr_rate}%\n"
        f"     ----------------------------------\n"
        f"     Mean: {format_timedelta_to_text(mean)}"
        f" ({format_timedelta_to_hours(mean)} hours)\n"
        f"     Median: {format_timedelta_to_text(median)}"
        f" ({format_timedelta_to_hours(median)} hours)\n"
        f"     95 percentile: {format_timedelta_to_text(percentile)}"
        f" ({format_timedelta_to_hours(percentile)} hours)\n"
    )
