from baselayer.app.access import auth_or_token
import requests
import pandas as pd
import io

from skyportal.models.obj import Obj

from ..base import BaseHandler
from ...models import Instrument
from astropy.time import Time
from .photometry import add_external_photometry

FINK_ZTF_API = 'https://api.ztf.fink-portal.org'
FINK_LSST_API = 'https://api.lsst.fink-portal.org'

ZTF_BANDS = {1: 'ztfg', 2: 'ztfr', 3: 'ztfi'}
LSST_BANDS = {'u': 'lsstu', 'g': 'lsstg', 'r': 'lsstr', 'i': 'lssti', 'z': 'lsstz', 'y': 'lssty'}

# Keep legacy alias for backwards compatibility
bands = ZTF_BANDS

FINK_SURVEYS = [
    {
        'name': 'ztf',
        'base_url': FINK_ZTF_API,
        'instrument_name': 'ZTF',
    },
    {
        'name': 'lsst',
        'base_url': FINK_LSST_API,
        'instrument_name': 'LSST',
    },
]


def _resolve_fink_objects(names):
    """
    Resolve a list of names (object ID + aliases) using Fink TNS resolvers.

    For each name, queries both ZTF and LSST Fink resolvers and returns a
    deduplicated list of (survey_name, fink_object_id) tuples.
    """
    results = []
    seen = set()
    for name in names:
        if not name:
            continue
        for survey in FINK_SURVEYS:
            try:
                r = requests.get(
                    f'{survey["base_url"]}/api/v1/resolver',
                    params={'name': name, 'resolver': 'tns'},
                    timeout=10,
                )
                if r.status_code != 200 or not r.content:
                    continue
                data = r.json()
                if not isinstance(data, list):
                    continue
                for item in data:
                    obj_id = item.get('i:objectId') or item.get('d:objectId')
                    key = (survey['name'], obj_id)
                    if obj_id and key not in seen:
                        seen.add(key)
                        results.append(key)
            except Exception:
                continue
    return results


def _fetch_ztf_photometry(fink_object_id, obj_id, instrument_id, group_ids, user):
    """Fetch ZTF photometry from Fink and post it to SkyPortal."""
    r = requests.post(
        f'{FINK_ZTF_API}/api/v1/objects',
        json={
            'objectId': fink_object_id,
            'output-format': 'json',
            'withupperlim': True,
        },
    )
    if r.status_code != 200:
        raise ValueError(
            f"Request to Fink ZTF API failed for object {fink_object_id} (status {r.status_code})"
        )

    df = pd.read_json(io.BytesIO(r.content))
    if len(df.index) == 0:
        return

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
    if not set(desired_columns).issubset(set(df.columns)):
        raise ValueError(
            f"Missing expected columns in Fink ZTF response for object {fink_object_id}"
        )

    data = {
        'obj_id': [obj_id] * len(df),
        'ra': df['i:ra'],
        'dec': df['i:dec'],
        'mag': df['i:magpsf'],
        'magerr': df['i:sigmapsf'],
        'limiting_mag': df['i:diffmaglim'],
        'filter': [ZTF_BANDS[int(band)] for band in df['i:fid']],
        'mjd': [Time(float(jd), format="jd").mjd for jd in df["i:jd"]],
        'magsys': ['ab'] * len(df),
        'instrument_id': instrument_id,
        'group_ids': group_ids,
    }
    add_external_photometry(data, user)
    return len(df)


