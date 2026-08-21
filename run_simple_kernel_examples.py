from sov_evidence_geometry_core import check_symmetric_matrix, check_identity_matrix, check_matrix_inverse
for name, receipt in {"symmetric":check_symmetric_matrix([[1,2],[2,4]]),"identity":check_identity_matrix([[1,0],[0,1]]),"inverse":check_matrix_inverse([[2,0],[0,3]],[[0.5,0],[0,1/3]])}.items():
    print(name, receipt["status"], receipt["plain_status"], receipt["receipt_id"])
