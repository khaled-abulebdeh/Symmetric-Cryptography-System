import requests
import re

URL = "https://triple-des-server.onrender.com/encrypt"

SHIFT_SCHEDULE = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

Final_P = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
] 

PC2 = [x - 1 for x in [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]]

PC1_Left = [
    49, 42, 35, 28, 21, 14, 7,
    0, 50, 43, 36, 29, 22, 15,
    8, 1, 51, 44, 37, 30, 23,
    16, 9, 2, 52, 45, 38, 31
]

PC1_Right = [
    55, 48, 41, 34, 27, 20, 13,
    6, 54, 47, 40, 33, 26, 19,
    12, 5, 53, 46, 39, 32, 25,
    18, 11, 4, 24, 17, 10, 3
]

expansion_table = [
        32, 1, 2, 3, 4, 5,
         4, 5, 6, 7, 8, 9,
         8, 9,10,11,12,13,
        12,13,14,15,16,17,
        16,17,18,19,20,21,
        20,21,22,23,24,25,
        24,25,26,27,28,29,
        28,29,30,31,32, 1
    ]

Initial_P = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

S_BOXES = [
    [ 
        [14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
        [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
        [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
        [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]
    ],
    [  
        [15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
        [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
        [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
        [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]
    ],
    [  
        [10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
        [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
        [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
        [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]
    ],
    [ 
        [7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
        [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
        [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
        [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]
    ],
    [  
        [2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
        [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
        [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
        [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]
    ],
    [  
        [12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
        [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
        [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
        [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]
    ],
    [  
        [4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
        [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
        [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
        [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]
    ],
    [  
        [13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
        [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
        [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
        [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]
    ]
]

P_box = [
        16, 7, 20, 21,
        29, 12, 28, 17,
        1, 15, 23, 26,
        5, 18, 31, 10,
        2, 8, 24, 14,
        32, 27, 3, 9,
        19, 13, 30, 6,
        22, 11, 4, 25
    ]

def key_generator(key_64bit):

    parity_indices = [7, 15, 23, 31, 39, 47, 55, 63]
    key_56bit = [bit for i, bit in enumerate(key_64bit) if i not in parity_indices]
    left = [key_56bit[i] for i in PC1_Left]
    right = [key_56bit[i] for i in PC1_Right]

    subkeys = []

    for round_num in range(16):
        shifts = SHIFT_SCHEDULE[round_num]
        right = right[shifts:] + right[:shifts]
        left = left[shifts:] + left[:shifts]

        combined = left + right

        subkey = [combined[i] for i in PC2]
        subkeys.append(subkey)

    return subkeys

def des_expansion(input_32bit):
    output_48bit = [input_32bit[i - 1] for i in expansion_table]
    return output_48bit

def xor_48bit(First, Second):
        return [f ^ s for f, s in zip(First, Second)]

def P_box_DES(input_32bit):
    output = [input_32bit[i - 1] for i in P_box]
    return output

def S_Box(input_48bit_list):

    output_bits = []
    
    for i in range(8):
        block_bits = input_48bit_list[i*6:(i+1)*6]

        row = (block_bits[0] << 1) | block_bits[5]
        col = (block_bits[1] << 3) | (block_bits[2] << 2) | (block_bits[3] << 1) | block_bits[4]

        sbox_val = S_BOXES[i][row][col]

        sbox_bits = [(sbox_val >> j) & 1 for j in reversed(range(4))]  
        output_bits.extend(sbox_bits)

    return output_bits

def initial_permutation(plaintext_64bit):
    return [plaintext_64bit[i - 1] for i in Initial_P]

def final_permutation(data_64bit):
    return [data_64bit[i - 1] for i in Final_P]

def DES_Encrypt(plaintext_64bit, subkeys):
    
    data = initial_permutation(plaintext_64bit)
    
    left = data[:32]
    right = data[32:]
    
    for i in range(16):
        expanded_right = des_expansion(right)
        xored = xor_48bit(expanded_right, subkeys[i])
        sbox_output = S_Box(xored)
        pbox_output = P_box_DES(sbox_output)
        new_right = xor_48bit(left, pbox_output)
        left = right
        right = new_right
    
    combined = right + left
    
    ciphertext = final_permutation(combined)
    return ciphertext

def bits_to_hex(bits_list):
    binary_str = ''.join(str(bit) for bit in bits_list)
    
    padding = (4 - (len(binary_str) % 4)) % 4
    binary_str = '0' * padding + binary_str
    
    hex_chars = []
    for i in range(0, len(binary_str), 4):
        chunk = binary_str[i:i+4]
        decimal = int(chunk, 2)
        hex_char = format(decimal, 'X') 
        hex_chars.append(hex_char)
    
    return ''.join(hex_chars)

def Convert_From_Hexa_To_Binary(Hex):
    HEX_TO_BITS = {
    '0': [0, 0, 0, 0], '1': [0, 0, 0, 1], '2': [0, 0, 1, 0], '3': [0, 0, 1, 1],
    '4': [0, 1, 0, 0], '5': [0, 1, 0, 1], '6': [0, 1, 1, 0], '7': [0, 1, 1, 1],
    '8': [1, 0, 0, 0], '9': [1, 0, 0, 1], 'A': [1, 0, 1, 0], 'B': [1, 0, 1, 1],
    'C': [1, 1, 0, 0], 'D': [1, 1, 0, 1], 'E': [1, 1, 1, 0], 'F': [1, 1, 1, 1],
    'a': [1, 0, 1, 0], 'b': [1, 0, 1, 1], 'c': [1, 1, 0, 0], 'd': [1, 1, 0, 1], 
    'e': [1, 1, 1, 0], 'f': [1, 1, 1, 1],
}
    binary_bits = []
    for digit in Hex: 
        binary_bits.extend(HEX_TO_BITS[f"{digit}"])
    return binary_bits

def DES_Decrypt(ciphertext_64bit, subkeys):
    reversed_subkeys = subkeys[::-1]  
    return DES_Encrypt(ciphertext_64bit, reversed_subkeys)

def is_hex(s):
    return bool(re.fullmatch(r"^[0-9A-Fa-f]+$", s))

def query_server(student_id, plaintext_hex):
    if len(plaintext_hex) != 16:
        raise ValueError("Plaintext must be 64 bits (16 hex characters)")

    response = requests.post(URL, json={
        "student_id": student_id,
        "plaintext": plaintext_hex 
    })

    if response.status_code == 200:
        return response.json().get("ciphertext")
    else:
        raise ValueError(f"Server Error: {response.text}")


def parity (binary: str):
    result=0
    for digit in binary:
        result^= int(digit)
    return result

def form_64bit_key (int_key: int ):
    binary_key=format(int_key, 'b')
    length= len(binary_key)
    if length<=7:
        result= "0"*(56) + "0"*(7-length) + binary_key + str(parity(binary_key))
        
    elif length <=14:
        low= binary_key[-7:]
        low_result=   low + str(parity(low))
        high= binary_key[:-7]
        high_result= "0"*(7-len(high)) + high + str(parity(high))
        result= "0"*(48)+ high_result+low_result
    #else: implement cases to handle strong keys (more than effective 12-bit keys)
    result = [int(char) for char in result] # to become a list of digits, [0,0,1,...,0]
    return result


if __name__ == "__main__":
    #stu_id = input("Enter your student ID: ").strip()
    stu_id=1220187
    #plaintext_hex = input("Enter 64-bit plaintext in hex (16 hex digits): ").strip().lower()
    plaintext_hex="ABCD1234EFEF5678"

    while True:
        try:
            ciphertext_hex = query_server(stu_id, plaintext_hex)
            print(ciphertext_hex)
            break
        except ValueError as e:
            print(e)

    plaintext_bits = Convert_From_Hexa_To_Binary(plaintext_hex)
    ciphertext_bits= Convert_From_Hexa_To_Binary(ciphertext_hex)

    # C= 𝑬𝒏𝒄(𝑲𝟏,𝑫𝒆𝒄(𝑲𝟐,𝑬𝒏𝒄(𝑲𝟏,𝑷))) 
    # let 𝑬𝒏𝒄(𝑲𝟏,𝑷)= temp1
    # let 𝑫𝒆𝒄(𝑲𝟐,𝑬𝒏𝒄(𝑲𝟏,𝑷))= temp2
    # let 𝑫𝒆𝒄(C, 𝑲𝟏)= temp3

    # Keys are weak, only 12 bits for each
    # K1 from 0 to 4096
    print("----Starting the attack----")
    stop=0
    K1_int=1402
    while not stop and K1_int <= 1402:
        key1_64bit = form_64bit_key(K1_int)
        subkeys1= key_generator(key1_64bit)
        temp1= bits_to_hex(key1_64bit)
        # implement temp1=𝑬𝒏𝒄(𝑲𝟏,𝑷)
        temp1_bits= DES_Encrypt(plaintext_bits, subkeys1) # temp1 in bits
        VAL1= bits_to_hex(temp1_bits)
        # implement temp3=𝑫𝒆𝒄(C, 𝑲𝟏)
        temp3_bits= DES_Decrypt(ciphertext_bits, subkeys1)

        K2_int=6719
        while not stop and K2_int<= 6719:

            key2_64bit = form_64bit_key(K2_int)
            subkeys2= key_generator(key2_64bit)

            temp2_bits= DES_Decrypt(temp1_bits, subkeys2)
            if temp2_bits==temp3_bits:
                stop=1
            K2_int+=1
        K1_int+=1


    K1_int-=1
    K2_int-=1
    key1_64bit= form_64bit_key(K1_int)
    key2_64bit= form_64bit_key(K2_int)
    key1_hex= bits_to_hex(key1_64bit)
    key2_hex= bits_to_hex(key2_64bit)
    if stop:
        print(f"Student ID: \"{stu_id}\"")
        print(f"Plaintext: \"{plaintext_hex}\"")
        print(f"Ciphertext: \"{ciphertext_hex}\"")

        print(f"64-bit Key1 in hexa: \"{key1_hex}\"")
        print(f"64-bit Key2 in hexa: \"{key2_hex}\"")
    else:
        print("NOT FOUND")

    
