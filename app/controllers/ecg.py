from flask import g
from main import app
from rq.job import Job
from rq.exceptions import NoSuchJobError
from core.errors import ECGException
from models.database import db_session, ECG, ECGLeads
from modules import metrics


@db_session
def process_ecg(ecg: dict):
    if ECG.get(id=ecg.get('id')):
        raise ECGException(f"ECG id: {ecg.get('id')} already exists")
    
    new_ecg = ECG(id=ecg.get('id'), user=g.user, date=ecg.get('date'))

    leads = [ECGLeads(ecg=new_ecg, **l) for l in ecg.get('leads', [])]

    job = app.queue.enqueue(metrics.process_all, ecg, job_id=new_ecg.id, description=f"ECG process all: {new_ecg.id}")

    return {"id": new_ecg.id, "status": "queued"}, 201


@db_session
def get_ecg(ecg_id):
    # Checking ECG Exists
    ecg = ECG.get(id=ecg_id, user=g.user)
    if not ecg:
        return {"id": ecg_id, "status": "not_found"}, 404

    # Gathering ECG Leads
    ecg_data = ecg.to_dict()
    ecg_leads = ECGLeads.select(ecg=ecg_id)[:]
    ecg_data['leads'] = [l.to_dict() for l in ecg_leads]

    try:
        job = Job.fetch(ecg_id, connection=app.cache)
    except NoSuchJobError:
        job = None

    # Check Job data persisted on db and persist
    if any(l['count_zero_crossings'] is not None for l in ecg_data['leads']):
        data = ecg_data
    elif not job:
        return {"id": ecg_id, "status": "not_found"}, 404
    elif job.is_finished:
        data = job.result
        for lead in data["leads"]:
            update_params = {
                "count_zero_crossings": lead.get("count_zero_crossings", 0),
            }
            ECGLeads.get(ecg=ecg_id, name=lead["name"]).set(**update_params)
    else:
        return {"id": ecg_id, "status": "queued"}, 200
    
    leads = [
        {
            lead['name']: {
                "zero_crossings": lead["count_zero_crossings"]
            }
        }
        for lead in data['leads']
    ]

    return {"id": ecg_id, "status": "completed", "leads": leads}, 200
