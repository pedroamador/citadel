#!/usr/bin/env python

import logging

import nodes.root
import tools


class Maven(nodes.root.Node):

    def __init__(self, yml, path):
        super(Maven, self).__init__(yml, path)

        if not isinstance(yml, dict):
            self.add_error('Parsing error, probably malformed yaml.')
            return

        # Unsure if this is python3 compatible
        # Always display maven's version
        mvn_exec = tools.get_executable('mvn') + ' -V'

        if 'build' in path:
            pom = 'pom.xml'
            lifecycle = 'clean install'
            opts = ''
            if 'lifecycle' in yml.keys():
                lifecycle = yml['lifecycle']
                del yml['lifecycle']
            else:
                self.add_error('Building with maven requires "lifecycle" to be specified.')
            if 'pom' in yml.keys():
                pom = yml['pom']
                del yml['pom']
            else:
                logging.debug('No "build/maven/pom" detected, defaulting to: %s' % (pom))

            if 'opts' in yml.keys():
                opts = yml['opts']
                del yml['opts']

            cmd = ['%s -f "%s" %s %s' % (mvn_exec, pom, lifecycle, opts)]
            for k, v in yml.items():
                cmd.append('-D%s=%s' % (k, v))
            self.output.append(self.format_cmd(cmd))

        elif 'publish' in path:
            if not 'file' in yml.keys():
                self.add_error('Publishing with maven requires "file" to be specified.')
                return
            cmd = ['%s deploy:deploy-file' % (mvn_exec)]
            if not 'version' in yml.keys():
                self.output.append(tools.get_version(yml['file']))
                yml['version'] = '${VERSION}'
            if 'snapshot' in yml.keys():
                if yml['snapshot']:
                    yml['version'] += '-SNAPSHOT'
                del yml['snapshot']
            for k, v in yml.items():
                cmd.append('-D%s=%s' % (k, v))
            self.output.append(self.format_cmd(cmd))