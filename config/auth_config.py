AUTH_CONFIG = {
    "linkedin": {
        "login_url": "https://www.linkedin.com/login",
        "username_selector": "#username",
        "password_selector": "#password",
        "submit_selector": "button[type=submit]",
        "success_url": "**/feed",
        "storage_file": "auth_linkedin.json"
    },

    "github": {
        "login_url": "https://github.com/login",
        "username_selector": "#login_field",
        "password_selector": "#password",
        "submit_selector": "input[type=submit]",
        "success_url": "**/dashboard",
        "storage_file": "auth_github.json"
    }
}
