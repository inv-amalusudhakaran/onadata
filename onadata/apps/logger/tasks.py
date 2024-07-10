import logging

from django.core.cache import cache
from django.db import DatabaseError
from django.utils import timezone

from onadata.apps.logger.models import EntityList, Project
from onadata.celeryapp import app
from onadata.libs.utils.cache_tools import BATCH_PROJECT_IDS_CACHE, safe_delete
from onadata.libs.utils.project_utils import set_project_perms_to_object


logger = logging.getLogger(__name__)


@app.task(retry_backoff=3, autoretry_for=(DatabaseError, ConnectionError))
def set_entity_list_perms_async(entity_list_id):
    """Set permissions for EntityList asynchronously

    Args:
        pk (int): Primary key for EntityList
    """
    try:
        entity_list = EntityList.objects.get(pk=entity_list_id)

    except EntityList.DoesNotExist as err:
        logger.exception(err)
        return

    set_project_perms_to_object(entity_list, entity_list.project)


@app.task(retry_backoff=3, autoretry_for=(DatabaseError, ConnectionError))
def apply_project_date_modified_async():
    project_ids = cache.get(BATCH_PROJECT_IDS_CACHE, set())
    if not project_ids:
        return

    # Update project date_modified field in batches
    Project.objects.filter(pk__in=project_ids).update(date_modified=timezone.now())

    # Clear cache after updating
    safe_delete(BATCH_PROJECT_IDS_CACHE)
