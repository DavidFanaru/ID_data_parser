from flask import Flask, request, jsonify
import jwt
import datetime
import main  # Import your main module here

# Constants
SECRET_KEY = 'asdfgh'

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

        if 'authentificationData' not in json_data or 'token' not in json_data['authentificationData']:
            return jsonify({'error': 'Token not found in request'}), 400

        jwt_token = json_data['authentificationData']['token']
        jwt_payload = validate_jwt(jwt_token)

        # main.start_ocr()  # Call the startmain method from main.py

        return jsonify({'message': 'Data processed successfully'}), 200

    except TokenExpiredError:
        return jsonify({'error': 'JWT is expired'}), 401
    except TokenValidationError as e:
        return jsonify({'error': f'Validation error: {str(e)}'}), 400

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