from flask import Flask, request
import requests

app = Flask(__name__)

@app.route("/negevKametraProxy", methods=['POST'])
def negevKametraProxy():
    # Extract the data and headers from the incoming request
    incoming_data = request.form.to_dict()  # Handle form-encoded data
    incoming_headers = {key: value for key, value in request.headers}

    # Define the target URL
    url = "http://crm.negevdelivery.co.il/Baldarp/service.asmx/SaveData"

    # Forward the request to the target URL
    response = requests.post(
        url,
        data=incoming_data,
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )

    # Log the response from the target server
    print("Response from BALDAR system:", response.text)

    # Return the response back to the client
    return response.text, response.status_code


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000, debug=True
    )
