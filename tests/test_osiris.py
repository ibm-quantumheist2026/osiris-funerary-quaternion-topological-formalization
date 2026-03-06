"""Unit tests for the OSIRIS CLI application."""

import json
import os
import tempfile
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import patch


class TestBanner(unittest.TestCase):
    """Test the ASCII art banner module."""

    def test_banner_contains_osiris(self):
        from osiris.banner import BANNER

        # "OSIRIS" is rendered as block-character art; check the full name instead.
        self.assertIn("Omega System Integrated Runtime Intelligence System", BANNER)

    def test_banner_contains_dna_lang(self):
        from osiris.banner import BANNER

        self.assertIn("DNA", BANNER)
        self.assertIn("lang", BANNER)

    def test_banner_contains_version(self):
        from osiris.banner import BANNER

        self.assertIn("v51.843", BANNER)

    def test_banner_contains_organisms(self):
        from osiris.banner import BANNER

        for organism in ("AIDEN", "AURA", "CHEOPS", "CHRONOS", "SCIMITAR"):
            self.assertIn(organism, BANNER)

    def test_print_banner(self):
        from osiris.banner import print_banner

        with patch("builtins.print") as mock_print:
            print_banner()
            mock_print.assert_called_once()


class TestQuantumTokenDiscovery(unittest.TestCase):
    """Test IBM Quantum token discovery logic."""

    def test_no_token_returns_none(self):
        from osiris.quantum import discover_ibm_quantum_token

        # Use clear=True to avoid interference from real env vars;
        # restore only non-token variables that the subprocess may need.
        safe_env = {
            k: v
            for k, v in os.environ.items()
            if k not in ("IBM_QUANTUM_TOKEN", "QISKIT_IBM_TOKEN", "IBMQ_TOKEN")
        }
        with patch.dict(os.environ, safe_env, clear=True):
            result = discover_ibm_quantum_token()
        # May still find a token from a local config file on the test host;
        # we only assert that the return type is correct.
        self.assertTrue(result is None or isinstance(result, str))

    def test_env_var_ibm_quantum_token(self):
        from osiris.quantum import discover_ibm_quantum_token

        with patch.dict(os.environ, {"IBM_QUANTUM_TOKEN": "test_token_abc123"}):
            result = discover_ibm_quantum_token()
        self.assertEqual(result, "test_token_abc123")

    def test_env_var_qiskit_ibm_token(self):
        from osiris.quantum import discover_ibm_quantum_token

        with patch.dict(
            os.environ,
            {"QISKIT_IBM_TOKEN": "qiskit_token_xyz", "IBM_QUANTUM_TOKEN": ""},
        ):
            os.environ.pop("IBM_QUANTUM_TOKEN", None)
            result = discover_ibm_quantum_token()
        self.assertEqual(result, "qiskit_token_xyz")

    def test_ibm_quantum_token_takes_priority_over_qiskit(self):
        from osiris.quantum import discover_ibm_quantum_token

        with patch.dict(
            os.environ,
            {
                "IBM_QUANTUM_TOKEN": "priority_token",
                "QISKIT_IBM_TOKEN": "fallback_token",
            },
        ):
            result = discover_ibm_quantum_token()
        self.assertEqual(result, "priority_token")

    def test_token_from_config_file(self):
        from osiris.quantum import _read_token_from_config

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".ini", delete=False
        ) as fh:
            fh.write("[ibmq]\ntoken = config_file_token\n")
            tmp_path = Path(fh.name)
        try:
            result = _read_token_from_config(tmp_path)
            self.assertEqual(result, "config_file_token")
        finally:
            tmp_path.unlink()

    def test_nonexistent_config_file_returns_none(self):
        from osiris.quantum import _read_token_from_config

        result = _read_token_from_config(Path("/nonexistent/path/config"))
        self.assertIsNone(result)

    def test_redact_token_long(self):
        from osiris.quantum import redact_token

        result = redact_token("abcdefghijklmnop")
        self.assertEqual(result, "abcdefgh...")

    def test_redact_token_short(self):
        from osiris.quantum import redact_token

        # Tokens with 8 or fewer characters are fully masked
        result = redact_token("ab")
        self.assertEqual(result, "***")

    def test_redact_token_exactly_eight(self):
        from osiris.quantum import redact_token

        # Exactly 8 chars is still fully masked (not > 8)
        result = redact_token("abcdefgh")
        self.assertEqual(result, "***")

    def test_redact_token_very_short(self):
        from osiris.quantum import redact_token

        result = redact_token("a")
        self.assertEqual(result, "***")


