class Report:
    def standart_rate_name(self, columns: list[str]) -> list[str]:
        rate_vars = ["rate", "hourly_rate", "salary"]
        for var in rate_vars:
            try:
                rate_index = columns.index(var)
                columns[rate_index] = "rate"
                return columns
            except ValueError:
                continue
        return columns

    def parse_data(self, path: str, columns_target: list[str]) -> list[list]:
        with open(path, "r") as file:
            columns_head = self.standart_rate_name(file.readline().rstrip().split(","))
            employees = []
            for line in file:
                columns = line.rstrip().split(",")
                employees.append(
                    [columns[columns_head.index(column)] for column in columns_target]
                )
        return employees

    def create_report():
        pass


class PayoutReport(Report):
    def create_report(
        self,
        employees: list[list],
        indexes: dict,
        *args: str,
        default_columns: bool = False,
    ) -> list[dict]:
        """print colums from payout report\n
        variants of columns:\n
            - id
            - email
            - name
            - department
            - hours_worked
            - rate
            - payout"""
        args = list(args)
        if not len(args) or default_columns:
            args.extend(["name", "payout"])
        for employee in employees:
            payout = int(employee[indexes["rate"]]) * int(
                employee[indexes["hours_worked"]]
            )
            employee.append(payout)
        fields_with_payout = indexes.copy()
        fields_with_payout.update({"payout": len(indexes)})
        json_employees = [
            {arg: employee[fields_with_payout[arg]] for arg in args}
            for employee in employees
        ]
        return json_employees


class AvgRate(Report):
    def create_report(self, employees: list[list], indexes: dict) -> list[dict]:
        sum_rates = {}
        counts = {}
        for employee in employees:
            department = employee[indexes["department"]]
            if department in sum_rates:
                sum_rates[department] += int(employee[indexes["rate"]])
                counts[department] += 1
            else:
                sum_rates[department] = int(employee[indexes["rate"]])
                counts[department] = 1
        avg_rates = sum_rates.copy()
        for key in sum_rates.keys():
            avg_rates[key] = round(avg_rates[key] / counts[key], 1)
        return [avg_rates]
