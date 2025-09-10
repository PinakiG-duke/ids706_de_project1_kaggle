# ids706_de_project1_kaggle
Data Engineering multi-week assignment incorporating data import, data cleansing, exploratory analysis, predictive modelling, visualisation and evaluation
**Conceptual Workflow**
flowchart LR
  A[Ingest CSV] --> B[Clean]
  B --> C[EDA]
  C --> D[Plot]
  C --> E[Model (baseline)]
  B -->|writes| P[data/processed/*]
  C & D & E -->|write| F[artifacts/*]
  
