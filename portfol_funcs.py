def news_check(data,port):
    print("============================ PORTFOLIO CHECK =============================")
    for i in port:
        if i in data:
            print("Percentage change for",i, (data[i]-port[i])/port[i])
            print(i,'score:',data[i])
    print("===========================================================================")


def update_port(scores):
    import json
    import re
    # keeps alphanumeric chars
    def clean_string(s):
        s = s.replace(' ','')
        return s

    with open('json_files/port.json','r') as f:
        curr = json.load(f)
    print("Current Portfolio:", curr)
    
    tick = input("Add changes in the form <ticker>:B/S; ")
    ticks = []
    if ';' in tick:
        for i in tick.split(';'):
            ticks.append(i)

    # ticks = [<ticker>(A/R),...]
    for el in ticks:
        for ticker,option in el.split(':'):
            if  option.lower() == 'b':
                if ticker in scores:
                    curr[ticker] = scores[ticker]
            elif option.lower() == 's':
                del curr[ticker]

    with open('json_files/port.json', 'w') as f:
        json.dump(curr,f)