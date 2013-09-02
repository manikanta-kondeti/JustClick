def index():
    images = db().select(db.image.ALL, orderby=db.image.title)
    users = db().select(db.auth_user.ALL, orderby=db.auth_user.first_name)

    return dict(images=images,users=users)
    
@auth.requires_login() 
def upload():
    form=SQLFORM(db.image)
    if form.accepts(request.vars):   response.flash="New Image Added"
    allimages=db().select(db.image.ALL , orderby=db.image.title)
    return dict(form=form , allimages=allimages)
     
def user():
    return dict(form=auth())
    
    
    
@auth.requires_membership('manager')
def manage():
    grid = SQLFORM.smartgrid(db.image)
    return dict(grid=grid)


@auth.requires_login()
def show():
    images=db().select(db.image.ALL , orderby=db.image.title)
    image = db.image(request.args(0)) 
    return dict( images=images , image=image)
    
    

def showimagecomments():
    allimages=db().select(db.image.ALL , orderby=db.image.title)
    image = db.image(request.args(0)) 
    db.comment.image_id.default = image.id
    form = crud.create(db.comment, next=URL(args=image.id),
                     message='your comment is posted')
    comments = db(db.comment.image_id==image.id).select()
    return dict( allimages=allimages , image=image, comments=comments, form=form)
    
    
def delete(): 
    if(auth.user.first_name==request.args[0] ):
        db(db.image.id==request.args[1]).delete()
        k=1
    else:
        k=0
    images=db().select(db.image.ALL , orderby=db.image.title)
    return dict(k=k ,  images=images)  
    
    
    
@auth.requires_membership('Admin')
def deleteasadmin(): 
    db(db.image.id==request.args[0]).delete()
    images = db().select(db.image.ALL, orderby=db.image.title)
    users = db().select(db.auth_user.ALL, orderby=db.auth_user.first_name)
    redirect(URL(r=request,f='index'))
    return dict(  images=images) 
    
    
def admns():
  auth.add_membership('Admin',request.args[0])
  session.flash='Given Administrator Rights'
  redirect(URL(r=request,f='index') )
  return dict()   
    
    
def like():
       o = request.args
       db.like.insert(name=o[0],imageid=o[1])
       db(db.image.id==o[1]).update(likecount=o[2])
       redirect(URL(r=request,f='index'))
       return dict()
       

def download():
    return response.download(request, db)
