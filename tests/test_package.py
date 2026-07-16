def test_package_exposes_version() -> None:
    import investkb

    assert investkb.__version__ == "0.1.0"
