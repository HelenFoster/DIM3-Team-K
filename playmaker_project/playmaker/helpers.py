def get_context_dictionary(request):
    if request.user.is_authenticated():
        context_dict = { 'username': request.user, }
    else:
        context_dict = { 'username': None, }

    return context_dict