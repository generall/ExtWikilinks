from fuzzywuzzy import fuzz

prev_right_context = ""
prev_left_context = ""
 

import sys
import re

input_filename = sys.argv[1]
output_filename = sys.argv[2]

threshold = 70

with open(input_filename) as inp:
    with open(output_filename, 'w') as out:

        for line in inp:

            if line.count('\t') != 3:
                continue

            passed = True

            concept, left_context, mention_text, right_context = line.split('\t')

            fuzzy_ratio = fuzz.ratio(left_context, prev_left_context) 
            if fuzzy_ratio > threshold:
                passed = False
            
            fuzzy_ratio = fuzz.ratio(right_context, prev_right_context)
            if fuzzy_ratio > threshold:
                passed = False

            prev_right_context = right_context
            prev_left_context = left_context

            if passed:
                out.write("\t".join([concept, left_context, mention_text, right_context]))