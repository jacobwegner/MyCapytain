# -*- coding: utf-8 -*-
"""
.. module:: MyCapytain.resources.proto.text
   :synopsis: Prototypes for CtsText

.. moduleauthor:: Thibault Clérice <leponteineptique@gmail.com>


"""
from typing import Union, List, Iterator
from rdflib.namespace import DC
from rdflib import BNode, URIRef, Graph, Literal
from rdflib.term import Identifier
from MyCapytain.common.reference import URN, Citation, NodeId, BaseReference, BaseReferenceSet
from MyCapytain.common.metadata import Metadata
from MyCapytain.common.constants import Mimetypes, get_graph, RDF_NAMESPACES
from MyCapytain.common.base import Exportable
from MyCapytain.resources.prototypes.metadata import Collection
from MyCapytain.resources.prototypes.cts.inventory import CtsTextMetadata


__all__ = [
    "TextualElement",
    "TextualGraph",
    "TextualNode",
    "CtsText",
    "InteractiveTextualNode",
    "CtsNode"
]


class TextualElement(Exportable):
    """ Node representing a text passage.

    :param identifier: Identifier of the text
    :type identifier: str
    :param metadata: Collection Information about the Item
    :type metadata: Collection

    :cvar default_exclude: Default exclude for exports
    """

    default_exclude = []

    def __init__(self, identifier: str=None, metadata: Metadata=None):
        self._graph = get_graph()
        self._identifier = identifier

        self._node = BNode()
        self._metadata = metadata or Metadata(node=self.asNode())

        self._graph.addN([
            (self._node, RDF_NAMESPACES.DTS.implements, URIRef(identifier), self._graph)#,
            #(self.__node__, RDF_NAMESPACES.DTS.metadata, self.metadata.asNode(), self.__graph__)
        ])

    def __repr__(self) -> str:
        return "%s(%s)" % (self.__class__.__name__, self.id)

    @property
    def graph(self) -> Graph:
        return self._graph

    @property
    def text(self) -> str:
        """ String representation of the text

        :return: String representation of the text
        """
        return self.export(output=Mimetypes.PLAINTEXT, exclude=self.default_exclude)

    @property
    def id(self) -> str:
        """ Identifier of the text

        :return: Identifier of the text
        """
        return self._identifier

    @property
    def metadata(self) -> Metadata:
        """ Metadata information about the text

        :return: Collection object with metadata about the text
        :rtype: Metadata
        """
        return self._metadata

    def asNode(self) -> Identifier:
        return self._node

    def get_creator(self, lang: str=None) -> Literal:
        """ Get the DC Creator literal value

        :param lang: Language to retrieve
        :return: Creator string representation
        :rtype: Literal
        """
        return self.metadata.get_single(key=DC.creator, lang=lang)

    def set_creator(self, value: Union[Literal, Identifier, str], lang: str= None):
        """ Set the DC Creator literal value

        :param value: Value of the creator node
        :param lang: Language in which the value is
        """
        self.metadata.add(key=DC.creator, value=value, lang=lang)

    def get_title(self, lang: str=None) -> Literal:
        """ Get the title of the object

        :param lang: Lang to retrieve
        :return: Title string representation
        :rtype: Literal
        """
        return self.metadata.get_single(key=DC.title, lang=lang)

    def set_title(self, value: Union[Literal, Identifier, str], lang: str= None):
        """ Set the DC Title literal value

        :param value: Value of the title node
        :param lang: Language in which the value is
        """
        return self.metadata.add(key=DC.title, value=value, lang=lang)

    def get_description(self, lang: str=None) -> Literal:
        """ Get the description of the object

        :param lang: Lang to retrieve
        :return: Description string representation
        :rtype: Literal
        """
        return self.metadata.get_single(key=DC.description, lang=lang)

    def set_description(self, value: Union[Literal, Identifier, str], lang: str= None):
        """ Set the DC Description literal value

        :param value: Value of the title node
        :param lang: Language in which the value is
        """
        return self.metadata.add(key=DC.description, value=value, lang=lang)

    def get_subject(self, lang=None) -> Literal:
        """ Get the subject of the object

        :param lang: Lang to retrieve
        :return: Subject string representation
        :rtype: Literal
        """
        return self.metadata.get_single(key=DC.subject, lang=lang)

    def set_subject(self, value: Union[Literal, Identifier, str], lang: str= None):
        """ Set the DC Subject literal value

        :param value: Value of the subject node
        :param lang: Language in which the value is
        """
        return self.metadata.add(key=DC.subject, value=value, lang=lang)

    def export(self, output: str=None, exclude: List[str]=None, **kwargs):
        """ Export the collection item in the Mimetype required.

        ..note:: If current implementation does not have special mimetypes, reuses default_export method

        :param output: Mimetype to export to (Uses MyCapytain.common.constants.Mimetypes)
        :type output: str
        :param exclude: Information to exclude. Specific to implementations
        :type exclude: [str]
        :return: Object using a different representation
        """
        return Exportable.export(self, output, exclude=exclude, **kwargs)


