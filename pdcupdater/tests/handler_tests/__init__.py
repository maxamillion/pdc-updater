from os.path import dirname
import functools
import unittest
import logging

import vcr

import fedmsg.utils

from nose.tools import raises

import pdcupdater.utils

import pdc_client.test_helpers

log = logging.getLogger(__name__)


cassette_dir = dirname(dirname(__file__)) + '/vcr-request-data/'

def mock_404():
    import beanbag.bbexcept
    class Mock404Response(object):
        status_code = 404
    response = Mock404Response()
    raise beanbag.bbexcept.BeanBagException(response, "404, nope.")

def mock_pdc(function):
    @functools.wraps(function)
    @pdc_client.test_helpers.mock_api
    def wrapper(self, pdc, *args, **kwargs):
        # Mock out POST endpoints
        pdc.add_endpoint('component-group-types', 'POST', 'wat')
        pdc.add_endpoint('component-groups', 'POST', 'wat')
        pdc.add_endpoint('global-components', 'POST', 'wat')
        pdc.add_endpoint('release-components', 'POST', 'wat')
        pdc.add_endpoint('compose-images', 'POST', 'wat')
        pdc.add_endpoint('compose-rpms', 'POST', 'wat')
        pdc.add_endpoint('persons', 'POST', 'wat')
        pdc.add_endpoint('rpms', 'POST', 'wat')

        # Mock out GET endpoints
        pdc.add_endpoint('composes/Fedora-24-20151130.n.2', 'GET', mock_404)

        pdc.add_endpoint('releases/fedora-24', 'GET', {})
        pdc.add_endpoint('releases/fedora-23-updates', 'GET', {})
        pdc.add_endpoint('releases/fedora-22-updates', 'GET', {})
        pdc.add_endpoint('releases/fedora-21-updates', 'GET', {})
        pdc.add_endpoint('releases/fedora-20-updates', 'GET', {})
        pdc.add_endpoint('releases/epel-7-updates', 'GET', {})
        pdc.add_endpoint('releases/epel-6-updates', 'GET', {})


        pdc.add_endpoint('component-groups', 'GET', {
            'count': 4,
            'next': None,
            'previous': None,
            'results': [{
                'release': 'fedora-24',
                'description': 'Deps for atomic-docker-host https://git.fedorahosted.org/cgit/fedora-atomic.git/plain/',
                'group_type': 'atomic-docker-host',
                'id': 1,
            }, {
                'release': 'fedora-23-updates',
                'description': 'Deps for atomic-docker-host https://git.fedorahosted.org/cgit/fedora-atomic.git/plain/',
                'group_type': 'atomic-docker-host',
                'id': 2,
            }, {
                'release': 'fedora-22-updates',
                'description': 'Deps for atomic-docker-host https://git.fedorahosted.org/cgit/fedora-atomic.git/plain/',
                'group_type': 'atomic-docker-host',
                'id': 3,
            }, {
                'release': 'fedora-21-updates',
                'description': 'Deps for atomic-docker-host https://git.fedorahosted.org/cgit/fedora-atomic.git/plain/',
                'group_type': 'atomic-docker-host',
                'id': 3,
            }],
        })

        pdc.add_endpoint('persons', 'GET', {
            'count': 2,
            'next': None,
            'previous': None,
            'results': [
                {'username': 'ralph', 'email': 'ralph@fedoraproject.org'},
                {'username': 'lmacken', 'email': 'lmacken@fedoraproject.org'},
            ],
        })

        pdc.add_endpoint('rpms', 'GET', {
            'count': 2,
            'next': None,
            'previous': None,
            'results': [{
                'name': 'dvisvgm',
                'arch': 'src',
                'epoch': 0,
                'version': '1.11',
                'release': '1.el7',
                'linked_releases': [
                    'epel-7-updates',
                ],
                'srpm_name': 'dvisvgm',
                'srpm_nevra': None,
            }, {
                'name': 'rubygem-jmespath-doc',
                'arch': 'noarch',
                'epoch': 0,
                'version': '1.1.3',
                'release': '1.el7',
                'linked_releases': [
                    'epel-7-updates',
                ],
                'srpm_name': 'rubygem-jmespath',
                'srpm_nevra': 'rubygem-jmespath-1.1.3-1.el7',
            }],
        })

        pdc.add_endpoint('release-components', 'GET', {
            'count': 11,
            'next': None,
            'previous': None,
            'results': [
              {'active': True,
               'brew_package': u'guake',
               'bugzilla_component': u'guake',
               'dist_git_branch': u'master',
               'global_component': u'guake',
               'name': u'guake',
               'release': {
                    'release_id': u'fedora-24',
               },
               'type': 'srpm'},
              {'active': True,
               'brew_package': u'guake',
               'bugzilla_component': u'guake',
               'dist_git_branch': u'el6',
               'global_component': u'guake',
               'name': u'guake',
               'release': {
                    'release_id': u'epel-6-updates',
               },
               'type': 'srpm'},
              {'active': True,
               'brew_package': u'guake',
               'bugzilla_component': u'guake',
               'dist_git_branch': u'f20',
               'global_component': u'guake',
               'name': u'guake',
               'release': {
                    'release_id': u'fedora-20-updates',
               },
               'type': 'srpm'},
              {'active': True,
               'brew_package': u'guake',
               'bugzilla_component': u'guake',
               'dist_git_branch': u'epel7',
               'global_component': u'guake',
               'name': u'guake',
               'release': {
                    'release_id': u'epel-7-updates',
               },
               'type': 'srpm'},
              {'active': True,
               'brew_package': u'guake',
               'bugzilla_component': u'guake',
               'dist_git_branch': u'f21',
               'global_component': u'guake',
               'name': u'guake',
               'release': {
                    'release_id': u'fedora-21-updates',
               },
               'type': 'srpm'},
              {'active': True,
               'brew_package': u'guake',
               'bugzilla_component': u'guake',
               'dist_git_branch': u'f22',
               'global_component': u'guake',
               'name': u'guake',
               'release': {
                    'release_id': u'fedora-22-updates',
               },
               'type': 'srpm'},
              {'active': True,
               'brew_package': u'guake',
               'bugzilla_component': u'guake',
               'dist_git_branch': u'f23',
               'global_component': u'guake',
               'name': u'guake',
               'release': {
                    'release_id': u'fedora-23-updates',
               },
               'type': 'srpm'},
              {'active': True,
               'brew_package': u'geany',
               'bugzilla_component': u'geany',
               'dist_git_branch': u'master',
               'global_component': u'geany',
               'name': u'geany',
               'release': {
                    'release_id': u'fedora-24',
               },
               'type': 'srpm'},
              {'active': True,
               'brew_package': u'geany',
               'bugzilla_component': u'geany',
               'dist_git_branch': u'el6',
               'global_component': u'geany',
               'name': u'geany',
               'release': {
                    'release_id': u'epel-6-updates',
               },
               'type': 'srpm'},
              {'active': True,
               'brew_package': u'geany',
               'bugzilla_component': u'geany',
               'dist_git_branch': u'epel7',
               'global_component': u'geany',
               'name': u'geany',
               'release': {
                    'release_id': u'epel-7-updates',
               },
               'type': 'srpm'},
              {'active': True,
               'brew_package': u'geany',
               'bugzilla_component': u'geany',
               'dist_git_branch': u'f23',
               'global_component': u'geany',
               'name': u'geany',
               'release': {
                    'release_id': u'fedora-23-updates',
               },
               'type': 'srpm'},
            ]
        })

        pdc.add_endpoint('global-components', 'GET', {
            'count': 11,
            'next': None,
            'previous': None,
            'results': [
              {'name': u'geany'},
              {'name': u'guake'},
            ]
        })

        pdc.add_endpoint('composes', 'GET', {
            'count': 2,
            'next': None,
            'previous': None,
            'results': [{
                "acceptance_testing": "ComposeAcceptanceTestingState.name",
                "compose_date": "20151130",
                "compose_id": "Fedora-24-20151130.n.2",
                "compose_label": "Fedora-24-20151130.n.2",
                "compose_respin": "2",
                "compose_type": "nightly",
                "deleted": "boolean",
                "linked_releases": [],
                "release": "rawhide",
                "rpm_mapping_template": "some url",
                "rtt_tested_architectures": { },
                "sigkeys": [],
            }],
        })

        return function(self, pdc, *args, **kwargs)
    return wrapper


