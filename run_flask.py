from flask import Flask
import requests
app = Flask(__name__)

@app.route("/")
def hello():
    # return "Hello, this is a secure Flask app!"

    url = "http://crm.negevdelivery.co.il/Baldarp/service.asmx/SaveData"
    payload = 'pParam=1%3B%D7%95%D7%99%D7%A6%D7%9E%D7%9F%2091%3B%D7%95%D7%99%D7%A6%D7%9E%D7%9F%2091%3B%D7%AA%D7%9C%20%D7%90%D7%91%D7%99%D7%91%20%3B%D7%95%D7%99%D7%A6%D7%9E%D7%9F%2090%3B%D7%95%D7%99%D7%A6%D7%9E%D7%9F%2090%3B%D7%AA%D7%9C%20%D7%90%D7%91%D7%99%D7%91%20%3B%D7%91%D7%93%D7%99%D7%A7%D7%AA%20%D7%91%D7%9C%D7%91%D7%93!%3B%D7%9C%D7%90%20%D7%9C%D7%A9%D7%9C%D7%95%D7%97%20%3B%20-%20%3B1%3B1%3B1%3B1%3B1%3B0%3BWoo%20%23000000%3B2059%3B0%3B%3B0%3B%D7%A2%D7%99%D7%A8-%D7%9E%D7%95%D7%A6%D7%90-2%3B%3Bidanbit80%40gmail.com%20-%200584770076%3B%3B0'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

    return response.text

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5001,
        # ssl_context=("selfsigned.crt", "selfsigned.key")  # SSL certificate and key
    )
