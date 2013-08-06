from django.core.files.storage import default_storage

from pyrpm import yum, rpm
from pyrpm.tools.createrepo import YumRepository


class CloudYumRepository(YumRepository):

    def _retr_file(self, filename):
        raise NotImplementedError()

    def _store_file(self, file, filename):
        # fixup for django filesystem storage
        def chunks():
            file.seek(0)
            yield file.read()
        file.chunks = chunks

        # real file store
        if default_storage.exists("%s/%s" % (self.repodir, filename)):
            default_storage.delete("%s/%s" % (self.repodir, filename))
        default_storage.save("%s/%s" % (self.repodir, filename), file)


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
        self.filesize = rpm_package.filesize

        # load header entries from db
        for header_entry in rpm_package.headers.all():
            self.header.entries.append(rpm.Entry(tag=header_entry.tag, value=header_entry.value))

        self._match_composite()
