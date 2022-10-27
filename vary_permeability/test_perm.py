import pytest
from create_permeability_field import *

def test_combi_perm_field_create_and_plot():
    perm_created = create_perm_field(1, "test", random_bool=False)
    # read h5 perm file
    perm_read = read_and_plot_perm_field("permeability_fields/permeability_base_8325804_test.h5")

    assert (perm_created==perm_read).all(), "read perm_field differs from create perm_field"