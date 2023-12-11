import datetime
from typing import Annotated

from sqlalchemy import func, DateTime
from sqlalchemy.orm import mapped_column

time_created = Annotated[datetime.datetime, mapped_column(DateTime(timezone=True), server_default=func.now())]
