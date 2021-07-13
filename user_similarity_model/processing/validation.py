from typing import List, Optional

from pydantic import BaseModel


class UserDataInputSchema(BaseModel):
    user_handle: Optional[int]


class MultipleUserDataInputs(BaseModel):
    inputs: List[UserDataInputSchema]