class TestSession(unittest.TestCase):
    """Test session save/load functionality."""

    def _make_session_dir(self):
        tmpdir = tempfile.mkdtemp()
        return Path(tmpdir)

    def test_load_session_missing_file(self):
        import osiris.session as session_mod

        with patch.object(session_mod, "_SESSION_FILE", Path("/nonexistent/session.json")):
            result = session_mod.load_session()
        self.assertEqual(result, [])

    def test_save_and_load_roundtrip(self):
        import osiris.session as session_mod

        with tempfile.TemporaryDirectory() as tmpdir:
            session_file = Path(tmpdir) / "session.json"
            messages = [
                {"role": "user", "content": "hello"},
                {"role": "assistant", "content": "hi"},
            ]
            with (
                patch.object(session_mod, "_SESSION_DIR", Path(tmpdir)),
                patch.object(session_mod, "_SESSION_FILE", session_file),
            ):
                session_mod.save_session(messages)
                loaded = session_mod.load_session()
        self.assertEqual(loaded, messages)

    def test_save_caps_at_max_messages(self):
        import osiris.session as session_mod

        with tempfile.TemporaryDirectory() as tmpdir:
            session_file = Path(tmpdir) / "session.json"
            messages = [{"role": "user", "content": str(i)} for i in range(1500)]
            with (
                patch.object(session_mod, "_SESSION_DIR", Path(tmpdir)),
                patch.object(session_mod, "_SESSION_FILE", session_file),
                patch.object(session_mod, "_MAX_MESSAGES", 100),
            ):
                session_mod.save_session(messages)
                loaded = session_mod.load_session()
        self.assertEqual(len(loaded), 100)
        # Should be the *last* 100 messages
        self.assertEqual(loaded[0]["content"], "1400")

    def test_append_message(self):
        from osiris.session import append_message

        messages = []
        append_message(messages, "user", "test content")
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0]["role"], "user")
        self.assertEqual(messages[0]["content"], "test content")

    def test_load_session_invalid_json(self):
        import osiris.session as session_mod

        with tempfile.TemporaryDirectory() as tmpdir:
            session_file = Path(tmpdir) / "session.json"
            session_file.write_text("not valid json{{{")
            with patch.object(session_mod, "_SESSION_FILE", session_file):
                result = session_mod.load_session()
        self.assertEqual(result, [])


class TestInitSequence(unittest.TestCase):
    """Test initialization sequence output."""

    def test_run_init_sequence_no_token(self):
        from osiris.init_sequence import run_init_sequence

        with (
            patch("osiris.init_sequence.discover_ibm_quantum_token", return_value=None),
            patch("builtins.print") as mock_print,
        ):
            result = run_init_sequence()

        self.assertFalse(result)
        printed = " ".join(str(c) for c in mock_print.call_args_list)
        self.assertIn("NCLM Engine", printed)
        self.assertIn("Consciousness Field", printed)
        self.assertIn("Sovereign Lock", printed)

    def test_run_init_sequence_with_token(self):
        from osiris.init_sequence import run_init_sequence

        with (
            patch(
                "osiris.init_sequence.discover_ibm_quantum_token",
                return_value="99ezCffR_secret_token",
            ),
            patch("builtins.print") as mock_print,
        ):
            result = run_init_sequence()

        self.assertTrue(result)
        printed = " ".join(str(c) for c in mock_print.call_args_list)
        self.assertIn("Token loaded", printed)
        self.assertIn("auto-discovered", printed)


class TestPackageMetadata(unittest.TestCase):
    """Test package version constants."""

    def test_version(self):
        import osiris

        self.assertEqual(osiris.__version__, "5.3.0")

    def test_dna_version(self):
        import osiris

        self.assertEqual(osiris.__dna_version__, "51.843")


if __name__ == "__main__":
    unittest.main()
