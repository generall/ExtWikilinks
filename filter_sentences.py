"""
This script should filter trash sentences
"""

import sys
import re

input_filename = sys.argv[1]
output_filename = sys.argv[2]

def check_mention(mention):
    word_count = mention.count(' ')
    if word_count > 3:
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

def convert_concept(concept):
    concept = concept.strip('><')
    m = re.search(r'/([^/]+)$', concept)
    if m:
        concept = m.groups()[0]
    else:
        concept = ''
    return concept

redirects = {}
with open('./cleaned_redirects.tsv') as fd:
    for line in fd:
        from_c, to_c = line.strip().split('\t')
        redirects[from_c] = to_c


with open(input_filename) as inp:
    with open(output_filename, 'w') as out:
        for line in inp:
            left_context, mention_text, mention_link, right_context = line.split('\t')

            passed = True

            passed &= check_mention(mention_text)

            if len(left_context) + len(right_context) < 10:
                passed = False

            concept = convert_concept(mention_link)
            concept = redirects.get(concept, concept)

            if passed:
                out.write("\t".join([concept, left_context, mention_text, right_context]))

