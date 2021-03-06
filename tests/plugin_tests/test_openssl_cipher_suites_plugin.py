import unittest

import logging

from sslyze.plugins.openssl_cipher_suites_plugin import OpenSslCipherSuitesPlugin, Sslv20ScanCommand, Sslv30ScanCommand, \
    Tlsv10ScanCommand, Tlsv11ScanCommand, Tlsv12ScanCommand
from sslyze.server_connectivity import ServerConnectivityInfo
from tests.plugin_tests.openssl_server import NotOnLinux64Error
from tests.plugin_tests.openssl_server import VulnerableOpenSslServer


class OpenSslCipherSuitesPluginTestCase(unittest.TestCase):

    def test_sslv2_enabled(self):
        try:
            server = VulnerableOpenSslServer(port=8013)
        except NotOnLinux64Error:
            # The test suite only has the vulnerable OpenSSL version compiled for Linux 64 bits
            logging.warning('WARNING: Not on Linux - skipping test_sslv2_enabled() test')
            return
        server.start()
        server_info = ServerConnectivityInfo(hostname=server.hostname, ip_address=server.ip_address,  port=server.port)
        server_info.test_connectivity_to_server()

        plugin = OpenSslCipherSuitesPlugin()
        plugin_result = plugin.process_task(server_info, Sslv20ScanCommand())
        server.terminate()

        # The embedded server does not have a preference
        self.assertFalse(plugin_result.preferred_cipher)
        accepted_cipher_name_list = [cipher.name for cipher in plugin_result.accepted_cipher_list]
        self.assertEquals({'SSL_CK_RC4_128_EXPORT40_WITH_MD5', 'SSL_CK_IDEA_128_CBC_WITH_MD5',
                           'SSL_CK_RC2_128_CBC_EXPORT40_WITH_MD5', 'SSL_CK_DES_192_EDE3_CBC_WITH_MD5',
                           'SSL_CK_DES_192_EDE3_CBC_WITH_MD5', 'SSL_CK_RC4_128_WITH_MD5',
                           'SSL_CK_RC2_128_CBC_WITH_MD5', 'SSL_CK_DES_64_CBC_WITH_MD5'},
                          set(accepted_cipher_name_list))

        self.assertTrue(plugin_result.accepted_cipher_list)
        self.assertTrue(plugin_result.rejected_cipher_list)
        self.assertFalse(plugin_result.errored_cipher_list)

        self.assertTrue(plugin_result.as_text())
        self.assertTrue(plugin_result.as_xml())

    def test_sslv2_disabled(self):
        server_info = ServerConnectivityInfo(hostname=u'www.google.com')
        server_info.test_connectivity_to_server()

        plugin = OpenSslCipherSuitesPlugin()
        plugin_result = plugin.process_task(server_info, Sslv20ScanCommand())

        self.assertIsNone(plugin_result.preferred_cipher)
        self.assertFalse(plugin_result.accepted_cipher_list)
        self.assertTrue(plugin_result.rejected_cipher_list)
        self.assertFalse(plugin_result.errored_cipher_list)

        self.assertTrue(plugin_result.as_text())
        self.assertTrue(plugin_result.as_xml())

    def test_sslv3_enabled(self):
        try:
            server = VulnerableOpenSslServer(port=8014)
        except NotOnLinux64Error:
            # The test suite only has the vulnerable OpenSSL version compiled for Linux 64 bits
            logging.warning('WARNING: Not on Linux - skipping test_sslv3_enabled() test')
            return
        server.start()
        server_info = ServerConnectivityInfo(hostname=server.hostname, ip_address=server.ip_address,  port=server.port)
        server_info.test_connectivity_to_server()

        plugin = OpenSslCipherSuitesPlugin()
        plugin_result = plugin.process_task(server_info, Sslv30ScanCommand())
        server.terminate()

        # The embedded server does not have a preference
        self.assertFalse(plugin_result.preferred_cipher)
        accepted_cipher_name_list = [cipher.name for cipher in plugin_result.accepted_cipher_list]
        self.assertEquals({'TLS_DHE_RSA_EXPORT_WITH_DES40_CBC_SHA', 'TLS_RSA_WITH_3DES_EDE_CBC_SHA',
                           'TLS_DH_anon_WITH_AES_128_CBC_SHA', 'TLS_ECDH_anon_WITH_AES_128_CBC_SHA',
                           'TLS_DH_anon_WITH_SEED_CBC_SHA', 'TLS_RSA_EXPORT_WITH_RC2_CBC_40_MD5',
                           'TLS_ECDHE_RSA_WITH_NULL_SHA', 'TLS_ECDHE_RSA_WITH_RC4_128_SHA',
                           'TLS_DHE_RSA_WITH_SEED_CBC_SHA', 'TLS_DH_anon_WITH_AES_256_CBC_SHA',
                           'TLS_DH_anon_WITH_CAMELLIA_128_CBC_SHA', 'TLS_ECDH_anon_WITH_RC4_128_SHA',
                           'TLS_DH_anon_WITH_3DES_EDE_CBC_SHA', 'TLS_ECDH_anon_WITH_3DES_EDE_CBC_SHA',
                           'TLS_DH_anon_EXPORT_WITH_RC4_40_MD5', 'TLS_RSA_EXPORT_WITH_DES40_CBC_SHA',
                           'TLS_DHE_RSA_WITH_CAMELLIA_256_CBC_SHA', 'TLS_ECDH_anon_WITH_NULL_SHA',
                           'TLS_DH_anon_WITH_CAMELLIA_256_CBC_SHA', 'TLS_RSA_WITH_RC4_128_SHA',
                           'TLS_DHE_RSA_WITH_AES_128_CBC_SHA', 'TLS_RSA_EXPORT_WITH_RC4_40_MD5',
                           'TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA', 'TLS_RSA_WITH_NULL_MD5',
                           'TLS_DH_anon_EXPORT_WITH_DES40_CBC_SHA', 'TLS_DH_anon_WITH_DES_CBC_SHA',
                           'TLS_RSA_WITH_SEED_CBC_SHA', 'TLS_RSA_WITH_DES_CBC_SHA',
                           'TLS_ECDH_anon_WITH_AES_256_CBC_SHA', 'TLS_ECDHE_RSA_WITH_3DES_EDE_CBC_SHA',
                           'TLS_DHE_RSA_WITH_3DES_EDE_CBC_SHA', 'TLS_RSA_WITH_CAMELLIA_256_CBC_SHA',
                           'TLS_DHE_RSA_WITH_DES_CBC_SHA', 'TLS_RSA_WITH_AES_256_CBC_SHA',
                           'TLS_RSA_WITH_RC4_128_MD5', 'TLS_RSA_WITH_CAMELLIA_128_CBC_SHA',
                           'TLS_DHE_RSA_WITH_AES_256_CBC_SHA', 'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA',
                           'TLS_DHE_RSA_WITH_CAMELLIA_128_CBC_SHA', 'TLS_RSA_WITH_NULL_SHA',
                           'TLS_RSA_WITH_IDEA_CBC_SHA', 'TLS_RSA_WITH_AES_128_CBC_SHA', 'TLS_DH_anon_WITH_RC4_128_MD5'},
                          set(accepted_cipher_name_list))

        self.assertTrue(plugin_result.accepted_cipher_list)
        self.assertTrue(plugin_result.rejected_cipher_list)
        self.assertFalse(plugin_result.errored_cipher_list)

        self.assertTrue(plugin_result.as_text())
        self.assertTrue(plugin_result.as_xml())

    def test_sslv3_disabled(self):
        server_info = ServerConnectivityInfo(hostname=u'www.google.com')
        server_info.test_connectivity_to_server()

        plugin = OpenSslCipherSuitesPlugin()
        plugin_result = plugin.process_task(server_info, Sslv30ScanCommand())

        self.assertIsNone(plugin_result.preferred_cipher)
        self.assertFalse(plugin_result.accepted_cipher_list)
        self.assertTrue(plugin_result.rejected_cipher_list)
        self.assertFalse(plugin_result.errored_cipher_list)

        self.assertTrue(plugin_result.as_text())
        self.assertTrue(plugin_result.as_xml())

    def test_tlsv1_0_enabled(self):
        server_info = ServerConnectivityInfo(hostname=u'www.google.com')
        server_info.test_connectivity_to_server()

        plugin = OpenSslCipherSuitesPlugin()
        plugin_result = plugin.process_task(server_info, Tlsv10ScanCommand())

        self.assertTrue(plugin_result.preferred_cipher)
        accepted_cipher_name_list = [cipher.name for cipher in plugin_result.accepted_cipher_list]
        self.assertEquals({'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA', 'TLS_RSA_WITH_AES_256_CBC_SHA',
                           'TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA', 'TLS_RSA_WITH_AES_128_CBC_SHA',
                           'TLS_RSA_WITH_3DES_EDE_CBC_SHA'},
                          set(accepted_cipher_name_list))

        self.assertTrue(plugin_result.accepted_cipher_list)
        self.assertTrue(plugin_result.rejected_cipher_list)
        self.assertFalse(plugin_result.errored_cipher_list)

        self.assertTrue(plugin_result.as_text())
        self.assertTrue(plugin_result.as_xml())

    def test_tlsv1_0_disabled(self):
        # TBD
        pass


    def test_tlsv1_1_enabled(self):
        server_info = ServerConnectivityInfo(hostname=u'www.google.com')
        server_info.test_connectivity_to_server()

        plugin = OpenSslCipherSuitesPlugin()
        plugin_result = plugin.process_task(server_info, Tlsv11ScanCommand())

        self.assertTrue(plugin_result.preferred_cipher)
        self.assertTrue(plugin_result.accepted_cipher_list)
        accepted_cipher_name_list = [cipher.name for cipher in plugin_result.accepted_cipher_list]
        self.assertEquals({'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA', 'TLS_RSA_WITH_AES_256_CBC_SHA',
                           'TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA', 'TLS_RSA_WITH_AES_128_CBC_SHA',
                           'TLS_RSA_WITH_3DES_EDE_CBC_SHA'},
                          set(accepted_cipher_name_list))

        self.assertTrue(plugin_result.rejected_cipher_list)
        self.assertFalse(plugin_result.errored_cipher_list)

        self.assertTrue(plugin_result.as_text())
        self.assertTrue(plugin_result.as_xml())


    def test_tlsv1_2_enabled(self):
        server_info = ServerConnectivityInfo(hostname=u'www.google.com')
        server_info.test_connectivity_to_server()

        plugin = OpenSslCipherSuitesPlugin()
        # Also do full HTTP connections
        plugin_result = plugin.process_task(server_info, Tlsv12ScanCommand(http_get=True))

        self.assertTrue(plugin_result.preferred_cipher)
        self.assertTrue(plugin_result.accepted_cipher_list)
        accepted_cipher_name_list = [cipher.name for cipher in plugin_result.accepted_cipher_list]

        self.assertEquals({'TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384', 'TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA',
                           'TLS_RSA_WITH_AES_256_GCM_SHA384', 'TLS_RSA_WITH_AES_256_CBC_SHA',
                           'TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA', 'TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256',
                           'TLS_RSA_WITH_AES_128_GCM_SHA256', 'TLS_RSA_WITH_AES_128_CBC_SHA',
                           'TLS_RSA_WITH_3DES_EDE_CBC_SHA'},
                          set(accepted_cipher_name_list))

        self.assertTrue(plugin_result.rejected_cipher_list)
        self.assertFalse(plugin_result.errored_cipher_list)

        self.assertTrue(plugin_result.as_text())
        self.assertTrue(plugin_result.as_xml())

    def test_dh_info(self):
        server_info = ServerConnectivityInfo(hostname=u'dh1024.badssl.com')
        server_info.test_connectivity_to_server()

        plugin = OpenSslCipherSuitesPlugin()
        plugin_result = plugin.process_task(server_info, Tlsv12ScanCommand())

        self.assertTrue(plugin_result.preferred_cipher)
        self.assertEquals(plugin_result.preferred_cipher.dh_info['GroupSize'], u'1024')
        self.assertTrue(plugin_result.as_text())
        self.assertTrue(plugin_result.as_xml())

    def test_null_cipher_suites(self):
        server_info = ServerConnectivityInfo(hostname=u'null.badssl.com')
        server_info.test_connectivity_to_server()

        plugin = OpenSslCipherSuitesPlugin()
        plugin_result = plugin.process_task(server_info, Tlsv12ScanCommand())

        accepted_cipher_name_list = [cipher.name for cipher in plugin_result.accepted_cipher_list]
        self.assertEquals({'TLS_ECDH_anon_WITH_AES_256_CBC_SHA', 'TLS_DH_anon_WITH_AES_256_CBC_SHA256',
                           'TLS_DH_anon_WITH_CAMELLIA_256_CBC_SHA', 'TLS_DH_anon_WITH_AES_256_GCM_SHA384',
                           'TLS_DH_anon_WITH_AES_256_CBC_SHA', 'TLS_ECDH_anon_WITH_AES_128_CBC_SHA',
                           'TLS_DH_anon_WITH_AES_128_CBC_SHA256', 'TLS_DH_anon_WITH_AES_128_CBC_SHA',
                           'TLS_DH_anon_WITH_AES_128_GCM_SHA256', 'TLS_DH_anon_WITH_SEED_CBC_SHA',
                           'TLS_DH_anon_WITH_CAMELLIA_128_CBC_SHA', 'TLS_ECDHE_RSA_WITH_NULL_SHA',
                           'TLS_ECDH_anon_WITH_NULL_SHA', 'TLS_RSA_WITH_NULL_SHA256', 'TLS_RSA_WITH_NULL_SHA'},
                          set(accepted_cipher_name_list))

        self.assertTrue(plugin_result.as_text())
        self.assertTrue(plugin_result.as_xml())


    def test_rc4_cipher_suites(self):
        server_info = ServerConnectivityInfo(hostname=u'rc4.badssl.com')
        server_info.test_connectivity_to_server()

        plugin = OpenSslCipherSuitesPlugin()
        plugin_result = plugin.process_task(server_info, Tlsv12ScanCommand())

        accepted_cipher_name_list = [cipher.name for cipher in plugin_result.accepted_cipher_list]
        self.assertEquals({'TLS_ECDHE_RSA_WITH_RC4_128_SHA', 'TLS_RSA_WITH_RC4_128_SHA'},
                          set(accepted_cipher_name_list))

        self.assertTrue(plugin_result.as_text())
        self.assertTrue(plugin_result.as_xml())


    def test_rc4_md5_cipher_suites(self):
        server_info = ServerConnectivityInfo(hostname=u'rc4-md5.badssl.com')
        server_info.test_connectivity_to_server()

        plugin = OpenSslCipherSuitesPlugin()
        plugin_result = plugin.process_task(server_info, Tlsv12ScanCommand())

        accepted_cipher_name_list = [cipher.name for cipher in plugin_result.accepted_cipher_list]
        self.assertEquals({'TLS_RSA_WITH_RC4_128_MD5'},
                          set(accepted_cipher_name_list))

        self.assertTrue(plugin_result.as_text())
        self.assertTrue(plugin_result.as_xml())

    def test_follows_client_cipher_suite_preference(self):
        # Google.com does not follow client cipher suite preference
        server_info = ServerConnectivityInfo(hostname=u'www.google.com')
        server_info.test_connectivity_to_server()

        plugin = OpenSslCipherSuitesPlugin()
        plugin_result = plugin.process_task(server_info, Tlsv12ScanCommand())

        self.assertTrue(plugin_result.preferred_cipher)
        self.assertTrue(plugin_result.accepted_cipher_list)
        
        # Sogou.com follows client cipher suite preference
        server_info = ServerConnectivityInfo(hostname=u'www.sogou.com')
        server_info.test_connectivity_to_server()

        plugin = OpenSslCipherSuitesPlugin()
        plugin_result = plugin.process_task(server_info, Tlsv12ScanCommand())

        self.assertIsNone(plugin_result.preferred_cipher)
        self.assertTrue(plugin_result.accepted_cipher_list)
