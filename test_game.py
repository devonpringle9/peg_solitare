import peg_solitare as sp
import pytest

def test_create_board():
    board = sp.Board().board
    assert board == [[1], [1, 1], [1, 1, 1], [1, 1, 1, 1], [1, 1, 0, 1, 1]]

@pytest.mark.parametrize('position,result', [
    (sp.Position(0, 0), True),
    (sp.Position(0, 1), False),
    (sp.Position(4, 4), True),
    (sp.Position(4, 5), False),
    (sp.Position(1, 0), True),
    (sp.Position(4, 0), True),
    (sp.Position(-1, 0), False),
    (sp.Position(0, -1), False),
    (sp.Position(5, 0), False),
    (sp.Position(0, 5), False),
])
def test_position_exists(position, result):
    print(position, result)
    assert sp.Position.position_exists(position) == result


@pytest.mark.parametrize('position,surr_positions', [
    (sp.Position(0, 0), [sp.Position(1,0), sp.Position(1,1)]),
    (sp.Position(3, 1), [sp.Position(3,0), sp.Position(4,1), sp.Position(4,2), sp.Position(3,2), sp.Position(2,1), sp.Position(2,0)]),
    (sp.Position(4, 4), [sp.Position(4,3), sp.Position(3,3)]),
])
def test_positions_around(position, surr_positions):
    res = position.positions_around()
    assert res == surr_positions
    assert True


def test_jump_positions():
    jump = sp.Position(1, 0).jump_position(sp.Position(2,1))
    assert jump == sp.Position(3, 2)