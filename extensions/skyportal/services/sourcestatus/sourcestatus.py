from astropy.time import Time
from datetime import datetime, timedelta
import requests

from sqlalchemy import and_

from baselayer.log import make_log
from baselayer.app.models import init_db
from baselayer.app.env import load_env
from baselayer.app.flow import Flow
from skyportal.models import (
    DBSession,
    Classification,
    Taxonomy,
    Obj
)
from baselayer.app.models import User
import time

env, cfg = load_env()

init_db(**cfg['database'])

log = make_log('sourcestatus')

REQUEST_TIMEOUT_SECONDS = cfg['health_monitor.request_timeout_seconds']


def is_loaded():
    port = cfg['ports.app_internal']
    try:
        r = requests.get(
            f'http://localhost:{port}/api/sysinfo', timeout=REQUEST_TIMEOUT_SECONDS
        )
    except:  # noqa: E722
        status_code = 0
    else:
        status_code = r.status_code

    if status_code == 200:
        return True
    else:
        return False


def service():
    last_update = datetime.utcnow()
    updated = False
    while True:
        if is_loaded():
            try:
                remove_previous_status(last_update)
                last_update = datetime.utcnow()
            except Exception as e:
                log(e)
        time.sleep(15)

def remove_previous_status(last_update):
    ws_flow = Flow()
    with DBSession() as session:
        try:
            user = session.query(User).get(1)
            grandma_taxonomy = session.query(Taxonomy).filter(Taxonomy.name == 'Grandma Campaign Source Status').first()
            if grandma_taxonomy is None:
                log("No Grandma Campaign Source Status taxonomy found")
                return False
            else:
                stmt = Obj.select(user).where(
                    and_(Obj.classifications.any(Classification.taxonomy_id == grandma_taxonomy.id),
                         Obj.classifications.any(Classification.modified > last_update)
                        )
                    ).group_by(Obj.id)
                # write the same query, but filter obj which has at least 2 classifications with the grandma taxonomy
                #stmt = Obj.select(user).group_by(Obj.id).having(func.count(Obj.classifications.any(Classification.taxonomy_id == grandma_taxonomy.id)) > 1) TO FIX

                objs = session.scalars(stmt).all()
                for obj in objs:
                    if len(obj.classifications) > 1:
                        grandma_classifications = [classification for classification in obj.classifications if classification.taxonomy_id == grandma_taxonomy.id]
                        if len(grandma_classifications) > 1:
                            # remove the most recent one from that list
                            grandma_classifications.sort(key=lambda x: x.created_at, reverse=True)

                            log(f"Removing previous status for object {obj.id}")
                            # now remove those classifications
                            for classification in grandma_classifications[1:]:
                                session.delete(classification)
                                session.commit()

                            ws_flow.push(
                                user_id='*',
                                action_type='skyportal/REFRESH_SOURCE',
                                payload={'obj_key': obj.internal_key}
                            )

        except Exception as e:
            log(str(e))
            session.rollback()


if __name__ == "__main__":
    service()
