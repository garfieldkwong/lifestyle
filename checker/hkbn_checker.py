"""Checker for hkbn"""
import re
from . import gmail_checker


class Checker(gmail_checker.Checker):
    """CLP checker"""
    def __init__(
        self, creds_filename
    ):
        """Init"""
        super().__init__(
            creds_filename,
            '賬單/HKBN 賬單',
            (re.compile(
                r'.*本期應繳賬項.*(\$[0-9]+(\.[0-9]*)?).*'
                r'到期繳款日.*([0-9]{4}\/[0-9]{2}\/[0-9]{2}).*'
            ), 1, 3),
            '%Y/%m/%d'
        )
