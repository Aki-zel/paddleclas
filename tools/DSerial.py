import serial  # 导入模块
import serial.tools.list_ports
import time

class DSerial:
    # 打开串口
    # 端口，GNU / Linux上的/ dev / ttyUSB0 等 或 Windows上的 COM3 等
    # 波特率，标准值之一：50,75,110,134,150,200,300,600,1200,1800,2400,4800,9600,19200,38400,57600,115200
    # 超时设置,None：永远等待操作，0为立即返回请求结果，其他值为等待超时时间(单位为秒）
    def __init__(self, bps, timeout):
        self.ser = None
        self.port = ""
        self.bps = bps
        self.timeout = timeout

    def set(self, portx, bps, timeout):
        self.ser = None
        self.port = portx
        self.bps = bps
        self.timeout = timeout

    def open(self):
        ret = False
        try:
            # 打开串口，并得到串口对象
            self.ser = serial.Serial(self.port, self.bps, timeout=self.timeout)
            # 判断是否打开成功
            if self.ser.is_open:
                ret = True
        except Exception as e:
            print("---异常---：", e)

        return ret

    # 写数据
    def DWritePort(self, text):
        time.sleep(0.5)
        text=text+'\\'
        result = self.ser.write(text.encode("gbk"))  # 写数据
        print(text.encode("gbk"))
        return result

    # 读数据
    def DReadPort(self):
        time.sleep(0.9)
        message = ""
        # 读取信息
        # while self.ser.in_waiting > 0:
        #     # STRGLO = self.ser.read(self.ser.in_waiting).decode("gbk")
        while self.ser.in_waiting >0:#如果等待队列有消息
            character = self.ser.read().decode("gbk")#单个字符地接收
            if character == '\n':
                break
            message += character
        if message != "":
            print("receive:"+message)
        return message

    # 发送抓取信息的函数
    def catchStuff(self, box_pos, type):
        # type 表示是对于储物柜还是对于格子
        # 1 表示当前是对于C区格子的抓取
        # 2 表示当前是对于A区格子的吸取
        # 3 表示当前是对于A区储物柜的吸取
        # 4 表示当前是对于D区格子的抓取
        # 5 表示当前是对于D区储物柜的抓取
        msg = ""
        if type == 1:
            msg = "m" + ("1" if box_pos == 2 else "2")
        elif type == 2:
            msg = "xm" + ("1" if box_pos == 2 else "2")
        elif type == 3:
            msg = "s" + str(box_pos)
        elif type == 4:
            if box_pos == 1 or box_pos == 4:
                msg = "d_l" + ("1" if box_pos == 1 else "2")
            elif box_pos == 2 or box_pos == 5:
                msg = "d_m" + ("1" if box_pos == 2 else "2")
            elif box_pos == 3 or box_pos == 6:
                msg = "d_r" + ("1" if box_pos == 3 else "2")
        elif type == 5:
            msg = "ss" + str(box_pos)
            
        return self.DWritePort(msg)
    
    # 发送放置信息的函数
    def putStuff(self, box_pos, type):
        # type 表示是对于储物柜还是对于格子
        # 1 表示当前是对于C区格子的抓取的放置
        # 2 表示当前是对于A区格子的吸取的放置
        # 3 表示当前是对于A区储物柜的吸取的放置
        # 5 表示当前是对于D区格子的抓取的放置
        # 4 表示当前是对于D区储物柜的抓取的放置
        # 6 表示当前是对于D区对AD钙的放置（特有）
        msg = ""
        if type == 1:
            msg = "m" + ("1" if box_pos == 2 else "2") + "_f"
        elif type == 2:
            msg = "xl" + ("1" if box_pos == 1 else "2") + "_f"
        elif type == 3:
            msg = "s" + str(box_pos) + "_f"
        elif type == 4:
            msg = "d_m" + ("1" if box_pos == 2 else "2") + "_f"
        elif type == 5:
            msg = "ss" + str(box_pos) + "_f"
        elif type == 6:
            msg = "ad_m2"

        return self.DWritePort(msg)

    # 发送推倒信息
    def fallStuff(self, position):
        if position != -1:
            msg = "t" + str(position)
            return self.DWritePort(msg)

    def goTo(self, position):
        msg = "go_" + str(position)
        return self.DWritePort(msg)

    def go(self):
        msg = "go"
        self.DWritePort(msg)
        while True:
            if self.DReadPort() == "GO_OK":
                return True
            
    def go_end(self):
        msg = "go_end"
        self.DWritePort(msg)
        while True:
            if self.DReadPort() == "END_OK":
                return True

    def capture(self, type):
        msg = "take_" + type
        self.DWritePort(msg)
        while True:
            if self.DReadPort() == "TAKE_OK":
                return True

    def overMsg(self):
        msg = "send_over"
        return self.DWritePort(msg)


    # 关闭串口
    def DClosePort(self):
        self.ser.close()

    def open_serial_port(self):
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            if p.pid is not None:
                try:
                    self.set(p.device, 115200, None)
                    ret = self.open()
                    # 是否成功实例化串口
                    if ret:
                        print("当前打开的端口为" + p.device)
                    return True
                except:
                    print("Error opening serial port.")
                    return False
        print("No serial port found.")
        return False

    def start(self, mission):
        msg = "start_"+mission
        self.DWritePort(msg)
        while True:
            if self.DReadPort() == "START_OK":
                return True
    def open_machine(self):
        while True:
            if self.DReadPort()=="READY":
                return True
            self.DWritePort("open")
            time.sleep(0.9)#0.1秒
# def DopenSer():
#     # 设置串口链接是否成功
#     ser = DSerial( 115200, None)
#     ret = False
#     while not ret:
#         # 检测本机现在连接的串口
#         port_list = list(serial.tools.list_ports.comports())
#         # 当他有返回值时
#         if len(port_list) != 0:
#             # 循环访问内部串口
#             for i in port_list:
#                 # 判断这个串口是否正常
#                 if i.pid is not None:
#                     # 实例化这个串口
#                     ser.set(i[0], 115200, None)
#                     ret = ser.open()
#                     # 是否成功实例化串口
#                     if ret:
#                         # 例子i[0]="com1"   i={"com1"."aa","bb"}
#                         print("当前打开的端口为" + i[0])
#                         return ser, ret
#     return None, False
