from hachoir_core.tools import (humanDatetime,
    timestampUNIX, timestampMac32, timestampWin64)
from hachoir_core.field import Bits, FieldSet
from datetime import datetime

class GenericTimestamp(Bits):
    def __init__(self, parent, name, size, description=None):
        Bits.__init__(self, parent, name, size, description)

    def createDisplay(self):
        return humanDatetime(self.value)

    def createRawDisplay(self):
        value = Bits.createValue(self)
        return unicode(value)

def timestampFactory(cls_name, handler, size):
    class Timestamp(GenericTimestamp):
        def __init__(self, parent, name, description=None):
            GenericTimestamp.__init__(self, parent, name, size, description)

        def createValue(self):
            value = Bits.createValue(self)
            return handler(value)
    cls = Timestamp
    cls.__name__ = cls_name
    return cls

TimestampUnix32 = timestampFactory("TimestampUnix32", timestampUNIX, 32)
TimestampMac32 = timestampFactory("TimestampUnix32", timestampMac32, 32)
TimestampWin64 = timestampFactory("TimestampWin64", timestampWin64, 64)

class TimestampMSDOS32(FieldSet):
    static_size = 32

    def createFields(self):
        # TODO: Create type "MSDOS_Second" : value*2
        yield Bits(self, "second", 5, "Second/2")
        yield Bits(self, "minute", 6)
        yield Bits(self, "hour", 5)
        yield Bits(self, "day", 5)
        yield Bits(self, "month", 4)
        # TODO: Create type "MSDOS_Year" : value+1980
        yield Bits(self, "year", 7, "Number of year after 1980")

    def createValue(self):
        return datetime(
            1980+self["year"].value, self["month"].value, self["day"].value,
            self["hour"].value, self["minute"].value, 2*self["second"].value)

    def createDisplay(self):
        return humanDatetime(self.value)

