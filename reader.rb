require_relative "sentence.pb.rb"

class ExtWikilinksReader

  def self.read_sentence(stream)
    return nil if stream.eof?
    length = Protobuf::Varint.decode(stream)
    Sentence.decode(stream.read(length))
  end

  def self.write_sentence(stream, snt)
    byte_data = snt.encode
    stream << "#{Protobuf::Field::VarintField.encode(byte_data.size)}#{byte_data}"    
  end

end

