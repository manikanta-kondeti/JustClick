db = DAL("sqlite://storage.sqlite")


from gluon.tools import Auth
auth = Auth(db)
auth.define_tables()

from gluon.tools import Crud
crud = Crud(db)


    

db.define_table('image',
   Field('title', unique=True),
   Field('likecount','integer',default=0),
   Field('uploaded_by'),
   Field('url'),
   Field('file', 'upload'),
   format = '%(title)s')

db.define_table('comment',
   Field('image_id', db.image),
   Field('author'),
   Field('email'),
   Field('body', 'text'))
   
db.define_table('like',
   Field('imageid','integer'),
   Field('name','string'))
   
if auth.is_logged_in():
    db.image.uploaded_by.default = auth.user.first_name 
    db.comment.author.default = auth.user.first_name 
    db.comment.email.default = auth.user.email

db.image.title.requires = IS_NOT_IN_DB(db, db.image.title)
db.comment.image_id.requires = IS_IN_DB(db, db.image.id, '%(title)s')
db.comment.email.requires = IS_EMAIL()
db.comment.body.requires = IS_NOT_EMPTY()

db.comment.image_id.writable = db.comment.image_id.readable = False
