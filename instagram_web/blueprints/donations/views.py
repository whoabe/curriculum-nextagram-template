from flask import Blueprint, render_template, request, flash, redirect, url_for
from models.user import User
from models.post import Post
from helpers import gateway

import braintree

donations_blueprint = Blueprint('donations',
                            __name__,
                            template_folder='templates')



@donations_blueprint.route('/<id>', methods=["GET"])
def new(id):
    #new donation html page
    user = User.get_by_id(id)

    client_token = gateway.client_token.generate()

    return render_template('donations/new_donation.html', user = user, client_token = client_token)



TRANSACTION_SUCCESS_STATUSES = [
    braintree.Transaction.Status.Authorized,
    braintree.Transaction.Status.Authorizing,
    braintree.Transaction.Status.Settled,
    braintree.Transaction.Status.SettlementConfirmed,
    braintree.Transaction.Status.SettlementPending,
    braintree.Transaction.Status.Settling,
    braintree.Transaction.Status.SubmittedForSettlement
]

@donations_blueprint.route('/checkouts', methods=['POST'])
def create_checkout():
    result = gateway.transaction.sale({
        'amount': request.form['amount'],
        'payment_method_nonce': request.form['payment_method_nonce'],
        'options': {
            "submit_for_settlement": True
        }
    })

    if result.is_success or result.transaction:
        return redirect(url_for('donations.show_checkout',transaction_id=result.transaction.id))
    else:
        for x in result.errors.deep_errors: flash('Error: %s: %s' % (x.code, x.message))
        return redirect(url_for('donations.profile_page'))
        #need to change this url_for view function


@donations_blueprint.route('/checkouts/<transaction_id>', methods=['GET'])
def show_checkout(transaction_id):
    
    transaction = gateway.transaction.find(transaction_id)
    result = {}
    if transaction.status in TRANSACTION_SUCCESS_STATUSES:
        result = {
            'header': 'Sweet Success!',
            'icon': 'success',
            'message': 'Your test transaction has been successfully processed. See the Braintree API response and try again.'
        }
    else:
        result = {
            'header': 'Transaction Failed',
            'icon': 'fail',
            'message': 'Your test transaction has a status of ' + transaction.status + '. See the Braintree API response and try again.'
        }

    return render_template('users/show.html', transaction=transaction, result=result)
    #goes back to the user profile page

# @users_blueprint.route("/client_token", methods=["GET"])
# def client_token():
#   return gateway.client_token.generate()

# @users_blueprint.route("/checkout", methods=["POST"])
# def create_purchase():
#   nonce_from_the_client = request.form["payment_method_nonce"]
#   # Use payment method nonce here...