import os

def export_model_to_onnx(model, filepath: str, input_shape: tuple):
    """
    Export any trained model to ONNX format.
    The model must implement export_onnx().
    """
    model.export_onnx(filepath, input_shape)
    return filepath
