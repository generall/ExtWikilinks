# encoding: utf-8

##
# This file is auto-generated. DO NOT EDIT!
#
require 'protobuf/message'


##
# Message Classes
#
class Position < ::Protobuf::Message; end
class Params < ::Protobuf::Message; end
class Context < ::Protobuf::Message; end
class Concept < ::Protobuf::Message; end
class Mention < ::Protobuf::Message; end
class Token < ::Protobuf::Message; end
class Sentence < ::Protobuf::Message; end


##
# Message Fields
#
class Position
  required :int32, :fromPos, 1
  required :int32, :toPos, 2
end

class Params
  optional :double, :sum_weight, 1
  optional :double, :avg_wight, 2
  optional :double, :max_wight, 3
  optional :int32, :word_count, 4
end

class Context
  required :int32, :size, 1
  optional :string, :left, 2
  optional :string, :right, 3
end

class Concept
  required :string, :link, 1
  optional :int32, :hits, 2
  optional :double, :avgScore, 3
  optional :double, :maxScore, 4
  optional :double, :minScore, 5
  optional :double, :avgNorm, 6
  optional :double, :avgSoftMax, 7
end

class Mention
  required :int32, :id, 1
  optional :string, :resolver, 2
  optional :string, :text, 3
  optional ::Position, :position, 4
  optional ::Params, :params, 5
  optional ::Context, :context, 6
  repeated ::Concept, :concepts, 7
end

class Token
  optional :string, :token, 1
  optional :string, :lemma, 2
  optional :string, :pos_tag, 3
  optional :string, :parserTag, 4
  optional :int32, :group, 5
  repeated :int32, :mentions, 6
end

class Sentence
  optional :string, :sent, 1
  repeated ::Mention, :mentions, 2
  optional :string, :parser_name, 3
  repeated ::Token, :parse_result, 4
  optional :string, :prevSentence, 5
  optional :string, :nextSentence, 6
end

