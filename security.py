def XSSSanitizer(raw: str):
    replace_table={
        "<":"",
        "<":"",
        "<":"",
        "<":"",
        "<":"",
        "<":"",
    }

    # This is a selling app, it is very unlikly these strings appear in the input data
    refusedList=[
        "onerror=",
        "javascript:",
        "document.cookie",
    ]
    count = 0
    for i in refusedList:
        if(i in raw):
            return -1,"Fuck you! Attacker!"

    for i in replace_table.keys:
        raw = raw.replace(i,replace_table[i])

    return 0,raw
    
def SQLSanitizer(raw: str):
    pass
    # Not using SQL directlly