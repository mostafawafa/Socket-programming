import socket
import subprocess, os
from PIL import Image
import PIL
import scipy.misc
import numpy
from PyQt4.uic import loadUiType
from PyQt4.QtGui import *
Ui_MainWindow, QMainWindow = loadUiType('clientGUI.ui')

class Client(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(Client, self).__init__()
        self.setupUi(self)

        self.connexion_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP connection
        self.connexion_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #prevent timeout

        self.pushButton.clicked.connect(self.browse_img)
        ##self.pushButton_2.clicked.connect(self.connect)# for sending it to server
        self.pushButton_2.clicked.connect(self.edit_image)
        self.pushButton_3.clicked.connect(self.save_img)



    def connect(self):
        self.host = "127.0.0.1" #ip server
        self.port = 12345 #port server
        self.connexion_socket.connect((self.host, self.port))
        print("\n[*] Connected to " + self.host + " on port " + str(self.port) + ".\n")




    def edit_image(self):
        #to determine the effect which the clint want
        if self.radioButton.isChecked() == True:
            self.action=1
        if self.radioButton_2.isChecked() == True:
            self.action=2
        if self.radioButton_3.isChecked() == True:
            self.action=3
        if self.radioButton_4.isChecked() == True:
            self.action=4
        if self.radioButton_5.isChecked() == True:
            self.action=5

        # read 1024 bytes at each iteration so we don't overflow the receiver buffer
        self.connexion_socket.send(str(self.action)) #send to server
        #..................................................................


        img1 = open(self.filepath, 'rb')
        data = img1.read(1024)

        # add "done" at the end of our data to make the server stop waiting for more bytes
        while (data != ''):
            self.connexion_socket.send(data)
            data = img1.read(1024)

        self.connexion_socket.send('done')

        img1.close()

        #  waiting for the edited img from the server
        #while True:
            #data = self.connexion_socket.recv(1024)
        if(os.path.isfile('filtred.png')):
            os.remove('filtred.png')
    #___________________________________________________________________________________________________
        img_filtered = open('filtred.png', 'ab')
        self.returned_data = self.connexion_socket.recv(1024)
        while True:
            if self.returned_data.endswith('done'):
                img_filtered.write(self.returned_data[:-4])
                break

            img_filtered.write(self.returned_data)
            self.returned_data = self.connexion_socket.recv(1024)

        img_filtered.close()

        #self.connexion_socket.close()
        pixmap = QPixmap('filtred.png')
        self.label_2.setPixmap(pixmap)
        print('Succeeded!')

            #exit()

    def browse_img(self):
        self.flag1 = 1
        self.filepath = QtGui.QFileDialog.getOpenFileName(self, 'Single File', "Desktop", '*.jpg')

        self.name = str(self.filepath)
        if self.name != "":
            pixmap = QPixmap(self.filepath)
            self.label.setPixmap(pixmap)
            #img = open(self.name, 'rb')



    def save_img(self):
        name = QtGui.QFileDialog.getSaveFileName(self, 'Save Point', "Desktop", '*.jpg')
        #file = open(name, "w")
        filee = str(name)

        I = numpy.asarray(PIL.Image.open('filtred.png'))

        scipy.misc.imsave(filee,I )





if __name__ == "__main__":
    import sys
    from PyQt4 import QtGui


    try:
        app = QtGui.QApplication(sys.argv)
        our_client = Client()
        our_client.show()
        our_client.connect()

        sys.exit(app.exec_())
        #our_client.edit_image()

    except KeyboardInterrupt:
        exit('\ninterrupted\n')
