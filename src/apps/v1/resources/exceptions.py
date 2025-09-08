from enum import Enum

from fastapi import HTTPException


class SkillHttpExceptionTypeEnum(Enum):
    SKILL_NOT_FOUND = "404"


EXCEPTIONS_HTTP_DICT = {
    SkillHttpExceptionTypeEnum.SKILL_NOT_FOUND: HTTPException(404, "Skill not found"),
}


def skill_exception_fabric(exc_type: SkillHttpExceptionTypeEnum) -> HTTPException:
    return EXCEPTIONS_HTTP_DICT[exc_type]
