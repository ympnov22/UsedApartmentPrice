#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

pd_DATA = pd.read_csv('UsedApartmentPrice.csv', header = 0, encoding = "utf-8")

pd_DATA = pd_DATA.fillna(0)

#pd_DATA = pd_DATA[u'価格'].astype(float)

#print(pd_DATA.info())

pd_DATA.to_csv("UsedApartmentPrice.csv",encoding = "utf-8")