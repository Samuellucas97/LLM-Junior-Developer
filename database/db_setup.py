import os
import time
from datetime import datetime
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import OperationFailure, ConnectionFailure, ServerSelectionTimeoutError
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI") or "mongodb://admin:supersecret@mongodb:27017/?authSource=admin"
DB_NAME = os.getenv("MONGO_DB") or "junior_llm"

def connect_with_retry(max_retries=10, retry_interval=3):
    """Try to connect to MongoDB with retries"""
    for attempt in range(1, max_retries + 1):
        try:
            print(f"Attempting to connect to MongoDB (attempt {attempt}/{max_retries})...")
            client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=5000)
            client.admin.command('ping')
            print(f"Successfully connected to MongoDB!")
            return client
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            print(f"Connection attempt {attempt} failed: {e}")
            if attempt < max_retries:
                print(f"Retrying in {retry_interval} seconds...")
                time.sleep(retry_interval)
            else:
                print(f"Failed to connect after {max_retries} attempts")
                raise

client = connect_with_retry()
db = client[DB_NAME]

def ensure_collection(name, **kwargs):
    if name not in db.list_collection_names():
        db.create_collection(name, **kwargs)
        print(f"Created collection: {name}")
    else:
        print(f"Collection exists: {name}")

def ensure_indexes(coll, specs):
    """specs = [ (keys_dict, opts_dict), ... ]"""
    for keys, opts in specs:
        db[coll].create_index(list(keys.items()), **(opts or {}))
        print(f"Index ok on {coll}: {keys} {opts or ''}")

def main():
    # USERS
    ensure_collection("users")
    ensure_indexes("users", [
        ({"username": ASCENDING}, {"unique": True, "name": "uniq_username"}),
        ({"roles": ASCENDING}, {"name": "idx_roles"}),
        ({"created_at": DESCENDING}, {"name": "idx_created_at_desc"}),
    ])

    # LEARNING_PROFILES (1:1 with users)
    ensure_collection("learning_profiles")
    ensure_indexes("learning_profiles", [
        ({"user_id": ASCENDING}, {"unique": True, "name": "uniq_user_id"}),
        ({"updated_at": DESCENDING}, {"name": "idx_updated_at_desc"}),
    ])

    # CONVERSATIONS
    ensure_collection("conversations")
    ensure_indexes("conversations", [
        ({"user_id": ASCENDING, "started_at": DESCENDING}, {"name": "idx_user_started"}),
        ({"user_id": ASCENDING, "last_activity_at": DESCENDING}, {"name": "idx_user_lastactivity"}),
        ({"status": ASCENDING, "last_activity_at": DESCENDING}, {"name": "idx_status_lastactivity"}),
    ])
    # MESSAGES
    ensure_collection("messages")
    ensure_indexes("messages", [
        ({"conversation_id": ASCENDING, "seq": ASCENDING}, {"unique": True, "name": "uniq_conv_seq"}),
        ({"conversation_id": ASCENDING, "date_created": ASCENDING}, {"name": "idx_conv_created"}),
    ])

    # STUCK_EVENTS
    ensure_collection("stuck_events")
    ensure_indexes("stuck_events", [
        ({"conversation_id": ASCENDING, "date_detected": DESCENDING}, {"name": "idx_conv_detected"}),
        ({"status": ASCENDING, "date_detected": DESCENDING}, {"name": "idx_status_detected"}),
    ])

    # ESCALATIONS (0..1 per stuck_event)
    ensure_collection("escalations")
    ensure_indexes("escalations", [
        ({"stuck_event_id": ASCENDING}, {"unique": True, "name": "uniq_stuck_event"}),
        ({"escalation_status": ASCENDING, "priority": ASCENDING, "sla_due_at": ASCENDING}, {"name": "idx_status_priority_sla"}),
        ({"assigned_to": ASCENDING, "escalation_status": ASCENDING, "sla_due_at": ASCENDING}, {"name": "idx_assignee_status_sla"}),
    ])

    # TOOL_RUNS
    ensure_collection("tool_runs")
    ensure_indexes("tool_runs", [
        ({"conversation_id": ASCENDING, "created_at": DESCENDING}, {"name": "idx_conv_created_desc"}),
        ({"input_hash": ASCENDING}, {"name": "idx_input_hash"}),
    ])

    # FEEDBACK
    ensure_collection("feedback")
    ensure_indexes("feedback", [
        ({"conversation_id": ASCENDING, "created_at": DESCENDING}, {"name": "idx_conv_created_desc"}),
        ({"user_id": ASCENDING, "created_at": DESCENDING}, {"name": "idx_user_created_desc"}),
    ])

    # METRICS_TS (time-series)
    if "metrics_ts" not in db.list_collection_names():
        db.create_collection(
            "metrics_ts",
            timeseries={"timeField": "t", "metaField": "meta", "granularity": "minutes"},
        )
        print("Created time-series collection: metrics_ts")
    ensure_indexes("metrics_ts", [
        ({"meta.user_id": ASCENDING, "t": DESCENDING}, {"name": "idx_user_time"}),
    ])

    # HELP_REQUESTS
    ensure_collection("help_requests")
    ensure_indexes("help_requests", [
        ({"assigned_senior_id": ASCENDING, "status": ASCENDING, "created_at": DESCENDING}, 
         {"name": "idx_senior_status_created"}),
        ({"student_id": ASCENDING, "created_at": DESCENDING}, 
         {"name": "idx_student_created"}),
        ({"status": ASCENDING, "created_at": DESCENDING}, 
         {"name": "idx_status_created"}),
    ])

    print(f"Schema setup complete for DB: {DB_NAME}")

if __name__ == "__main__":
    main()
