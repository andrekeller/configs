"""
confi.gs common model mixins
"""


class ValidateModelMixin:
    """
    Mixin to force validation upon save.

    The mixin ensures, that the models full_clean() method is called prior to
    save.
    """

    def save(self, *args, **kwargs):
        """
        unconditionally call models full_clean() method prior to save().
        """
        self.full_clean()
        super(ValidateModelMixin, self).save(*args, **kwargs)
