from setuptools import setup, find_packages

setup(
    name="amip",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy", "pandas", "scikit-learn", "xgboost", "lightgbm",
        "torch", "onnx", "onnxruntime", "psycopg2-binary", "sqlalchemy",
        "hdbscan", "matplotlib", "seaborn", "ta", "scipy", "joblib"
    ],
    author="AMIP ML Team",
    description="Python ML pipeline for AI Market Intelligence Platform",
)
