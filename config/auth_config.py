AUTH_CONFIG = {
    "moneycontrol": {
        "login_url": "https://www.moneycontrol.com/login",
        "username_selector": "#username",
        "password_selector": "#password",
        "submit_selector": "button[type=submit]",
        "success_url": "**/feed",
        "storage_file": "login_mc.json",
        "validate_url": "https://www.moneycontrol.com/portfolio-management/user/update_profile",
        "validate_selector": ".span.username_txt"
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
