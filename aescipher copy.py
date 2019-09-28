import os, random, struct, hashlib,json,sys
from Crypto.Cipher import AES
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

SCOREFILENAME = "gamescorestest.json"




def encrypt_file(key, in_filename, out_filename=None, chunksize=64*1024):
    """
    Encrypts a file using AES (CBC mode) with the given key.
    :param key: The encryption key - a string that must be either 16, 24 or 32 bytes long. Longer keys are more secure.
    :type key: string
    :param in_filename: Name of the input file
    :type in_filename: string
    :param out_filename: If None, '<in_filename>.enc' will be used.
    :type out_filename: string
    :param chunksize: Sets the size of the chunk which the function uses to read and encrypt the file. Larger chunk sizes can be faster for some files and machines. chunksize must be divisible by 16.
    :type chunksize: string
    :return: None
    """
    if not out_filename:
        out_filename = in_filename + '.enc'

    #iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    cipher = AES.new(key, AES.MODE_CFB) # CFB mode
    
    

    data = open(in_filename, "rb")
    ciphered_data = cipher.encrypt(data) # Only need to encrypt the data, no padding required for this mode


    file_out = open(out_filename, "wb")
    file_out.write(cipher.iv)
    file_out.write(ciphered_data)
    file_out.close()


    #    iv = 16 * b'\x00'
    #    encryptor = AES.new(key, AES.MODE_CFB, iv)
     #   filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
           # outfile.write(struct.pack('<Q', filesize))
           # outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += (' ' * (16 - len(chunk) % 16)).encode('utf8')

                outfile.write(encryptor.encrypt(chunk))


def decrypt_file(key, in_filename, out_filename=None, chunksize=24*1024):
    """
    Decrypts a file using AES (CBC mode) with the given key. 
    :param key: The encryption key - a string that must be either 16, 24 or 32 bytes long. Longer keys are more secure.
    :type key: string
    :param in_filename: Name of the input file
    :type in_filename: string
    :param out_filename: If None, '<in_filename> will be used.
    :type out_filename: string
    :param chunksize: Sets the size of the chunk which the function uses to read and encrypt the file. Larger chunk sizes can be faster for some files and machines. chunksize must be divisible by 16.
    :type chunksize: string
    :return: None
    """
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                print(str(chunk))
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origsize)


def encrypt_file_CFB(key, in_filename, out_filename=None):
    """
    Encrypts a file using AES (CBC mode) with the given key.
    :param key: The encryption key - a string that must be either 16, 24 or 32 bytes long. Longer keys are more secure.
    :type key: string
    :param in_filename: Name of the input file
    :type in_filename: string
    :param out_filename: If None, '<in_filename>.enc' will be used.
    :type out_filename: string
    :param chunksize: Sets the size of the chunk which the function uses to read and encrypt the file. Larger chunk sizes can be faster for some files and machines. chunksize must be divisible by 16.
    :type chunksize: string
    :return: None
    """
    if not out_filename:
        out_filename = in_filename + '.enc'

    #iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    cipher = AES.new(key, AES.MODE_CFB) # CFB mode
    
    

    f = open(in_filename, "rb")
    data =f.read()
    ciphered_data = cipher.encrypt(data) # Only need to encrypt the data, no padding required for this mode
    file_out = open(out_filename, "wb")
    file_out.write(cipher.iv)
    file_out.write(ciphered_data)
    file_out.close()

def decrypt_file_CFB(key, in_filename, out_filename=None):
    """
    Decrypts a file using AES (CBC mode) with the given key. 
    :param key: The encryption key - a string that must be either 16, 24 or 32 bytes long. Longer keys are more secure.
    :type key: string
    :param in_filename: Name of the input file
    :type in_filename: string
    :param out_filename: If None, '<in_filename> will be used.
    :type out_filename: string
    :param chunksize: Sets the size of the chunk which the function uses to read and encrypt the file. Larger chunk sizes can be faster for some files and machines. chunksize must be divisible by 16.
    :type chunksize: string
    :return: None
    """
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]


    file_in = open(in_filename, 'rb')
    iv = file_in.read(16)
    ciphered_data = file_in.read()
    file_in.close()

    cipher = AES.new(key, AES.MODE_CFB, iv=iv)
    original_data = cipher.decrypt(ciphered_data) # No need to un-pad
    return original_data

