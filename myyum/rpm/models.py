from django.db import models
from django.core.files.storage import default_storage
from django.contrib.auth.models import User

from pyrpm import yum, rpm

from myyum.rpm.fields import *

class Repository(models.Model):
    owner = models.ForeignKey(User)
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    
    metadata_url = models.URLField()
    
    class Meta:
        unique_together = (
            ("owner", "name"),
        )


class RPMPackage(models.Model):
    repository = models.ForeignKey(Repository, related_name="packages")
    
    # general information
    pkgid = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    #summary = models.TextField(max_length=255)
    #description = models.TextField()
    #architecture = models.CharField(max_length=20)
    
    # version information
    #version = models.CharField(max_length=20)
    #release = models.CharField(max_length=20)
    #epoch = models.IntegerField(max_length=20)
    
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
    
    def delete(self, *args, **kwargs):
        # check for file and delete it if existing
        if default_storage.exists(self.url):
            default_storage.delete(self.url)
        super(RPMPackage, self).delete(*args, **kwargs)
    
class RPMHeader(models.Model):
    package = models.ForeignKey(RPMPackage, related_name='headers')
    
    tag = models.IntegerField()
    value = PickledObjectField()

class YumPackageAdapter(yum.YumPackage):
    """ Adapter for using the RPM header entries from
    the database instead from a file"""
    
    def __init__(self, rpm_package):
        self.binary = True
        self.source = False
        self.header = rpm.Header(None)
        self.signature = rpm.Signature(None)
        self.filelist = []
        self.changelog = []
        
        self.provides = []
        self.requires = []
        self.obsoletes = []
        self.conflicts = []
        
        self.checksum = rpm_package.pkgid
        
        # load header entries from db
        for header_entry in rpm_package.headers.all():
            self.header.entries.append(rpm.Entry(tag=header_entry.tag, value=header_entry.value))
        
        self._match_composite()