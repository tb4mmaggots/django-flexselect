import json

from django.http import HttpResponse
from django.forms.widgets import Select
from django.contrib.auth.decorators import login_required

from flexselect import (FlexSelectWidget, FlexSelectMultipleWidget, choices_from_instance, instance_from_request)


@login_required
def field_changed(request):
    """
    Ajax callback called when a trigger field or base field has changed. Returns
    html for new options and details for the dependent field as json.
    """
    widget = None
    hashed_name = request.POST.__getitem__('hashed_name')
    print("Hashed name:", hashed_name)
    if hashed_name in FlexSelectWidget.instances:
        widget = FlexSelectWidget.instances[hashed_name]
    elif hashed_name in FlexSelectMultipleWidget.instances:
        widget = FlexSelectMultipleWidget.instances[hashed_name]
    else:
        print("No widget for hashed_name:", hashed_name)

    instance = instance_from_request(request, widget)
    print("data", request.POST.data)

    if bool(int(request.POST.__getitem__('include_options'))):
        print("include_options", request.POST.__getitem__('include_options'))
        choices = choices_from_instance(instance, widget)
        options = Select(choices=choices).render_options([])
    else:
        print("POST does not contain attribute: 'include_options' ")
        options = None

    return HttpResponse(json.dumps({
        'options': options,
    }), content_type='application/json')
