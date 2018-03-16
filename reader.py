import sentence_pb2
import sys
import json

from google.protobuf.internal.encoder import _VarintBytes
from google.protobuf.internal.decoder import _DecodeVarint32

from google.protobuf.internal import decoder


def get_delimited_message_bytes(byte_stream, nr=4):
    ''' Parse a delimited protobuf message. This is done by first getting a protobuf varint from
    the stream that represents the length of the message, then reading that amount of
    from the message and then parse it.
    Since the int can be represented as max 4 bytes, first get 4 bytes and try to decode.
    The decoder returns the value and the position where the value was found, so we need
    to rewind the buffer to the position, because the remaining bytes belong to the message
    after.
    '''
    length_bites = byte_stream.read(nr)

    (length, pos) = decoder._DecodeVarint32(length_bites, 0)
    delimiter_bytes = nr - pos
 
    message_bytes = byte_stream.read(length - delimiter_bytes)

    total_len = length + pos
    return (total_len, length_bites[-delimiter_bytes:] + message_bytes)

while True:
    _, msg_buf = get_delimited_message_bytes(sys.stdin)
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

