class AutosaveMixin(object):
    """
    Mixin that will save object when an attribute is updated.
    """

    def __setattr__(self, key, value):
        super(AutosaveMixin, self).__setattr__(key, value)
        self.save()
