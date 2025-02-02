from functools import lru_cache
from environs import Env

path_to_env = ".env"


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
        "first_user_username": env.str("first_user_username"),
        "first_user_password": env.str("first_user_password"),
        "access_token_duration_hours": env.int("access_token_duration_hours"),
    }
    return env_data


main_config = get_config()
