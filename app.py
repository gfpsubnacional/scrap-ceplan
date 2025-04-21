from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

app = Flask(__name__)

@app.route('/scrape')
def scrape():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'Falta el parámetro url'}), 400

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/google-chrome"

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    headers = [h.text for h in driver.find_elements(By.TAG_NAME, "h2")]
    driver.quit()

    return jsonify({'headers': headers})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
