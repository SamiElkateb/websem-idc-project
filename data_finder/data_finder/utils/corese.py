import atexit
import subprocess
from time import sleep

from py4j.java_gateway import JavaGateway

# Start java gateway
java_process = subprocess.Popen(
    ["java", "-jar", "-Dfile.encoding=UTF-8", "data_finder/corese-library-python-4.5.0.jar"]
)
sleep(1)
gateway = JavaGateway()


def exit_handler():
    # Stop java gateway at the enf od script
    gateway.shutdown()
    print("\n" * 2)
    print("Gateway Server Stop!")


atexit.register(exit_handler)

# Import of class
Graph = gateway.jvm.fr.inria.corese.core.Graph
Load = gateway.jvm.fr.inria.corese.core.load.Load
Transformer = gateway.jvm.fr.inria.corese.core.transform.Transformer
QueryProcess = gateway.jvm.fr.inria.corese.core.query.QueryProcess
RDF = gateway.jvm.fr.inria.corese.core.logic.RDF


def export_to_file(graph, format, path):
    """Export a graph to a file

    :param graph: graph to export
    :param format: format of export
    :param path: path of the exported file
    """
    transformer = Transformer.create(graph, format)
    transformer.write(path)


def load(path):
    """Load a graph from a local file or a URL

    :param path: local path or a URL
    :returns: the graph load
    """
    graph = Graph()

    ld = Load.create(graph)
    ld.parse(path)

    return graph

def sparql_query(graph, query):
    """Run a query on a graph

    :param graph: the graph on which the query is executed
    :param query: query to run
    :returns: query result
    """
    exec = QueryProcess.create(graph)
    return exec.query(query)
