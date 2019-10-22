from test_layer import TestLayer
import time

def main():
    top_layer = TestLayer(TestLayer, None, 5)
    top_layer.out_buffer.put(7)
    time.sleep(1)

if __name__ == '__main__':
    main()