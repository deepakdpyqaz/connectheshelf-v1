def encrypter(message):
    messagenew=""
    for i in message:
        if(i<='Z' and i>='A'):
            messagenew+=chr(ord('A')-ord(i)+ord('Z'))
        elif(i<='z' and i>='a'):
            messagenew+=chr(ord('a')-ord(i)+ord('z'))
        elif(i<='9' and i>='0'):
            messagenew+=chr(ord('0')-ord(i)+ord('9'))
        else:
            messagenew+=i
    return messagenew
