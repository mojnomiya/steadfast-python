"""Return request module for Steadfast SDK."""

from typing import Union
from ..http_client import HTTPClient
from ..models import ReturnRequest, ReturnRequestList
from ..validators import (
    validate_consignment_id,
    validate_invoice,
    validate_identifier_type,
)


class ReturnRequestModule:
    """Module for managing return requests."""

    def __init__(self, http_client: HTTPClient) -> None:
        """Initialize return request module.

        Args:
            http_client: HTTPClient instance for API calls
        """
        self.http_client = http_client

    def create(
        self,
        identifier: Union[int, str],
        identifier_type: str = "consignment_id",
        reason: str = "",
    ) -> ReturnRequest:
        """Create a return request.

        Args:
            identifier: Consignment ID, invoice, or tracking code
            identifier_type: Type of identifier (consignment_id, invoice,
                tracking_code)
            reason: Optional reason for return

        Returns:
            ReturnRequest object

        Raises:
            ValidationError: If inputs are invalid
            NotFoundError: If consignment not found
            APIError: If API returns error
            NetworkError: If network error occurs
        """
        validate_identifier_type(identifier_type)

        if identifier_type == "consignment_id":
            validate_consignment_id(int(identifier))
        elif identifier_type == "invoice":
            validate_invoice(str(identifier))

        payload: dict = {
            "identifier": identifier,
            "identifier_type": identifier_type,
        }
        if reason:
            payload["reason"] = reason

        response = self.http_client.post("/return-request/store", payload)

        return ReturnRequest(
            id=response.get("id", 0),
            user_id=response.get("user_id", 0),
            consignment_id=response.get("consignment_id", 0),
            reason=response.get("reason"),
            status=response.get("status", "pending"),
            created_at=response.get("created_at"),
            updated_at=response.get("updated_at"),
        )

    def get(self, return_request_id: int) -> ReturnRequest:
        """Get a specific return request.

        Args:
            return_request_id: ID of the return request

        Returns:
            ReturnRequest object

        Raises:
            ValidationError: If return_request_id is invalid
            NotFoundError: If return request not found
            APIError: If API returns error
            NetworkError: If network error occurs
        """
        if not isinstance(return_request_id, int) or return_request_id <= 0:
            from ..exceptions import ValidationError

            raise ValidationError(
                "Return request ID must be a positive integer",
                "return_request_id",
            )

        response = self.http_client.get(f"/return-request/{return_request_id}")

        return ReturnRequest(
            id=response.get("id", 0),
            user_id=response.get("user_id", 0),
            consignment_id=response.get("consignment_id", 0),
            reason=response.get("reason"),
            status=response.get("status", "pending"),
            created_at=response.get("created_at"),
            updated_at=response.get("updated_at"),
        )

    def list(self) -> ReturnRequestList:
        """List all return requests.

        Returns:
            ReturnRequestList object with paginated results

        Raises:
            APIError: If API returns error
            NetworkError: If network error occurs
        """
        response = self.http_client.get("/return-request/list")

        requests = []
        for item in response.get("data", []):
            requests.append(
                ReturnRequest(
                    id=item.get("id", 0),
                    user_id=item.get("user_id", 0),
                    consignment_id=item.get("consignment_id", 0),
                    reason=item.get("reason"),
                    status=item.get("status", "pending"),
                    created_at=item.get("created_at"),
                    updated_at=item.get("updated_at"),
                )
            )

        return ReturnRequestList(data=requests)
