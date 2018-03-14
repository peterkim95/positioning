import numpy as np

import torch
from torch.autograd import Variable

from model import RNN
from utils import *

def eval_model(rnn, data_loader):
    # Test the Model
    correct, total = 0, 0
    for batch_X, batch_y in data_loader:
        points = Variable(torch.from_numpy(batch_X))
        labels = torch.from_numpy(batch_y)
        if next(rnn.parameters()).is_cuda:
            points, labels = points.cuda(), labels.cuda()
        outputs = rnn(points)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum()
    return correct / total


def test_model(args):
    # Hyper Parameters
    sequence_length = args.seq_len
    input_size = args.input_size
    hidden_size = args.hidden_size
    num_layers = args.num_layers
    num_classes = args.num_classes
    batch_size = args.batch_size
    num_epochs = args.num_epochs
    learning_rate = args.learning_rate
    dropout = args.dropout

    # Load back the best performing model
    rnn = RNN('LSTM', input_size, hidden_size, num_layers, num_classes, dropout)
    if args.cuda:
        rnn = rnn.cuda()
    rnn.load_state_dict(torch.load(args.model_path))

    train_dataset = create_dataset('data/train/', timesteps=sequence_length)
    train_loader = dataloader(train_dataset, batch_size=batch_size)
    test_dataset = create_dataset('data/test/', timesteps=sequence_length)
    test_loader = dataloader(test_dataset, batch_size=batch_size)

    # print('training accuracy = %.4f, test accuracy = %.4f' % (eval_model(rnn, train_loader), eval_model(rnn, test_loader)))
    print('training accuracy = %.4f' % eval_model(rnn, train_loader))
    print('test accuracy = %.4f' % eval_model(rnn, test_loader))
