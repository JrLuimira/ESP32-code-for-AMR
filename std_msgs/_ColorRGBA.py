import ustruct as struct
from ugenpy.message import Message
class ColorRGBA(Message):
            _md5sum = "a29a96539573343b1310c73607334b00"
            _type = "std_msgs/ColorRGBA"
            _has_header = False
            _full_text = '''float32 r
float32 g
float32 b
float32 a'''

            __slots__ = ['r','g','b','a']
            _slots_types = ['float32','float32','float32','float32']        
            
            def __init__(self, *args, **kwds):
            
                if args or kwds:
                    super(ColorRGBA, self).__init__(*args, **kwds)

                    if self.float32 is None:
                        self.float32 = 0.
                    if self.float32 is None:
                        self.float32 = 0.
                    if self.float32 is None:
                        self.float32 = 0.
                    if self.float32 is None:
                        self.float32 = 0.
            
            def _get_types(self):
                return self._slot_types
            
            def serialize(self, buff):
                try:
                    buff.write(struct.pack('<f',self.r))
                    buff.write(struct.pack('<f',self.g))
                    buff.write(struct.pack('<f',self.b))
                    buff.write(struct.pack('<f',self.a))
                except Exception as e:
                    print(e)
            
            def deserialize(self, str):
                try:
                    end = 0
                    start = end
                    end += 4
                    (self.r,) = struct.unpack('<f', str[start:end])
                    start = end
                    end += 4
                    (self.g,) = struct.unpack('<f', str[start:end])
                    start = end
                    end += 4
                    (self.b,) = struct.unpack('<f', str[start:end])
                    start = end
                    end += 4
                    (self.a,) = struct.unpack('<f', str[start:end])
                    return self
                except Exception as e:
                    print(e)