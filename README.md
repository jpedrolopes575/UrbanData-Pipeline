<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        @page {
            size: A4;
            margin: 15mm 12mm;
            background-color: #ffffff;
        }

        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            line-height: 1.6;
            color: #2c3e50;
            margin: 0;
            padding: 0;
            font-size: 11pt;
        }

        .header {
            background-color: #2c3e50;
            color: #ecf0f1;
            padding: 40px 30px;
            text-align: left;
            border-bottom: 6px solid #3498db;
        }

        h1 {
            margin: 0;
            font-size: 24pt;
            font-weight: 700;
        }

        .subtitle {
            font-size: 13pt;
            opacity: 0.8;
            margin-top: 10px;
        }

        .content {
            padding: 30px;
        }

        h2 {
            color: #2980b9;
            font-size: 16pt;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 5px;
            margin-top: 30px;
        }

        h3 {
            color: #34495e;
            font-size: 13pt;
            margin-top: 20px;
        }

        p {
            margin-bottom: 15px;
            text-align: justify;
        }

        ul {
            margin-bottom: 20px;
        }

        li {
            margin-bottom: 8px;
        }

        .tech-tags {
            margin: 20px 0;
        }

        .tag {
            display: inline-block;
            background: #e1f5fe;
            color: #01579b;
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 10pt;
            font-weight: bold;
            margin-right: 8px;
        }

        .info-box {
            background-color: #f8f9fa;
            border-left: 5px solid #3498db;
            padding: 20px;
            margin: 25px 0;
            font-style: italic;
        }

        .footer {
            margin-top: 50px;
            font-size: 9pt;
            color: #7f8c8d;
            text-align: center;
            border-top: 1px solid #eee;
            padding-top: 20px;
        }

        strong {
            color: #2c3e50;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Urban Mobility Data Framework</h1>
        <div class="subtitle">Computational Pipeline for Ingestion & Semantic Enrichment</div>
    </div>

    <div class="content">
        <div class="tech-tags">
            <span class="tag">Python</span>
            <span class="tag">Big Data</span>
            <span class="tag">Smart Cities</span>
            <span class="tag">Spatial Mining</span>
        </div>

        <h2>About the Project</h2>
        <p>
            This repository hosts the development and implementation of a computational <strong>framework</strong> designed to process large-scale urban mobility data from heterogeneous sources. The project focuses on building a robust <strong>data pipeline</strong> for the ingestion, cleaning, and semantic enrichment of spatial and temporal data.
        </p>
        <p>
            The ultimate goal is to enable the precise extraction of movement profiles and the identification of typical and anomalous behaviors within urban infrastructure, ensuring data integrity for predictive modeling and public management support.
        </p>

        <h2>Key Modules</h2>
        
        <h3>1. Ingestion and Quality Module</h3>
        <ul>
            <li><strong>Multimodal Collection:</strong> Aggregation of diverse datasets, including bus trajectories, ticketing data, traffic sensors, and social media records.</li>
            <li><strong>Cleaning and Filtering:</strong> Application of algorithms to remove signal noise, handle duplicate records, and correct inconsistent trajectories.</li>
            <li><strong>Standardization:</strong> Conversion of raw data into interoperable formats such as <strong>GTFS</strong> and <strong>GeoJSON</strong>.</li>
        </ul>

        <h3>2. Analysis and Patterns Module</h3>
        <ul>
            <li><strong>Semantic Enrichment:</strong> Cross-referencing movement data with Points of Interest (POIs) to identify trip contexts (e.g., work, leisure, education).</li>
            <li><strong>Flow and Profile Mining:</strong> Identification of frequent routes, mobility community detection, and the generation of O-D matrices.</li>
            <li><strong>Anomaly Detection:</strong> Development of statistical methods to identify pattern deviations, such as atypical congestion or sudden flow changes.</li>
        </ul>

        <h2>Technology Stack</h2>
        <p>
            The framework is built using industry-standard tools for data engineering:
            <strong>Languages:</strong> Python, SQL, C++. 
            <strong>Libraries:</strong> Pandas, Geopandas, Scikit-learn, Shapely.
            <strong>Formats:</strong> GeoJSON, GTFS, NoSQL.
        </p>

        <div class="info-box">
            This work is a technological initiation subproject (Bolsista CNPq ITI/A) contributing to the project: 
            "An Intelligent Framework for the Characterization, Modeling, and Prediction of Urban Mobility using Spatio-Temporal and Semantic Data".
        </div>

        <div class="footer">
            Developed by João Pedro Lopes Machado &bull; 2026
        </div>
    </div>
</body>
</html>
