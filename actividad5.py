for i in range(3,40):
    num=2
    numero=i
    while num<numero:
        if numero%num == 0:
            print(f'{numero} no es numero primo')
            break
        num+=1
    if num==numero:
        print(f'{numero} es numero primo')
