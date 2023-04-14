from app.main import *

templates = Jinja2Templates(directory="./templates/")


@app.get("/")
async def get_forum(request : Request, response: Response, Cookies: str | None = Cookie(default=None)):
    if Cookies is None:
        return templates.TemplateResponse('./page.html', context={'request': request})
    else:
        try:
            verify_auth_token(Cookies)
        except:
            response = RedirectResponse('/login', status_code=status.HTTP_302_FOUND)
            response.delete_cookie(key='Cookies')
            return response
        usr = db.execute('read_user', {'user': verify_auth_token(Cookies)}).one(User)
        groupuser = []
        if db.execute('read_groupuser',{'user_id': usr.user_id}).all(GroupUser) is not None:
            groupuser = [gr.group_id for gr in db.execute('read_groupuser',{'user_id': usr.user_id}).all(GroupUser)]
        if usr.isvip:
            groups = db.execute('read_all_groups').all(Group)
            if db.execute('read_groupuser', {'user_id':usr.user_id}).all(GroupUser) is not None:
                ridgrupusr = db.execute('read_groupuser', {'user_id': usr.user_id}).all(GroupUser)
                for gr in groups:
                    if gr.group_id not in [ge.group_id for ge in ridgrupusr]:
                        db.execute('add_groupuser',{'user_id':usr.user_id,'group_id':gr.group_id}).none()
            else:
                for gr in groups:
                    db.execute('add_groupuser', {'user_id': usr.user_id, 'group_id': gr.group_id}).none()
        else:
            groups = db.execute('read_groups_public').all(Group)
            allgr = db.execute('read_all_groups').all(Group)
            if allgr is not None:
                for gr in allgr:
                    if groups is None and gr.creator == usr.user_id:
                        groups = [gr]
                    elif gr.creator == usr.user_id and gr.group_id not in [gr.group_id for gr in groups]:
                        groups.append(gr)
            if db.execute('read_groupuser', {'user_id': usr.user_id}).all(GroupUser) is not None and db.execute('read_user_groups', {'name': usr.user_id}).all(Group):
                groupsofuser = db.execute('read_user_groups', {'name': usr.user_id}).all(Group)
        if groups is not None:
            for group in groups:
                group.creator_name = db.execute('read_user_by_id', {'id':group.creator}).one(User).nickname
                if db.execute('read_thread', {'id': group.group_id}).all(Thread) is not None:
                    group.number_of_threads = len(db.execute('read_thread', {'id': group.group_id}).all(Thread))
                    for thread in db.execute('read_thread', {'id': group.group_id}).all(Thread):
                        if db.execute('read_comments', {'thread': thread.thread_id}).all(Comment) is not None:
                            group.number_of_comments += len(db.execute('read_comments', {'thread': thread.thread_id}).all(Comment))
        return templates.TemplateResponse('./page_auth.html', context={'request': request, 'groups': groups, 'username' : db.execute('read_user',{'user' : verify_auth_token(Cookies)}).one(UserLogin).nickname, "groupuser" : groupuser})

@app.post("/")
async def create_group(request: Request, isPublic:bool = Form(default=False), groupName: str = Form(default=None), groupDescription: str = Form(default=None), Cookies: str | None = Cookie(default=None)):
    try:

        verify_auth_token(Cookies)

    except:
        response = RedirectResponse('/login', status_code=status.HTTP_302_FOUND)
        response.delete_cookie(key='Cookies')
        return response
    usr = db.execute('read_user', {'user': verify_auth_token(Cookies)}).one(User)
    if db.execute('read_group',{'name':groupName}).one(Group) is None:

        db.execute('create_group', {'name': groupName, 'description': groupDescription, 'isPublic' : isPublic, 'creator': usr.user_id}).none()
        db.execute('add_groupuser',{'user_id':usr.user_id,'group_id':db.execute('read_group',{'name':groupName}).one(Group).group_id}).none()
    else:
        raise HTTPException(status_code=409)
    return RedirectResponse('/', status_code=status.HTTP_302_FOUND)

