import pytest
from NMM.base.Property.Implement.Path import Path


def testPath():
    path = Path('example', 'testPath')
    assert path.name == 'example'
    assert path.type == 'Path'
    assert path.value == 'testPath'

