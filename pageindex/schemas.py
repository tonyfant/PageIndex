from pydantic import BaseModel, Field, RootModel
from typing import Literal, List, Optional

class TOCDetectionResult(BaseModel):
    thinking: str = Field(description="Explain why you think there is or isn't a table of contents in the text.")
    toc_detected: Literal["yes", "no"] = Field(description="Answer strictly 'yes' or 'no'.")

class TOCExtractionCompleteResult(BaseModel):
    thinking: str = Field(description="Explain why you think the table of contents is complete or not.")
    completed: Literal["yes", "no"] = Field(description="Answer strictly 'yes' if it contains all main sections, or 'no' if it does not.")

class TOCTransformationCompleteResult(BaseModel):
    thinking: str = Field(description="Explain why you think the cleaned table of contents is complete or not compared to the raw one.")
    completed: Literal["yes", "no"] = Field(description="Answer strictly 'yes' if the cleaned table of contents is complete, or 'no' otherwise.")

class TOCPageIndexDetectionResult(BaseModel):
    thinking: str = Field(description="Explain why you think there are or aren't page numbers/indices given within the table of contents.")
    page_index_given_in_toc: Literal["yes", "no"] = Field(description="Answer strictly 'yes' if page numbers/indices are present, or 'no' if they are not.")

class TOCIndexEntry(BaseModel):
    structure: Optional[str] = Field(description="The numeric system representing the hierarchy index, e.g., '1', '1.1', or null if not applicable.")
    title: str = Field(description="The title of the section.")
    physical_index: Optional[str] = Field(description="The physical location tag of the page, e.g., '<physical_index_X>', or null if the section is not in the provided pages.")

class TOCIndexList(RootModel):
    root: List[TOCIndexEntry]

class TOCPageNumberEntry(BaseModel):
    structure: Optional[str] = Field(description="The numeric system representing the hierarchy index, e.g., '1', '1.1', or null.")
    title: str = Field(description="The title of the section.")
    start: Literal["yes", "no"] = Field(description="Answer strictly 'yes' if the target section starts in the partial document, or 'no' if it does not.")
    physical_index: Optional[str] = Field(description="The physical location tag of the page, e.g., '<physical_index_X>', or null if it does not start here.")

class TOCPageNumberList(RootModel):
    root: List[TOCPageNumberEntry]


class TOCNode(BaseModel):
    structure: Optional[str] = Field(description="The numeric system representing the hierarchy index, e.g., '1', '1.1'.")
    title: str = Field(description="The original title extracted from the text, fixing only space inconsistencies.")
    physical_index: str = Field(description="The physical location tag where the section starts, keeping the exact '<physical_index_X>' format.")

class TOCNodeList(RootModel):
    root: List[TOCNode]