@app.get("/logout")
async def logout(request: Request, response: Response):
    response = RedirectResponse('/', status_code=status.HTTP_302_FOUND)
    response.delete_cookie(key='Cookies')
    return response

@app.get("/login")
async def get_login(request : Request, responce: Response):
    response = templates.TemplateResponse('./login.html', context={'request': request})
    response.delete_cookie(key='Cookies')
    return response
@app.post("/login")
async def post_login(request: Request, responce: Response, inputName: str = Form(...), inputPassword: str = Form(...),remember_me: bool = Form(False)):

    usr = db.execute('read_user', {'user': inputName}).one(UserLogin)
    if usr == None:
        return RedirectResponse('/register', status_code=status.HTTP_302_FOUND)
    elif verify_hash(usr.password, inputPassword):
        responce = RedirectResponse('/', status_code=status.HTTP_302_FOUND)
        responce.set_cookie(key='Cookies', value=get_auth_token(inputName))
        return responce
    else:
        return templates.TemplateResponse('./login.html', context={'request': request, 'invalpass': 'Password incorrect!'})

@app.get("/register")
async def get_register(request : Request):
    return templates.TemplateResponse('./register.html', context={'request': request})
@app.post("/register")
async def post_register(request: Request, inputName: str = Form(...), inputPassword: str = Form(...), inputConfirmPassword: str = Form(...)):

    usr = db.execute('read_user', {'user': inputName}).one(UserLogin)
    if inputPassword != inputConfirmPassword:
        return templates.TemplateResponse('./register.html', context={'request': request, 'invalpass': "Passwords aren't similar!"})
    elif usr != None:
        return templates.TemplateResponse('./register.html', context={'request': request, 'invalpass': "Name is already taken!"})
    else:
        with open("./static/default.png", mode='rb') as default_pic:
            img_data = default_pic.read()
        db.execute('create_user',{'inputName': inputName, 'inputPassword': hash_sha256(inputPassword), 'image':img_data}).none()
        return RedirectResponse('/login', status_code=status.HTTP_302_FOUND)
@app.get("/user")
async def get_user(request: Request, Cookies: str | None = Cookie(default=None)):
    try:
        verify_auth_token(Cookies)
    except:
        response = RedirectResponse('/login', status_code=status.HTTP_302_FOUND)
        response.delete_cookie(key='Cookies')
        return response
    res = db.execute('read_user_profile',{'user':verify_auth_token(Cookies)}).one(User)
    return templates.TemplateResponse('./profile.html', context={'request': request,'byte_arr': base64.b64encode(bytes(res.img)).decode('utf-8'),'user':res, 'username' : res.nickname, 'isVipProfile' : ("обычный аккаунт", "VIP статус")[res.isvip]})
@app.post("/user")
async def post_user(request: Request, inputAvatar: UploadFile = File(default=None), inputBio: str = Form(default=None), inputPrivatbio: str = Form(default=None), Cookies: str | None = Cookie(default=None), isVip:str=Form(default=False)):

    try:

        verify_auth_token(Cookies)

    except:
        response = RedirectResponse('/login', status_code=status.HTTP_302_FOUND)
        response.delete_cookie(key='Cookies')
        return response
    allowed_types = ['image/jpeg', 'image/png']
    usr = db.execute('read_user', {'user': verify_auth_token(Cookies)}).one(User)
    if inputAvatar is not None:
        if inputAvatar.content_type in allowed_types:
            img_data = await inputAvatar.read()

            usr = db.execute('read_user', {'user': verify_auth_token(Cookies)}).one(User)
            db.execute('add_image', {'user_id': usr.user_id, 'image_data': img_data}).none()
        else:
            logging.warning(f'id:{usr.user_id}, nickname:{usr.nickname}  gruzit cringe')

    db.execute('modify_user',{'user': usr.nickname, 'inputBio': inputBio, 'inputPrivateBio': inputPrivatbio, 'profileStatus': isVip}).none()
    usr = db.execute('read_user', {'user': verify_auth_token(Cookies)}).one(User)
    return RedirectResponse('/user', status_code=status.HTTP_302_FOUND)
