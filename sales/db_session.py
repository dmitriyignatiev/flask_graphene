from contextlib import contextmanager

from sales.models import db_session

@contextmanager
def db_session_(autocommit=True):
    try:
        yield db_session
        if autocommit:
            db_session.commit()
    except Exception:
        db_session.rollback()
        raise
    finally:
        pass

