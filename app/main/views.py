from app.main import main_bp
from flask import render_template
from flask import request, current_app, jsonify
from app.QueryFactory import ProductQueryBulder, ProductReviewQueryBulder
from pydantic import ValidationError
from app.schema import ProductQuery, ProductReviewQuery, KeyNamingScheme, ProductReviewOut

import pdb

@main_bp.route('/') 
def index():
    return render_template('index.html')


@main_bp.route('/product/review/search', methods=['POST'])
def product_review_search():

    try:

        user_query = ProductReviewQuery(**request.json)

        query = ProductReviewQueryBulder.build(user_query)

        results = current_app.redis_client.ft(
            KeyNamingScheme.PRODUCT_REVIEW_INDEXER.value
        ).search(
            query,
            {
                "vector_blob": ProductReviewQueryBulder.get_embeddings_blob(user_query.query),
                "items":user_query.items
            }
        ).docs

        products = list(map(
            lambda item : ProductReviewOut(**item.__dict__).__dict__,
            results
        ))

        return jsonify(products)

    except ValidationError as e:

        return jsonify(e.errors())


@main_bp.route('/product/search', methods=['POST'])
def product_search():

    try:

        user_query = ProductQuery(**request.json)

        query = ProductQueryBulder.build(user_query)

        products = current_app.redis_client.ft(
            KeyNamingScheme.PRODUCT_INDEXER.value
        ).search(
            query,
            {
                "vector_blob": ProductQueryBulder.get_embeddings_blob(user_query.query),
                "items":user_query.items
            }
        ).docs

        return ""

    except ValidationError as e:

        return jsonify(e.errors())

    return ""


