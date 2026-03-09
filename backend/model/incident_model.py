"""
Incident Data Models
Pydantic models for incident management
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class IncidentStatus(str, Enum):
    OPEN = "Open"
    INVESTIGATING = "Investigating"
    RESOLVED = "Resolved"
    CLOSED = "Closed"
    FALSE_POSITIVE = "False Positive"

class IncidentSeverity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class TimelineEvent(BaseModel):
    timestamp: datetime
    action: str
    description: str
    analyst: Optional[str] = None

class IncidentNote(BaseModel):
    timestamp: datetime
    analyst: str
    note: str

class IncidentCreate(BaseModel):
    title: str
    description: str
    severity: IncidentSeverity
    related_alert_ids: List[str] = []
    mitre_tactic: Optional[str] = None
    mitre_technique: Optional[str] = None

class IncidentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[IncidentSeverity] = None
    status: Optional[IncidentStatus] = None
    assigned_analyst: Optional[str] = None

class IncidentStatusUpdate(BaseModel):
    status: IncidentStatus
    note: Optional[str] = None

class IncidentAssignment(BaseModel):
    analyst: str
    note: Optional[str] = None

class IncidentNoteAdd(BaseModel):
    analyst: str
    note: str

class IncidentResponse(BaseModel):
    incident_id: str
    title: str
    description: str
    severity: str
    status: str
    related_alert_ids: List[str]
    alert_count: int
    assigned_analyst: Optional[str]
    created_at: datetime
    updated_at: datetime
    mitre_tactic: Optional[str]
    mitre_technique: Optional[str]
    timeline: List[TimelineEvent]
    notes: List[IncidentNote] = []
    correlation_rule: Optional[str] = None

class IncidentStats(BaseModel):
    total_incidents: int
    by_status: dict
    by_severity: dict
    avg_resolution_time_hours: Optional[float]
    open_incidents: int
    critical_incidents: int
