import random

def get_response(message: str) -> str:
    p_message = message.lower()
    iuthuong1 = 'nhớ'
    iuthuong2 = 'yêu'
    jill = 'jill'
    
    if p_message == 'hello':
        return 'Hey there!'
    
    if p_message == 'roll':
        return str(random.randint(1, 10))
    
    if p_message == 'hao':
        return 'Hao Truong ml'
    
    if p_message == "hao truong":
        return 'Hao dep trai'
    
    if iuthuong1 in p_message:
        return 'em cũng nhớ anh'
    
    if iuthuong2 in p_message:
        return 'em cũng yêu anh'
    
    if jill in p_message:
        return 'the prettiest, cuttest sea otter in the world'
    
    if p_message == '!help':
        return '`This is a help message that you can modify.`'
    
    
    return 'I didn\'t understand what you wrote. Try typing "!help".'