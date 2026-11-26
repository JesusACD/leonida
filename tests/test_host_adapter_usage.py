"""Host D3D12 comparison tests must select hardware adapters through host_adapter.h."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parent.parent
TEST_DIR = ROOT / "runtime" / "test"

PARITY_TESTS = (
    "d3d12_predication_atomic_copy_test.cpp",
    "d3d12_dxr_validation_test.cpp",
    "d3d12_cross_device_validation_test.cpp",
)


class HostAdapterUsageTest(unittest.TestCase):
    def test_parity_tests_route_hardware_adapter_through_host_adapter_header(self):
        for name in PARITY_TESTS:
            with self.subTest(test=name):
                text = (TEST_DIR / name).read_text(encoding="utf-8")
                self.assertIn('#include "host_adapter.h"', text)
                self.assertIn('#include "host_wine.h"', text)
                self.assertIn("hostwine::host_is_wine()", text)
                self.assertIn("hostadapter::reference(", text)
                self.assertIsNone(
                    re.search(r"->\s*EnumAdapters1?\s*\(", text),
                    f"{name} enumerates DXGI adapters directly instead of using hostadapter::reference",
                )

    def test_host_adapter_reference_supports_caller_feature_level(self):
        header = (TEST_DIR / "host_adapter.h").read_text(encoding="utf-8")
        self.assertRegex(
            header,
            r"inline\s+bool\s+reference\([^)]*D3D_FEATURE_LEVEL\s+level\s*=\s*D3D_FEATURE_LEVEL_11_0\)",
        )


if __name__ == "__main__":
    unittest.main()
