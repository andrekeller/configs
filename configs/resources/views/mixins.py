from django.core.exceptions import ObjectDoesNotExist, ImproperlyConfigured
from django.views.generic.detail import SingleObjectMixin


class ParentModifyMixin(SingleObjectMixin):
    parent_model = None
    parent_ref = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.parent_model is None:
            raise ImproperlyConfigured(
                'Need to set parent_model for ParentMixin'
            )
        if self.parent_ref is None:
            self.parent_ref = self.model.__name__.lower()

        try:
            context['parent'] = self.parent_model.objects.filter(
              **{self.parent_ref: context['view'].kwargs['pk']}
            ).first()
        except (KeyError, ObjectDoesNotExist) as exc:
            pass
        else:
            return context

        try:
            context['parent'] = self.parent_model.objects.get(
                pk=context['view'].kwargs['parent']
            )
            context['create'] = True
        except (KeyError, ObjectDoesNotExist):
            pass

        return context


class ParentCreateMixin:

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update(self.kwargs)
        return kwargs
