import os,json, hashlib
from Crypto.Cipher import AES

"""
This modul contains the methods to read and write to the aes encrypted highscore file.
"""

def encrypt_file_CFB(key, in_filename, out_filename=None):
    """
    Encrypts a file using AES (CFB mode) with the given key.
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
    cipher = AES.new(key, AES.MODE_CFB) 

    f = open(in_filename, "rb")
    data =f.read()
    ciphered_data = cipher.encrypt(data) 
    file_out = open(out_filename, "wb")
    file_out.write(cipher.iv)
    file_out.write(ciphered_data)
    file_out.close()

def decrypt_file_CFB(key, in_filename, out_filename=None):
    """
    Decrypts a file using AES (CFB mode) with the given key. 
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
    original_data = cipher.decrypt(ciphered_data)
    return original_data

def read_highscore(key, in_filename):
    """
    This function reads the highscore from the aes encrypted json file.
    :param key: bstring representing aes key, 32 bytes long.
    :type key: bstring
    :param in_filename: filename to read from
    :type in_filename: string
    :return param: list with all highscore strings
    :return type: list
    """
    try:
        highscore_list = []
        file_in = open(in_filename, 'rb')
        iv = file_in.read(16)
        ciphered_data = file_in.read()
        file_in.close()

        cipher = AES.new(key, AES.MODE_CFB, iv=iv)
        original_data = cipher.decrypt(ciphered_data)
        cleartext=original_data.decode()
        data = json.loads(cleartext)
        for d in data:
            highscore_list.append('{:^13} {:^13} {:^13}'.format("Mode: "+d,"Player: "+ data[d][0]['player'],"Score: "+ str(data[d][0]['score'])))
        return highscore_list
    except:
        print("read error")

def save_player_score(player,difficulty,point_counter,key,in_filename):
    """
    This function saves the player score. decryps the file, checks for a new highscore and encrypts it again.
    :param player: string representing the game player
    :type player: string
    :param difficulty: string representing the game difficulty
    :type difficulty: string
    :param point_counter: string representing the game highscore
    :type point_counter: string
    :param key: bstring representing aes key, 32 bytes long.
    :type key: bstring
    :param in_filename: filename to read from
    :type in_filename: string
    :return: None
    """
    try:
        file_in = open(in_filename, 'rb')
        iv = file_in.read(16)
        ciphered_data = file_in.read()
        file_in.close()

        cipher = AES.new(key, AES.MODE_CFB, iv=iv)
        original_data = cipher.decrypt(ciphered_data)
        cleartext=original_data.decode()
        data = json.loads(cleartext)

        if difficulty not in data:
            data[difficulty] = ([{'player':player,'score':point_counter}])       
            jdumpdata=json.dumps(data)
            data=jdumpdata.encode()
            cipher = AES.new(key, AES.MODE_CFB)
            ciphered_data = cipher.encrypt(data)
            file_out = open(in_filename, "wb")
            file_out.write(cipher.iv)
            file_out.write(ciphered_data)
            file_out.close()

        elif data[difficulty][0]['score'] < point_counter:
            data[difficulty][0]['score'] = point_counter
            data[difficulty][0]['player'] = player
            jdumpdata=json.dumps(data)
            data=jdumpdata.encode()
            cipher = AES.new(key, AES.MODE_CFB) 
            ciphered_data = cipher.encrypt(data) 
            file_out = open(in_filename, "wb")
            file_out.write(cipher.iv)
            file_out.write(ciphered_data)
            file_out.close()
    except:
        print("Saving error")