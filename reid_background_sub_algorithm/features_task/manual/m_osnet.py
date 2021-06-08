from torch import nn

from torchreid.models.osnet import OSNet, Conv1x1, ConvLayer, OSBlock


class MultichannelOSNet(OSNet):
    def __init__(self, num_classes, blocks, layers, channels, in_channels=3, feature_dim=512, loss='softmax', IN=False,
                 **kwargs):
        super(OSNet, self).__init__()
        num_blocks = len(blocks)
        assert num_blocks == len(layers)
        assert num_blocks == len(channels) - 1
        self.loss = loss

        # convolutional backbone
        self.conv1 = ConvLayer(in_channels, channels[0], 7, stride=2, padding=3, IN=IN)
        self.maxpool = nn.MaxPool2d(3, stride=2, padding=1)
        self.conv2 = self._make_layer(blocks[0], layers[0], channels[0], channels[1], reduce_spatial_size=True, IN=IN)
        self.conv3 = self._make_layer(blocks[1], layers[1], channels[1], channels[2], reduce_spatial_size=True)
        self.conv4 = self._make_layer(blocks[2], layers[2], channels[2], channels[3], reduce_spatial_size=False)
        self.conv5 = Conv1x1(channels[3], channels[3])
        self.global_avgpool = nn.AdaptiveAvgPool2d(1)
        # fully connected layer
        self.fc = self._construct_fc_layer(feature_dim, channels[3], dropout_p=None)
        # identity classification layer
        self.classifier = nn.Linear(self.feature_dim, num_classes)

        self._init_params()


def osnet_x0_25(num_classes=1000, loss='softmax', in_channels=3, **kwargs):
    # very tiny size (width x0.25)
    model = MultichannelOSNet(num_classes, blocks=[OSBlock, OSBlock, OSBlock],
                              layers=[2, 2, 2], channels=[16, 64, 96, 128],
                              in_channels=in_channels, loss=loss, **kwargs)


