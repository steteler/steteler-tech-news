from tech_news.analyzer.reading_plan import ReadingPlanService
from unittest.mock import MagicMock
import pytest
from tests.assets.news import NEWS


@pytest.fixture
def news():
    return NEWS


def test_reading_plan_group_news(news):
    ReadingPlanService._db_news_proxy = MagicMock(return_value=news)

    message = "Valor 'available_time' deve ser maior que zero"
    with pytest.raises(ValueError, match=message):
        ReadingPlanService.group_news_for_available_time(available_time=0)

    result = ReadingPlanService.group_news_for_available_time(14)
    readable = result["readable"]

    assert len(readable) == 3
    assert readable[0]["unfilled_time"] == 5
    assert len(readable[0]["chosen_news"]) == 1
    assert readable[1]["unfilled_time"] == 9
    assert len(readable[1]["chosen_news"]) == 1
    assert len(result["unreadable"]) == 1
