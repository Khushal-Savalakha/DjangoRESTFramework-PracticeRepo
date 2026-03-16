def extract_serializer_errors(exception):
    """Extracts error messages from serializer validation errors."""
    if hasattr(exception, "detail"):
        error_messages = exception.detail
    else:
        error_messages = str(exception)

    if isinstance(error_messages, dict):
        for _key, value in error_messages.items():
            if isinstance(value, list) and value:
                error_message = value[0]
            elif isinstance(value, str):
                error_message = value
            else:
                error_message = "Validation failed"
            return str(error_message).replace('"', "").replace("'", "")
    elif isinstance(error_messages, str):
        return error_messages.replace('"', "").replace("'", "")
    elif isinstance(error_messages, list):
        return (
            str(error_messages[0]).replace('"', "").replace("'", "")
        )  # Extract first error

    return "Validation failed"
