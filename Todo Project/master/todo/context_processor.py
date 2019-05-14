from .models import List


def nav_list(request):
    user = request.user
    if not user.is_anonymous:
        lists = user.list_set.all()
    else:
        lists = List.objects.all()
    # else:

    return {
        'lists': lists
    }
