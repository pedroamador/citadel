#!/usr/bin/env python

import citadel.nodes.root


class Build(citadel.nodes.root.Node):

    def __init__(self, yml, path):
        super(Build, self).__init__(yml, path)
        self.output.append('\necho "### Build ###"')
