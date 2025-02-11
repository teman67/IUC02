import networkx as nx
import holoviews as hv
from holoviews.operation.datashader import bundle_graph
hv.extension('bokeh')

G = nx.karate_club_graph()
hv_graph = hv.Graph.from_networkx(G, nx.layout.spring_layout).opts(tools=['hover'], node_size=10)
bundled = bundle_graph(hv_graph)

bundled.opts(width=800, height=600)
