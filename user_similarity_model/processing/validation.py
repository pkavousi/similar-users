# type: ignore
from typing import List

from pydantic import BaseModel, conint


class UserDataInputSchema(BaseModel):
    # User handle should be greater than 0 ans smaller than 10001
    # MyPY gets syntax error because of a bug. So "#type: ignore" is added
    # to the top of the file
    user_handle: conint(gt=0, lt=10001)


class MultipleUserDataInputs(BaseModel):
    inputs: List[UserDataInputSchema]
