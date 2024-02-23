#!/bin/bash

export PATH=/pdisk/anaconda/envs/skyportal/bin:${PATH}
cd /pdisk/htdocs/skyportal/deployment/grandma_skyportal; /pdisk/anaconda/envs/skyportal/bin/python -m launcher $@
#/usr/bin/env python -m launcher $@
