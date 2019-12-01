

def float_to_bin(number):
    rounded_num = round(number,20) #Max decimal places 

    whole, dec = str(rounded_num).split(".")

    places = len(dec)
    whole = int(whole)
    dec = int(dec)

    result = bin(whole).lstrip("0b") + "."

    for i in range(places):
        whole, dec = str((whole_to_dec(dec)) * 2).split(".")

        dec = int(dec)

        result += whole

    return result

def bin_to_float(bin_number):
    hex_num = bin_number

    if int(hex_num[0],16) >= 8:
        sign = "1" #Negative

    else:
        sign = "0" #Positive

    bin_number = sign + bin(int(hex_num,16)).lstrip("0b") 
    exp = int(bin_number[1:12],2) - 1024
    fract = bin_number[12:48]
    
    whole = int(fract[0:exp],2)
    dec = fract[exp:len(fract)]


    total = 0.0
    for i in range(len(dec)):
        if dec[i] == '1':
            total += (1 * 2^(-i))
        
    dec = str(total)

    if(sign == 1):
        result = "-" + whole + dec
    else:   
        result = whole + dec

    return float(result)
    
def whole_to_dec(num):
    while num > 1:
        num /= 10
    return num


print(float_to_bin(5.75))
print(bin_to_float("403B80000000"))
