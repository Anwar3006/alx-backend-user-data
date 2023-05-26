#!/usr/bin/env python3
"""
Regex-ing
"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    filter_datum that returns the log message obfuscated:

    Parameters
    ____________
    Arguments:
    fields: a list of strings representing all fields to obfuscate
    redaction: a string representing by what the field will be obfuscated
    message: a string representing the log line
    separator: a string representing by which character is separating all
    fields in the log line (message)

    Return:
    """
    for field in fields:
        reg_Ex = r"" + field + r"=([^" + separator + r"]+)"
        found = re.search(reg_Ex, message)
        message = re.sub(found.group(1), redaction, message)
    return message
