import struct
from controller import Robot

from .Consts import ROBOTNAMES, NROBOTS

class DataReceiver:
    def __init__(self, robot: Robot, timestep: int) -> None:
        self.receiver = robot.getDevice("receiver")
        self.receiver.enable(timestep)

    def GetNewData(self) -> dict:
        packet = self.receiver.getData()
        self.receiver.nextPacket()

        return self.__ParseSuperVisorMsg(packet)

    def IsNewData(self) -> bool:
        return self.receiver.getQueueLength() > 0

    def __ParseSuperVisorMsg(self, packet: str) -> dict:
        struct_fmt = 'ddd' * NROBOTS + 'dd'

        unpacked = struct.unpack(struct_fmt, packet)

        data = {}
        for i, r in enumerate(ROBOTNAMES):
            data[r] = {
                "x": unpacked[3 * i],
                "y": unpacked[3 * i + 1],
                "orientation": unpacked[3 * i + 2]
            }
        data["ball"] = {
            "x": unpacked[3 * NROBOTS],
            "y": unpacked[3 * NROBOTS + 1]
        }
        return data