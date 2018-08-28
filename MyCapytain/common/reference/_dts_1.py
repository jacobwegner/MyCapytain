from ._base import BaseCitationSet, BaseCitation
from MyCapytain.common.constants import RDF_NAMESPACES


_dts = RDF_NAMESPACES.DTS
_cite_type_term = str(_dts.term("citeType"))
_cite_structure_term = str(_dts.term("citeStructure"))


class DtsCitation(BaseCitation):
    def __init__(self, name=None, children=None, root=None):
        super(DtsCitation, self).__init__(name=name, children=children, root=root)

    @classmethod
    def ingest(cls, resource, root=None, **kwargs):
        """ Ingest a dictionary of DTS Citation object (as parsed JSON-LD) and
        creates the Citation Graph

        :param resource: List of Citation objects from the
            DTS Collection Endpoint (as expanded JSON-LD)
        :type resource: dict
        :param root: Root of the citation tree
        :type root: BaseCitationSet
        :return:
        """
        cite = cls(
            name=resource.get(_cite_type_term, [{"@value": None}])[0]["@value"],  # Not really clean ?
            root=root
        )
        for subCite in resource.get(_cite_structure_term, []):
            cite.add_child(cls.ingest(subCite, root=root))
        return cite

    def match(self, passageId):
        raise NotImplementedError("Passage Match is not part of the DTS Standard Citation")


class DtsCitationSet(BaseCitationSet):
    """ Set of citation that are supposed

    """

    def __repr__(self):
        return "<MyCapytain.common.reference.DtsCitationSet object at %s>" % id(self)

    CitationClass = DtsCitation

    def match(self, passageId):
        raise NotImplementedError("Passage Match is not part of the DTS Standard Citation")

    @classmethod
    def ingest(cls, resource):
        """ Ingest a list of DTS Citation object (as parsed JSON-LD) and
        creates the Citation Graph

        :param resource: List of Citation objects from the
            DTS Collection Endpoint (as expanded JSON-LD)
        :type resource: list
        :return: Citation Graph
        """
        _set = cls()
        for data in resource:
            _set.add_child(
                cls.CitationClass.ingest(data, root=_set)
            )
        return _set
