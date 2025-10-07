# VISPILS Backend

A Flask-based REST API for ionic liquid property prediction and molecular visualization.

## 🏗️ Architecture

```
backend/
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── data/              # Data files (referenced from parent)
    └── vispils-v1.csv # Ionic liquid database
```

## 🚀 Quick Start

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the server:**

   ```bash
   python app.py
   ```

3. **Access the API:**
   - Frontend: http://localhost:5001
   - API Base URL: http://localhost:5001/api

## 📋 API Endpoints

### 1. Home Page

- **GET** `/`
- **Description:** Main landing page
- **Response:** HTML template

### 2. Selection Handler

- **POST** `/api/selection`
- **Description:** Handle ionic liquid component selection
- **Content-Type:** `application/json`

**Request Body:**

```json
{
  "select-cfams": "family_name" | "select-afams": "family_name" | "select-cations": "smiles" | "select-anions": "smiles"
}
```

**Response:**

```json
{
  "success": true,
  "candidates": [
    {
      "smiles": "CCn1cc[n+](C)c1",
      "image_url": "data:image/png;base64,..."
    }
  ],
  "count": 5
}
```

### 3. Ionic Liquid Creation

- **POST** `/api/ionic-liquid`
- **Description:** Create ionic liquid from selected cation and anion
- **Content-Type:** `application/json`

**Request Body:**

```json
{
  "select-cations": "cation_smiles",
  "select-anions": "anion_smiles"
}
```

**Response:**

```json
{
  "success": true,
  "ionic_liquid": {
    "smiles": "cation.anion",
    "cation": "cation_smiles",
    "anion": "anion_smiles",
    "molfile_3d": "3D MOL file content"
  }
}
```

### 4. Property Prediction

- **POST** `/api/predict`
- **Description:** Predict ionic liquid properties
- **Content-Type:** `application/x-www-form-urlencoded`

**Form Data:**

- `SMILES_input`: Ionic liquid SMILES
- `Temperature_input`: Temperature in Kelvin

**Response:**

```json
{
  "success": true,
  "prediction": {
    "output": ["smiles", "viscosity", "temperature", "source", "prediction"],
    "prediction_text": "η = 45.2 mPas at 298.15 K"
  }
}
```

## 🔧 Configuration

### Environment Variables

- `FLASK_ENV`: Set to `development` for debug mode
- `FLASK_DEBUG`: Set to `1` for auto-reload

### Data Files

The application expects the following data structure:

```
data/
└── vispils-v1.csv     # Main ionic liquid database
```

## 🧪 Testing

Run tests with pytest:

```bash
pytest tests/
```

## 📊 Data Structure

### VISPILS Database Schema

- `cSMILES`: Cation SMILES
- `aSMILES`: Anion SMILES
- `cfam1`: Cation family
- `afam1`: Anion family
- `cfam_class`: Cation family class
- `afam_class`: Anion family class
- `Iso SMILES`: Isomeric SMILES
- `Log viscosity`: Log of viscosity
- `Temperature`: Temperature in Kelvin
- `DataSource`: Data source
- `GC Pred.`: Graph convolutional prediction

## 🔍 Error Handling

The API returns consistent error responses:

```json
{
  "error": "Error message",
  "success": false
}
```

**HTTP Status Codes:**

- `200`: Success
- `400`: Bad Request (invalid input)
- `404`: Not Found
- `500`: Internal Server Error

## 🛠️ Development

### Code Organization

- **Utility Functions:** Molecular conversion, data loading
- **Routes:** API endpoints with proper error handling
- **Error Handlers:** Global error management
- **Configuration:** App setup and initialization

### Adding New Features

1. Add utility functions in the appropriate section
2. Create new routes with proper documentation
3. Add error handling for new endpoints
4. Update this README

## 🚀 Production Deployment

For production deployment:

1. **Install production dependencies:**

   ```bash
   pip install gunicorn redis
   ```

2. **Set environment variables:**

   ```bash
   export FLASK_ENV=production
   export FLASK_DEBUG=0
   ```

3. **Run with Gunicorn:**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5001 app:app
   ```

## 📝 TODO

- [ ] Add ML prediction modules
- [ ] Implement caching with Redis
- [ ] Add authentication
- [ ] Add rate limiting
- [ ] Add comprehensive logging
- [ ] Add API versioning
- [ ] Add OpenAPI/Swagger documentation

## 🤝 Contributing

1. Follow the existing code structure
2. Add proper error handling
3. Include docstrings for all functions
4. Update this README for new features
5. Test thoroughly before submitting

## 📄 License

This project is part of the VISPILS ionic liquid research platform.
