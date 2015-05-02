#!/usr/bin/env python

import models

def test_model():
    try:
        if models.session:
            print("session object exists")
    except:
        raise


if __name__ == "__main__":
    test_model()
