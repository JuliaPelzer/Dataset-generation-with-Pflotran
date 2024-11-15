import os
import subprocess

from scripts.create_varying_field import (create_vary_fields,
                                               read_and_plot_vary_field)
from scripts.make_general_settings import load_yaml


def test_combi_perm_field_create_and_plot():
    settings = load_yaml("unittests")
    perm_created = create_vary_fields(1, "test", settings)

    # read h5 perm file
    for file in os.listdir(f"test/permeability_fields"):
        if file.endswith(".h5"):
            perm_read = read_and_plot_vary_field(
                settings, filename=f"test/permeability_fields/{file}"
            )
    assert (
        perm_created == perm_read
    ).all(), "read perm_field differs from create perm_field"

    subprocess.call("rm -r test", shell=True)
    subprocess.call("rm -r permeability_perlin_noise_*", shell=True)
