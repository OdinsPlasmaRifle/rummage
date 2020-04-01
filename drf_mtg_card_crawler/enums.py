from enumfields.enums import Enum


class SearchStatus(Enum):
    QUEUED = 'queued'
    PROCESSING = 'processing'
    FAILED = 'failed'
    COMPLETE = 'complete'
