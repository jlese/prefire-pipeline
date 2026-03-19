import os


def validate_env(required_vars: list[str]) -> bool:
    """Check that all required environment variables are set.

    Args:
        required_vars: List of env var names to check.

    Returns:
        True if all are present, False otherwise.
    """
    missing = [v for v in required_vars if not os.getenv(v)]
    if missing:
        print(f"Error: Missing required environment variables: {', '.join(missing)}")
        print("Please check your .env file.")
        return False
    return True