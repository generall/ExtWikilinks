import sentence_pb2
import sys
import json

from google.protobuf.internal.encoder import _VarintBytes
from google.protobuf.internal.decoder import _DecodeVarint32

buf = sys.stdin.read()
n = 0
while n < len(buf):
    msg_len, new_pos = _DecodeVarint32(buf, n)
    n = new_pos
    msg_buf = buf[n:n+msg_len]
    n += msg_len
    sentence = sentence_pb2.Sentence()
    sentence.ParseFromString(msg_buf)

    mention_link = ''
    mention_text = ''
    left_context = ''
    right_context = ''

    for mention in sentence.mentions:
        if mention.resolver == 'wikilink':
            mention_link = mention.concepts[0].link
            mention_text = mention.text

            left_context = mention.context.left
            right_context = mention.context.right
            break
    
    print("\t".join([
        left_context,
        mention_text,
        mention_link,
        right_context
    ]))
