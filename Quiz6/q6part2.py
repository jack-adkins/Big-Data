import base64

filename = 'abandon-2.txt'

negative_words = []
hash_values = [0] * 1500

with open(filename, 'r') as file:
    for line in file:
        word, tag = line.strip().split('\t')
        
        # Converting the tag to integer and checking if it's -4 or -5
        if int(tag) in [-4, -5]:
            negative_words.append(word)

# Hash function to map words to the bit vector
def h(s):
    return hash(s) % 1500

for bw in negative_words:
    hash_values[h(bw)] = 1

# Converting the bit vector into a binary string and then into Base64 format
tBytes = bytes(hash_values)
HV_in_b64 = base64.b64encode(tBytes)
b64_string = HV_in_b64.decode('utf-8')

with open('bit_vector_base64.txt', 'w') as out_file:
    out_file.write(b64_string)

