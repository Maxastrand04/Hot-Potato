import socket, pygame, threading, json, requests
from settings import *
from debug import debug

class Server():
    def __init__(self, main_menu):

        # hämtar alla variabler från menyn
        self.main_menu = main_menu

        self.default_player_data = {
                'X': 2,
                'Y': 2,
                'init_X': 2,
                'init_Y': 2,
                'direction_X': 0,
                'direction_Y': 0, 
                'animation_index': 0,
                'status': 'idle',
                'hot_potato': False,
                'hot_potato_given': None
            }


        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 5050
        self.format = 'utf-8'
        self.this_is_host = None

        self.my_key = "{}:{}".format(self.host, self.port)
        self.host_key = "{}:{}".format(self.host, self.port)

        self.update = pygame.time.Clock()

        self.start_draw = False
        self.IP = self.get_public_ip()
        self.server = None
        self.server_shutdown = False
        self.unable_to_join = False

        self.IP_to_join = self.main_menu.input_text

    def get_public_ip(self):
        response = requests.get('https://api.ipify.org?format=json')
        ip = response.json()['ip']
        return ip

    def start_thread(self, function, arguments = None):
        if arguments == None: 
            threading.Thread(target=function).start()
        else:
            threading.Thread(target=function, args=arguments).start()

# SERVER SIDAN 
    def start_listen(self):
        
        # Startar servern och lyssnar efter anslutningar
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.this_is_host = True

        self.server.bind((self.host, self.port))
        self.server.listen()

        # Börjar rita spelet
        self.start_draw = True


        # Lägger till Hosten som en spelare
        players[self.host_key] = self.default_player_data

        try:
            while True:

                client, addr = self.server.accept()

                print('New connection from {}'.format(addr))
                
                # Lägger till den tillagda klienten som en spelare
                client_key = '{}:{}'.format(addr[0], addr[1])
                players[client_key] = self.default_player_data
                
                # Skickar den initiala datan till spelaren
                init_data = json.dumps(players)
                client.send(init_data.encode(self.format))

                players[self.my_key]['hot_potato'] = True

                self.start_thread(self.handle_client, (client, addr))
        
        except:
            self.server.close()

    def handle_client(self, client, addr):

        client_key = '{}:{}'.format(addr[0], addr[1])
        
        while True:
            if self.server_shutdown:
                self.send_data(client, client_key, True)
                break

            self.send_data(client, client_key)

            self.update.tick(SERVER_UPDATE)
        
        
        client.close()

    def send_data(self, client, key, server_closed = False):
        # Börjar med att ta emot
        data_upd = client.recv(1024)

        if not server_closed:

            #Sparar serverns information om hot potato innan den överskriver informationen
            hot_potato = players[key]['hot_potato']

            if not data_upd:
                client.close()
            else:
                data_upd = data_upd.decode(self.format)
                data_upd = json.loads(data_upd)
                players[key] = data_upd

                #Ändrar hot potato till det som servern anser är korrekt
                players[key]['hot_potato'] = hot_potato

                if players[key]['hot_potato_given'] != None:
                    players[players[key]['hot_potato_given']]['hot_potato'] = True
                    players[key]['hot_potato_given'] = None
                    players[key]['hot_potato'] = False

            # Därefter skickar vidare
            json_data = json.dumps(players)
            client.send(json_data.encode(self.format))
        
        else:
            client.send(SERVER_CLOSED.encode(self.format))
    
    def close_server(self):
        pass



# KLIENT SIDAN AV SERVERN
    def join_server(self):
        connected = False
        while True:
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((self.IP_to_join, self.port))

                connected = True

            except:
                self.unable_to_join = True
                break

            if connected == True:

                # Lägger till denna klient som en spelare
                self.my_key = '{}:{}'.format(client.getsockname()[0], client.getsockname()[1])
                
                self.start_thread(self.handle_conn, (client,))

                break

    def handle_conn(self, client):


        # Hämtar allas postion från servern
        init_data = client.recv(1024)

        if not init_data:
            client.close()
        else:
            init_data = init_data.decode(self.format)
            init_data = json.loads(init_data)
            for player, values in init_data.items():
                players[player] = values

        # Körs sedan för att uppdatera bilden

        self.start_draw = True
        while True:
            self.get_data(client)

            self.update.tick(SERVER_UPDATE)

            if self.server_shutdown:
                break
        
        client.close()

    def get_data(self, client):

        #Börjar med att skicka värden
        if self.my_key:

            data_to_send = players[self.my_key]
            json_data_123123 = json.dumps(data_to_send)
            client.send(json_data_123123.encode(self.format))

            if players[self.my_key]['hot_potato_given']!= None:
                players[self.my_key]['hot_potato_given'] = None


            # Därefter tar emot värden
            get_data = client.recv(1024)

            if not get_data:
                client.close()
            else:
                get_data = get_data.decode(self.format)
                
                if get_data == SERVER_CLOSED:
                    self.server_shutdown = True
                    return
                
                get_data = json.loads(get_data)

                for player, values in get_data.items():
                    if not player == self.my_key:
                        players[player] = values
                    else:
                        if values['hot_potato'] == True:
                            players[player]['hot_potato'] = True                                            

