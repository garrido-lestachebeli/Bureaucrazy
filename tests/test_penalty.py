from app.services.penalty import day_should_continue


def test_a_day_continues_when_mistakes_are_within_the_limit():
    assert day_should_continue(0, 1) is True
    assert day_should_continue(1, 1) is True
    assert day_should_continue(2, 1) is False
