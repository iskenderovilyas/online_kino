from app.models.posts.post_model import Post,PostGenres,Genre
from app.models.basemodel import db
from datetime import date
from typing import List
from peewee import fn
from app.schemas.posts import PostAllSchema,PostOneSchema,PostCreateSchema

# @db
# def create_post(
#     title:str,
#     description:str,
#     year:date,
#     country:str,
#     genres:List[str]) -> Post:
#     post = Post.create(title=title,description=description,year=year,country=country ) 
       
#     for genre in genres:
#         g = Genre.get(title=genre)
#         post.genre.add(g)
#     return post


@db
def create_post(post_in: PostCreateSchema):
    post = Post.create(
        title=post_in.title,
        description=post_in.description,
        year=post_in.year,
        country=post_in.country
    )
    for genre in post_in.genre:
        g = Genre.get(title=genre)
        post.genre.add(g)
    return post 
@db
def get_all_films():
    posts = Post.select(Post.id, Post.title,Post.year)
    return [PostAllSchema.from_orm(post) for post in posts]

@db
def get_film_by_id(id) -> Post:
    post = Post.select(Post,fn.array_agg(Genre.title).alias('genre_titles')).join(PostGenres).join(Genre).where(Post.id == id).group_by(Post.id).get_or_none()
    return PostOneSchema.from_orm(post)
#    return {
#         'id': post.id,
#         'title': post.title,
#         'year': post.year,
#         'country': post.country,
#         'genres': [genre.title for genre in post.genre]
#     }
@db
def delete_post(id, genre):
    deleted = Post.get(Post.id == id)

    print(deleted)
    deleted.genre.remove(Genre.select().where(Genre.title.startswith(genre)))
    deleted.delete_instance()
