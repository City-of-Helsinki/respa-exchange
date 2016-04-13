from respa_exchange.base import EWSRequest
from respa_exchange.xml import M, T


def get_distinguished_folder_id_element(principal, folder_id):
    """
    Build a DistinguishedFolderId element.

    :param principal: The principal (email) whose folder is requested.
    :param folder_id: The distinguished folder name. (See MSDN.)
    :return: XML element
    """
    return T.DistinguishedFolderId(
        {"Id": folder_id},
        T.Mailbox(
            T.EmailAddress(principal)
        )
    )


class GetFolderRequest(EWSRequest):
    """
    Encapsulates a request to get the details of a distinguished folder.
    """
    def __init__(self, principal, dist_id):
        body = M.GetFolder(
            M.FolderShape(
                T.BaseShape("Default")
            ),
            M.FolderIds(
                get_distinguished_folder_id_element(principal, dist_id)
            )
        )
        super(GetFolderRequest, self).__init__(body=body, impersonation=principal)
