import pysvg


def test_pysvg_version():
    """Test to verify pysvg can be imported and has a version number."""
    assert hasattr(pysvg, "__version__"), "pysvg should have a __version__ attribute"
    print(f"\npysvg version: {pysvg.__version__}")
