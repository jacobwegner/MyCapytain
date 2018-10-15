from .base import *
from .base import _load_mock, _load_json_mock


class TestHttpDtsResolverCollection(unittest.TestCase):
    def setUp(self):
        self.root_uri = "http://foobar.com/api/dts"
        self.resolver = HttpDtsResolver(self.root_uri)

    @requests_mock.mock()
    def test_simple_root_access(self, mock_set):
        mock_set.get(self.root_uri, text=_load_mock("root.json"))
        mock_set.get(
            self.root_uri+"/collections",
            text=_load_mock("collection", "example1.json"),
            complete_qs=True
        )
        collection = self.resolver.getMetadata()
        self.assertEqual(
            3, collection.size,
            "There should be 3 collections"
        )
        self.assertEqual(
            "Cartulaires", str(collection["/cartulaires"].get_label()),
            "Titles of subcollection and subcollection should be "
            "stored under their IDs"
        )
        self.assertEqual(
            "Collection Générale de l'École Nationale des Chartes",
            str(collection.get_label()),
            "Label of the main collection should be correctly parsed"
        )
        self.assertEqual(
            ["https://viaf.org/viaf/167874585", "École Nationale des Chartes"],
            sorted([
                str(obj)
                for obj in collection.metadata.get(
                    URIRef("http://purl.org/dc/terms/publisher")
                )
            ])
        )

    @requests_mock.mock()
    def test_simple_collection_access(self, mock_set):
        mock_set.get(self.root_uri, text=_load_mock("root.json"))
        mock_set.get(
            self.root_uri+"/collections?id=lasciva_roma",
            text=_load_mock("collection", "example2.json"),
            complete_qs=True
        )
        collection = self.resolver.getMetadata("lasciva_roma")
        self.assertEqual(
            1, collection.size,
            "There should be 3 collections"
        )
        self.assertEqual(
            "Priapeia", str(collection["urn:cts:latinLit:phi1103.phi001"].get_label()),
            "Titles of subcollection and subcollection should be "
            "stored under their IDs"
        )
        self.assertEqual(
            ["Thibault Clérice", "http://orcid.org/0000-0003-1852-9204"],
            sorted([
                str(obj)
                for obj in collection.metadata.get(
                    URIRef("http://purl.org/dc/terms/creator")
                )
            ])
        )

    @requests_mock.mock()
    def test_simple_collection_child_interaction(self, mock_set):
        mock_set.get(self.root_uri, text=_load_mock("root.json"))
        mock_set.get(
            self.root_uri+"/collections?id=lasciva_roma",
            text=_load_mock("collection", "example2.json"),
            complete_qs=True
        )

        collection_parent = self.resolver.getMetadata("lasciva_roma")
        collection = collection_parent.children["urn:cts:latinLit:phi1103.phi001"]

        self.assertEqual(
            {key: val for key, val in collection_parent.children.items()},
            {"urn:cts:latinLit:phi1103.phi001": collection},
            "Collections should retrieve children when retrieving metadata"
        )

        self.assertEqual(
            str(collection.metadata.get_single("http://purl.org/dc/terms/creator", lang="eng")),
            "Anonymous",
            "Unfortunately, before it's resolved, "
        )

        mock_set.get(
            self.root_uri+"/collections?id=urn:cts:latinLit:phi1103.phi001",
            text=_load_mock("collection", "example3.json"),
            complete_qs=True
        )
        collection.retrieve()

        self.assertEqual(collection.size, 1, "Size is parsed through retrieve")
        self.assertEqual(
            str(collection.metadata.get_single("http://purl.org/dc/terms/creator", lang="eng")),
            "Anonymous",
            "Metadata has been retrieved"
        )
