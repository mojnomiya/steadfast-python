"""Location module for Steadfast SDK."""

from ..http_client import HTTPClient
from ..models import PoliceStation, PoliceStationList


class LocationModule:
    """Module for managing locations."""

    def __init__(self, http_client: HTTPClient) -> None:
        """Initialize location module.

        Args:
            http_client: HTTPClient instance for API calls
        """
        self.http_client = http_client

    def get_police_stations(self) -> PoliceStationList:
        """Get list of police stations.

        Returns:
            PoliceStationList object with police stations

        Raises:
            APIError: If API returns error
            NetworkError: If network error occurs
        """
        response = self.http_client.get("/location/police-stations")

        stations = []
        for item in response.get("data", []):
            stations.append(
                PoliceStation(
                    id=item.get("id", 0),
                    name=item.get("name", ""),
                    location=item.get("location", ""),
                )
            )

        return PoliceStationList(data=stations)
