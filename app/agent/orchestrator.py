from app.queue.redis_client import redis_client


STREAM_NAME = "soc_alerts"
CONSUMER_GROUP = "investigation_group"
CONSUMER_NAME = "orchestrator_1"


def initialize_consumer_group():
    try:
        redis_client.xgroup_create(
            name=STREAM_NAME,
            groupname=CONSUMER_GROUP,
            id="0",
            mkstream=True
        )
    except Exception as error:
        if "BUSYGROUP" not in str(error):
            raise


def get_next_alert():
    messages = redis_client.xreadgroup(
        groupname=CONSUMER_GROUP,
        consumername=CONSUMER_NAME,
        streams={STREAM_NAME: ">"},
        count=1,
        block=1000
    )

    if not messages:
        return None

    stream_name, entries = messages[0]
    message_id, data = entries[0]

    return {
        "message_id": message_id,
        "data": data
    }