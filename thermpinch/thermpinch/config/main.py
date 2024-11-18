STORE_ID = "thermpinch" + "_store"
PROJECT_NAME = "thermpinch".replace("_", " ").title()
PROJECT_SLUG = "thermpinch"

CONFIG_SIDEBAR = {
    "logo_path": "/thermpinch/assets/logo_horizontal.png",
    "sidenav_title": "STEPS",
    "nav_items": [
        {"name": "Start", "path": "ta-start"},
        {"name": "Data Collection", "path": "ta-data"},
        {"name": "Pinch Point Temperature ", "path": "ta-pinchet"},
        {"name": "Temperature Interval Diagram", "path": "ta-tid"},
        {"name": "Problem Table", "path": "ta-ptable"},
        {"name": "Heat Cascade and Utility ", "path": "ta-hcas"},
        {
            "name": "The Shifted Temperature-Enthalpy Composite Diagram ",
            "path": "ta-stec",
        },
        {"name": "The Temperature-Enthalpy Composite Diagram", "path": "ta-tecd"},
        {"name": "The Grand Composite Curve", "path": "ta-gcc"},
        {"name": "Report", "path": "ta-report"},
    ],
}
