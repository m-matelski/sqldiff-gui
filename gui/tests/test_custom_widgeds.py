import unittest

import sqlparse

from gui.custom_widgets import SqlText


class TestSqlText(unittest.TestCase):
    def setUp(self) -> None:
        self.query1 = \
            "/* my super select query */\n" \
            "select\n" \
            "-- line comment \n" \
            "(case when round(tt.f_decimal_10) > 0.5 then 'NOT ZERO' else 'ZERO' end) " \
            "|| ' - ' || tt.f_varchar_10 as field_2\n" \
            "from test_db.test_table_1 tt"
        self.sql_text = SqlText()

    def test_parser(self):
        parsed = sqlparse.parse(self.query1)[0]
        # isinstance (token, sqlparse.sql.Comment) can be used if it is ken class (not type) name is in header
        a = 1
        self.assertTrue(True)

    def test_sql_text(self):
        t = [i for i in self.sql_text._get_tagged_tokens(self.query1)]
        self.assertTrue(True)
        a = 1
