from baselayer.app.access import auth_or_token
import requests
import pandas as pd
import io

from skyportal.models.obj import Obj

from ..base import BaseHandler
from ...models import Instrument
from astropy.time import Time
from .photometry import add_external_photometry

bands = {1: 'ztfg', 2: 'ztfr', 3: 'ztfi'}


class FinkPhotometryHandler(BaseHandler):
    @auth_or_token
    async def post(self, object_id):
        try:
            with self.Session() as session:
                if not isinstance(object_id, str):
                    return self.error("Invalid object ID")
                object_id = object_id.strip()
                obj = session.scalars(
                    Obj.select(session.user_or_token).where(Obj.id == object_id)
                ).first()
                if not obj:
                    return self.error("Object not found")
                r = requests.post(
                    'https://fink-portal.org/api/v1/objects',
                    json={'objectId': object_id, 'output-format': 'json'},
                )
                if r.status_code != 200:
                    return self.error("Request to Fink's API failed")
                df_request = pd.read_json(io.BytesIO(r.content))
                if len(df_request.index) > 0:
                    desired_columns = [
                        'i:objectId',
                        'i:ra',
                        'i:dec',
                        'i:magpsf',
                        'i:sigmapsf',
                        'i:diffmaglim',
                        'i:fid',
                        'i:jd',
                    ]
                    if not set(desired_columns).issubset(set(df_request.columns)):
                        return self.error('Missing expected column')

                    stmt = Instrument.select(session.user_or_token).where(
                        Instrument.name == 'CFH12k' or Instrument.name == 'ZTF'
                    )
                    instrument = session.scalars(stmt).first()
                    if not instrument:
                        return self.error(
                            'No instrument named CFH12k or ZTF found to post the photometry'
                        )
                    instrument_id = instrument.id
                    data = {
                        'obj_id': df_request['i:objectId'],
                        'ra': df_request['i:ra'],
                        'dec': df_request['i:dec'],
                        'mag': df_request['i:magpsf'],
                        'magerr': df_request['i:sigmapsf'],
                        'limiting_mag': df_request['i:diffmaglim'],
                        'filter': [bands[band] for band in df_request['i:fid']],
                        'mjd': [Time(jd, format="jd").mjd for jd in df_request["i:jd"]],
                        'magsys': ['ab' for i in range(len(df_request))],
                        'instrument_id': instrument_id,
                        'group_ids': [
                            g.id for g in self.current_user.accessible_groups
                        ],
                    }

                    add_external_photometry(data, self.associated_user_object)
                self.push_all(
                    action='skyportal/REFRESH_SOURCE',
                    payload={'obj_key': obj.internal_key},
                )
                return self.success()
        except Exception as e:
            return self.error(str(e))
