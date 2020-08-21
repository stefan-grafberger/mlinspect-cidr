"""
Tests whether the fluent API works
"""
import os

import networkx
from testfixtures import compare

from mlinspect.instrumentation.analyzers.materialize_first_rows_analyzer import MaterializeFirstRowsAnalyzer
from mlinspect.utils import get_project_root
from mlinspect.pipeline_inspector import PipelineInspector
from mlinspect.visualisation import save_fig_to_path
from .utils import get_expected_dag_adult_easy_ipynb, get_expected_dag_adult_easy_py

ADULT_EASY_FILE_PY = os.path.join(str(get_project_root()), "test", "pipelines", "adult_easy.py")
HEALTHCARE_FILE_PY = os.path.join(str(get_project_root()), "test", "pipelines", "healthcare.py")
FILE_NB = os.path.join(str(get_project_root()), "test", "pipelines", "adult_easy.ipynb")


def test_inspector_adult_easy_py_pipeline():
    """
    Tests whether the .py version of the inspector works
    """
    inspection_result = PipelineInspector\
        .on_pipeline_from_py_file(ADULT_EASY_FILE_PY)\
        .add_analyzer(MaterializeFirstRowsAnalyzer(5))\
        .execute()
    extracted_dag = inspection_result.dag
    expected_dag = get_expected_dag_adult_easy_py()
    compare(networkx.to_dict_of_dicts(extracted_dag), networkx.to_dict_of_dicts(expected_dag))


def test_inspector_healthcare_py_pipeline():
    """
    Tests whether the .py version of the inspector works
    """
    inspection_result = PipelineInspector\
        .on_pipeline_from_py_file(HEALTHCARE_FILE_PY) \
        .add_analyzer(MaterializeFirstRowsAnalyzer(5)) \
        .execute()
    extracted_dag = inspection_result.dag

    filename = os.path.join(str(get_project_root()), "test", "pipelines", "healthcare.png")
    save_fig_to_path(extracted_dag, filename)

    assert os.path.isfile(filename)
    # expected_dag = get_expected_dag_adult_easy_py()
    # compare(networkx.to_dict_of_dicts(extracted_dag), networkx.to_dict_of_dicts(expected_dag))

    analyzer_results = inspection_result.analyzer_to_annotations
    result = analyzer_results[MaterializeFirstRowsAnalyzer(5)]
    assert len(result) == 4


def test_inspector_adult_easy_ipynb_pipeline():
    """
    Tests whether the .ipynb version of the inspector works
    """
    inspection_result = PipelineInspector\
        .on_pipeline_from_ipynb_file(FILE_NB)\
        .add_analyzer(MaterializeFirstRowsAnalyzer(5))\
        .execute()
    extracted_dag = inspection_result.dag
    expected_dag = get_expected_dag_adult_easy_ipynb()
    compare(networkx.to_dict_of_dicts(extracted_dag), networkx.to_dict_of_dicts(expected_dag))


def test_inspector_adult_easy_str_pipeline():
    """
    Tests whether the str version of the inspector works
    """
    with open(ADULT_EASY_FILE_PY) as file:
        code = file.read()

        inspection_result = PipelineInspector\
            .on_pipeline_from_string(code)\
            .add_analyzer(MaterializeFirstRowsAnalyzer(5))\
            .execute()
        extracted_dag = inspection_result.dag
        expected_dag = get_expected_dag_adult_easy_py()
        assert networkx.to_dict_of_dicts(extracted_dag) == networkx.to_dict_of_dicts(expected_dag)
