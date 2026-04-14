
# Step 2 — Create the project directory structure
# Run these commands to scaffold the full structure:

# Core application directories
mkdir -p backend/app/simulation/modules
mkdir -p backend/app/simulation/engine
mkdir -p backend/app/api/routes
mkdir -p backend/app/data/loaders
mkdir -p backend/tests/unit
mkdir -p backend/tests/integration
mkdir -p backend/tests/backtesting

# Frontend
mkdir -p frontend/src/components/map
mkdir -p frontend/src/components/dashboard
mkdir -p frontend/src/components/scenario
mkdir -p frontend/src/store

# Infrastructure
mkdir -p infrastructure/cdk
mkdir -p infrastructure/docker

# Documentation
mkdir -p docs/adr
mkdir -p docs/data-sources
mkdir -p docs/methodology

# GitHub configuration
mkdir -p .github/workflows
mkdir -p .github/ISSUE_TEMPLATE

# Step 3 — Create placeholder files so Git tracks the directories

# Backend
touch backend/app/__init__.py
touch backend/app/simulation/__init__.py
touch backend/app/simulation/engine/__init__.py
touch backend/app/simulation/modules/__init__.py
touch backend/app/api/__init__.py
touch backend/app/data/__init__.py
touch backend/tests/__init__.py

# Essential config files
touch backend/requirements.txt
touch backend/Dockerfile
touch frontend/.gitkeep
touch infrastructure/.gitkeep

# Step 4 — Create your .gitignore

cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*.egg-info/
.env
venv/
.venv/
*.egg

# Node
node_modules/
.next/
dist/
build/

# Environment
.env
.env.local
.env.*.local

# AWS CDK
cdk.out/
*.js.map

# Data files (large, not for version control)
*.nc
*.geojson
data/raw/

# IDE
.vscode/settings.json
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Test coverage
.coverage
htmlcov/
.pytest_cache/
EOF

# Step 5 — Write your first Architecture Decision Record

cat > docs/adr/ADR-001-simulation-core-data-model.md << 'EOF'
# ADR-001: Simulation Core Data Model

## Status
Accepted

## Date
2026-04-14

## Context
The simulation engine requires a foundational data model that represents
the entities, relationships, and state that the simulation operates on.
This model must support:
- Multiple levels of geographic resolution (country to subnational)
- Temporal state tracking across simulation timesteps
- Event propagation between interconnected entities
- Multiple measurement frameworks simultaneously (financial, human, ecological)
- Extensibility — new modules plug in without restructuring core

The data model is the most consequential early decision. It either
enables or constrains everything built on top of it.

## Decision

### Core Entity: SimulationEntity
All entities in the simulation (countries, regions, institutions) inherit
from a common base. This allows the event propagation engine to operate
uniformly regardless of entity type.

```python
class SimulationEntity:
    id: str                    # unique identifier
    entity_type: str           # 'country', 'region', 'institution'
    parent_id: Optional[str]   # for hierarchical relationships
    geometry: Optional[Geometry]  # PostGIS spatial reference
    attributes: Dict[str, float]  # current state variables
    metadata: Dict[str, Any]   # non-simulation data (name, codes, etc.)
```

### Core Structure: SimulationState
The complete state of the simulation at a single timestep.

```python
class SimulationState:
    timestep: datetime
    resolution: ResolutionConfig   # which levels are active
    entities: Dict[str, SimulationEntity]
    relationships: List[Relationship]  # trade, alliance, debt, etc.
    events: List[Event]            # events active this timestep
    scenario_config: ScenarioConfig
```

### Core Structure: Relationship
Directed relationships between entities carry the propagation weights.

```python
class Relationship:
    source_id: str
    target_id: str
    relationship_type: str     # 'trade', 'debt', 'alliance', 'currency'
    weight: float              # propagation strength
    attributes: Dict[str, float]  # relationship-specific data
```

### Core Structure: Event
Events propagate through the relationship graph each timestep.

```python
class Event:
    event_id: str
    source_entity_id: str
    event_type: str            # 'policy_change', 'shock', 'threshold_crossed'
    affected_attributes: Dict[str, float]  # what changes and by how much
    propagation_rules: List[PropagationRule]
    timestep_originated: datetime
```

### Measurement Frameworks
State variables are tagged with their measurement framework.
No conversion rates between frameworks. Outputs are parallel, not aggregated.

