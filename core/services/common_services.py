import copy

from django.db.models import QuerySet
from django.utils import timezone


def item_update(instance, commit=False, **kwargs):
    """
    :param instance: Model instance
    :param commit: необязательное, при commit=False возаращает инстанс с
    обновленными полями без сохранения в БД
    """
    model = instance.__class__
    m2m_fields = {}
    kwargs_copy = copy.deepcopy(kwargs)
    for field in model._meta.local_many_to_many:
        if field.name in kwargs_copy.keys():
            m2m_fields[field.name] = kwargs_copy.pop(field.name, [])
    for key, value in kwargs_copy.items():
        setattr(instance, key, value)
    if commit:
        instance.save()
    for key, value in m2m_fields.items():
        getattr(instance, key).clear()
        for val in value:
            getattr(instance, key).add(val)
    return instance


def object_create(model, full_check=True, **kwargs):
    m2m_fields = {}
    kwargs_copy = copy.deepcopy(kwargs)
    for field in model._meta.local_many_to_many:
        if field.name in kwargs_copy.keys():
            m2m_fields[field.name] = kwargs_copy.pop(field.name, [])

    obj = model(**kwargs_copy)

    if full_check:
        obj.full_clean()

    obj.save()
    obj.refresh_from_db()

    for key, value in m2m_fields.items():
        for val in value:
            getattr(obj, key).add(val)

    return obj


def object_filter(qs: QuerySet, *args, **kwargs):
    return qs.filter(*args, **kwargs)


def object_delete(qs: QuerySet, *args, **kwargs):
    """Safe delete. CreatedUpdatedMixin required"""
    return object_update(qs.filter(*args, **kwargs), deleted=timezone.now())


def object_update(qs: QuerySet, **kwargs):
    updated_objs = list()
    for obj in qs.all():
        if hasattr(obj, "updated"):
            kwargs["updated"] = timezone.now()
        new_obj = item_update(obj, commit=False, **kwargs)
        updated_objs.append(new_obj)
    qs.model.objects.bulk_update(updated_objs, fields=kwargs.keys(), batch_size=100)
    return qs


def object_exist(objects: QuerySet, *args, **kwargs):
    return object_filter(objects, *args, **kwargs).exists()