class TextualNode(TextualElement, NodeId):
    """ Node representing a text passage.

    :param identifier: Identifier of the text
    :type identifier: str
    :param metadata: Collection Information about the Item
    :type metadata: Collection
    :param citation: XmlCtsCitation system of the text
    :type citation: Citation
    :param children: Current node Children's Identifier
    :type children: [str]
    :param parent: Parent of the current node
    :type parent: str
    :param siblings: Previous and next node of the current node
    :type siblings: str
    :param depth: Depth of the node in the global hierarchy of the text tree
    :type depth: int

    :cvar default_exclude: Default exclude for exports
    """

    def __init__(self, identifier: str=None, citation: Citation=None, **kwargs):
        super(TextualNode, self).__init__(identifier=identifier, **kwargs)
        self._citation = citation or Citation()

    @property
    def citation(self) -> Citation:
        """ Citation system of the object

        :rtype: Citation
        """
        return self._citation

    @citation.setter
    def citation(self, value: Citation):
        if not isinstance(value, Citation):
            raise TypeError("Citation property can only host a Citation object")
        self._citation = value


class TextualGraph(TextualNode):
    """ Node representing a text passage.

    :param identifier: Identifier of the text
    :type identifier: str
    :param metadata: Collection Information about the Item
    :type metadata: Collection
    :param citation: XmlCtsCitation system of the text
    :type citation: Citation
    :param children: Current node Children's Identifier
    :type children: [str]
    :param parent: Parent of the current node
    :type parent: str
    :param siblings: Previous and next node of the current node
    :type siblings: str
    :param depth: Depth of the node in the global hierarchy of the text tree
    :type depth: int
    :param resource: Resource used to navigate through the textual graph

    :cvar default_exclude: Default exclude for exports
    """
    def __init__(self, identifier: str=None, **kwargs):
        super(TextualGraph, self).__init__(identifier=identifier, **kwargs)

    def getTextualNode(self, subreference: BaseReference) -> "TextualGraph":
        """ Retrieve a passage and store it in the object

        :param subreference: CtsReference of the passage to retrieve
        :returns: Object representing the passage

        :raises: *TypeError* when reference is not a list or a CtsReference
        """

        raise NotImplementedError()

    def getReffs(self, level: int=1, subreference: BaseReference=None) -> BaseReferenceSet:
        """ CtsReference available at a given level

        :param level: Depth required. If not set, should retrieve first encountered level (1 based)
        :param subreference: Subreference (optional)
        :returns: List of levels
        """
        raise NotImplementedError()


class InteractiveTextualNode(TextualGraph):
    """ Node representing a text passage.

    :param identifier: Identifier of the text
    :type identifier: str
    :param metadata: Collection Information about the Item
    :type metadata: Collection
    :param citation: XmlCtsCitation system of the text
    :type citation: Citation
    :param children: Current node Children's Identifier
    :type children: [str]
    :param parent: Parent of the current node
    :type parent: str
    :param siblings: Previous and next node of the current node
    :type siblings: str
    :param depth: Depth of the node in the global hierarchy of the text tree
    :type depth: int
    :param resource: Resource used to navigate through the textual graph

    :cvar default_exclude: Default exclude for exports
    """
    def __init__(self, identifier: str=None, **kwargs):
        super(InteractiveTextualNode, self).__init__(identifier=identifier, **kwargs)
        self._childIds = None

    @property
    def prev(self) -> "InteractiveTextualNode":
        """ Get Previous TextualNode
        """
        if self.prevId is not None:
            return self.getTextualNode(self.prevId)

    @property
    def next(self) -> "InteractiveTextualNode":
        """ Get Next TextualNode
        """
        if self.nextId is not None:
            return self.getTextualNode(self.nextId)

    @property
    def children(self) -> Iterator["InteractiveTextualNode"]:
        """ Children TextualNode

        """
        for ID in self.childIds:
            yield self.getTextualNode(ID)

    @property
    def parent(self) -> "InteractiveTextualNode":
        """ Parent TextualNode

        """
        return self.getTextualNode(self.parentId)

    @property
    def first(self) -> TextualNode:
        """ First TextualNode
        """
        if self.firstId is not None:
            return self.getTextualNode(self.firstId)

    @property
    def last(self) -> TextualNode:
        """ Last CapitainsCtsPassage
        """
        if self.lastId is not None:
            return self.getTextualNode(self.lastId)

    @property
    def childIds(self) -> BaseReferenceSet:
        """ Identifiers of children

        :return: Identifiers of children
        """
        if self._childIds is None:
            self._childIds = self.getReffs()
        return self._childIds

    @property
    def firstId(self) -> BaseReference:
        """ First child's id of current TextualNode
        """
        if self.childIds is not None:
            if len(self.childIds) > 0:
                return self.childIds[0]
            return None
        else:
            raise NotImplementedError

    @property
    def lastId(self) -> BaseReference:
        """ Last child's id of current TextualNode
        """
        if self.childIds is not None:
            if len(self.childIds) > 0:
                return self.childIds[-1]
            return None
        else:
            raise NotImplementedError


