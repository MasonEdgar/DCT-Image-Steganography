'''
Author: Mason Edgar
ECE 529 - Algorithm Project
Image Steganography
'''
#------ External Libraries ------#
import bitstring
import numpy as np
#================================#

def extract_encoded_data_from_DCT(dct_blocks):
    extracted_data = ""
    for current_dct_block in dct_blocks:
        for i in range(1, len(current_dct_block)):
            curr_coeff = np.int32(current_dct_block[i])
            if (curr_coeff > 1):
                extracted_data += bitstring.pack('uint:1', np.uint8(current_dct_block[i]) & 0x01)
    return extracted_data

# ============================================================================= #
# ============================================================================= #
# ============================================================================= #
# ============================================================================= #

def embed_encoded_data_into_DCT(encoded_bits, dct_blocks):
    data_complete = False; encoded_bits.pos = 0
    encoded_data_len = bitstring.pack('uint:32', len(encoded_bits))
    converted_blocks = []
    for current_dct_block in dct_blocks:
        for i in range(1, len(current_dct_block)):
            curr_coeff = np.int32(current_dct_block[i])
            if (curr_coeff > 1):
                curr_coeff = np.uint8(current_dct_block[i])
                if (encoded_bits.pos == (len(encoded_bits) - 1)): data_complete = True; break
                pack_coeff = bitstring.pack('uint:8', curr_coeff)
                if (encoded_data_len.pos <= len(encoded_data_len) - 1): pack_coeff[-1] = encoded_data_len.read(1)
                else: pack_coeff[-1] = encoded_bits.read(1)
                # Replace converted coefficient
                current_dct_block[i] = np.float32(pack_coeff.read('uint:8'))
        converted_blocks.append(current_dct_block)

    if not(data_complete): raise ValueError("Data didn't fully embed into cover image!")

    return converted_blocks