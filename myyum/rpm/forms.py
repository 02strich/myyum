from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.storage import default_storage

from rpm.models import *

class RepositoryForm(forms.ModelForm):
    class Meta:
        model = Repository
        exclude = ('owner','metadata_url',)

    def validate_unique(self):
        exclude = self._get_validation_exclusions()
        exclude.remove('owner') # allow checking against the missing attribute

        try:
            self.instance.validate_unique(exclude=exclude)
        except forms.ValidationError, e:
            self._update_errors(e.message_dict)


class PackageUploadForm(forms.Form):
    package = forms.FileField()

    def __init__(self, repository, *args, **kwargs):
        super(PackageUploadForm, self).__init__(*args, **kwargs)
        self.repository = repository

    def clean(self):
        # TODO: test if filename is available
        return self.cleaned_data

    def save(self):
        # get file
        package_file = self.cleaned_data.get('package')

        return RPMPackage.create_from_rpm_file(self.repository, package_file)
