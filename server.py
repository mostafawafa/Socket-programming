import socket
import Filter
from thread import start_new_thread
import os


class Server:

    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # creates server TCP socket
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # prevents from getting timeout issues
        self.server_socket.bind((self.host,self.port))


    def listen(self):
        self.server_socket.listen(5)
        print("\n[*] Listening on port " + str(self.port) + ", waiting for connections.")
        while True:
            client_connection, (client_ip, client_port) = self.server_socket.accept()
            print("[*] Client " + client_ip + " connected.\n")
            start_new_thread(self.client_socket, (client_connection,))


    def client_socket(self,client_connection):

        #the first thing we recieve from any client is the type of edit

        self.edit_type = client_connection.recv(1024)

        print self.edit_type


        while True:

            img = open('filtred.jpg', 'ab')
            data = client_connection.recv(1024)
            while True:
                #check if client send all data
                if data.endswith('done'):
                    img.write(data[:-4])
                    break

                img.write(data)

                data = client_connection.recv(1024)

            img.close()

            # we select the appropriate filter according to client input
            self.filter_selection()

            # return the image to the client ( After editing!)
            img = open('edited.png', 'rb')
            data = img.read(1024)
            while (data != ''):
                client_connection.send(data)
                data = img.read(1024)

            client_connection.send('\ndone')
            img.close()
            client_connection.close()

            # remove all the files which we created in the server, because we will deal with many images from many clients and
            # it's a SERVER NOT GALLERY

            os.remove('filtred2.jpg')
            os.remove('edited2.jpg')

            break

    # method which return the correct filter, there're little conditions so we use if
    # if we have more conditions, we'll need to use another method ( like Factory design pattern)
    def filter_selection(self):

        filtered_img = Filter.Filter('filtred.jpg')

        if self.edit_type == '1':
            filtered_img.crop().save('edited.png')
        elif self.edit_type == '2':
            filtered_img.blur().save('edited.png')
        elif self.edit_type == '3':
            filtered_img.blackwhite().save('edited.png')
        elif self.edit_type == '4':
            filtered_img.border().save('edited.png')
        elif self.edit_type == '5':
            filtered_img.remove_color('red').save('edited.png')




if __name__ == "__main__":

    try:
        our_client = Server(" 127.0.0.1", 12345)
        our_client.listen()

    except KeyboardInterrupt:
        exit('\ninterrupted\n')