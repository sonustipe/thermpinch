"""
beat.config.schemas.input
 
This module contains the Pydantic schemas for the page input data.
"""

from typing import List, Dict, Optional, Final
from pydantic import BaseModel, Field, field_validator, model_validator
import uuid
from pydantic import BaseModel, Field, field_validator, model_validator
from thermpinch.schemas.meta import MetaInput
from thermpinch.schemas.page1 import Page1Input
from thermpinch.schemas.page2 import Page2Input


class ProjectData(BaseModel):
    meta_input: MetaInput
    page1_input: Page1Input
    page2_input: Page2Input