def _fetch_lsst_photometry(fink_object_id, obj_id, instrument_id, group_ids, user):
    """Fetch LSST photometry from Fink (flux-space, nJy, zp=31.4) and post it to SkyPortal."""
    r = requests.post(
        f'{FINK_LSST_API}/api/v1/objects',
        json={
            'objectId': fink_object_id,
            'output-format': 'json',
            'withupperlim': True,
        },
    )
    if r.status_code != 200:
        raise ValueError(
            f"Request to Fink LSST API failed for object {fink_object_id} (status {r.status_code})"
        )

    df = pd.read_json(io.BytesIO(r.content))
    if len(df.index) == 0:
        return

    desired_columns = [
        'd:objectId',
        'd:ra',
        'd:dec',
        'd:psfFlux',
        'd:psfFluxErr',
        'd:band',
        'd:midpointMjdTai',
    ]
    if not set(desired_columns).issubset(set(df.columns)):
        raise ValueError(
            f"Missing expected columns in Fink LSST response for object {fink_object_id}"
        )

    unknown_bands = set(df['d:band']) - set(LSST_BANDS)
    if unknown_bands:
        raise ValueError(
            f"Unknown LSST band(s) in Fink response: {unknown_bands}"
        )

    data = {
        'obj_id': [obj_id] * len(df),
        'ra': df['d:ra'],
        'dec': df['d:dec'],
        'flux': df['d:psfFlux'],
        'fluxerr': df['d:psfFluxErr'],
        'filter': [LSST_BANDS[b] for b in df['d:band']],
        'mjd': df['d:midpointMjdTai'],
        'magsys': ['ab'] * len(df),
        'zp': [31.4] * len(df),
        'instrument_id': instrument_id,
        'group_ids': group_ids,
    }
    add_external_photometry(data, user)
    return len(df)


def _fetch_photometry_for_survey(
    survey_name, fink_object_id, obj_id, instrument_id, group_ids, user
):
    """Dispatch photometry fetching to the correct survey handler. Returns row count."""
    if survey_name == 'ztf':
        return _fetch_ztf_photometry(fink_object_id, obj_id, instrument_id, group_ids, user) or 0
    elif survey_name == 'lsst':
        return _fetch_lsst_photometry(fink_object_id, obj_id, instrument_id, group_ids, user) or 0
    return 0


class FinkPhotometryHandler(BaseHandler):
    @auth_or_token
    async def post(self, object_id):
        if not isinstance(object_id, str):
            return self.error("Invalid object ID")
        object_id = object_id.strip()

        data = self.get_json()
        current_magsys = data.get('magsys', 'ab')
        if current_magsys is None:
            current_magsys = 'ab'
        elif current_magsys not in ['ab', 'vega']:
            return self.error('Invalid magsys, must be either ab or vega')

        try:
            with self.Session() as session:
                obj = session.scalars(
                    Obj.select(session.user_or_token).where(Obj.id == object_id)
                ).first()
                if not obj:
                    return self.error("Object not found")

                group_ids = [
                    g.id
                    for g in self.current_user.accessible_groups
                    if not g.single_user_group
                ]

                # Collect all names to try: the skyportal object ID plus any aliases
                names_to_resolve = [object_id] + (obj.alias or [])

                # Try to resolve via Fink TNS resolvers on both ZTF and LSST endpoints
                resolved = _resolve_fink_objects(names_to_resolve)

                total_points = 0

                if resolved:
                    for survey_name, fink_object_id in resolved:
                        survey = next(
                            s for s in FINK_SURVEYS if s['name'] == survey_name
                        )
                        stmt = Instrument.select(session.user_or_token).where(
                            Instrument.name == survey['instrument_name']
                        )
                        instrument = session.scalars(stmt).first()
                        if not instrument:
                            return self.error(
                                f'Could not find any instrument named {survey["instrument_name"]}, '
                                f'cannot post {survey_name.upper()} photometry from Fink'
                            )
                        total_points += _fetch_photometry_for_survey(
                            survey_name,
                            fink_object_id,
                            object_id,
                            instrument.id,
                            group_ids,
                            self.associated_user_object,
                        )
                else:
                    # No TNS resolver match — try each name directly against both
                    # ZTF and LSST Fink APIs (covers direct ZTF/LSST IDs)
                    for name in names_to_resolve:
                        if not name:
                            continue
                        for survey in FINK_SURVEYS:
                            stmt = Instrument.select(session.user_or_token).where(
                                Instrument.name == survey['instrument_name']
                            )
                            instrument = session.scalars(stmt).first()
                            if not instrument:
                                continue
                            try:
                                total_points += _fetch_photometry_for_survey(
                                    survey['name'],
                                    name,
                                    object_id,
                                    instrument.id,
                                    group_ids,
                                    self.associated_user_object,
                                )
                            except Exception:
                                # This name may not exist in this survey — silently skip
                                continue

                self.push_all(
                    action='skyportal/REFRESH_SOURCE_PHOTOMETRY',
                    payload={'obj_id': obj.id, 'magsys': current_magsys},
                )
                return self.success(data={'total_points': total_points})
        except Exception as e:
            return self.error(str(e))
