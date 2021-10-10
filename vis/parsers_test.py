import unittest
import parsers
from datetime import datetime

class TestParsersMethods(unittest.TestCase):

    def test_where_conditions(self):
        integrantes_dict= {'user': [84, 36, 847, 232, 869]}
        expected_where_conditions = ' pbla_uid = 84 OR pbla_uid = 36 OR pbla_uid = 847 OR pbla_uid = 232 OR pbla_uid = 869'
        self.assertEqual(parsers.where_conditions(integrantes_dict), expected_where_conditions)

    def test_timestamp_parser(self):
        timestamp_passed = '2018-12-24T12:33:35.145Z'
        expected_datetime = datetime(2018, 12, 24, 12, 33, 35, 145000 )
        self.assertEqual(parsers.timestamp_parser(timestamp_passed), expected_datetime)