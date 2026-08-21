from sov_evidence_geometry_core import check_symmetric_matrix

def test_simple_kernel_returns_readable_verified_receipt():
    receipt = check_symmetric_matrix([[1, 2], [2, 4]])
    assert receipt["status"] == "verified" and receipt["plain_status"] == "holds in this check"
    assert receipt["receipt_id"].startswith("sov:sha256:")
def test_simple_kernel_explains_a_failure():
    receipt = check_symmetric_matrix([[1, 3], [2, 4]])
    assert receipt["status"] == "fail" and receipt["details"]["mismatches"][0]["at"] == [0, 1]
def test_simple_kernel_does_not_guess_on_bad_input():
    receipt = check_symmetric_matrix([[1, 2, 3], [2, 4]])
    assert receipt["status"] == "unverifiable" and receipt["details"]["reason_code"] == "E_INPUT_NOT_SQUARE_NUMERIC"
def test_identity_and_inverse_receipts_are_practical_checks():
    from sov_evidence_geometry_core import check_identity_matrix, check_matrix_inverse
    assert check_identity_matrix([[1,0],[0,1]])["status"] == "verified"
    inverse=check_matrix_inverse([[2,0],[0,3]], [[0.5,0],[0,1/3]])
    assert inverse["status"] == "verified" and inverse["details"]["product"] == [[1.0,0.0],[0.0,1.0]]
def test_inverse_receipt_exposes_product_mismatch():
    from sov_evidence_geometry_core import check_matrix_inverse
    assert check_matrix_inverse([[2]], [[0.4]])["status"] == "fail"
