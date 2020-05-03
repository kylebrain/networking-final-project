from .layer_base import LayerBase, BaseLayerArgs
from .link_layer import LinkLayer, LinkLayerArgs
from .networking_layer import NetworkingLayer, NetworkingLayerArgs
from .transport_layer import TransportLayer, TransportLayerArgs
from .application_layer import ApplicationLayer, ApplicationLayerArgs
from .test_top_layer import TestTopLayer, TestTopLayerArgs

def create_layers(simulation_mng, metric_mng, node_data, layer_classes, layer_args):
    """
    Create the layers specified by the arguments

    Arguments
        simulation_mng - used to stop the simulation when a node goes offline
        metric_mng - used to keep track of loss and delay
        note_data - initialized node data including ID and battery life
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
        layer = layer_class(simulation_mng, metric_mng, node_data, i, layer_arg)
        if i > 0:
            layer.below_layer = layers[i-1]
            layers[i-1].above_layer = layer
        layers.append(layer)
    return layers
