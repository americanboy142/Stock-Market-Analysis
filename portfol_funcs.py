def news_check(data,port):
    print("============================ PORTFOLIO CHECK =============================")
    for i in port:
        if i in data:
            print("Percentage change for",i, (data[i]-port[i])/port[i])
            print(i,'score:',data[i])
        else:
            print(f"{i} Not in News")
    print("===========================================================================")


def EDIT_PORTFOLIO(option:str,port:dict = None) -> dict:
    """
    will return portfolio with option 'r'
    and will write to the porfolio file with option 'w' and a given updated portfolio
    """
    import json

    if option == 'r':
        with open('json_files/port.json','r') as f:
            port = json.load(f)

        print("Current Portfolio:", port)
        return port
    
    if option == 'w':
        with open('json_files/port.json', 'w') as f:
            json.dump(port,f)
        print("Updated Portfolio:", port)

def clean_user_input_portfolio(input:str) -> str:
    "user input of form <ticker>:<option>; ..."
    # remove spaces
    if ' ' in input:
        input = input.replace(' ','')
    # check for ;, i.e. multiple entires
    #   - removes the last ; if present
    #   - splits input on ;
    ticker_dict = {}
    if ';' in input:
        if input[-1] == ';':
            input = input[:-1]
        for i in input.split(';'):
            ticker_dict[i.split(':')[0]] = i.split(':')[1]
    else:
        ticker_dict[input.split(':')[0]] = input.split(':')[1]
    return ticker_dict
    


def update_port(scores:dict,port:dict,input:str) -> dict:
    """
    returns an updated portfolio given (scores, old portfolio, user input)
    """
    #tick = input("Add changes in the form\n=== <ticker>:B/S; === \n")
    ticks = []
    """ if ';' in input:
        if input[-1] == ';':
            input = input[:-1]
        for i in input.split(';'):
            input.append(i) """
    
    ticks = clean_user_input_portfolio(input)

    # ticks = {<ticker>:(B/S),...}
    for key in ticks:
        #ticker,option = tuple(el.split(':'))
        if  ticks[key].lower() == 'b':
            if key in scores:
                port[key] = scores[key]
            else:
                print(f"ERROR: {key} not found in scores")
        elif ticks[key].lower() == 's':
            if key in port:
                del port[key]
            else:
                print(f"Error: {key} not in your portfolio.")
        else:
            print(f'Error: Unknown option for {key}')
    return port
    #EDIT_PORTFOLIO('w',port)


if __name__ == '__main__':
    import json 

    with open('json_files/news_main.json','r') as f:
        scores = json.load(f)

    port = EDIT_PORTFOLIO('r')
    update_port(scores,port,input('<ticker>:option;\n'))