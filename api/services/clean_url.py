def sanitize_url(url: str) -> str:
    """
    Sanitize the given URL by:
    - Removing the protocol (http:// or https://)
    - Removing trailing slashes
    - Removing the www. prefix if present
    """
    if not url:
        return "unknown"

    # Remove protocol
    clean_url = url.replace("https://", "").replace("http://", "")

    # Remove trailing slashes
    clean_url = clean_url.rstrip("/")

    # Remove www. prefix
    clean_url = clean_url.lstrip("www.")

    return clean_url
