from ast import Pass
import asyncio, socket, json, threading
import game

Randomlist = ["Rock", "Paper", "Scissors"]
Room = [{"Player":None, "Punch":None, "Gamestage":None, "transport":None},
        {"Player":None, "Punch":None, "Gamestage":None, "transport":None}]

class GameServer(asyncio.Protocol):
    def __init__(self):
        self.callback = {"Role":None, "Stage":"None", "P2Stage": "None", "Punch":"", "Ans":None}

    def connection_made(self, transport):
        self.transport = transport
        self.address = transport.get_extra_info('peername')
        self.data = b''

        if Room[0]["Player"] and Room[1]["Player"] != None:
            self.transport.write(b'{"Stage":Roomfull}')
            
        if Room[0]["Player"] == None:
            self.callback["Role"] = 0
            Room[0]["Player"] = self.address
            Room[0]["transport"] = self.transport
        else:
            self.callback["Role"] = 1
            Room[1]["Player"] = self.address
            Room[1]["transport"] = self.transport

        print('Accepted connection from {}'.format(self.address))

    def data_received(self, data):

        data = data.decode("utf-8")
        self.data = json.loads(data)

        print(data, self.address)
        print(self.callback, self.address)
        #print("Room", Room)

        if self.data["Stage"] == "Again":
            Room[self.callback["Role"]]["Punch"] = None
            Room[self.callback["Role"]]["Ans"] = None
            Room[self.callback["Role"]]["P2Stage"] = None
            Room[self.callback["Role"]]["Stage"] = None

        if self.data["Punch"] != None:
            Room[self.callback["Role"]]["Punch"] = self.data["Punch"]
            self.callback["Punch"] = self.data["Punch"]
            return

        if Room[0]["Player"] == None or Room[1]["Player"] == None:
            self.callback["Stage"] = "WaitP2"
            Room[self.callback["Role"]]["Gamestage"] = "WaitP2"
            self.transport.write(json.dumps(self.callback).encode("utf-8"))

        if Room[0]["Player"] != None and Room[1]["Player"] != None:
            for i in Room:
                if i["Player"] != self.address:
                    if i["Gamestage"] == "WaitP2":
                        Room[self.callback["Role"]]["Gamestage"] = "WaitJoinP2"
                        self.callback["Stage"] = "WaitP2_button"
                        self.transport.write(json.dumps(self.callback).encode("utf-8"))
                    else:
                        if Room[self.callback["Role"]]["Gamestage"] != "WaitJoinP2":
                            for i in Room:
                                if i["Player"] != self.address:
                                    i["Gamestage"] = "JoinP2"
                                    send = {"Role": 1, "Stage": "JoinP2", "P2Stage": "JoinP2", "Punch":"None", "Ans":None}
                                    i["transport"].write(json.dumps(send).encode("utf-8"))
                        self.callback["Stage"] = "JoinP2"
                        self.callback["P2Stage"] = "JoinP2"
                        self.transport.write(json.dumps(self.callback).encode("utf-8"))

    def connection_lost(self, exc):
        if exc:
            print('Client {} error: {}'.format(self.address, exc))

            if Room[0]["Player"] == self.address :
                for key in Room[0]:
                    Room[0][key] = None
            else:
                for key in Room[1]:
                    Room[1][key] = None

        elif self.data:
            print('Client {} sent {} but then closed'
                  .format(self.address, self.data))
        else:
            print('Client {} closed socket'.format(self.address))

def RunServer():
    address = ("127.0.0.1", GetPort())
    loop = asyncio.get_event_loop()
    coro = loop.create_server(GameServer, *address)
    server = loop.run_until_complete(coro)
    print('Listening at {}'.format(address))
    try:
        loop.run_forever()
    finally:
        server.close()
        loop.close()

def GetPort():  
    sock = socket.socket()
    sock.bind(('', 0))
    port = sock.getsockname()[1]
    sock.close()
    return port

def Channel():
    while True:
        if Room[0]["Punch"] != None and Room[1]["Punch"] != None:
            rulest = game.RPSgame(Room[0]["Punch"], Room[1]["Punch"])
            P1back = {"Role":None, "Stage":"Rulest", "P2Stage": Room[1]["Punch"], "Punch":Room[0]["Punch"], "Ans":rulest["Player1"]}
            P2back = {"Role":None, "Stage":"Rulest", "P2Stage": Room[0]["Punch"], "Punch":Room[1]["Punch"], "Ans":rulest["Player2"]}
            Room[0]["transport"].write(json.dumps(P1back).encode("utf-8"))
            Room[1]["transport"].write(json.dumps(P2back).encode("utf-8"))
            Room[0]["Punch"] = None
            Room[1]["Punch"] = None
            Room[0]["Ans"] = None
            Room[1]["Ans"] = None


                


if __name__ == '__main__':
    Channel = threading.Thread(target = Channel)
    Channel.start()

    RunServer()