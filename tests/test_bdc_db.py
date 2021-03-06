#
# This file is part of BDC-DB.
# Copyright (C) 2020 INPE.
#
# BDC-DB is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Unit-test for BrazilDataCubeExtension."""

from click.testing import CliRunner
from flask.cli import ScriptInfo
from sqlalchemy_utils.functions import database_exists

import bdc_db.cli as bdc_cli
from bdc_db import BrazilDataCubeDB
from bdc_db.config import SQLALCHEMY_DATABASE_URI


def test_cli(app, db):
    """Test database creation."""
    BrazilDataCubeDB(app=app, db=db)

    sinfo = ScriptInfo(create_app=lambda _: app)

    runner = CliRunner()

    result = runner.invoke(bdc_cli.init, [], obj=sinfo)
    assert result.exit_code == 0
    assert database_exists(SQLALCHEMY_DATABASE_URI)

    result = runner.invoke(bdc_cli.create_extension_postgis, [], obj=sinfo)
    assert result.exit_code == 0
    with app.app_context():
        assert db.engine.has_table('spatial_ref_sys', schema='public')

    result = runner.invoke(bdc_cli.destroy, ['--force'], obj=sinfo)
    assert result.exit_code == 0
    assert not database_exists(SQLALCHEMY_DATABASE_URI)


if __name__ == '__main__':
    import pytest
    pytest.main(['--color=auto', '--no-cov'])