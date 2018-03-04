from django.http.response import HttpResponseRedirect
from .models import UserRole, Post
from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib import messages


def get_user_role(user):
    user_role = UserRole.objects.filter(user=user)
    if user_role:
        return user_role[0].role
    return 'No User Role'


class AdminOnlyMixin(object):

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not (user.is_authenticated and user.is_active):
            return HttpResponseRedirect('/dashboard/')
        user_role = UserRole.objects.filter(user=request.user).last()
        if user_role:
            user_role = True if user_role.role == "Admin" else False
        else:
            user_role = False
        if not (user.is_superuser or user_role):
            messages.warning(request, "You don't have permission")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', "/"))
        return super(AdminOnlyMixin, self).dispatch(request, *args, **kwargs)


class AuthorNotAllowedMixin(object):

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not (user.is_authenticated and user.is_active):
            return HttpResponseRedirect('/dashboard/')
        user_role = UserRole.objects.filter(user=request.user).last()
        if user_role:
            user_role = user_role.role in ["Admin", "Publisher"]
        if not (user.is_superuser or user_role):
            messages.warning(request, "You don't have permission")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', "/"))
        return super(AuthorNotAllowedMixin, self).dispatch(request, *args, **kwargs)


class AdminMixin(object):

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        if not (user.is_authenticated and user.is_active):
            return HttpResponseRedirect('/dashboard/')
        # if not user.is_superuser:
        #     return HttpResponseRedirect("/")
        return super(AdminMixin, self).dispatch(request,
                                                *args,
                                                **kwargs)


class PostAccessRequiredMixin(object):

    def dispatch(self, request, *args, **kwargs):
        self.object = get_object_or_404(Post, slug=kwargs.get('blog_slug'))

        # Checking the permissions
        if not(
            self.object.is_deletable_by(request.user) or
            request.user.is_superuser is True or
            get_user_role(request.user) != 'Author'
        ):
            # TODO: Add "PermissionDenied" message
            messages.warning(request, "You don't have permission")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        return super(PostAccessRequiredMixin, self).dispatch(
            request, *args, **kwargs)
