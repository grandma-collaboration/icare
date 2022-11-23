import sqlalchemy as sa
from sqlalchemy import event, inspect
from .classification import Classification
from .taxonomy import Taxonomy
from .obj import Obj
from baselayer.log import make_log
from skyportal.models import DBSession
from baselayer.app.models import User
from .group import Group
import re

log = make_log('source_events')

@sa.event.listens_for(Obj, "after_insert")
def source_after_insert(mapper, connection, target):
    # add a classification I-care from the Grandma Campaign Source Classification taxonomy


    @event.listens_for(inspect(target).session, "after_flush", once=True)
    def receive_after_flush(session, context):
        # find the taxonomy
        try:
            user = session.scalars(sa.select(User).where(User.id == 1)).first()
            groups = session.scalars(sa.select(Group)).all()
            source_classification_taxonomy = session.scalars(sa.select(Taxonomy).where(Taxonomy.name == "Grandma Campaign Source Classification")).first()
            source_obs_taxonomy = session.scalars(sa.select(Taxonomy).where(Taxonomy.name == "Grandma Campaign Source Observation")).first()
            if source_classification_taxonomy is None or source_obs_taxonomy is None:
                log(f"Could not find the grandma source classification or observation taxonomy")
                return
            else:
                classification = Classification(
                    obj_id=target.id,
                    classification="I-care",
                    probability=1,
                    taxonomy_id=source_classification_taxonomy.id,
                    author=user,
                    author_name=user.username,
                    groups=groups,
                )
                session.add(classification)

                # if the name of the source contains 'GRB' or 'GW', add a classification 'GO GRANDMA' from the Grandma Campaign Source Observation taxonomy
                # do the same if the source name is like 'YYYY-MM-DDTHH-MM-SS.sss' (using regex)
                if re.search(r'GRB', target.id) or re.search(r'GW', target.id) or re.search(r'\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}\.\d{3}', target.id):
                    classification = Classification(
                        obj_id=target.id,
                        classification="GO GRANDMA",
                        probability=1,
                        taxonomy_id=source_obs_taxonomy.id,
                        author=user,
                        author_name=user.username,
                        groups=groups,
                    )
                    session.add(classification)

        except Exception as e:
            log(f"Could not add classification I-care or GO GRANDMA: {e}")

@sa.event.listens_for(Classification, "after_insert")
def classification_before_insert(mapper, connection, target):
    # if a source gets a classification from the Grandma Campaign Source Classification taxonomy,
    # remove all previous classifications from the Grandma Campaign Source Classification taxonomy on that source

    @event.listens_for(inspect(target).session, "after_flush", once=True)
    def receive_after_flush(session, context):
        try:
            with DBSession() as secondSession:
                source_classification_taxonomy = secondSession.scalars(sa.select(Taxonomy).where(Taxonomy.name == "Grandma Campaign Source Classification")).first()
                source_obs_taxonomy = secondSession.scalars(sa.select(Taxonomy).where(Taxonomy.name == "Grandma Campaign Source Observation")).first()
                if source_classification_taxonomy is None or source_obs_taxonomy is None:
                    log(f"Could not find taxonomy Grandma Campaign Source Classification or Grandma Campaign Observation Status")
                    return
                else:
                    if target.taxonomy_id == source_classification_taxonomy.id:
                        stmt = sa.select(Classification).where(
                            Classification.obj_id == target.obj_id
                        ).where(Classification.taxonomy_id == source_classification_taxonomy.id)
                        classifications = secondSession.scalars(stmt).all()
                        for classification in classifications:
                            secondSession.delete(classification)
                    elif target.taxonomy_id == source_obs_taxonomy.id:
                        stmt = sa.select(Classification).where(
                            Classification.obj_id == target.obj_id
                        ).where(Classification.taxonomy_id == source_obs_taxonomy.id)
                        classifications = secondSession.scalars(stmt).all()
                        for classification in classifications:
                            secondSession.delete(classification)
                secondSession.commit()
        except Exception as e:
            log(f"Could not remove previous classifications: {e}")
