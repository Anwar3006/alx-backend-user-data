import re


def filter_datum(fields, redaction, message, separator):
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
    found_items = []
    for field in fields:
        reg_Ex = r"" + field + r"=([^" + separator + r"]+)"
        found = re.search(reg_Ex, message)
        if found:
            found_items.append(found.group(1))
    for word in range(len(found_items)):
        if found_items[word] in message:
            message = message.replace(found_items[word], redaction)
    return message
