
import os
import json
from qiskit.test.mock.fake_qasm_backend import FakeQasmBackend
from qiskit.providers.models import QasmBackendConfiguration, BackendProperties
from qiskit.test.mock.utils.json_decoder import (
    decode_backend_configuration,
    decode_backend_properties,
)

class FakeBrisbane(FakeQasmBackend):
    """A fake 127 qubit backend."""

    dirname = os.path.dirname(__file__)
    conf_filename = "fake_provider/backends/brisbane/conf_brisbane.json"
    props_filename = "fake_provider/backends/brisbane/props_brisbane.json"
    backend_name = "fake_brisbane"