@app.get('/user/{user_id}')
async def get_user_profile(request: Request, user_id: str = Path(), Cookies: str | None = Cookie(default=None)):
    if Cookies is not None:
        try:
            verify_auth_token(Cookies)
        except:
            response = RedirectResponse('/login', status_code=status.HTTP_302_FOUND)
            response.delete_cookie(key='Cookies')
            return response
    else:
        response = RedirectResponse('/login', status_code=status.HTTP_302_FOUND)
        response.delete_cookie(key='Cookies')
        return response
    if user_id.isdigit() == False or db.execute('read_user_by_id', {'id': user_id}).one(User) is None:
        raise HTTPException(status_code=404)
    usr = db.execute('read_user', {'user': verify_auth_token(Cookies)}).one(User)
    usrid = db.execute('read_user_by_id', {'id': user_id}).one(User)
    if usr.user_id == int(user_id):
        return RedirectResponse('/user', status_code=status.HTTP_302_FOUND)
    else:
        return templates.TemplateResponse('./profile_guest.html',
                                          context={'request': request,'nickname':usr.nickname ,'username': usrid.nickname,
                                                   'isVipProfile': usrid.isvip, 'user': usrid, 'byte_arr': base64.b64encode(bytes(usrid.img)).decode('utf-8')})

@app.get("/group/{group_id}")
async def get_group(request: Request, group_id: str = Path(), Cookies: str | None = Cookie(default=None)):
    try:
        verify_auth_token(Cookies)
    except:
        response = RedirectResponse('/login', status_code=status.HTTP_302_FOUND)
        response.delete_cookie(key='Cookies')
        return response
    if group_id.isdigit() == False or db.execute('read_group_by_id', {'id': group_id}).one(Group) is None:
        raise HTTPException(status_code=404)
    usr = db.execute('read_user', {'user': verify_auth_token(Cookies)}).one(User)
    groupuser = []
    if db.execute('read_groupuser', {'user_id': usr.user_id}).all(GroupUser) is not None:
        grofusr = db.execute('read_groupuser', {'user_id': usr.user_id}).all(GroupUser)
        groupuser = [gr.group_id for gr in grofusr]
        for gr in grofusr:
            gr.group_name = db.execute('read_group_by_id',{'id': gr.group_id}).one(Group).name
    threads = db.execute('read_thread', {'id': group_id}).all(Thread)
    if threads is not None:
        for thread in threads:
            if db.execute('read_comments', {'thread': thread.thread_id}).all(Comment) is not None:
                thread.number_of_comments += len(db.execute('read_comments', {'thread': thread.thread_id}).all(Comment))
                comments = db.execute('read_comments', {'thread': thread.thread_id}).all(Comment)
                for comment in comments:
                    if comment.name is None:
                        comment.name = db.execute('read_user_by_id', {'id': comment.user_id}).one(User).nickname
                if comments is not None:
                    thread.last_comment_username = comments[len(comments)-1].name
                    thread.last_comment_userid = comments[len(comments) - 1].user_id
    if int(group_id) in groupuser:
        return templates.TemplateResponse('./page_tred.html', context={'request': request, 'username' : usr.nickname, 'threads': threads, 'group_id': group_id, 'grofusr': grofusr})
    else:
        raise HTTPException(status_code=403)

