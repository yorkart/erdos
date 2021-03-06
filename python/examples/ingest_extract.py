"""Every second:
1) Send a number from the python script.
2) An operator squares the number.
3) The python script receives the result.
"""
import erdos
import time


class SquareOp(erdos.Operator):
    def __init__(self, read_stream, write_stream):
        read_stream.add_callback(self.callback, [write_stream])

    def callback(self, msg, write_stream):
        print("SquareOp: received {msg}".format(msg=msg))
        msg = erdos.Message(msg.timestamp, msg.data * msg.data)
        write_stream.send(msg)

    @staticmethod
    def connect(read_streams):
        return [erdos.WriteStream()]


def driver():
    ingest_stream = erdos.IngestStream()
    (square_stream, ) = erdos.connect(SquareOp, [ingest_stream])
    extract_stream = erdos.ExtractStream(square_stream)

    return ingest_stream, extract_stream


if __name__ == "__main__":
    ingest_stream, extract_stream = erdos.run_async(driver)

    count = 0
    while True:
        timestamp = erdos.Timestamp(coordinates=[count])
        send_msg = erdos.Message(timestamp, count)
        print("IngestStream: sending {send_msg}".format(send_msg=send_msg))
        ingest_stream.send(send_msg)
        ingest_stream.send(erdos.WatermarkMessage(timestamp))
        recv_msg = extract_stream.read()
        print("ExtractStream: received {recv_msg}".format(recv_msg=recv_msg))

        count += 1
        time.sleep(1)
