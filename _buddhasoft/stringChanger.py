incomeString = "1, 2, 3, 4, 5, There is some rabbit went to walk. But 1 hunter made 2 shots and kill it."
numbersDict = {0:'zero',1:'one',2:'two',3:'three',4:'four',5:'five',6:'sx',7:'seven',8:'eight',9:'nine'}

def replace(text, dic):
    for key, value in iter(dic.items()):
        text = text.replace(str(key), value)
    return text

print(replace(incomeString, numbersDict))
