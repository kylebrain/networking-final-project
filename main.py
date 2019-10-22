from layers.test_layer import TestLayer
import time

def main():
    top_layer = TestLayer(TestLayer, None, 5)

    for _ in range(2):
        top_layer.out_buffer.put(7)

    for _ in range(2):
        msg = top_layer.in_buffer.get()
        print("Top layer found: %d" % (msg, ))


if __name__ == '__main__':
    main()