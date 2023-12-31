from enum import StrEnum


PASSWORD_MASK = "X" * 10


class TimeGrain(StrEnum):
    SECOND = "PT1S"
    FIVE_SECONDS = "PT5S"
    THIRTY_SECONDS = "PT30S"
    MINUTE = "PT1M"
    FIVE_MINUTES = "PT5M"
    TEN_MINUTES = "PT10M"
    FIFTEEN_MINUTES = "PT15M"
    THIRTY_MINUTES = "PT30M"
    HALF_HOUR = "PT0.5H"
    HOUR = "PT1H"
    SIX_HOURS = "PT6H"
    DAY = "P1D"
    WEEK = "P1W"
    WEEK_STARTING_SUNDAY = "1969-12-28T00:00:00Z/P1W"
    WEEK_STARTING_MONDAY = "1969-12-29T00:00:00Z/P1W"
    WEEK_ENDING_SATURDAY = "P1W/1970-01-03T00:00:00Z"
    WEEK_ENDING_SUNDAY = "P1W/1970-01-04T00:00:00Z"
    MONTH = "P1M"
    QUARTER = "P3M"
    QUARTER_YEAR = "P0.25Y"
    YEAR = "P1Y"