@given(u'I have enabled volumes for new services')
def step_impl(context):
    context.volume_enabled = True