class BaseHandlerTest(unittest.TestCase):
    maxDiff = None
    handler_path = None
    config = {
        'pdcupdater.fas': {
            'base_url': 'whatever',
            'username': 'whatever',
            'password': 'whatever',
        },
        'pdcupdater.pkgdb_url': 'blihblihblih',
        'pdcupdater.koji_url': 'http://koji.fedoraproject.org/kojihub',
        'pdcupdater.old_composes_url': 'https://kojipkgs.fedoraproject.org/compose',
        'pdcupdater.fedora_atomic_git_url': 'https://git.fedorahosted.org/cgit/fedora-atomic.git/plain/',
    }

    def setUp(self):
        if not self.handler_path:
            log.info("!! Warning - no handler path declared by base class.")

        config = BaseHandlerTest.config
        if self.handler_path:
            log.info("Initializing handler %s(%r)", self.handler_path, config)
            self.handler = fedmsg.utils.load_class(self.handler_path)(config)

        log.info("Setting up vcr cassette in %s", cassette_dir)
        filename = cassette_dir + self.id()
        self.vcr = vcr.use_cassette(filename, record_mode='new_episodes')
        self.vcr.__enter__()

    def tearDown(self):
        self.vcr.__exit__()


class TestBaseHarness(BaseHandlerTest):
    @raises(IOError)
    def test_get_nonexistant_fedmsg(self):
        pdcupdater.utils.get_fedmsg('wat')

    def test_get_fedmsg(self):
        idx = '2015-6c98c8e3-0dcb-497d-a0d8-0b3d026a4cfb'
        msg = pdcupdater.utils.get_fedmsg(idx)
        self.assertEquals(msg['msg']['user']['username'], 'ralph')
