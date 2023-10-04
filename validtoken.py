from flask import Flask, request, jsonify, send_file
import jwt
import datetime
import main  # Import your main module here
import os

# Constants
SECRET_KEY = 'K4v/+mWYHq1751qa7Kycp58YFN7YAGEKhw71B1STU0yPfskISCK+/oG4Lq9ir3uNq4goZgcxvCmBAIUZQfahwHNDE5eWAonwK/qB7OIX6CwyixIci8vkaMhkgyi5OPxChGro0WwPIlzJboQ7v4Wag4P0ooNemtdN6vxvYBhUdAftxgki84JWULze2s/FufCg5jSxcaLf2Wp83MD9U4G2RcV1vSW8zxle4TTxYj4ISj10gkQEShQXUEsvW1uQjq47u1RVPm4c1RRSL32aPqHUYH1nbykpnCGDmrnyTyeg+W+yZVwxCI65+wTVuwBn2HD6wLq7Rthe0N8FjlrSzYojroSHVe5+0kcfiw2XymLyo7Ottq7KL3/OzwuH2yLTbvKvXqhP3YmiyLe7zMV3IR02uzeZwk7aMvfPNkR8+kzniVsq950unz8+VnESjydNG67X5rWnI0+Hi8X3Bmo8dl2WBmB9a2cJjgD/038PREhcxR4tA4IZmvjCiwxQWVmMQtbkaItA241oOeCVwpSEMlOWEKvGbXFB1MIZXdmViKZIe1HmRJyWolpTFouzm0QYiex51tYnCenQDNNiK4hABKhdS2lECdF8yFqB/2vOigZH49/lrtkgDAmazBoP2a6KqeoD3jQ6dRJNK+KU1Nk1zyBkHtkQpT7jsDLYSZ0unu1GAUZTIise8bOE7jOGVPC1vqoo9hn8KkA4Cc/OAJw0kbVyOKIbesXlcbQqju6kMnPDsriYLoUmG372o2gvZ9mvrbmJqC0vaRZamt1gSgqzcy1/E5fdQ4dmN97qf+AVMLIptnCSMo9rEDjJFTjrYsJDNqF7ydenuHfWizGtYLpcS2PPkkhTATfdSAWUtRStM6ncXFpwZyGhuU9wl0yxtXtpnLRDcdrMUMgIHB0k8hlYVsbwTQeRn8rX2I+WoCsi9Zb5JDM81L9czzd+gYSgw32ffRCoGmQod0v73BeQ4jDl88qDIAJfWcL5qQlLw3R0J+QZYmEMeuMtfJZRvnvU5p3KfZH4FvJtVMDAaILiZ+tLg1mE2FidpIbd7VTCCiAluSzSQb6uBxcVhd3yTFUJQHpFLAbl4eiloEVD0Z0gqOoPUYud91S1199djPA686AzuNpGo9wqDvupsBCBbYinKXM6yf7VHyMNy2fO5N6GX9y544Gn+hOmnUaDx2Fffx/FXwneeILTT0lAkbPWZw9jd0SdqBWUcECrX9gEic6U/QpHlhiu234Xfx1mwBcyCQ+M1jm2aESJmlxfj/lhPZ5fyGX8Ftwi08g53amphhg8WNGBx/aBtUBX+gFY0Saeg5ES+CFE+CM7ytu4L/r8imkuAFtNYjuwRhwkdCpYOTmblur6bJFkHwTtSYfX/EzkOAQ5pRksFrg='


app = Flask(__name__)

class TokenValidationError(Exception):
    pass

class TokenExpiredError(TokenValidationError):
    pass

def validate_jwt(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        expiration_timestamp = payload['exp']
        current_timestamp = datetime.datetime.utcnow().timestamp()

        if current_timestamp >= expiration_timestamp:
            raise TokenExpiredError("JWT has expired")

        # If the token is valid, return the payload
        return payload

    except jwt.ExpiredSignatureError:
        raise TokenExpiredError("JWT has expired")

    except jwt.DecodeError:
        raise TokenValidationError("Invalid token format")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise TokenValidationError("An error occurred while processing the token")

@app.route('/process_data', methods=['POST'])
def process_data():
    try:
        json_data = request.get_json()
        print(json_data)

        if 'authentificationData' not in json_data or 'token' not in json_data['authentificationData']:
            return jsonify({'error': 'Token not found in request'}), 400
        

        jwt_token = json_data['authentificationData']['token']
        jwt_payload = validate_jwt(jwt_token)

        photobyte = json_data['data']['file_bytea']

        # Call the startmain method from main.py
        main.start_ocr(photobyte)  

        # Send output.json back to the request
        if os.path.exists('output.json'):
            response = send_file('output.json', as_attachment=True, download_name='output.json'), 200
            os.remove('output.json')
            return response, 200
        else:
            return jsonify({'error': 'output.json not found'}), 404
        
        
        # return jsonify({'message': 'Data processed successfully'}), 200

    except TokenExpiredError:
        return jsonify({'error': 'JWT is expired'}), 401
    except TokenValidationError as e:
        return jsonify({'error': f'Validation error: {str(e)}'}), 408

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)  # Change the host and port as needed








# import jwt
# import datetime
# import main  # Import your main module here

# # Constants
# SECRET_KEY = 'asdfgh'
# JWT_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJleHAiOjE2OTYxNjg4NDZ9.M8tMm5R5qghccRFR69s0dMllfYWRWYxi3leIGnyNSy0'

# class TokenValidationError(Exception):
#     pass

# class TokenExpiredError(TokenValidationError):
#     pass

# def validate_jwt(token):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
#         expiration_timestamp = payload['exp']
#         current_timestamp = datetime.datetime.utcnow().timestamp()

#         if current_timestamp >= expiration_timestamp:
#             raise TokenExpiredError("JWT has expired")

#         # If the token is valid, return the payload
#         return payload

#     except jwt.ExpiredSignatureError:
#         raise TokenExpiredError("JWT has expired")
#     except jwt.DecodeError:
#         raise TokenValidationError("Invalid token format")
#     except Exception as e:
#         print(f"An error occurred: {str(e)}")
#         raise TokenValidationError("An error occurred while processing the token")

# try:
#     jwt_payload = validate_jwt(JWT_TOKEN)
#     main.start_ocr()  # Call the startmain method from main.py
# except TokenExpiredError:
#     print("Error 505: JWT is expired")
# except TokenValidationError as e:
#     print(f"Validation error: {str(e)}")