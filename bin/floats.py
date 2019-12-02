

def float_to_bin(number):
    #Returns the absolute value of a float in binary representation of up to 36 bits

    rounded_num = round(abs(number),20) #Max of 20 decimal places 

    whole, dec = str(rounded_num).split(".")

    places = len(dec)
    whole = int(whole)
    dec = float("." + dec)

    if whole > 0:
        result = bin(whole).lstrip("0b") + "."

    else:
        result = "0" + "."

    if dec != 0:
        length = len(result) - 1 # Number of bits already used - max of 36
        dec_result = ""
        dec_intermediate = dec
        for i in range(36 - length):
            dec_intermediate *= 2
            if (dec_intermediate) > 1:
                dec_result += "1"
                dec_intermediate -= 1
            
            elif (dec_intermediate) < 1:
                dec_result += "0"

            else:
                #If equal to 1, rest of binary number will be 0's
                dec_result += "1"
                dec_result.ljust(36, '0')
                break
                
        result += dec_result
           
    else:
        result += "0"

    return result

def bin_to_sicfloat(number, bin_number):
    whole_places = bin_number.find('.')
    exp = bin(whole_places + 1024).lstrip("0b")

    #Normalization
    if whole_places > 1:
        frac = (bin_number[:whole_places] + bin_number[whole_places + 1:])

    if number >= 0:
        #Sign bit = 0 if positive
        result = "0" + exp + frac
    
    else:
        #Sign bit = 1 if negative
        result = "1" + exp + frac

    return hex(int(result,2)).lstrip("0x")

def hex_to_float(bin_number):
    #Returns the float of a hex number
    hex_num = bin_number
    if int(hex_num[0],16) >= 8:
        sign = "1" #Negative

    else:
        sign = "0" #Positive

    bin_number = sign + bin(int(hex_num,16)).lstrip("0b") 
    exp = int(bin_number[1:12],2) - 1024
    fract = bin_number[12:48]
    
    whole = str(int(fract[0:exp],2))
    dec = fract[exp:len(fract)]


    total = 0.0
    for i in range(len(dec)):
        if dec[i] == '1':
            total += (1 * (2**(-(i+1))))
        
    dec = str(total).split('0')[1]

    if(sign == 1):
        result = "-" + whole + dec
    else:   
        result = whole + dec

    return round(float(result),2)

def float_to_hex(number):
    return bin_to_sicfloat(number,float_to_bin(number)).upper()
    
def whole_to_dec(num):
    while num > 1:
        num /= 10
    return num


print(hex_to_float(bin_to_sicfloat(3.2,float_to_bin(3.2))))

