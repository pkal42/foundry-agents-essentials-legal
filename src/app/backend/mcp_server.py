from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from onboarding import tracker, Status

mcp = FastMCP(
    "Client Onboarding MCP Server",
    streamable_http_path="/",
    transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
)


@mcp.tool()
def list_onboardings() -> list[dict]:
    """List all client onboardings with their current status, client name, engagement type, and description."""
    return tracker.list_all()


@mcp.tool()
def get_onboarding(onboarding_id: str) -> dict:
    """Get the full details of a specific client onboarding by its ID (e.g., OB-001).

    Args:
        onboarding_id: The unique onboarding ID, such as OB-001 or OB-002.
    """
    result = tracker.get(onboarding_id)
    if result is None:
        return {"error": f"Onboarding '{onboarding_id}' not found."}
    return result


@mcp.tool()
def create_onboarding(client_name: str, engagement_type: str, description: str, contact_email: str = "") -> dict:
    """Create a new client onboarding record. Returns the new onboarding with its assigned ID.

    Args:
        client_name: The name of the client company or individual.
        engagement_type: The type of engagement (e.g., 'Litigation Support', 'Building Renovation', 'Strategy Advisory').
        description: A brief description of the engagement scope.
        contact_email: Optional email address for the primary client contact.
    """
    return tracker.create(client_name, engagement_type, description, contact_email)


@mcp.tool()
def update_status(onboarding_id: str, new_status: str) -> dict:
    """Update the status of an existing client onboarding.

    Args:
        onboarding_id: The unique onboarding ID (e.g., OB-001).
        new_status: The new status. Valid values: pending, in-review, approved, active, completed, on-hold.
    """
    result = tracker.update_status(onboarding_id, new_status)
    if result is None:
        return {"error": f"Onboarding '{onboarding_id}' not found."}
    return result


@mcp.tool()
def add_note(onboarding_id: str, text: str) -> dict:
    """Add a note or comment to a client onboarding record.

    Args:
        onboarding_id: The unique onboarding ID (e.g., OB-001).
        text: The note text to add.
    """
    result = tracker.add_note(onboarding_id, text)
    if result is None:
        return {"error": f"Onboarding '{onboarding_id}' not found."}
    return result
