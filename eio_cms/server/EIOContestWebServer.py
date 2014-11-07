# -*- coding: utf-8 -*-
"""
EIO-CMS - adaptations of CMS for EIO.

Author: Konstantin Tretyakov
License: MIT
"""

"""
We need to modify the templates used in cms.server.ContestWebServer,
hence we subclass it and change the constructor to use our template directory.
"""

from cms.server.ContestWebServer import *
from cms.server.ContestWebServer import _cws_handlers

class EIOContestWebServer(ContestWebServer):
    def __init__(self, shard, contest):
	"""This is a direct copy of ContestWebServer.__init__ with the only change in "template_path" and "static_path" values below."""
        parameters = {
            "login_url": "/",
            "template_path": pkg_resources.resource_filename(
                "eio_cms.server", "templates/contest"),
            "static_path": pkg_resources.resource_filename(
                "eio_cms.server", "static"),
            "cookie_secret": base64.b64encode(config.secret_key),
            "debug": config.tornado_debug,
            "is_proxy_used": config.is_proxy_used,
        }

        try:
            listen_address = config.contest_listen_address[shard]
            listen_port = config.contest_listen_port[shard]
        except IndexError:
            raise ConfigError("Wrong shard number for %s, or missing "
                              "address/port configuration. Please check "
                              "contest_listen_address and contest_listen_port "
                              "in cms.conf." % __name__)

        super(ContestWebServer, self).__init__(
            listen_port,
            _cws_handlers,
            parameters,
            shard=shard,
            listen_address=listen_address)

        self.contest = contest

        # This is a dictionary (indexed by username) of pending
        # notification. Things like "Yay, your submission went
        # through.", not things like "Your question has been replied",
        # that are handled by the db. Each username points to a list
        # of tuples (timestamp, subject, text).
        self.notifications = {}

        # Retrieve the available translations.
        self.localization_dir = pkg_resources.resource_filename('cms.server', 'mo')
        self.langs = ["en-US"] + [
            path.split("/")[-3].replace("_", "-") for path in glob.glob(
                os.path.join(self.localization_dir,
                             "*", "LC_MESSAGES", "cms.mo"))]

        self.file_cacher = FileCacher(self)
        self.evaluation_service = self.connect_to(
            ServiceCoord("EvaluationService", 0))
        self.scoring_service = self.connect_to(
            ServiceCoord("ScoringService", 0))

        ranking_enabled = len(config.rankings) > 0
        self.proxy_service = self.connect_to(
            ServiceCoord("ProxyService", 0),
            must_be_present=ranking_enabled)

        printing_enabled = config.printer is not None
        self.printing_service = self.connect_to(
            ServiceCoord("PrintingService", 0),
            must_be_present=printing_enabled)

