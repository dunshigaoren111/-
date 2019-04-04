import socketserver
from attention_test import mainx

HOST,PORT="localhost",9999


class TCPHandler(socketserver.BaseRequestHandler):
    # 一个连接调用一次handle()
    def handle(self):
        print("已经连接！")
        while 1:
            try:
                data=self.request.recv(1024).strip()#接受数据
                ip= self.client_address[0]
                data = data.decode('utf-8')
                print("接受的数据是：",data)
                data_list = []
                for i in range(len(data)):
                    data_list.append(data[i])
                data_list.append("<eos>")
                data=" ".join(data_list)
                print(data)
                data=mainx(data)
                data=data+"\n"
                self.request.sendall(bytes(data,encoding="utf-8"))

            except ConnectionResetError as e:
                print("客户端连接断开。")
                break
            except ConnectionAbortedError as x:
                print("客户端连接断开。")
                break




if __name__=="__main__":
    print("从"+str(HOST)+" "+str(PORT)+"开始等待连接……")
    server=socketserver.ThreadingTCPServer(("10.206.15.132",PORT),TCPHandler)
    server.serve_forever()