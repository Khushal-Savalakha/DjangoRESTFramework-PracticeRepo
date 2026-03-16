import re

from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


def get_model_name(view):
    if hasattr(view, "queryset") and view.queryset is not None:
        model = view.queryset.model
        formatted_name = re.sub(r"(?<!^)([A-Z])", r" \1", model.__name__)
        return formatted_name
    return "Unknown"


class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        """Modify api response format.
        Example success:
        {
            "code": 200,
            "status": "success",
            "message": "ModelName action successfully",
            "data": {
                "username": "username"
            }
        }
        Example error:
        {
            "code": 400,
            "status": "failed",
            "message": "Error message"
            "error": {
                [
                    {
                        "source": "detail"
                        "detail": "Error message"
                    }
                ]
            }
        }
        """
        response = renderer_context.get("response")
        request = renderer_context.get("request")
        view = renderer_context.get("view")

        modified_data = {}
        modified_data["code"] = response.status_code
        modified_data["status"] = (
            "success" if 200 <= response.status_code < 300 else "failed"
        )
        method = request.method
        model_name = get_model_name(view)

        if response.status_code in [200, 201, 204]:
            if data is not None:
                if "message" in data:
                    modified_data["message"] = data["message"]
                    if "data" in data:
                        data = data["data"]
                    else:
                        data = {}
                else:
                    if method == "POST":
                        modified_data["message"] = f"{model_name} created successfully"
                    elif method in ["PUT", "PATCH"]:
                        modified_data["message"] = f"{model_name} updated successfully"
                    elif method == "DELETE":
                        modified_data["message"] = f"{model_name} deleted successfully"
                    else:
                        modified_data["message"] = f"{model_name} fetched successfully"
            else:
                if method == "DELETE":
                    modified_data["message"] = f"{model_name} deleted successfully"

        if status.is_client_error(response.status_code) or status.is_server_error(
            response.status_code
        ):
            if isinstance(data, dict) and "errors" in data:
                modified_data["error"] = data["errors"]
            else:
                modified_data["error"] = self.get_clean_error(data)

            if isinstance(data, dict) and "message" in data:
                msg = data["message"]
                if isinstance(msg, str):
                    modified_data["message"] = msg
                elif isinstance(msg, dict):
                    first_key = next(iter(msg), None)
                    first_val = msg.get(first_key)
                    if isinstance(first_val, list) and first_val:
                        modified_data["message"] = str(first_val[0])
                    elif isinstance(first_val, str):
                        modified_data["message"] = first_val
                    else:
                        modified_data["message"] = "Something went wrong"
                else:
                    modified_data["message"] = "Something went wrong"
            elif (
                isinstance(modified_data.get("error"), list) and modified_data["error"]
            ):
                first_error = modified_data["error"][0]
                if isinstance(first_error, dict) and "detail" in first_error:
                    modified_data["message"] = first_error["detail"]
                else:
                    modified_data["message"] = "Something went wrong"
            else:
                modified_data["message"] = "Something went wrong"

        else:
            modified_data["data"] = data

        return super().render(modified_data, accepted_media_type, renderer_context)

    def get_api_error(self, source, detail):
        error_obj = {}
        error_obj["source"] = source
        error_obj["detail"] = detail
        return error_obj

    def get_clean_error(self, data):
        errors = []
        if isinstance(data, dict):
            for key, val in data.items():
                ed = ErrorDetail(val)
                if isinstance(val, list):
                    try:
                        val = " ,".join(val)
                    except Exception:
                        pass
                if val == "Given token not valid for any token type":
                    val = "Token is invalid or expired"
                    errors.append(self.get_api_error(source=key, detail=val))
                    break
                errors.append(self.get_api_error(source=key, detail=val))
        else:
            for v in data:
                ed = ErrorDetail(v)
                if isinstance(v, list):
                    try:
                        v = ", ".join(v)
                    except Exception:
                        pass
                errors.append(self.get_api_error(source="non_field_errors", detail=v))
        return errors


def get_response(
    status_code=HTTP_200_OK,
    message="Request has been processed successfully.",
    is_success=False,
    data=None,
    errors=None,
):
    if status_code == HTTP_200_OK:
        is_success = True
    return Response(
        {
            "status": is_success,
            "message": message,
            "data": data,
            "errors": errors,
        },
        status=status_code,
    )
