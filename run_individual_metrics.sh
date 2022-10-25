START_DATE="2022-10-17"
END_DATE="2022-10-23"
echo "Getting metrics for individuals between $START_DATE and $END_DATE"
python github_metrics/run.py --start-date=$START_DATE --end-date=$END_DATE --filter-authors=jthodge > jthodge.txt
python github_metrics/run.py --start-date=$START_DATE --end-date=$END_DATE --filter-authors=tlillis > tlillis.txt
python github_metrics/run.py --start-date=$START_DATE --end-date=$END_DATE --filter-authors=kymccrohan> kymccrohan.txt
python github_metrics/run.py --start-date=$START_DATE --end-date=$END_DATE --filter-authors=ncrum > ncrum.txt

echo "Done"
