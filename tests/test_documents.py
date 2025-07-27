import pytest
import yaml, pathlib

criteria = yaml.safe_load(
    pathlib.Path("docs/acceptance_criteria.yaml").read_text()
)["documents"]

@pytest.mark.parametrize("case", criteria)
def test_documents_requirements(case):
    pytest.skip(f"{case['id']} not implemented yet")
