import re
import pytest
import pdb

pytestmark = pytest.mark.usefixtures("master", "minion")

@pytest.fixture(scope='module')
def module_config(request):
    return {
        'masters': [
            {
                'config': {
                    'container__config__salt_config__sls': {
                        'rsync': 'tests/sls/rsync.sls',
                        'archextract': 'tests/sls/archextract.sls',
                    }
                },
                'minions': [{'config': {}}, {'config': {}}]
            }
        ]
    }


@pytest.fixture()
def master(setup):
    config, initconfig = setup
    return config['masters'][0]['fixture']


@pytest.fixture()
def minion(setup):
    config, initconfig = setup
    master = config['masters'][0]
    return master['minions'][0]['fixture']


@pytest.mark.tags('sles')
def test_zypp_gpg_pkg(master, minion):
    '''
    Fake packages gpg-pubkey* should be filtered out by zypper.
    '''
    resp = master.salt(minion['id'], "pkg.info_installed")[minion['id']]
    assert not bool([pk for pk in resp.keys() if 'gpg-pubkey' in pk])


def test_rsync_port(master, minion):
    '''
    Test rsync port from 2016.3.
    '''
    resp = master.salt(minion['id'], "state.apply rsync")[minion['id']]
    assert resp['pkg_|-rsyncpackage_|-rsync_|-installed']['result']
    assert resp['rsync_|-/tmp_|-/tmp_|-synchronized']['result']


def test_archive_extracted(master, minion):
    '''
    Test if the archive.extracted overwrites the destination.
    '''
    resp = master.salt(minion['id'], "state.apply archextract")[minion['id']]
    assert resp['archive_|-extract-zip-archive_|-/tmp/_|-extracted']['result']