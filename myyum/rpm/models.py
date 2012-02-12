from django.db import models, IntegrityError
from django.core.files.storage import default_storage
from django.contrib.auth.models import User

from myyum.rpm.fields import *
from myyum.rpm.tools import *

class Repository(models.Model):
    owner = models.ForeignKey(User)
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    metadata_url = models.URLField()
    
    class Meta:
        unique_together = (
            ("owner", "name"),
        )
    
    
    @property
    def repodir(self):
        return "%s/%s" % (self.owner.username, self.name)
    
    def update_metadata(self):
        yum_repo = CloudYumRepository(self.repodir)
        
        for pkg in self.packages.all():
            yum_repo.add_package(pkg.get_yum_package)
        
        yum_repo.save()

class RPMPackage(models.Model):
    repository = models.ForeignKey(Repository, related_name="packages")
    
    # general information
    pkgid = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    filesize = models.IntegerField()
    
    # storage information
    filename = models.CharField(max_length=255)
    url = models.URLField()
    
    @property
    def get_yum_package(self):
        return YumPackageAdapter(self)
    
    @property
    def summary(self):
        try:
            return self.headers.filter(tag=1004).get().value
        except:
            return ""
    
    @property
    def version_string(self):
        try:
            return "%s-%s" % (self.headers.filter(tag=1001).get().value, self.headers.filter(tag=1002).get().value)
        except:
            return ""
    
    @classmethod
    def create_from_rpm_file(cls, repository, package_file):
        # parse it
        rpm_pkg = rpm.RPM(package_file)
        
        # ckech for duplicates
        if repository.packages.filter(pkgid=rpm_pkg.checksum).exists():
            raise IntegrityError()
        
        # create in db
        pkg = cls.objects.create(repository=repository, pkgid=rpm_pkg.checksum, name=rpm_pkg.header.name, filesize=rpm_pkg.filesize)
        for header_entry in rpm_pkg.header:
            RPMHeader.objects.create(package=pkg, tag=header_entry.tag, value=header_entry.value)
        
        # upload it
        pkg.url = default_storage.save("%s/%s" % (repository.repodir, rpm_pkg.canonical_filename), package_file)
        pkg.save()
        
        # update repo
        repository.update_metadata()
        
        # return the new package
        return pkg
    
    def delete(self, *args, **kwargs):
        # check for file and delete it if existing
        if self.url and default_storage.exists(self.url):
            default_storage.delete(self.url)
        
        # call super
        super(RPMPackage, self).delete(*args, **kwargs)
        
        # update repo
        self.repository.update_metadata()
    
class RPMHeader(models.Model):
    package = models.ForeignKey(RPMPackage, related_name='headers')
    
    tag = models.IntegerField()
    value = PickledObjectField()
