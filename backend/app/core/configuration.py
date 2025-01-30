from functools import lru_cache
from environs import Env

path_to_env = "../.env"


@lru_cache
def get_config():
    """Load and cache configuration from .env.

    Raise errors if some value is missing or .env doesn't exist.
    """
    env = Env()
    env.read_env(path_to_env, recurse=False)
    env_data: dict = {
        "database_url": env.str("database_url"),
        "jwt_secret_key": env.str("jwt_secret_key"),
        "jwt_algorithm": env.str("jwt_algorithm"),
        "admin_username": env.str("admin_username"),
        "admin_email": env.str("admin_email"),
        "admin_password": env.str("admin_password"),
        "access_token_duration_hours": env.int("access_token_duration_hours"),
    }
    return env_data


app_config = get_config()
