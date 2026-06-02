"""Medical office tools for the Fraser North Nephrology receptionist agent."""

from datetime import datetime
from typing import Dict, Optional


# In-memory patient store (replace with EMR integration)
_patient_store: Dict[str, dict] = {}


def register_patient(
    first_name: str,
    last_name: str,
    phone_number: str,
    date_of_birth: Optional[str] = None,
) -> Dict[str, str]:
    """
    Registers a new patient or retrieves an existing patient record
    using their name and phone number.

    Args:
        first_name: Patient's first name.
        last_name: Patient's last name.
        phone_number: Patient's phone number.
        date_of_birth: Patient's date of birth (YYYY-MM-DD), optional.

    Returns:
        A dictionary with the patient's registration status and details.
    """
    key = f"{first_name.lower()}_{last_name.lower()}_{phone_number}"
    if key in _patient_store:
        patient = _patient_store[key]
        return {
            "status": "existing_patient",
            "patient_id": patient["patient_id"],
            "message": f"Patient {first_name} {last_name} found in records.",
            "has_referral": patient.get("has_referral", "unknown"),
        }

    patient_id = f"FNN-{len(_patient_store) + 1001}"
    _patient_store[key] = {
        "patient_id": patient_id,
        "first_name": first_name,
        "last_name": last_name,
        "phone_number": phone_number,
        "date_of_birth": date_of_birth,
        "has_referral": "unknown",
        "registered_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    return {
        "status": "new_patient",
        "patient_id": patient_id,
        "message": f"New patient {first_name} {last_name} registered.",
    }


def check_schedule(
    provider_id: int,
    date: Optional[str] = None,
) -> Dict[str, str]:
    """
    Checks available appointment slots for a given provider on a specific date.

    Args:
        provider_id: The provider's ID (1=Dr. Brown, 2=Dr. Da Roza, 3=Dr. Schwartz, 4=Dr. Birks).
        date: The date to check in YYYY-MM-DD format. Defaults to today.

    Returns:
        A dictionary with available slots and provider information.
    """
    providers = {
        1: {"name": "Dr. Melanie Brown", "slot_duration": 45},
        2: {"name": "Dr. Gerald Da Roza", "slot_duration": 30},
        3: {"name": "Dr. Daniel Schwartz", "slot_duration": 35},
        4: {"name": "Dr. Peter Birks", "slot_duration": 40},
    }

    if provider_id not in providers:
        return {"status": "error", "message": "Invalid provider ID."}

    provider = providers[provider_id]
    check_date = date or datetime.now().strftime("%Y-%m-%d")

    # Placeholder: return mock available slots
    return {
        "status": "success",
        "provider": provider["name"],
        "date": check_date,
        "slot_duration_minutes": str(provider["slot_duration"]),
        "available_slots": "10:00 AM, 11:30 AM, 2:00 PM",
        "message": f"{provider['name']} has openings on {check_date}.",
    }


def transfer_call(destination: str, reason: str) -> Dict[str, str]:
    """
    Transfers the current call to the specified destination.

    Args:
        destination: The phone number or extension to transfer to
                     (e.g., 'voicemail', 'nurse_marianne', or a phone number).
        reason: Brief reason for the transfer.

    Returns:
        A dictionary with the transfer status.
    """
    destinations = {
        "voicemail": "604-516-7774 (voicemail)",
        "nurse_marianne": "+1-778-848-0967 (Nurse Marianne Robbie)",
    }

    resolved = destinations.get(destination, destination)

    return {
        "status": "transferred",
        "destination": resolved,
        "reason": reason,
        "message": f"Call transferred to {resolved}. Reason: {reason}",
    }
