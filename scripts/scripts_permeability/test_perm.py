import pytest
from create_permeability_field import *

def test_combi_perm_field_create_and_plot():
    settings = Settings(random_bool=False)
    perm_created = create_perm_field(1, "test", settings)

    # read h5 perm file
    for file in os.listdir(f"test/permeability_fields"):
        if file.endswith(".h5"):
            perm_read = read_and_plot_perm_field(settings, filename=f"test/permeability_fields/{file}")
    assert (perm_created==perm_read).all(), "read perm_field differs from create perm_field"

if __name__ == "__main__":
    test_combi_perm_field_create_and_plot()