```python
class MeasurementFramework(Enum):
    FINANCIAL = "financial"
    HUMAN_DEVELOPMENT = "human_development"
    ECOLOGICAL = "ecological"
    GOVERNANCE = "governance"
```

### Module Interface
Every simulation module implements this interface.
Modules register with the engine. The engine calls them each timestep.

```python
class SimulationModule(ABC):
    @abstractmethod
    def compute(
        self,
        entity: SimulationEntity,
        state: SimulationState,
        timestep: datetime
    ) -> List[Event]:
        """
        Given current entity state and global simulation state,
        compute this module's contribution and return events
        to propagate.
        """
        pass

    @abstractmethod
    def get_subscribed_events(self) -> List[str]:
        """
        Which event types does this module respond to?
        """
        pass
```

## Alternatives Considered

**Relational tables only (no graph)**
Simpler to query. But relationship traversal for event propagation
becomes expensive SQL joins. The graph structure is the simulation's
core operation — it should be a first-class architectural concept,
not an emergent property of table joins.

**Single measurement framework with conversion**
Simpler outputs. But false aggregation hides exactly the information
that matters most — a country that is financially stable but in a
human development crisis looks fine in a single metric. The parallel
framework approach is non-negotiable given the project's mission.

**Agent-based from the start**
More realistic emergence. But computational cost at global scale
is prohibitive for initial build and the questions we're answering
in early milestones don't require individual-level agents.
Architecture supports adding this layer later at Level 6.

## Consequences

**Positive**
- Event propagation engine operates uniformly across all entity types
- New modules plug in by implementing SimulationModule interface
- Measurement framework separation is enforced architecturally
- Hierarchical resolution is native to the entity model
- Temporal state tracking supports backtesting naturally

**Negative**
- More abstract than a simple table-per-concept approach
- Requires discipline to maintain module interface contracts
- Graph operations require careful performance management at scale

## Next ADR
ADR-002 will address the database schema and PostGIS spatial data model.
EOF

# Step 6 — Create GitHub Issue templates

cat > .github/ISSUE_TEMPLATE/feature.md << 'EOF'
---
name: Feature
about: New simulation capability or application feature
---

## Summary
Brief description of what this adds.

## Simulation Module(s) Affected
Which modules does this touch?

## ADR Reference
Link to relevant Architecture Decision Record, or note that one is needed.

## Human Cost Ledger Impact
Does this feature affect human impact outputs? How?

## Acceptance Criteria
- [ ] Implementation matches ADR
- [ ] Unit tests written and passing
- [ ] Backtesting suite still passes
- [ ] Human cost outputs verified
- [ ] Documentation updated

## Estimated Complexity
Small / Medium / Large
EOF

cat > .github/ISSUE_TEMPLATE/backtest.md << 'EOF'
---
name: Backtesting Case
about: Add a historical case for model validation
---

## Historical Case
Country, period, event.

## Data Sources
Where does the ground truth data come from?

## Variables to Validate
Which simulation outputs should match historical record?

## Expected Fidelity
What level of match is acceptable for this case?

## Failure Mode Being Tested
Spin / Coffin Corner / Hypoxia / Backside of curve / Other
EOF

# Step 7 — Create the CI skeleton

cat > .github/workflows/ci.yml << 'EOF'
name: WorldSim CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt

      - name: Run unit tests
        run: |
          cd backend
          pytest tests/unit -v

      - name: Run integration tests
        run: |
          cd backend
          pytest tests/integration -v

      - name: Run backtesting suite
        run: |
          cd backend
          pytest tests/backtesting -v

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install linting tools
        run: pip install ruff mypy

      - name: Lint
        run: |
          cd backend
          ruff check .
          mypy app/
EOF

# Step 8 — Add initial Python requirements

cat > backend/requirements.txt << 'EOF'
# Web framework
fastapi==0.115.0
uvicorn==0.30.0

# Database
sqlalchemy==2.0.36
asyncpg==0.30.0
geoalchemy2==0.15.2
psycopg2-binary==2.9.10

# Simulation
numpy==2.1.3
pandas==2.2.3
networkx==3.4.2
xarray==2024.10.0

# Data loading
httpx==0.27.2
pydantic==2.9.2

# Testing
pytest==8.3.3
pytest-asyncio==0.24.0
pytest-cov==6.0.0

# Code quality
ruff==0.7.2
mypy==1.13.0
EOF

# Step 9 — Commit everything

git add .
git commit -m "Milestone 0: Project scaffold, ADR-001, CI skeleton, directory structure"
git push origin main

