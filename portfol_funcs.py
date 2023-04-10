def news_check(data,port):
    print("============================ PORTFOLIO CHECK =============================")
    for i in port:
        if i in data:
            if data[i] < .03 and data[i] >= 0:
                print("CHECK:", i)
            elif data[i] < 0:
                print("PROBABLY SELL:", i)
            else:
                print("HOLD:", i)
    print("===========================================================================")

def update_port():
    import json
    import datetime

    tick = input("Ticker: ")
    price = input("Price: ")

    with open('json_files/port.json','r') as f:
        curr = json.load(f)

    curr[tick] = [datetime.datetime.now(),price]
