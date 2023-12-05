import re
import logging
from django.db.utils import InterfaceError
from django.db.backends.postgresql.base import DatabaseWrapper as PGWrapper


logger = logging.getLogger(__name__)


class DatabaseWrapper(PGWrapper):

    def _cursor(self, **kwargs):
        try:
            return super(DatabaseWrapper, self)._cursor(**kwargs)
        except InterfaceError as e:  # Try to reconnect to DB
            logger.exception(e)
            if self.connection is not None:
                if not self.is_usable():
                    self.connection.close()
                    self.connection = None
            return super(DatabaseWrapper, self)._cursor(**kwargs)
