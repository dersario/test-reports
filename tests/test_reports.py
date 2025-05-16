import pytest

from defs import AvgRate, PayoutReport, Report


@pytest.fixture
def sample_csv_data():
    return (
        "id,name,email,department,hours_worked,salary\n"
        "1,John,john@example.com,IT,40,20\n"
        "2,Jane,jane@example.com,HR,35,30\n"
    )

def test_standart_rate_name_replaces_salary():
    columns = ["id", "name", "email", "department", "hours_worked", "salary"]
    updated = Report().standart_rate_name(columns.copy())
    assert "rate" in updated
    assert updated.index("rate") == columns.index("salary")


def test_standart_rate_name_keeps_columns_if_no_rate_match():
    columns = ["id", "name", "email", "department", "hours_worked", "wage"]
    updated = Report().standart_rate_name(columns.copy())
    assert "rate" not in updated
    assert updated == columns


def test_parse_data(monkeypatch, sample_csv_data):
    def mock_open(*args, **kwargs):
        from io import StringIO

        return StringIO(sample_csv_data)

    monkeypatch.setattr("builtins.open", mock_open)

    expected_columns = ["id", "name", "email", "department", "hours_worked", "rate"]
    data = Report().parse_data("fake.csv", expected_columns)

    assert len(data) == 2
    assert data[0] == ["1", "John", "john@example.com", "IT", "40", "20"]
    assert data[1][1] == "Jane"


def test_payout_report_default_columns():
    columns = ["id", "name", "email", "department", "hours_worked", "rate"]
    indexes = {col: i for i, col in enumerate(columns)}
    employees = [
        ["1", "John", "john@example.com", "IT", "40", "20"],
        ["2", "Jane", "jane@example.com", "HR", "35", "30"],
    ]

    result = PayoutReport().create_report(employees, indexes, default_columns=True)

    assert len(result) == 2
    assert result[0]["name"] == "John"
    assert result[0]["payout"] == 800
    assert result[1]["payout"] == 1050


def test_avg_rate_report():
    columns = ["id", "name", "email", "department", "hours_worked", "rate"]
    indexes = {col: i for i, col in enumerate(columns)}
    employees = [
        ["1", "John", "john@example.com", "IT", "40", "20"],
        ["2", "Jane", "jane@example.com", "IT", "35", "30"],
        ["3", "Bob", "bob@example.com", "HR", "30", "50"],
    ]

    result = AvgRate().create_report(employees, indexes)

    assert isinstance(result, list)
    assert result[0]["IT"] == 25.0
    assert result[0]["HR"] == 50.0
