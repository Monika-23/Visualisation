import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QSpinBox,QMainWindow,QComboBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5 import QtCore
import plotly.graph_objs as go
import json
import networkx as nx
import plotly.offline as pyo

class HTMLViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('HTML Viewer')
        self.setGeometry(100, 100, 800, 800)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Create a QWebEngineView to display HTML content
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)
        
        self.web_view.setFixedSize(1900, 700)
        
        
        
        subset_label = QLabel('Select subset size:')
        self.subset_spinbox = QSpinBox()
        self.subset_spinbox.setMinimum(1)
        self.subset_spinbox.setMaximum(3000)
        self.subset_spinbox.setValue(100)  # Default value
        
        
        
        
        
        node_label = QLabel('Select highlighted node:')
        self.node_combobox = QComboBox()
        self.node_combobox.addItems([
            'Spanish Shrimp  Carriers',
            '8561',
            'Jacob Caldwell',
            '8327'
        ]) 
        
        subset_button = QPushButton('Display Graph')
        subset_button.clicked.connect(self.showGraph)
        
        layout.addWidget(subset_label)
        layout.addWidget(self.subset_spinbox)
        layout.addWidget(node_label)
        layout.addWidget(self.node_combobox)
        
        layout.addWidget(subset_button)
        
        
        
        
        
        
    def showGraph(self):
        import json
        import networkx as nx
        import plotly.graph_objs as go

        # Load JSON file
        with open('MC1.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Create a graph
        G = nx.Graph()

        # Add nodes and edges from JSON data
        for node in data['nodes']:
            G.add_node(node['id'])

        for edge in data['links']:
            G.add_edge(edge['source'], edge['target'], weight=edge['weight'])

        # Set maximum number of nodes to display
        max_nodes =self.subset_spinbox.value()  # Adjust this number as needed

        # Subsample the graph
        sub_nodes = list(G.nodes())[:max_nodes]
        sub_G = G.subgraph(sub_nodes)

        # Generate layout for the subsampled graph
        sub_pos = nx.spring_layout(sub_G)

        # Create edges trace
        edge_trace = go.Scatter(
            x=[],
            y=[],
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')

        for edge in sub_G.edges():
            x0, y0 = sub_pos[edge[0]]
            x1, y1 = sub_pos[edge[1]]
            edge_trace['x'] += tuple([x0, x1, None])
            edge_trace['y'] += tuple([y0, y1, None])

        # Create figure
        fig = go.Figure(layout=go.Layout(
                            title='Interactive Force-Directed Graph (Subsampled)',
                            titlefont=dict(size=16),
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=20, l=5, r=5, t=40),
                            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                        )

        # Loop through nodes to assign colors and sizes and display the graph for each node
        for node in sub_G.nodes():
            # Create nodes trace with interactive dragging
            node_trace = go.Scatter(
                x=[sub_pos[node][0]],
                y=[sub_pos[node][1]],
                text=[node],  # Add node ID as label
                mode='markers+text',
                hoverinfo='text',
                marker=dict(
                    showscale=True,
                    colorscale='YlGnBu',
                    color='blue',  # Default color
                    size=10,  # Default size
                    colorbar=dict(
                        thickness=15,
                        title='Node Connections',
                        xanchor='left',
                        titleside='right'
                    ),
                    line=dict(width=2)),
                textposition='bottom center')

            # Assign color and size for the current node
            if str(node) == self.node_combobox.currentText():
                node_trace['marker']['color'] = 'red'  # Color for highlighted node
                node_trace['marker']['size'] = 50  # Larger size for highlighted node

            # Add edges and nodes trace to the figure
            fig.add_trace(edge_trace)
            fig.add_trace(node_trace)

            # Display the updated graph for the current node
        fig.show()
        pyo.plot(fig, filename='temp_graph.html', auto_open=False)
        import os
        file_path = os.path.join(os.getcwd(), "temp_graph.html")

        # Load an HTML file
        self.loadHTMLFile(file_path)

    def loadHTMLFile(self, file_path):
        # Load the HTML file into the QWebEngineView
        self.web_view.setUrl(QtCore.QUrl.fromLocalFile(file_path))

def main():
    app = QApplication(sys.argv)
    viewer = HTMLViewer()
    viewer.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
