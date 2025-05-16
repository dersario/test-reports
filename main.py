import argparse
import json

from defs import AvgRate, PayoutReport, Report

parser = argparse.ArgumentParser(description="Files and type of report")
parser.add_argument("files", nargs="*", type=str, help="path to csv file")
parser.add_argument("--report", type=str, default="payout", help="name of report")
parser.add_argument("--type", type=str, default="payout", help="type of report")

my_args = parser.parse_args()
files = my_args.files


rep = Report()
columns = rep.standart_rate_name(open(files[0], "r").readline().rstrip().split(","))
data = []
for file in files:
    data.extend(rep.parse_data(file, columns))

match my_args.type:
    case "payout":
        rep = PayoutReport()
    case "avg":
        rep = AvgRate()


column_indexes = {column: i for i, column in enumerate(columns)}
report = rep.create_report(data, column_indexes, "department", default_columns=True)

with open(f"reports/{my_args.report}.json", "w") as file:
    file.write(json.dumps(report))
