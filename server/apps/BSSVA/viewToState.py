
def transWebViews(segs,error):
    for i in range(len(segs)):
        seg = segs[i]
        view = seg['view']
        baseKind = 0
        if view[0] == 5 and view[1] == 5: #空
            baseKind = 0
        elif view[0] == 4 and view[1] == 4: #矩形
            baseKind = 1
        elif view[0] == 3 and view[1] == 4: #上半
            baseKind = 2
        elif view[0] == 4 and view[1] == 2: #下半
            baseKind = 3
        elif view[0] == 3 and view[1] == 2: #圆
            baseKind = 4
        elif view[0] == 2 and view[1] == 3: #101
            baseKind = 5
        if len(view) == 3:
            baseKind+=4
        baseKind+=1
        seg['baseKind'] = baseKind
        seg['error'] = error
def transView(view):
    newView = 0
    if isinstance(view,int):
        return view
    else:
        #左三角+右三角 等于 圆
        if view[0] == 3 and view[1] == 2: #类似圆
            newView = 1
        elif view[0] == 5 and view[1] == 5: #类似空
            newView = 5
        elif view[0] == 4 and view[1] == 4: #类似矩形
            newView = 4
        elif view[0] == 3 and view[1] == 4: #类似上半
            newView = 3
        elif view[0] == 4 and view[1] == 2: #类似下半
            newView = 2
        elif view[0] == 2 and view[1] == 3: #101
            newView = 6
    return newView
