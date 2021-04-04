from flask import request
from flask_paginate import get_page_parameter,Pagination
import config
from apps.models import PostModel,CommentModel,PostStarModel,CommentStarModel


def user_post_details(user):
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * config.PER_PAGE
    end = start + config.PER_PAGE
    total = PostModel.query.with_parent(user).count()
    pagination = Pagination(bs_version=3, page=page, total=total, outer_window=0, inner_window=2)
    posts = PostModel.query.with_parent(user).order_by(PostModel.create_time.desc()).slice(start, end)

    context = {
        'user':user,
        'posts': posts,
        'pagination': pagination
    }
    return context


def user_comments_detail(user):
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * config.PER_PAGE
    end = start + config.PER_PAGE
    total = CommentModel.query.with_parent(user).count()
    pagination = Pagination(bs_version=3, page=page, total=total, outer_window=0, inner_window=2)
    comments = CommentModel.query.with_parent(user).order_by(CommentModel.create_time.desc()).slice(start, end)
    context = {
        'user':user,
        'comments':comments,
        'pagination':pagination
    }
    return context


def user_poststars_detail(user):
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * config.PER_PAGE
    end = start + config.PER_PAGE
    total = PostStarModel.query.with_parent(user).count()
    pagination= Pagination(bs_version=3, page=page, total=total, outer_window=0, inner_window=2)
    post_stars = PostStarModel.query.with_parent(user).order_by(PostStarModel.create_time.desc()).slice(start, end)
    comment_stars = CommentStarModel.query.with_parent(user).order_by(CommentStarModel.create_time.desc()).slice(start, end)
    context = {
        'user':user,
        'post_stars':post_stars,
        'comment_stars':comment_stars,
        'pagination':pagination
    }
    return context

