"""
This script should filter trash mentions
"""

import sys
import re

input_filename = sys.argv[1]
output_filename = sys.argv[2]


def check_mention(mention):
    word_count = mention.count(' ')
    if word_count > 2:
        return False

    length = len(mention)

    if length > 50:
        return False

    numbers = sum(c.isdigit() for c in mention)
    chars = sum(c.isalpha() for c in mention)
    other = length - numbers - chars

    if numbers > chars:
        return False

    if other > chars:
        return False

    if re.match(r'^[\s\d\w\-\,]*$', mention) is None:
        return False

    return True

with open(input_filename) as inp:
    with open(output_filename, 'w') as out:
        for line in inp:
            if check_mention(line):
                out.write(line)
