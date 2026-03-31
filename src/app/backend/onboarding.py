from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from typing import Optional
import uuid


class Status(str, Enum):
    PENDING = "pending"
    IN_REVIEW = "in-review"
    APPROVED = "approved"
    ACTIVE = "active"
    COMPLETED = "completed"
    ON_HOLD = "on-hold"


@dataclass
class Note:
    id: str
    text: str
    created_at: str

    def to_dict(self) -> dict:
        return {"id": self.id, "text": self.text, "created_at": self.created_at}


@dataclass
class Onboarding:
    id: str
    client_name: str
    engagement_type: str
    description: str
    status: Status = Status.PENDING
    contact_email: str = ""
    created_at: str = ""
    notes: list[Note] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "client_name": self.client_name,
            "engagement_type": self.engagement_type,
            "description": self.description,
            "status": self.status.value,
            "contact_email": self.contact_email,
            "created_at": self.created_at,
            "notes": [n.to_dict() for n in self.notes],
        }


class OnboardingTracker:
    def __init__(self):
        self._onboardings: dict[str, Onboarding] = {}
        self._seed_data()

    def _seed_data(self):
        seed = [
            Onboarding(
                id="OB-001",
                client_name="Contoso Construction Ltd",
                engagement_type="Building Renovation",
                description="Full renovation of downtown office complex, 12 floors",
                status=Status.IN_REVIEW,
                contact_email="j.smith@contoso.com",
                created_at="2026-03-15T09:00:00Z",
                notes=[
                    Note(id="N-001", text="Initial scope review completed. Awaiting compliance check.", created_at="2026-03-16T14:30:00Z")
                ],
            ),
            Onboarding(
                id="OB-002",
                client_name="Woodgrove Legal Partners",
                engagement_type="Litigation Support",
                description="Contract dispute advisory for commercial lease agreement",
                status=Status.APPROVED,
                contact_email="m.chen@woodgrove.com",
                created_at="2026-03-10T11:00:00Z",
                notes=[
                    Note(id="N-002", text="Conflict check passed. Engagement letter sent.", created_at="2026-03-11T09:00:00Z"),
                    Note(id="N-003", text="Client signed engagement letter.", created_at="2026-03-12T16:00:00Z"),
                ],
            ),
            Onboarding(
                id="OB-003",
                client_name="Fabrikam Consulting Group",
                engagement_type="Strategy Advisory",
                description="Digital transformation roadmap for supply chain operations",
                status=Status.PENDING,
                contact_email="a.patel@fabrikam.com",
                created_at="2026-03-28T08:30:00Z",
            ),
        ]
        for ob in seed:
            self._onboardings[ob.id] = ob

    def list_all(self) -> list[dict]:
        return [ob.to_dict() for ob in self._onboardings.values()]

    def get(self, onboarding_id: str) -> Optional[dict]:
        ob = self._onboardings.get(onboarding_id)
        return ob.to_dict() if ob else None

    def create(self, client_name: str, engagement_type: str, description: str, contact_email: str = "") -> dict:
        oid = f"OB-{len(self._onboardings) + 1:03d}"
        ob = Onboarding(
            id=oid,
            client_name=client_name,
            engagement_type=engagement_type,
            description=description,
            contact_email=contact_email,
            created_at=datetime.utcnow().isoformat() + "Z",
        )
        self._onboardings[oid] = ob
        return ob.to_dict()

    def update_status(self, onboarding_id: str, new_status: str) -> Optional[dict]:
        ob = self._onboardings.get(onboarding_id)
        if not ob:
            return None
        try:
            ob.status = Status(new_status)
        except ValueError:
            return {"error": f"Invalid status '{new_status}'. Valid: {[s.value for s in Status]}"}
        return ob.to_dict()

    def add_note(self, onboarding_id: str, text: str) -> Optional[dict]:
        ob = self._onboardings.get(onboarding_id)
        if not ob:
            return None
        note = Note(
            id=f"N-{uuid.uuid4().hex[:6]}",
            text=text,
            created_at=datetime.utcnow().isoformat() + "Z",
        )
        ob.notes.append(note)
        return ob.to_dict()


# Singleton in-memory state
tracker = OnboardingTracker()