def read_highscore(key, in_filename, out_filename=None):
    """
    This function reads the highscore from json file.
    :return param: list with all highscore strings
    :return type: list
    """
    highscore_list = []
    file_in = open(in_filename, 'rb')
    iv = file_in.read(16)
    ciphered_data = file_in.read()
    file_in.close()

    cipher = AES.new(key, AES.MODE_CFB, iv=iv)
    original_data = cipher.decrypt(ciphered_data) # No need to un-pad
    cleartext=original_data.decode()
    data = json.loads(cleartext)
    for d in data:
        highscore_list.append('{:^13} {:^13} {:^13}'.format("Mode: "+d,"Player: "+ data[d][0]['player'],"Score: "+ str(data[d][0]['score'])))
    return highscore_list
    #with open(in_filename, 'rb') as infile:
    #    origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
    #    iv = infile.read(16)
    #    decryptor = AES.new(key, AES.MODE_CBC, iv)
#
 #       bcleartext = b''
#
 #       while True:
  #          chunk = infile.read(chunksize)
   #         if len(chunk) == 0:
    #            break
     #       bcleartext+=decryptor.decrypt(chunk)

      #  cleartext=bcleartext.decode()#'utf8')

      #  data = json.loads(cleartext)
      #  for d in data:
      #      highscore_list.append('{:^13} {:^13} {:^13}'.format("Mode: "+d,"Player: "+ data[d][0]['player'],"Score: "+ str(data[d][0]['score'])))
    #return highscore_list

def save_player_score(player,difficulty,point_counter,in_filename):#,out_filename):
    """
    This function saves the player score.
    :param player: string representing the game player
    :type player: string
    :param difficulty: string representing the game difficulty
    :type difficulty: string
    :param score: string representing the game highscore
    :type score: string
    :return: None
    """
    #try:
    #with open(in_filename, 'rb') as infile:
    #    origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
    #    iv = infile.read(16)
    #    decryptor = AES.new(key, AES.MODE_CBC, iv)
    #
     #   bcleartext = b''
#
 #       while True:
 #           chunk = infile.read(chunksize)
 #           if len(chunk) == 0:
 #               break
  #          bcleartext+=decryptor.decrypt(chunk)

#

 #   cleartext=bcleartext.decode()#'utf8')
  #  print('save: '+cleartext)
    file_in = open(in_filename, 'rb')
    iv = file_in.read(16)
    ciphered_data = file_in.read()
    file_in.close()

    cipher = AES.new(key, AES.MODE_CFB, iv=iv)
    original_data = cipher.decrypt(ciphered_data) # No need to un-pad
    cleartext=original_data.decode()
    data = json.loads(cleartext)

    if difficulty not in data:
        data[difficulty] = ([{'player':player,'score':point_counter}])       
        jdumpdata=json.dumps(data)
        data=jdumpdata.encode()#'utf8')
        
        os.remove("gamescorestest.json.enc")

        cipher = AES.new(key, AES.MODE_CFB) # CFB mode

        ciphered_data = cipher.encrypt(data) # Only need to encrypt the data, no padding required for this mode
        file_out = open(in_filename, "wb")
        file_out.write(cipher.iv)
        file_out.write(ciphered_data)
        file_out.close()

        #iv = 16 * b'\x00'
        #file_out = open(in_filename, "wb") # Open file to write bytes
        #file_out.write(iv) # Write the iv to the output file (will be required for decryption)
        #file_out.write(bdata) # Write the varying length cipher text to the file (this is the encrypted data)
        #file_out.close()

        #filesize = sys.getsizeof(bdata)
        #iv = 16 * b'\x00'
        #with open(in_filename, 'wb') as outfile:
        #    outfile.write(struct.pack('<Q', filesize))
        #    outfile.write(iv)
        #    while True:
        #        chunk = bdata[:chunksize]
        #        print("test: "+chunk.decode('utf8'))
        #        bdata = bdata[chunksize:]
        #        if len(chunk) == 0:
        #            break
        #        elif len(chunk) % 16 != 0:
        #            chunk += (' ' * (16 - len(chunk) % 16)).encode('utf8')
        #
        #        outfile.write(encryptor.encrypt(chunk))

        #with open(in_filename, 'wb') as outfile:
        #    outfile.write(struct.pack('<Q', bdata))
        #    #while True:
        #    #    chunk = bdata.read(chunksize)
            #    if len(chunk) == 0:
            #        break
        #    outfile.write(decryptor.decrypt(bdata))

    elif data[difficulty][0]['score'] < point_counter:
        data[difficulty][0]['score'] = point_counter
        data[difficulty][0]['player'] = player
        jdumpdata=json.dumps(data)
        data=jdumpdata.encode()

        
        cipher = AES.new(key, AES.MODE_CFB) # CFB mode

        ciphered_data = cipher.encrypt(data) # Only need to encrypt the data, no padding required for this mode
        file_out = open(in_filename, "wb")
        file_out.write(cipher.iv)
        file_out.write(ciphered_data)
        file_out.close()

        #os.remove("gamescorestest.json.enc")
        #iv = 16 * b'\x00'
        #file_out = open(in_filename, "wb") # Open file to write bytes
        #file_out.write(iv) # Write the iv to the output file (will be required for decryption)
        #file_out.write(bdata) # Write the varying length cipher text to the file (this is the encrypted data)
        #file_out.close()

