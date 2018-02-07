from django.db.models.signals import post_save, post_delete
from django.db.models import Q
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model


from user_operation.models import UserConcernlove


@receiver(post_save, sender=UserConcernlove)
def create_userconcernlove(sender, instance=None, created=False, **kwargs):
    if created:
        concerndpersonal = instance.concertuser_id
        personalconcern  = instance.userConcern_id
        result = ''
        try:
            result = UserConcernlove.objects.get(Q(userConcern_id = concerndpersonal) &
                                                 Q(concertuser_id = personalconcern))
        except Exception as e:
            print(e)
        if result:
            result.matchsucess  = '0'
            result.save()
            instance.matchsucess = '0'
            instance.save()


@receiver(post_delete, sender=UserConcernlove)
def delete_userconcernlove(sender, instance=None, created=False, **kwargs):
    concerndpersonal = instance.concertuser_id
    personalconcern = instance.userConcern_id
    result = ''
    try:
        result = UserConcernlove.objects.get(Q(userConcern_id=concerndpersonal) &
                                             Q(concertuser_id=personalconcern))
    except Exception as e:
        print(e)
    if result:
        result.matchsucess = '1'
        result.save()
        instance.matchsucess = '1'
        instance.save()