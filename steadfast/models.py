"""Data models for Steadfast SDK."""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any


@dataclass
class Order:
    """Single order response model."""

    consignment_id: int
    invoice: str
    tracking_code: str
    recipient_name: str
    recipient_phone: str
    recipient_address: str
    cod_amount: float
    status: str
    note: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class BulkOrderResult:
    """Individual result in bulk order response."""

    invoice: str
    recipient_name: str
    recipient_address: str
    recipient_phone: str
    cod_amount: float
    note: Optional[str] = None
    consignment_id: Optional[int] = None
    tracking_code: Optional[str] = None
    status: str = "error"  # "success" or "error"
    error: Optional[str] = None


@dataclass
class BulkOrderResponse:
    """Bulk order creation response."""

    results: List[BulkOrderResult]


@dataclass
class OrderStatus:
    """Order status response model."""

    status: int  # HTTP status code
    delivery_status: str  # Current delivery status


@dataclass
class Balance:
    """Account balance response model."""

    status: int
    current_balance: float


@dataclass
class ReturnRequest:
    """Return request model."""

    id: int
    user_id: int
    consignment_id: int
    reason: Optional[str] = None
    status: str = "pending"  # pending, approved, processing, completed,
    # cancelled
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class ReturnRequestList:
    """List of return requests."""

    data: List[ReturnRequest]


@dataclass
class Payment:
    """Payment information model."""

    id: int
    amount: float
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class PaymentDetails:
    """Payment details with consignments."""

    id: int
    amount: float
    consignments: List[Dict[str, Any]]
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class PaymentList:
    """List of payments."""

    data: List[Payment]


@dataclass
class PoliceStation:
    """Police station information."""

    id: int
    name: str
    location: str


@dataclass
class PoliceStationList:
    """List of police stations."""

    data: List[PoliceStation]
