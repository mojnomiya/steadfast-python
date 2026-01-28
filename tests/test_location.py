"""Tests for location module."""

from unittest.mock import Mock
import pytest
from steadfast.modules.location import LocationModule
from steadfast.models import PoliceStationList
from steadfast.exceptions import APIError


@pytest.fixture
def mock_http_client() -> Mock:
    """Create mock HTTP client."""
    return Mock()


@pytest.fixture
def location_module(mock_http_client: Mock) -> LocationModule:
    """Create location module with mock client."""
    return LocationModule(mock_http_client)


class TestLocationGetPoliceStations:
    """Tests for get_police_stations method."""

    def test_get_police_stations_success(
        self, location_module: LocationModule, mock_http_client: Mock
    ) -> None:
        """Test getting police stations successfully."""
        mock_http_client.get.return_value = {
            "data": [
                {
                    "id": 1,
                    "name": "Dhaka Central Police Station",
                    "location": "Dhaka",
                },
                {
                    "id": 2,
                    "name": "Chittagong Police Station",
                    "location": "Chittagong",
                },
                {
                    "id": 3,
                    "name": "Sylhet Police Station",
                    "location": "Sylhet",
                },
            ]
        }

        result = location_module.get_police_stations()

        assert isinstance(result, PoliceStationList)
        assert len(result.data) == 3
        assert result.data[0].id == 1
        assert result.data[0].name == "Dhaka Central Police Station"
        assert result.data[0].location == "Dhaka"
        assert result.data[1].id == 2
        assert result.data[2].id == 3
        mock_http_client.get.assert_called_once_with("/location/police-stations")

    def test_get_police_stations_empty(
        self, location_module: LocationModule, mock_http_client: Mock
    ) -> None:
        """Test getting police stations with empty list."""
        mock_http_client.get.return_value = {"data": []}

        result = location_module.get_police_stations()

        assert isinstance(result, PoliceStationList)
        assert len(result.data) == 0

    def test_get_police_stations_missing_data_field(
        self, location_module: LocationModule, mock_http_client: Mock
    ) -> None:
        """Test getting police stations with missing data field."""
        mock_http_client.get.return_value = {}

        result = location_module.get_police_stations()

        assert isinstance(result, PoliceStationList)
        assert len(result.data) == 0

    def test_get_police_stations_api_error(
        self, location_module: LocationModule, mock_http_client: Mock
    ) -> None:
        """Test getting police stations with API error."""
        mock_http_client.get.side_effect = APIError("API error", 500)

        with pytest.raises(APIError):
            location_module.get_police_stations()

    def test_get_police_stations_partial_fields(
        self, location_module: LocationModule, mock_http_client: Mock
    ) -> None:
        """Test getting police stations with partial fields."""
        mock_http_client.get.return_value = {
            "data": [
                {"id": 1, "name": "Station 1"},
                {"id": 2, "location": "Location 2"},
                {"id": 3},
            ]
        }

        result = location_module.get_police_stations()

        assert len(result.data) == 3
        assert result.data[0].id == 1
        assert result.data[0].name == "Station 1"
        assert result.data[0].location == ""
        assert result.data[1].id == 2
        assert result.data[1].name == ""
        assert result.data[1].location == "Location 2"
        assert result.data[2].id == 3
        assert result.data[2].name == ""
        assert result.data[2].location == ""

    def test_get_police_stations_single_station(
        self, location_module: LocationModule, mock_http_client: Mock
    ) -> None:
        """Test getting single police station."""
        mock_http_client.get.return_value = {
            "data": [
                {
                    "id": 1,
                    "name": "Only Station",
                    "location": "Only Location",
                }
            ]
        }

        result = location_module.get_police_stations()

        assert len(result.data) == 1
        assert result.data[0].id == 1
        assert result.data[0].name == "Only Station"

    def test_get_police_stations_large_list(
        self, location_module: LocationModule, mock_http_client: Mock
    ) -> None:
        """Test getting large list of police stations."""
        data = [
            {"id": i, "name": f"Station {i}", "location": f"Location {i}"}
            for i in range(1, 101)
        ]
        mock_http_client.get.return_value = {"data": data}

        result = location_module.get_police_stations()

        assert len(result.data) == 100
        assert result.data[0].id == 1
        assert result.data[99].id == 100
        assert result.data[50].name == "Station 51"
