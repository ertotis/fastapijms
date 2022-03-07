from .. import models,schemas,utils, oath2
from typing import List,Optional
from fastapi import Body, FastAPI,Response, status,HTTPException, Depends,APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db  

router=APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.PostOut])
# @router.get("/",response_model=List[schemas.Post]) #list is from typing to put all post into a schema
def get_posts(db: Session = Depends(get_db), current_user:int = Depends (oath2.get_current_user),
limit :int = 10, skip: int = 0, search: Optional[str]=""):
    # Options
    # posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # posts=db.query(models.Post).all()
    # posts=db.query(models.Post),filter(models.Post.owner_id == current_user.id).all() get only my posts

    # posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts=db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(
            models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts

@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post:schemas.PostCreate,db: Session = Depends(get_db), current_user:int =
                Depends (oath2.get_current_user)):
     #the double asterisk unpacks the whole dictionary
    print(current_user.email)
    new_post=models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post) #refreshes the new post you created so you show it
    return new_post


@router.get("/{id}",response_model=schemas.PostOut) #id is a path parameter
def get_post(id: int, db: Session = Depends(get_db), current_user:int =
                Depends (oath2.get_current_user)):
    #look for first instance, could also do .all
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(
            models.Post.id).filter(models.Post.id == id).first()
    
    
    if not post:
        # one way to do it:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"{id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")

    return  post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db: Session = Depends(get_db), current_user:int =
                Depends (oath2.get_current_user)):
    post_query=db.query(models.Post).filter(models.Post.id == id)
    
    post=post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"Post with id {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                             detail=f"{id} is not authorized to perform action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)  
def update_post(id:int, updated_post: schemas.PostCreate,db: Session = Depends(get_db), current_user:int =
                Depends (oath2.get_current_user)):

    
    post_query=db.query(models.Post).filter(models.Post.id == id)
    post=post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"Post with id {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                             detail=f"{id} is not authorized to perform action")

    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return  post_query.first()