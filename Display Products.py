import pytest
from App import establish_connection, sales_distribution_analysis


def test_sales_distribution_analysis(db_connection):
    analysis = sales_distribution_analysis('B001')
    assert analysis is not None
