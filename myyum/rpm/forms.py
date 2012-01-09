from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.db import IntegrityError

from myyum.rpm.models import *
from pyrpm.rpm import RPM

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
        
        # parse it
        rpm = RPM(package_file)
        
        # ckech for duplicates
        if self.repository.packages.filter(pkgid=rpm.checksum).exists():
            raise IntegrityError()
        
        # create in db
        pkg = RPMPackage.objects.create(repository=self.repository, pkgid=rpm.checksum, name=rpm.header.name)
        for header_entry in rpm.header:
            RPMHeader.objects.create(package=pkg, tag=header_entry.tag, value=header_entry.value)
        
        # upload it
        pkg.url = default_storage.save("%s/%s/%s" % (self.repository.owner.username, self.repository.name, rpm.canonical_filename), package_file)
        pkg.save()
        
        # success
        return pkg