@app.post("/group/{group_id}")
async def create_thread(request: Request, group_id: str = Path(), threadName: str = Form(default=None), threadDescription: str = Form(default=None), Cookies: str | None = Cookie(default=None)):
    try:
        verify_auth_token(Cookies)
    except:
        response = RedirectResponse('/login', status_code=status.HTTP_302_FOUND)
        response.delete_cookie(key='Cookies')
        return response
    if group_id.isdigit() == False or db.execute('read_group_by_id', {'id': group_id}).one(Group) is None:
        raise HTTPException(status_code=404)
    if db.execute('read_thread_name', {'name': threadName, 'id':group_id}).all(Thread) is None:
        db.execute('create_thread', {'name': threadName, 'description': threadDescription, 'group': group_id}).none()
    else:
        raise HTTPException(status_code=409)
    url = '/group/' + group_id
    return RedirectResponse(url, status_code=status.HTTP_302_FOUND)

@app.get("/group")
async def redirect_group(response: Response):
    return RedirectResponse('/', status_code=status.HTTP_302_FOUND)

@app.get("/thread/{thread_id}")
async def get_thread(request: Request, thread_id: str = Path(), Cookies: str | None = Cookie(default=None)):
    try:
        verify_auth_token(Cookies)
    except:
        response = RedirectResponse('/login', status_code=status.HTTP_302_FOUND)
        response.delete_cookie(key='Cookies')
        return response
    usr = db.execute('read_user', {'user': verify_auth_token(Cookies)}).one(User)
    if db.execute('read_groupuser', {'user_id': usr.user_id}).one(GroupUser) is None or db.execute('read_thread_by_id',{'id': thread_id}).one(Thread).group_id not in [gr.group_id for gr in db.execute('read_groupuser', {'user_id': usr.user_id}).all(GroupUser)]:
        raise HTTPException(status_code=403)
    if thread_id.isdigit() == False or db.execute('read_thread_by_id', {'id': thread_id}).one(Thread) is None:
        raise HTTPException(status_code=404)
    comments = db.execute('read_comments',{'thread': thread_id}).all(Comment)
    if comments is not None:
        for comment in comments:
            if comment.name is None:
                comm = db.execute('read_user_by_id',{'id': comment.user_id}).one(User)
                comment.name = comm.nickname
                comment.img = base64.b64encode(bytes(db.execute('read_user_by_id',{'id': comment.user_id}).one(User).img)).decode('utf-8')
                comment.isvip = comm.isvip
        return templates.TemplateResponse('./page_comments.html', context={'request': request,'thread_id':thread_id, 'username' : usr.nickname, 'comments': comments, 'thread': db.execute('read_thread_by_id',{'id': thread_id}).one(Thread)})
    else:
        return templates.TemplateResponse('./page_comments.html', context={'request': request,'thread_id':thread_id, 'username': usr.nickname, 'comments': comments,  'thread': db.execute('read_thread_by_id',{'id': thread_id}).one(Thread)})
@app.post("/thread/{thread_id}")
async def post_thread(request: Request, addComment:str=Form(...), thread_id: str = Path(), Cookies: str | None = Cookie(default=None)):
    try:
        verify_auth_token(Cookies)
    except:
        response = RedirectResponse('/login', status_code=status.HTTP_302_FOUND)
        response.delete_cookie(key='Cookies')
        return response
    if thread_id.isdigit() == False or db.execute('read_thread_by_id', {'id': thread_id}).one(Thread) is None:
        raise HTTPException(status_code=404)
    usr = db.execute('read_user', {'user': verify_auth_token(Cookies)}).one(User)
    if db.execute('read_groupuser', {'user_id': usr.user_id}).one(GroupUser) is None or db.execute('read_thread_by_id',{'id': thread_id}).one(Thread).group_id not in [gr.group_id for gr in db.execute('read_groupuser', {'user_id': usr.user_id}).all(GroupUser)]:
        raise HTTPException(status_code=403)
    data = datetime.datetime.now() + datetime.timedelta(hours=7)
    time_data = f'{str(data)[:19]}'
    db.execute('create_comment',{'user': usr.user_id, 'thread': thread_id, 'text': addComment, 'time':time_data}).none()
    url = '/thread/' + thread_id
    return RedirectResponse(url, status_code=status.HTTP_302_FOUND)
