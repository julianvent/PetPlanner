from flask import Blueprint
from app.controllers.article_controler import create_article, get_all_articles, get_my_articles, get_article, update_article, delete_article
from app.utils.auth import token_required

article = Blueprint('article', __name__)


@article.route("/", methods=["GET"])
def get_articles_route():
    return get_all_articles()


@article.route("/me", methods=["GET"])
@token_required
def get_my_articles_route(current_user):
    return get_my_articles(current_user)


@article.route("/<int:article_id>", methods=["GET"])
@token_required
def get_article_route(current_user, article_id):
    return get_article(article_id)


@article.route("/", methods=["POST"])
@token_required
def create_article_route(current_user):
    return create_article(current_user)


@article.route("/<int:article_id>", methods=["PUT"])
@token_required
def update_article_route(current_user, article_id):
    return update_article(current_user, article_id)


@article.route("/<int:article_id>", methods=["DELETE"])
@token_required
def delete_article_route(current_user, article_id):
    return delete_article(current_user, article_id)
