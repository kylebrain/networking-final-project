from .layer_base import LayerBase, BaseLayerArgs
from .link_layer import LinkLayer, LinkLayerArgs
from .networking_layer import NetworkingLayer, NetworkingLayerArgs
from .transport_layer import TransportLayer, TransportLayerArgs
from .application_layer import ApplicationLayer, ApplicationLayerArgs

from .test_layer import TestLayer, TestLayerArgs

def create_layers(layer_classes, layer_args):
    """
    Create the layers specified by the arguments

    Arguments
        layer_classes - List of LayerBase classes, starting from the lowest layer
        layer_args - List of BaseLayerArg object, must correspond with the appropriate layer in layer_classes

    Returns
        A list of the layer objects connected by above/below layer members
    """
    layers = []
    for i, layer_class in enumerate(layer_classes):
        if not issubclass(layer_class, LayerBase):
            raise ValueError("Layer class: %s does not inherent from LayerBase" % (layer_class, ))

        layer_arg = layer_args[i]

        if not isinstance(layer_arg, BaseLayerArgs):
            raise ValueError("Layer args class: %s does not inherent from BaseLayerArgs" % (type(layer_arg), ))
        layer = layer_class(i, layer_arg)
        if i > 0:
            layer.below_layer = layers[i-1]
            layers[i-1].above_layer = layer
        layers.append(layer)
    return layers