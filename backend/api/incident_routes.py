"""
Incident Management API Routes
FastAPI endpoints for incident management
"""
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
import logging

from backend.model.incident_model import (
    IncidentResponse,
    IncidentStatusUpdate,
    IncidentAssignment,
    IncidentNoteAdd,
    IncidentStats,
    IncidentCreate
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/incidents", tags=["incidents"])

# Database will be injected
db = None

def set_database(database):
    global db
    db = database

@router.get("/", response_model=List[IncidentResponse])
async def get_incidents(
    status: Optional[str] = Query(None, description="Filter by status"),
    severity: Optional[str] = Query(None, description="Filter by severity"),
    limit: int = Query(50, le=500),
    skip: int = Query(0, ge=0)
):
    """Get list of incidents with optional filters"""
    try:
        query = {}
        
        if status:
            query['status'] = status
        if severity:
            query['severity'] = severity
        
        cursor = db.incidents.find(query).sort('created_at', -1).skip(skip).limit(limit)
        incidents = await cursor.to_list(length=limit)
        
        # Convert ObjectId to string
        for incident in incidents:
            incident['_id'] = str(incident['_id'])
        
        return incidents
        
    except Exception as e:
        logger.error(f"Error fetching incidents: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats", response_model=IncidentStats)
async def get_incident_stats():
    """Get incident statistics"""
    try:
        # Total incidents
        total = await db.incidents.count_documents({})
        
        # By status
        status_pipeline = [
            {'$group': {'_id': '$status', 'count': {'$sum': 1}}}
        ]
        status_results = await db.incidents.aggregate(status_pipeline).to_list(length=100)
        by_status = {item['_id']: item['count'] for item in status_results}
        
        # By severity
        severity_pipeline = [
            {'$group': {'_id': '$severity', 'count': {'$sum': 1}}}
        ]
        severity_results = await db.incidents.aggregate(severity_pipeline).to_list(length=100)
        by_severity = {item['_id']: item['count'] for item in severity_results}
        
        # Open incidents
        open_count = await db.incidents.count_documents({'status': 'Open'})
        
        # Critical incidents
        critical_count = await db.incidents.count_documents({'severity': 'CRITICAL'})
        
        # Average resolution time
        resolved_incidents = await db.incidents.find({
            'status': {'$in': ['Resolved', 'Closed']}
        }).to_list(length=1000)
        
        avg_resolution_time = None
        if resolved_incidents:
            total_time = 0
            count = 0
            for incident in resolved_incidents:
                created = incident.get('created_at')
                updated = incident.get('updated_at')
                if created and updated:
                    diff = (updated - created).total_seconds() / 3600  # hours
                    total_time += diff
                    count += 1
            
            if count > 0:
                avg_resolution_time = total_time / count
        
        return {
            'total_incidents': total,
            'by_status': by_status,
            'by_severity': by_severity,
            'avg_resolution_time_hours': avg_resolution_time,
            'open_incidents': open_count,
            'critical_incidents': critical_count
        }
        
    except Exception as e:
        logger.error(f"Error fetching incident stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{incident_id}", response_model=IncidentResponse)
async def get_incident(incident_id: str):
    """Get specific incident by ID"""
    try:
        incident = await db.incidents.find_one({'incident_id': incident_id})
        
        if not incident:
            raise HTTPException(status_code=404, detail="Incident not found")
        
        incident['_id'] = str(incident['_id'])
        return incident
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching incident {incident_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{incident_id}/status")
async def update_incident_status(incident_id: str, update: IncidentStatusUpdate):
    """Update incident status"""
    try:
        incident = await db.incidents.find_one({'incident_id': incident_id})
        
        if not incident:
            raise HTTPException(status_code=404, detail="Incident not found")
        
        # Add timeline event
        timeline_event = {
            'timestamp': datetime.utcnow(),
            'action': 'status_changed',
            'description': f"Status changed to {update.status}"
        }
        
        if update.note:
            timeline_event['description'] += f": {update.note}"
        
        # Update incident
        update_data = {
            'status': update.status,
            'updated_at': datetime.utcnow(),
            '$push': {'timeline': timeline_event}
        }
        
        result = await db.incidents.update_one(
            {'incident_id': incident_id},
            {'$set': update_data}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=400, detail="Failed to update incident")
        
        return {"message": "Incident status updated", "incident_id": incident_id}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating incident status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{incident_id}/assign")
async def assign_incident(incident_id: str, assignment: IncidentAssignment):
    """Assign incident to analyst"""
    try:
        incident = await db.incidents.find_one({'incident_id': incident_id})
        
        if not incident:
            raise HTTPException(status_code=404, detail="Incident not found")
        
        # Add timeline event
        timeline_event = {
            'timestamp': datetime.utcnow(),
            'action': 'assigned',
            'description': f"Assigned to {assignment.analyst}",
            'analyst': assignment.analyst
        }
        
        if assignment.note:
            timeline_event['description'] += f": {assignment.note}"
        
        # Update incident
        result = await db.incidents.update_one(
            {'incident_id': incident_id},
            {
                '$set': {
                    'assigned_analyst': assignment.analyst,
                    'updated_at': datetime.utcnow()
                },
                '$push': {'timeline': timeline_event}
            }
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=400, detail="Failed to assign incident")
        
        return {"message": "Incident assigned", "incident_id": incident_id, "analyst": assignment.analyst}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error assigning incident: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{incident_id}/notes")
async def add_incident_note(incident_id: str, note_data: IncidentNoteAdd):
    """Add note to incident"""
    try:
        incident = await db.incidents.find_one({'incident_id': incident_id})
        
        if not incident:
            raise HTTPException(status_code=404, detail="Incident not found")
        
        # Create note
        note = {
            'timestamp': datetime.utcnow(),
            'analyst': note_data.analyst,
            'note': note_data.note
        }
        
        # Add timeline event
        timeline_event = {
            'timestamp': datetime.utcnow(),
            'action': 'note_added',
            'description': f"Note added by {note_data.analyst}",
            'analyst': note_data.analyst
        }
        
        # Update incident
        result = await db.incidents.update_one(
            {'incident_id': incident_id},
            {
                '$set': {'updated_at': datetime.utcnow()},
                '$push': {
                    'notes': note,
                    'timeline': timeline_event
                }
            }
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=400, detail="Failed to add note")
        
        return {"message": "Note added", "incident_id": incident_id}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error adding note: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=IncidentResponse)
async def create_incident(incident: IncidentCreate):
    """Manually create incident"""
    try:
        import uuid
        
        incident_data = {
            'incident_id': str(uuid.uuid4()),
            'title': incident.title,
            'description': incident.description,
            'severity': incident.severity,
            'status': 'Open',
            'related_alert_ids': incident.related_alert_ids,
            'alert_count': len(incident.related_alert_ids),
            'assigned_analyst': None,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'mitre_tactic': incident.mitre_tactic,
            'mitre_technique': incident.mitre_technique,
            'timeline': [
                {
                    'timestamp': datetime.utcnow(),
                    'action': 'incident_created',
                    'description': 'Incident created manually'
                }
            ],
            'notes': [],
            'correlation_rule': None
        }
        
        result = await db.incidents.insert_one(incident_data)
        incident_data['_id'] = str(result.inserted_id)
        
        return incident_data
        
    except Exception as e:
        logger.error(f"Error creating incident: {e}")
        raise HTTPException(status_code=500, detail=str(e))