class CtsNode(InteractiveTextualNode):
    """ Initiate a Resource object
    
    :param urn: A URN identifier
    :type urn: MyCapytain.common.reference._capitains_cts.URN
    :param metadata: Collection Information about the Item
    :type metadata: Collection
    :param citation: XmlCtsCitation system of the text
    :type citation: Citation
    :param children: Current node Children's Identifier
    :type children: [str]
    :param parent: Parent of the current node
    :type parent: str
    :param siblings: Previous and next node of the current node
    :type siblings: str
    :param depth: Depth of the node in the global hierarchy of the text tree
    :type depth: int
    :param resource: Resource used to navigate through the textual graph

    :cvar default_exclude: Default exclude for exports
    """

    def __init__(self, urn: Union[URN, str]=None, **kwargs):
        super(CtsNode, self).__init__(identifier=str(urn), **kwargs)
        self._urn = None

        if urn is not None:
            self.urn = urn

    @property
    def urn(self) -> URN:
        """ URN Identifier of the object

        """
        return self._urn
    
    @urn.setter
    def urn(self, value: Union[URN, str]):
        """ Set the urn

        :param value: URN to be saved
        :raises: *TypeError* when the value is not URN compatible

        """
        if isinstance(value, str):
            value = URN(value)
        elif not isinstance(value, URN):
            raise TypeError()
        self._urn = value

    def get_cts_metadata(self, key: str, lang: str=None) -> Literal:
        """ Get easily a metadata from the CTS namespace

        :param key: CTS property to retrieve
        :param lang: Language in which it should be
        :return: Literal value of the CTS graph property
        """
        return self.metadata.get_single(RDF_NAMESPACES.CTS.term(key), lang)

    def getValidReff(self, level: int=1, reference: BaseReference=None) -> BaseReferenceSet:
        """ Given a resource, CtsText will compute valid reffs

        :param level: Depth required. If not set, should retrieve first encountered level (1 based)
        :param reference: Subreference (optional)
        :returns: List of levels
        """
        raise NotImplementedError()

    def getLabel(self) -> Collection:
        """ Retrieve metadata about the text

        :rtype: Collection
        :returns: Retrieve Label informations in a Collection format
        """
        raise NotImplementedError()

    def set_metadata_from_collection(self, text_metadata: CtsTextMetadata):
        """ Set the object metadata using its collections recursively

        :param text_metadata: Object representing the current text as a collection
        :type text_metadata: CtsEditionMetadata or CtsTranslationMetadata
        """
        edition, work, textgroup = tuple(([text_metadata] + text_metadata.parents)[:3])

        for node in textgroup.metadata.get(RDF_NAMESPACES.CTS.groupname):
            lang = node.language
            self.metadata.add(RDF_NAMESPACES.CTS.groupname, lang=lang, value=str(node))
            self.set_creator(str(node), lang)

        for node in work.metadata.get(RDF_NAMESPACES.CTS.title):
            lang = node.language
            self.metadata.add(RDF_NAMESPACES.CTS.title, lang=lang, value=str(node))
            self.set_title(str(node), lang)

        for node in edition.metadata.get(RDF_NAMESPACES.CTS.label):
            lang = node.language
            self.metadata.add(RDF_NAMESPACES.CTS.label, lang=lang, value=str(node))
            self.set_subject(str(node), lang)

        for node in edition.metadata.get(RDF_NAMESPACES.CTS.description):
            lang = node.language
            self.metadata.add(RDF_NAMESPACES.CTS.description, lang=lang, value=str(node))
            self.set_description(str(node), lang)

        if not self.citation.is_set() and edition.citation.is_set():
            self.citation = edition.citation


class CtsPassage(CtsNode):
    """ CapitainsCtsPassage objects possess metadata informations

    :param urn: A URN identifier
    :type urn: MyCapytain.common.reference._capitains_cts.URN
    :param metadata: Collection Information about the Item
    :type metadata: Collection
    :param citation: XmlCtsCitation system of the text
    :type citation: Citation
    :param children: Current node Children's Identifier
    :type children: [str]
    :param parent: Parent of the current node
    :type parent: str
    :param siblings: Previous and next node of the current node
    :type siblings: str
    :param depth: Depth of the node in the global hierarchy of the text tree
    :type depth: int
    :param resource: Resource used to navigate through the textual graph

    :cvar default_exclude: Default exclude for exports
    """

    def __init__(self, **kwargs):
        super(CtsPassage, self).__init__(**kwargs)

    @property
    def reference(self) -> BaseReference:
        return self.urn.reference


class CtsText(CtsNode):
    """ A CTS CtsText
    """
    def __init__(self, citation=None, metadata=None, **kwargs):
        super(CtsText, self).__init__(citation=citation, metadata=metadata, **kwargs)
        self._cts = None

    @property
    def reffs(self) -> BaseReferenceSet:
        """ Get all valid reffs for every part of the CtsText

        :rtype: [str]
        """
        if not self._cts:
            self._cts = BaseReferenceSet(
                [reff for reffs in [self.getReffs(level=i) for i in range(1, len(self.citation) + 1)] for reff in reffs]
            )
        return self._cts
