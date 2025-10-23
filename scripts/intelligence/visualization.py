#!/usr/bin/env python3
"""
Intelligence Visualization Layer - Making Data Come Alive

This creates interactive visualizations for the intelligence reports:
1. Trend velocity charts (time series)
2. Topic co-occurrence networks (force-directed graphs)
3. Influence maps (network graphs with PageRank sizing)
4. Cross-platform correlation matrices (heatmaps)
5. Sentiment flow diagrams (Sankey diagrams)
6. Geographic distribution maps (if location data available)

Uses Plotly for interactive, embeddable visualizations.
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import networkx as nx
import numpy as np
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from collections import defaultdict


class IntelligenceVisualizer:
    """
    Creates publication-ready interactive visualizations
    for intelligence reports.
    """
    
    def __init__(self, dark_mode: bool = True):
        self.dark_mode = dark_mode
        
        # Color schemes
        self.colors = {
            'primary': '#FFA500' if not dark_mode else '#FFB733',  # Amber
            'secondary': '#DC143C' if not dark_mode else '#E94B6B',  # Crimson
            'background': '#0f0f0f' if dark_mode else '#ffffff',
            'text': '#ffffff' if dark_mode else '#000000',
            'grid': '#333333' if dark_mode else '#e0e0e0'
        }
        
        # Default layout
        self.default_layout = {
            'paper_bgcolor': self.colors['background'],
            'plot_bgcolor': self.colors['background'],
            'font': {'color': self.colors['text'], 'family': 'Arial, sans-serif'},
            'xaxis': {'gridcolor': self.colors['grid']},
            'yaxis': {'gridcolor': self.colors['grid']},
            'hovermode': 'closest'
        }
    
    def create_trend_velocity_chart(
        self,
        trends: List[Dict],
        title: str = "Emerging Trends - Velocity Analysis"
    ) -> go.Figure:
        """
        Create interactive trend velocity chart showing:
        - Trend velocity (signals per hour)
        - Acceleration (change in velocity)
        - Platform diversity
        """
        
        # Extract data
        topics = [t['topic'] for t in trends]
        velocities = [t['velocity'] for t in trends]
        accelerations = [t.get('acceleration', 0) for t in trends]
        platforms = [t['platforms'] for t in trends]
        
        # Create figure with secondary y-axis
        fig = make_subplots(
            rows=1, cols=1,
            specs=[[{"secondary_y": True}]]
        )
        
        # Add velocity bars
        fig.add_trace(
            go.Bar(
                x=topics,
                y=velocities,
                name='Velocity (signals/hr)',
                marker_color=self.colors['primary'],
                hovertemplate='<b>%{x}</b><br>Velocity: %{y:.2f} signals/hr<extra></extra>'
            ),
            secondary_y=False
        )
        
        # Add acceleration line
        fig.add_trace(
            go.Scatter(
                x=topics,
                y=accelerations,
                name='Acceleration',
                mode='lines+markers',
                line=dict(color=self.colors['secondary'], width=3),
                marker=dict(size=10),
                hovertemplate='<b>%{x}</b><br>Acceleration: %{y:.2f}<extra></extra>'
            ),
            secondary_y=True
        )
        
        # Add platform diversity as marker size
        fig.add_trace(
            go.Scatter(
                x=topics,
                y=velocities,
                name='Platform Diversity',
                mode='markers',
                marker=dict(
                    size=[p * 10 for p in platforms],
                    color=self.colors['secondary'],
                    opacity=0.5,
                    line=dict(width=2, color='white')
                ),
                hovertemplate='<b>%{x}</b><br>Platforms: %{marker.size}<extra></extra>',
                showlegend=False
            ),
            secondary_y=False
        )
        
        # Update layout
        fig.update_layout(
            title=title,
            xaxis_title="Topic",
            **self.default_layout
        )
        
        fig.update_yaxes(title_text="Velocity (signals/hr)", secondary_y=False)
        fig.update_yaxes(title_text="Acceleration", secondary_y=True)
        
        return fig
    
    def create_topic_network(
        self,
        topic_graph: nx.Graph,
        title: str = "Topic Co-occurrence Network"
    ) -> go.Figure:
        """
        Create interactive force-directed graph of topic relationships.
        
        Node size = topic frequency
        Edge width = co-occurrence strength
        """
        
        # Get positions using spring layout
        pos = nx.spring_layout(topic_graph, k=0.5, iterations=50)
        
        # Create edge traces
        edge_traces = []
        for edge in topic_graph.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            
            weight = topic_graph[edge[0]][edge[1]].get('weight', 1)
            
            edge_trace = go.Scatter(
                x=[x0, x1, None],
                y=[y0, y1, None],
                mode='lines',
                line=dict(width=weight * 2, color=self.colors['grid']),
                hoverinfo='none',
                showlegend=False
            )
            edge_traces.append(edge_trace)
        
        # Create node trace
        node_x = []
        node_y = []
        node_text = []
        node_size = []
        
        for node in topic_graph.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            
            count = topic_graph.nodes[node].get('count', 1)
            node_size.append(count * 5)
            
            # Hover text
            connections = list(topic_graph.neighbors(node))
            hover_text = f"<b>{node}</b><br>Mentions: {count}<br>Related: {', '.join(connections[:3])}"
            node_text.append(hover_text)
        
        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            mode='markers+text',
            text=[node for node in topic_graph.nodes()],
            textposition='top center',
            hovertext=node_text,
            hoverinfo='text',
            marker=dict(
                size=node_size,
                color=self.colors['primary'],
                line=dict(width=2, color='white')
            ),
            showlegend=False
        )
        
        # Create figure
        fig = go.Figure(data=edge_traces + [node_trace])
        
        fig.update_layout(
            title=title,
            showlegend=False,
            hovermode='closest',
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            **self.default_layout
        )
        
        return fig
    
    def create_influence_map(
        self,
        user_graph: nx.DiGraph,
        top_n: int = 20,
        title: str = "Influence Network Map"
    ) -> go.Figure:
        """
        Create influence network with PageRank-sized nodes.
        
        Shows who influences whom in the AI/ML community.
        """
        
        # Compute PageRank
        pagerank = nx.pagerank(user_graph)
        
        # Get top N users
        top_users = sorted(pagerank.items(), key=lambda x: x[1], reverse=True)[:top_n]
        top_user_names = [u[0] for u in top_users]
        
        # Create subgraph
        subgraph = user_graph.subgraph(top_user_names)
        
        # Get positions
        pos = nx.spring_layout(subgraph, k=1, iterations=50)
        
        # Create edge traces
        edge_traces = []
        for edge in subgraph.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            
            edge_trace = go.Scatter(
                x=[x0, x1, None],
                y=[y0, y1, None],
                mode='lines',
                line=dict(width=1, color=self.colors['grid']),
                hoverinfo='none',
                showlegend=False,
                opacity=0.5
            )
            edge_traces.append(edge_trace)
        
        # Create node trace
        node_x = []
        node_y = []
        node_text = []
        node_size = []
        node_color = []
        
        for node in subgraph.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            
            pr = pagerank[node]
            node_size.append(pr * 10000)  # Scale for visibility
            
            # Color by influence
            node_color.append(pr)
            
            # Hover text
            out_degree = subgraph.out_degree(node)
            in_degree = subgraph.in_degree(node)
            hover_text = f"<b>{node}</b><br>Influence: {pr:.4f}<br>Influences: {out_degree}<br>Influenced by: {in_degree}"
            node_text.append(hover_text)
        
        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            mode='markers+text',
            text=[node[:15] for node in subgraph.nodes()],  # Truncate long names
            textposition='top center',
            hovertext=node_text,
            hoverinfo='text',
            marker=dict(
                size=node_size,
                color=node_color,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Influence"),
                line=dict(width=2, color='white')
            ),
            showlegend=False
        )
        
        # Create figure
        fig = go.Figure(data=edge_traces + [node_trace])
        
        fig.update_layout(
            title=title,
            showlegend=False,
            hovermode='closest',
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            **self.default_layout
        )
        
        return fig
    
    def create_platform_correlation_matrix(
        self,
        cross_platform_stories: List[Dict],
        title: str = "Cross-Platform Story Correlation"
    ) -> go.Figure:
        """
        Create heatmap showing which platforms share stories.
        """
        
        # Build platform co-occurrence matrix
        platforms = set()
        for story in cross_platform_stories:
            platforms.update(story['platforms'])
        
        platforms = sorted(list(platforms))
        n = len(platforms)
        
        # Initialize matrix
        matrix = np.zeros((n, n))
        
        # Fill matrix
        for story in cross_platform_stories:
            story_platforms = story['platforms']
            for i, p1 in enumerate(platforms):
                for j, p2 in enumerate(platforms):
                    if p1 in story_platforms and p2 in story_platforms:
                        matrix[i][j] += 1
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=matrix,
            x=platforms,
            y=platforms,
            colorscale='Viridis',
            hovertemplate='%{y} ↔ %{x}<br>Shared stories: %{z}<extra></extra>'
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Platform",
            yaxis_title="Platform",
            **self.default_layout
        )
        
        return fig
    
    def create_engagement_timeline(
        self,
        signals: List,
        title: str = "Engagement Timeline"
    ) -> go.Figure:
        """
        Create timeline showing engagement over time.
        """
        
        # Group signals by hour
        hourly_data = defaultdict(lambda: {'count': 0, 'engagement': 0})
        
        for signal in signals:
            hour = signal.timestamp.replace(minute=0, second=0, microsecond=0)
            hourly_data[hour]['count'] += 1
            hourly_data[hour]['engagement'] += sum(signal.engagement.values())
        
        # Sort by time
        times = sorted(hourly_data.keys())
        counts = [hourly_data[t]['count'] for t in times]
        engagements = [hourly_data[t]['engagement'] for t in times]
        
        # Create figure
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Add signal count
        fig.add_trace(
            go.Bar(
                x=times,
                y=counts,
                name='Signal Count',
                marker_color=self.colors['primary']
            ),
            secondary_y=False
        )
        
        # Add engagement
        fig.add_trace(
            go.Scatter(
                x=times,
                y=engagements,
                name='Total Engagement',
                mode='lines+markers',
                line=dict(color=self.colors['secondary'], width=3)
            ),
            secondary_y=True
        )
        
        fig.update_layout(
            title=title,
            xaxis_title="Time",
            **self.default_layout
        )
        
        fig.update_yaxes(title_text="Signal Count", secondary_y=False)
        fig.update_yaxes(title_text="Engagement", secondary_y=True)
        
        return fig
    
    def save_all_visualizations(
        self,
        intelligence_data: Dict,
        output_dir: str = "visualizations"
    ) -> Dict[str, str]:
        """
        Generate and save all visualizations.
        
        Returns dict mapping visualization type to file path.
        """
        
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        saved_files = {}
        
        # 1. Trend velocity chart
        if 'emerging_trends' in intelligence_data:
            fig = self.create_trend_velocity_chart(intelligence_data['emerging_trends'])
            path = os.path.join(output_dir, 'trend_velocity.html')
            fig.write_html(path)
            saved_files['trend_velocity'] = path
        
        # 2. Topic network
        if 'topic_graph' in intelligence_data:
            fig = self.create_topic_network(intelligence_data['topic_graph'])
            path = os.path.join(output_dir, 'topic_network.html')
            fig.write_html(path)
            saved_files['topic_network'] = path
        
        # 3. Influence map
        if 'user_graph' in intelligence_data:
            fig = self.create_influence_map(intelligence_data['user_graph'])
            path = os.path.join(output_dir, 'influence_map.html')
            fig.write_html(path)
            saved_files['influence_map'] = path
        
        # 4. Platform correlation
        if 'cross_platform_stories' in intelligence_data:
            fig = self.create_platform_correlation_matrix(intelligence_data['cross_platform_stories'])
            path = os.path.join(output_dir, 'platform_correlation.html')
            fig.write_html(path)
            saved_files['platform_correlation'] = path
        
        # 5. Engagement timeline
        if 'signals' in intelligence_data:
            fig = self.create_engagement_timeline(intelligence_data['signals'])
            path = os.path.join(output_dir, 'engagement_timeline.html')
            fig.write_html(path)
            saved_files['engagement_timeline'] = path
        
        return saved_files

