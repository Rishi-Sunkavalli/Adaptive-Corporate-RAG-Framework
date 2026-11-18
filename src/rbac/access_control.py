"""
Role-Based Access Control (RBAC) Module for Adaptive Corporate RAG.
Enforces pre-retrieval access boundary validation so that employees only retrieve
documents they are explicitly authorized to access according to their department and role.
"""

from enum import Enum
from typing import List, Dict, Any, Optional

class Role(str, Enum):
    GENERAL_EMPLOYEE = "General_Employee"
    HR_STAFF = "HR_Staff"
    IT_STAFF = "IT_Staff"
    FINANCE_STAFF = "Finance_Staff"
    OPERATIONS_STAFF = "Operations_Staff"
    LEGAL_COUNSEL = "Legal_Counsel"
    EXECUTIVE_ADMIN = "Executive_Admin"

# Document ID to permitted roles mapping
DOCUMENT_PERMISSIONS: Dict[str, List[Role]] = {
    # HR Documents
    "HR-DOC-001": [Role.GENERAL_EMPLOYEE, Role.HR_STAFF, Role.IT_STAFF, Role.FINANCE_STAFF, Role.OPERATIONS_STAFF, Role.LEGAL_COUNSEL, Role.EXECUTIVE_ADMIN],
    "HR-DOC-002": [Role.GENERAL_EMPLOYEE, Role.HR_STAFF, Role.IT_STAFF, Role.FINANCE_STAFF, Role.OPERATIONS_STAFF, Role.LEGAL_COUNSEL, Role.EXECUTIVE_ADMIN],
    "HR-DOC-003": [Role.GENERAL_EMPLOYEE, Role.HR_STAFF, Role.IT_STAFF, Role.FINANCE_STAFF, Role.OPERATIONS_STAFF, Role.LEGAL_COUNSEL, Role.EXECUTIVE_ADMIN],

    # IT Documents
    "IT-DOC-001": [Role.GENERAL_EMPLOYEE, Role.HR_STAFF, Role.IT_STAFF, Role.FINANCE_STAFF, Role.OPERATIONS_STAFF, Role.LEGAL_COUNSEL, Role.EXECUTIVE_ADMIN],
    "IT-DOC-002": [Role.IT_STAFF, Role.OPERATIONS_STAFF, Role.EXECUTIVE_ADMIN],  # Restricted to IT & Ops
    "IT-DOC-003": [Role.IT_STAFF, Role.EXECUTIVE_ADMIN],                         # Restricted to IT Security & Execs

    # Finance Documents
    "FIN-DOC-001": [Role.GENERAL_EMPLOYEE, Role.HR_STAFF, Role.IT_STAFF, Role.FINANCE_STAFF, Role.OPERATIONS_STAFF, Role.LEGAL_COUNSEL, Role.EXECUTIVE_ADMIN],
    "FIN-DOC-002": [Role.FINANCE_STAFF, Role.EXECUTIVE_ADMIN],                    # Restricted to Finance & Execs
    "FIN-DOC-003": [Role.FINANCE_STAFF, Role.EXECUTIVE_ADMIN],                    # Restricted to Finance & Execs

    # Operations Documents
    "OPS-DOC-001": [Role.OPERATIONS_STAFF, Role.IT_STAFF, Role.EXECUTIVE_ADMIN], # Restricted to Ops, IT & Execs
    "OPS-DOC-002": [Role.OPERATIONS_STAFF, Role.EXECUTIVE_ADMIN],                 # Restricted to Ops & Execs
    "OPS-DOC-003": [Role.OPERATIONS_STAFF, Role.FINANCE_STAFF, Role.EXECUTIVE_ADMIN],

    # Legal & Governance Documents
    "LEGAL-DOC-001": [Role.LEGAL_COUNSEL, Role.EXECUTIVE_ADMIN],                  # Restricted to Legal & Execs
    "LEGAL-DOC-002": [Role.GENERAL_EMPLOYEE, Role.HR_STAFF, Role.IT_STAFF, Role.FINANCE_STAFF, Role.OPERATIONS_STAFF, Role.LEGAL_COUNSEL, Role.EXECUTIVE_ADMIN],
}

class UserContext:
    def __init__(self, user_id: str, name: str, role: Role, department: str):
        self.user_id = user_id
        self.name = name
        self.role = role
        self.department = department

    def can_access_document(self, doc_id: str, doc_metadata: Optional[Dict[str, Any]] = None) -> bool:
        if self.role == Role.EXECUTIVE_ADMIN:
            return True

        # Check explicit permissions mapping
        if doc_id in DOCUMENT_PERMISSIONS:
            return self.role in DOCUMENT_PERMISSIONS[doc_id]

        # Check document metadata if passed
        if doc_metadata:
            allowed_roles = doc_metadata.get("allowed_roles")
            if allowed_roles:
                role_strs = [r.value if isinstance(r, Role) else str(r) for r in allowed_roles]
                return self.role.value in role_strs or self.role in allowed_roles

            clearance = doc_metadata.get("security_clearance", "Internal")
            if clearance in ["Public", "Internal"]:
                return True
            elif clearance == "Confidential":
                dept = doc_metadata.get("department", "")
                if self.department.lower() in dept.lower():
                    return True
                return False

        # Default restricted
        return False

    def __repr__(self):
        return f"<UserContext {self.user_id}: {self.name} ({self.role.value})>"


DEFAULT_USERS = {
    "emp_001": UserContext("emp_001", "Alex Smith (General Staff)", Role.GENERAL_EMPLOYEE, "Marketing"),
    "hr_001": UserContext("hr_001", "Sarah Jenkins (HR Specialist)", Role.HR_STAFF, "Human Resources"),
    "it_001": UserContext("it_001", "David Kumar (DevOps/IT Engineer)", Role.IT_STAFF, "Information Technology"),
    "fin_001": UserContext("fin_001", "Rachel Wong (Finance Officer)", Role.FINANCE_STAFF, "Finance"),
    "ops_001": UserContext("ops_001", "Marcus Brody (Ops Lead)", Role.OPERATIONS_STAFF, "Operations"),
    "legal_001": UserContext("legal_001", "Ananya Sharma (Legal Counsel)", Role.LEGAL_COUNSEL, "Legal & Compliance"),
    "admin_001": UserContext("admin_001", "Elena Vance (VP & CISO)", Role.EXECUTIVE_ADMIN, "Executive Leadership"),
}

def filter_authorized_documents(documents: List[Dict[str, Any]], user: UserContext) -> List[Dict[str, Any]]:
    """
    Applies strict pre-retrieval authorization filtering.
    Any chunk from an unauthorized document is excluded before similarity search.
    """
    return [doc for doc in documents if user.can_access_document(doc.get("doc_id", ""), doc)]
