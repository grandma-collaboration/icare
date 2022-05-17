"""
IAM OAuth2 backend, docs at:
    https://tech.coursera.org/app-platform/oauth2/
"""
from social_core.backends.oauth import BaseOAuth2


class IAMOAuth2(BaseOAuth2):
    """IAM OAuth2 authentication backend"""

    name = "iam-oauth2"
    REDIRECT_STATE = False
    AUTHORIZATION_URL = "https://iam-grandma.ijclab.in2p3.fr/authorize"
    ACCESS_TOKEN_URL = "https://iam-grandma.ijclab.in2p3.fr/token"
    ACCESS_TOKEN_METHOD = "POST"
    REVOKE_TOKEN_URL = "https://iam-grandma.ijclab.in2p3.fr/revoke"
    REVOKE_TOKEN_METHOD = "GET"
    REDIRECT_STATE = False
    DEFAULT_SCOPE = ["openid", "email", "profile"]
    EXTRA_DATA = [
        ("refresh_token", "refresh_token", True),
        ("expires_in", "expires"),
        ("token_type", "token_type", True),
    ]

    def _get_username_from_response(self, response):
        elements = response.get("elements", [])
        for element in elements:
            if "id" in element:
                return element.get("id")

        return None

    def get_user_details(self, response):
        """Return user details from IAM API account"""
        if "email" in response:
            email = response["email"]
        else:
            email = ""

        name, given_name, family_name = (
            response.get("name", ""),
            response.get("given_name", ""),
            response.get("family_name", ""),
        )

        fullname, first_name, last_name = self.get_user_names(
            name, given_name, family_name
        )
        return {
            "username": email.split("@", 1)[0],
            "email": email,
            "fullname": fullname,
            "first_name": first_name,
            "last_name": last_name,
        }

    def get_user_id(self, details, response):
        """Use email as unique id"""
        if self.setting("USE_UNIQUE_USER_ID", False):
            if "sub" in response:
                return response["sub"]
            else:
                return response["id"]
        else:
            return details["email"]

    def user_data(self, access_token, *args, **kwargs):
        """Return user data from IAM API"""
        return self.get_json(
            "https://iam-grandma.ijclab.in2p3.fr/userinfo",
            headers={
                "Authorization": "Bearer %s" % access_token,
            },
        )

    def get_auth_header(self, access_token):
        return {"Authorization": f"Bearer {access_token}"}

    def revoke_token_params(self, token, uid):
        return {"token": token}

    def revoke_token_headers(self, token, uid):
        return {"Content-type": "application/json"}
