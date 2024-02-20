from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from celery import Celery
import time
import threading  # Import the threading module
import pusher




app = Flask(__name__)
socketio = SocketIO(app)
pusher_client = pusher.Pusher(
    app_id='1755467',
    key='7b856bf6a6911e246815',
    secret='c7963e39ab916759aa20',
    cluster='ap2',
    ssl=True
)

# Product details
product_id = 1
product_name = "iPhone 14"
starting_price = 60000
current_bid = starting_price
auction_end_time = 'loading...'  # Time in seconds
winner = None


@app.route("/")
def index():
    return render_template("product.html", product_id=product_id, product_name=product_name,
                           starting_price=starting_price, current_bid=current_bid,
                           auction_end_time=auction_end_time)


@app.route("/bid", methods=["POST"])
def submit_bid():
    global current_bid
    global winner
    bid_amount = int(request.json["bid"])
    if bid_amount < current_bid:
        current_bid = bid_amount
        winner = "Seller" + str(current_bid)
        #pusher_client.trigger("auction-channel", "new-bid", {"bid": current_bid})
        #pusher_client.trigger("auction-channel", "initial_data", {"current_bid": current_bid, "auction_end_time": auction_end_time, "winner": winner})
        return jsonify({"message": "Bid received", "bid": current_bid})
    else:
        return jsonify({"message": "Bid should be lower than current bid"}), 400




@socketio.on('connect')
def handle_connect():
    emit('initial_data', {"current_bid": current_bid, "auction_end_time": auction_end_time, "winner": winner})


if __name__ == "__main__":
    socketio.run(app, debug=True)