#
 #       filesize = sys.getsizeof(bdata)+16
  #      print(filesize)
   #     print(len(bdata))
    #    filesize2 = len(bdata)+16
#
 #       iv = 16 * b'\x00'
  #      with open(in_filename, 'wb') as outfile:
   ##         outfile.write(struct.pack('<Q', filesize2))
     #       outfile.write(iv)
#
 #           while True:
  #              chunk = bdata[:16]
   ##             
     #           bdata = bdata[16:]
      #          if len(chunk) == 0:
           #         break
       #         elif len(chunk) % 16 != 0:
        #            chunk += (' ' * (16 - len(chunk))).encode('utf8')
         #       print(len(chunk))
         #       outfile.write(encryptor.encrypt(chunk))
         #   outfile.truncate(filesize2)

        
    #except Exception as e:
     #   print("Error while saving highscorelist: "+str(e))


buffer_size = 65536
password = 'kitty'.encode()
print(password)
#obj = AES.new('This is a key123'.encode("utf8"), AES.MODE_CBC, 'This is an IV456'.encode("utf8"))
key = hashlib.sha256(password).digest()
#print(key)
IV = 16 * b'\x00'
#IV.encode('utf8')       
mode = AES.MODE_CBC
encryptor = AES.new(key, mode, IV=IV)

text = b'j' * 64 + b'i' * 128
#text = text.encode('utf8')
ciphertext = encryptor.encrypt(text)

#print(ciphertext)
decryptor = AES.new(key, mode, IV=IV)
plain = decryptor.decrypt(ciphertext)


encrypt_file_CFB(key,'gamescorestest.json')
print(decrypt_file_CFB(key,'gamescorestest.json.enc'))
print(read_highscore(key,'gamescorestest.json.enc'))
save_player_score('script','MEDIUM',1500,'gamescorestest.json.enc')#,'gamescorestest001.json.enc')
print(read_highscore(key,'gamescorestest001.json.enc'))


#encrypt_file(key,'gamescorestest.json')
#print(read_highscore(key,'gamescorestest.json.enc'))
#print(read_highscore(key,'gamescorestest.json.enc'))
#save_player_score('script','MEDIUM',1500,'gamescorestest.json.enc')
#print(read_highscore(key,'gamescorestest.json.enc'))


#encrypt_file(key,'gamescorestest.json')
#decrypt_file(key,'gamescorestest.json.enc','decrypt.json')
#print('last: '+'''{"MULTI": [{"score": 400, "player": "wadf"}], "MEDIUM": [{"score": 1380, "player": "tassilo"}], "HARD": [{"score": 650, "player": "adsf"}], "EASY": [{"score": 2450, "player": " tas"}]}''')