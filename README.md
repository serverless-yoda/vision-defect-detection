
# Azure Vision Defect Detection Portal

A FastAPI-based microservice that analyzes images for defects using Azure Cognitive Services and stores results in a Microsoft Fabric-connected SQL database.

---

## 📁 Folder Structure
| Folder/File | Purpose |
|-------------|---------|
| `main.py` | Entry point of the application. Registers middleware, routes, and exception handlers. |
| `/api/v1/vision_routes.py` | Defines the `/inspect` endpoint for image analysis. |
| `/api/middleware.py` | Custom middleware for rate limiting, correlation ID, and request logging. |
| `/application/dto/` | Contains DTOs for request (`ImageRequestDTO`) and response (`DefectResultDTO`). |
| `/application/services/vision_service.py` | Business logic for image inspection. Connects DTOs, analyzer, and repository. |
| `/common/config.py` | Loads environment variables using `pydantic-settings`. |
| `/common/error_handlers.py` | Custom error handler for `VisionAnalysisError`. |
| `/common/logging.py` | Logging setup with correlation ID support. |
| `/domain/contracts/` | Interfaces for `IVisionAnalyzer` and `IFabricRepository`. |
| `/domain/entities/defect_result.py` | Domain model representing defect analysis result. |
| `/domain/exceptions.py` | Custom exceptions for vision and repository errors. |
| `/infrastructure/azure_vision_analyzer.py` | Azure Vision API integration. Implements `IVisionAnalyzer`. |
| `/infrastructure/fabric_repository.py` | SQL persistence layer. Implements `IFabricRepository`. |
| `/tests/unit/test_vision_service.py` | Unit test for `VisionService` using mock analyzer and repository. |
| `requirements.txt` | Project dependencies. |

---

## 🏗️ Architectural Design
### Layered Architecture
- **API Layer**: Routes and middleware (`vision_routes.py`, `middleware.py`)
- **Application Layer**: DTOs and services (`dto/`, `vision_service.py`)
- **Domain Layer**: Contracts, entities, exceptions (`contracts/`, `entities/`, `exceptions.py`)
- **Infrastructure Layer**: Azure and Fabric integrations (`azure_vision_analyzer.py`, `fabric_repository.py`)
- **Common Layer**: Config, logging, error handling (`config.py`, `logging.py`, `error_handlers.py`)

### Design Principles
- **Separation of Concerns**: Each layer has a distinct responsibility.
- **Dependency Injection**: Services receive analyzers and repositories via constructor injection.
- **Interface-Oriented Design**: Infrastructure classes implement domain contracts.

---

## 🧠 Code Responsibilities
| Component | Responsibility |
|----------|----------------|
| `VisionService` | Decodes image, analyzes defects, saves results, returns DTO. |
| `Routes` | Accepts request, injects service, returns response. |
| `DTOs` | Validate and serialize request/response data. |
| `Middleware` | Logs requests, limits rate, assigns correlation ID. |
| `Error Handlers` | Catch and format domain-specific exceptions. |

---

## 🔁 Request Flow: `/inspect`
1. **Client** sends POST `/api/v1/inspect` with base64 image.
2. **FastAPI** validates with `ImageRequestDTO`.
3. **VisionService**:
   - Decodes image
   - Calls `AzureVisionAnalyzer`
   - Gets `DefectResult`
   - (Optionally) saves to `FabricRepository`
   - Returns `DefectResultDTO`
4. **Response** sent to client with defect status and probabilities.

---

## 📦 Important Packages
| Package | Purpose |
|--------|---------|
| `fastapi`, `starlette` | Web framework and middleware support. |
| `pydantic`, `pydantic-settings` | Data validation and config management. |
| `httpx`, `aiohttp` | Async HTTP clients for Azure API. |
| `azure.identity`, `azure.keyvault.secrets` | Azure authentication and secret retrieval. |
| `pyodbc` | SQL database connectivity. |
| `pytest`, `pytest-asyncio` | Async unit testing. |

---



## ✅ How to Run
```bash
uvicorn main:app --reload --port 8000
```

---

## 🧪 How to Test
```bash
pytest tests/unit/test_vision_service.py
```

---

## 📜 License
MIT
