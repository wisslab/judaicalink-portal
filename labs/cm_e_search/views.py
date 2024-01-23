import logging
import html
from django.shortcuts import render
from django.http import HttpResponse
import pysolr
import math, json, pprint
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.core.cache.backends.base import DEFAULT_TIMEOUT

logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
SOLR_SERVER = settings.SOLR_SERVER


def get_names():
    """
    This function gets all the names from the solr index cm_entity_names
    :return:
    """
    # gets all entity names from solr
    try:
        names = []

        solr = pysolr.Solr(SOLR_SERVER + "cm_entity_names", always_commit=True, timeout=10,
                           auth=(settings.SOLR_USER, settings.SOLR_PASSWORD))
        res = solr.search('*:*', index="cm_entity_names", rows=10000)

        # logging
        logger.info("Got names from solr: ")
        logger.debug("Names found: ", res.hits)
        logger.info(res.debug)
        logger.info(res.hits)

        for doc in res.docs:
            # convert list to string
            doc['name'] = ''.join(map(str, doc['name']))
            names.append(doc['name'])
            logger.debug("Doc: ", doc['name'])
            logger.info(doc['name'])
        return names

    except Exception as e:
        logger.error("Error:", e)
        print("Error:", e)
        return None
    except pysolr.SolrError as e:
        logger.error("Error:", e)
        print("Error:", e)
        return None


#@cache_page(CACHE_TTL)
def index(request):
    names = get_names()
    data = names
    context = {'data': data}
    return render(request, 'cm_e_search/search_index.html', context)


@cache_page(CACHE_TTL)
def result(request):
    names = get_names()  # searches for all names in cm_entity_names
    logger.debug("Got names from solr: ")
    logger.debug(names)

    query = request.GET.get('query')
    logger.info("Query: " + query)
    print("Query: " + query)
    # add name: to query

    solr = pysolr.Solr(settings.SOLR_SERVER + 'cm_entities', always_commit=True, timeout=10,
                       auth=(settings.SOLR_USER, settings.SOLR_PASSWORD))

    fields = ["name", "e_type", "related_entities", 'ep', 'id', 'journal_occurs.j_name', 'journal_occurs.j_id',
              'journal_occurs.first', 'journal_occurs.last', 'journal_occurs.mentions.p_id',
              'journal_occurs.mentions.spot', 'journal_occurs.mentions.start', 'journal_occurs.mentions.end',
              'journal_occurs.mentions.p_link', 'journal_occurs.mentions.date', 'journal_occurs.mentions.year']
    search_fields = ["name", "journal_occurs.mentions.spot"]

    # create a dict from the fields and add the query
    # create a list for the fields that should be searched and add the query
    solr_query = [field + ":" + query for field in search_fields]

    # build the body for solr
    body = {
        "hl": "false",
        "indent": "true",
        'fl': ','.join(fields),
        "start": 0,
        "q.op": "OR",
        "rows": 1000,
        "useParams": ""
    }

    res = solr.search(q=solr_query, search_handler="/select", **body)

    logger.debug("Results found: ", res.hits)
    logger.debug("Got results from solr: ")
    logger.debug(res.docs)

    results = []
    for doc in res.docs:
        results.append(doc)
        doc['name'] = ''.join(map(str, doc['name']))
        doc['e_type'] = ''.join(map(str, doc['e_type']))
        if 'ep' in doc:
            doc['ep'] = ''.join(map(str, doc['ep']))
        else:
            doc['ep'] = ''

        print("Name: ", doc['name'])

        # create a dict for the related entities
        if 'related_entities' in doc:
            print("Related entities: ", len(doc['related_entities']))
            related_entities = []
            entity = {}
            for index in range(0, len(doc['related_entities']), 4):
                if index + 3 < len(doc['related_entities']):
                    # entity is a list with 4 elements
                    # 0: ep
                    # 1: name
                    # 2: score
                    # 3: type
                    entity['ep'] = doc['related_entities'][index]
                    entity['name'] = doc['related_entities'][index + 1]
                    entity['score'] = doc['related_entities'][index + 2]
                    entity['type'] = doc['related_entities'][index + 3]

                    print("Entity: ", entity)
                    related_entities.append(entity)
                    entity = {}
            doc['related_entities'] = related_entities
        else:
            doc['related_entities'] = []

    # print("Results: ", results)
    context = {
        "results": results,
        "data": json.dumps(names)
    }

    return render(request, 'cm_e_search/search_result.html', context)


def create_map(result):
    # creates a map from locations
    locations = []
    for r in result:
        if r.e_type == 'LOC':
            locations.append(r.name)
    pass


def create_timeline():
    pass


def create_graph_visualization():
    pass
