from github_metrics.helpers import filter_valid_prs



def call_pr_list(pr_list, exclude_authors, filter_authors):
    print(
        f"     \033[1mPR List\033[0m\n"
        f"     ----------------------------------\n"
    )
    valid_pr_list = filter_valid_prs(
        pr_list=pr_list, include_hotfixes=True, exclude_authors=exclude_authors, filter_authors=filter_authors
    )
    for pr in valid_pr_list:
        print(
        f"     {pr['title']}: {pr['url']}"
        )
