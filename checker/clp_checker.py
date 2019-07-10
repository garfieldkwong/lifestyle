"""Checker for clp bill"""
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
            '賬單/CLP',
            (re.compile(
                r'.*繳款到期日 (.*) 感謝您上期的付款 \$([0-9\.]*)，.*'
            ), 2, 1),
            '%d/%m/%Y'
        )