@app.get("/thread")
async def redirect_thread(response: Response):
    return RedirectResponse('/', status_code=status.HTTP_302_FOUND)

@app.post("/group/add/{group_id}")
async def add_user_to_group(request: Request, group_id: str = Path(), Cookies: str | None = Cookie(default=None)):
    try:
        verify_auth_token(Cookies)
    except:
        response = RedirectResponse('/login', status_code=status.HTTP_302_FOUND)
        response.delete_cookie(key='Cookies')
        return response
    usr = db.execute('read_user', {'user': verify_auth_token(Cookies)}).one(User)
    if group_id.isdigit() == False or db.execute('read_group_by_id', {'id': group_id}).one(Group) is None:
        raise HTTPException(status_code=404)
    if db.execute('read_groupuser', {'user_id':usr.user_id}).all(GroupUser) is not None:
        if group_id not in [us.group_id for us in db.execute('read_groupuser', {'user_id':usr.user_id}).all(GroupUser)]:
            db.execute('add_groupuser', {'user_id':usr.user_id, 'group_id':group_id}).none()
    else:
        db.execute('add_groupuser', {'user_id':usr.user_id, 'group_id':group_id}).none()
    return RedirectResponse('/', status_code=status.HTTP_302_FOUND)

@app.post("/group/quit/{group_id}")
async def add_user_to_group(request: Request, group_id: str = Path(), Cookies: str | None = Cookie(default=None)):
    try:
        verify_auth_token(Cookies)
    except:
        response = RedirectResponse('/login', status_code=status.HTTP_302_FOUND)
        response.delete_cookie(key='Cookies')
        return response
    usr = db.execute('read_user', {'user': verify_auth_token(Cookies)}).one(User)
    if group_id.isdigit() == False or db.execute('read_group_by_id', {'id': group_id}).one(Group) is None:
        raise HTTPException(status_code=404)
    else:
        db.execute('delete_groupuser', {'user_id': usr.user_id, 'group_id': group_id}).none()
    return RedirectResponse('/', status_code=status.HTTP_302_FOUND)

@app.post("/reply/{group_id}/{thread_id}")
async def thread_reply(request: Request, group_id: str = Path(), thread_id: str = Path(), Cookies: str | None = Cookie(default=None)):
    try:
        verify_auth_token(Cookies)
    except:
        response = RedirectResponse('/login', status_code=status.HTTP_302_FOUND)
        response.delete_cookie(key='Cookies')
        return response
    if (group_id.isdigit() == False or db.execute('read_group_by_id', {'id': group_id}).one(Group) is None) and ( thread_id.isdigit() == False or db.execute('read_thread_by_id', {'id': thread_id}).one(Thread) is None):
        raise HTTPException(status_code=404)
    this_thread = db.execute('read_thread_by_id', {'id': thread_id}).one(Thread)
    outter_thread = db.execute('read_thread_name',{'name': this_thread.name, 'id':group_id}).one(Thread)

    if outter_thread is None:
        db.execute('create_thread', {'name': this_thread.name, 'description': this_thread.description, 'group': group_id}).none()

        new_thread = db.execute('read_thread_name', {'name':this_thread.name, 'id':group_id}).one(Thread)

        comments = db.execute('read_comments',{'thread':thread_id}).all(Comment)
        if comments:
            for comment in comments:
                db.execute('create_comment',{'user': comment.user_id,'thread':new_thread.thread_id, 'text': comment.text, 'time': comment.time}).none()

    return RedirectResponse('/', status_code=status.HTTP_302_FOUND)


@app.exception_handler(404)
async def exception_404(request: Request, exc: HTTPException):
    return templates.TemplateResponse('./404.html',context={'request': request})
@app.exception_handler(403)
async def exception_403(request: Request, exc: HTTPException):
    return templates.TemplateResponse('./403.html',context={'request': request})
@app.exception_handler(409)
async def exception_409(request: Request, exc: HTTPException):
    return templates.TemplateResponse('./409.html',context={'request': request})
