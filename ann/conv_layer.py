from PIL import Image
import numpy as np
import theano
import pylab
from theano.tensor.nnet import conv2d
import theano.tensor as T

theano.config.floatX = 'float32'

class LeNetConvPoolLayer(object):
    """Pool Layer of a convolutional network."""

    def __init__(self, rng, input, filter_shape):
        """
        Allocate a LeNetConvPoolLayer with shared variable internal parameters.

        :type rng: np.random.RandomState
        :param rng: a random number generator used to initialize weights

        :type input: theano.tensor.dtensor4
        :param input: symbolic image tensor, of shape image_shape

        :type filter_shape: tuple or list of length 4
        :param filter_shape: (number of filters, num input feature maps,
                              filter height, filter width)

        :type image_shape: tuple or list of length 4
        :param image_shape: (batch size, num input feature maps,
                             image height, image width)

        :type poolsize: tuple or list of length 2
        :param poolsize: the downsampling (pooling) factor (#rows, #cols)
        """
        self.input = input

        # there are "num input feature maps * filter height * filter width"
        # inputs to each hidden unit
        W_bound = 1.0 / np.prod(filter_shape[1:])
        # each unit in the lower layer receives a gradient from:
        # "num output feature maps * filter height * filter width" /
        #   pooling size
        self.W = theano.shared(
            np.asarray(
                rng.uniform(low=-W_bound, high=W_bound, size=filter_shape),
                dtype=theano.config.floatX
            ),
            borrow=True
        )

        # the bias is a 1D tensor -- one bias per output feature map
        b_values = np.zeros((filter_shape[0],), dtype=theano.config.floatX)
        self.b = theano.shared(value=b_values, borrow=True)

        # convolve input feature maps with filters
        conv_out = conv2d(
            input=input,
            filters=self.W
        )

        # pool each feature map individually, using maxpooling
        # pooled_out = pool.pool_2d(
        #     input=conv_out,
        #     ds=poolsize,
        #     ignore_border=True
        # )

        # add the bias term. Since the bias is a vector (1D array), we first
        # reshape it to a tensor of shape (1, n_filters, 1, 1). Each bias will
        # thus be broadcasted across mini-batches and feature map
        # width & height
        self.output = T.tanh(conv_out + self.b.dimshuffle('x', 0, 'x', 'x'))

        # store parameters of this layer
        self.params = [self.W, self.b]

        # keep track of model input
        self.input = input


def main():
    img = Image.open("borrame/img.jpg")
    rng = np.random.RandomState(23455)

    input = T.tensor4(name="input")
    layer = LeNetConvPoolLayer(rng, input, (2, 3, 9, 9))
    layer2 = LeNetConvPoolLayer(rng, layer.output, (2, 2, 9, 9))

    foo = theano.function([input], layer2.output)
    img = np.array(img, dtype='float32')

    img_ = img.transpose(2, 0, 1).reshape(1, 3, 360, 544)
    filtered_img = foo(img_)

    # plot original image and first and second components of output
    pylab.subplot(1, 3, 1)
    pylab.axis('off')
    pylab.imshow(img)
    pylab.gray()
    # recall that the convOp output (filtered image) is actually a "minibatch",
    # of size 1 here, so we take index 0 in the first dimension:
    pylab.subplot(1, 3, 2)
    pylab.axis('off')
    pylab.imshow(filtered_img[0, 0, :, :])
    pylab.subplot(1, 3, 3)
    pylab.axis('off')
    pylab.imshow(filtered_img[0, 1, :, :])
    pylab.show()


if __name__ == "__main__":
    main()
