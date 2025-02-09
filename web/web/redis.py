from flask import jsonify, redirect, url_for
import redis
from web import jwt


revoked_store = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# https://github.com/vimalloc/flask-jwt-extended/blob/master/examples/redis_blacklist.py
@jwt.token_in_blacklist_loader
def check_if_token_is_revoked(decrypted_token):
    jti = decrypted_token['jti']
    entry = revoked_store.get(jti)
    if entry is None:
        return True
    return entry == 'true'

@jwt.invalid_token_loader
@jwt.expired_token_loader
def error_token_callback(error):
    # redirects to the login page when token is expired/invalid
    return redirect(url_for('auth_bp.login'))

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description': 'Request does not contain an access token',
        'error': 'authorization_required'
    }), 401

@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'description': 'The token is not fresh',
        'error': 'fresh_token_required'
    }), 401

@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': 'The token has been revoked',
        'error': 'token_revoked'
    }), 401
